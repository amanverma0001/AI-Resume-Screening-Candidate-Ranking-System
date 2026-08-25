import os
import io
import json
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from core.parser import extract_document_text
from core.extractor import parse_candidate_profile, parse_job_description
from core.matcher import rank_candidates

app = FastAPI(title="AI Resume Screening API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JD_DIR = os.path.join(BASE_DIR, "sample_data", "job_descriptions")
RESUME_DIR = os.path.join(BASE_DIR, "sample_data", "resumes")

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "AI Resume Screening Backend"}

@app.get("/api/sample-data")
def get_sample_data():
    jds = {}
    if os.path.exists(JD_DIR):
        for f in os.listdir(JD_DIR):
            if f.endswith(".txt"):
                role_name = f.replace(".txt", "").replace("_jd", "").replace("_", " ").title()
                with open(os.path.join(JD_DIR, f), "r", encoding="utf-8", errors="ignore") as fp:
                    jds[role_name] = fp.read()

    sample_resumes = []
    if os.path.exists(RESUME_DIR):
        for f in sorted(os.listdir(RESUME_DIR)):
            if f.endswith((".pdf", ".docx", ".txt")):
                file_path = os.path.join(RESUME_DIR, f)
                with open(file_path, "rb") as fp:
                    data_bytes = fp.read()
                text = extract_document_text(data_bytes, f)
                profile = parse_candidate_profile(text, f)
                sample_resumes.append({
                    "filename": f,
                    "text": text,
                    "profile": profile
                })

    return {
        "job_descriptions": jds,
        "sample_resumes_count": len(sample_resumes),
        "sample_resumes": sample_resumes
    }

@app.post("/api/analyze")
async def analyze_candidates(
    jd_text: str = Form(...),
    skill_weight: float = Form(0.40),
    experience_weight: float = Form(0.25),
    education_weight: float = Form(0.15),
    semantic_weight: float = Form(0.20),
    cutoff_score: float = Form(50.0),
    files: Optional[List[UploadFile]] = File(None),
    use_sample_resumes: bool = Form(False)
):
    try:
        jd_profile = parse_job_description(jd_text)
        candidates_data = []

        if use_sample_resumes:
            if os.path.exists(RESUME_DIR):
                for f in sorted(os.listdir(RESUME_DIR)):
                    if f.endswith((".pdf", ".docx", ".txt")):
                        file_path = os.path.join(RESUME_DIR, f)
                        with open(file_path, "rb") as fp:
                            data_bytes = fp.read()
                        text = extract_document_text(data_bytes, f)
                        profile = parse_candidate_profile(text, f)
                        candidates_data.append(profile)
        elif files:
            for file in files:
                contents = await file.read()
                text = extract_document_text(contents, file.filename)
                profile = parse_candidate_profile(text, file.filename)
                candidates_data.append(profile)
        else:
            raise HTTPException(status_code=400, detail="No resume files provided and use_sample_resumes is false.")

        weights = {
            "skill_weight": skill_weight,
            "exp_weight": experience_weight,
            "edu_weight": education_weight,
            "semantic_weight": semantic_weight
        }

        ranked_list = rank_candidates(candidates_data, jd_profile, weights)

        total = len(ranked_list)
        shortlisted = sum(1 for c in ranked_list if c.get("final_score", 0) >= cutoff_score)
        avg_score = round(sum(c.get("final_score", 0) for c in ranked_list) / max(total, 1), 1)
        top_cand = ranked_list[0]["candidate_name"] if total > 0 else "N/A"
        top_score = ranked_list[0]["final_score"] if total > 0 else 0.0

        jd_display_profile = {
            "detected_role": jd_profile.get("detected_role", "Software Engineer"),
            "required_experience_years": jd_profile.get("min_experience_years", 4.0),
            "required_skills": jd_profile.get("skills", []),
            "required_education": jd_profile.get("required_education", [])
        }

        return {
            "success": True,
            "metrics": {
                "total_applicants": total,
                "shortlisted_count": shortlisted,
                "average_match": avg_score,
                "top_candidate": top_cand,
                "top_score": top_score
            },
            "jd_profile": jd_display_profile,
            "ranked_candidates": ranked_list
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/export")
async def export_data(data: str = Form(...), format: str = Form("csv")):
    candidates = json.loads(data)
    df = pd.DataFrame(candidates)
    
    if format == "csv":
        output = io.StringIO()
        df.to_csv(output, index=False)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode("utf-8")),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=candidate_ranking_results.csv"}
        )
    elif format == "excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Rankings")
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=candidate_ranking_results.xlsx"}
        )
