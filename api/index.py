import os
import io
import json
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from core.parser import parse_resume_bytes, parse_resume_text
from core.extractor import extract_resume_entities, extract_jd_requirements
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
                parsed = parse_resume_bytes(open(file_path, "rb").read(), f)
                entities = extract_resume_entities(parsed["text"])
                sample_resumes.append({
                    "filename": f,
                    "text": parsed["text"],
                    "entities": entities
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
        jd_profile = extract_jd_requirements(jd_text)
        candidates_data = []

        if use_sample_resumes:
            if os.path.exists(RESUME_DIR):
                for f in sorted(os.listdir(RESUME_DIR)):
                    if f.endswith((".pdf", ".docx", ".txt")):
                        file_path = os.path.join(RESUME_DIR, f)
                        parsed = parse_resume_bytes(open(file_path, "rb").read(), f)
                        entities = extract_resume_entities(parsed["text"])
                        candidates_data.append(entities)
        elif files:
            for file in files:
                contents = await file.read()
                parsed = parse_resume_bytes(contents, file.filename)
                entities = extract_resume_entities(parsed["text"])
                candidates_data.append(entities)
        else:
            raise HTTPException(status_code=400, detail="No resume files provided and use_sample_resumes is false.")

        weights = {
            "skill": skill_weight,
            "experience": experience_weight,
            "education": education_weight,
            "semantic": semantic_weight
        }

        ranked_df = rank_candidates(candidates_data, jd_profile, weights)
        ranked_list = ranked_df.to_dict(orient="records")

        total = len(ranked_list)
        shortlisted = sum(1 for c in ranked_list if c.get("final_score", 0) >= cutoff_score)
        avg_score = round(sum(c.get("final_score", 0) for c in ranked_list) / max(total, 1), 1)
        top_cand = ranked_list[0]["candidate_name"] if total > 0 else "N/A"
        top_score = ranked_list[0]["final_score"] if total > 0 else 0.0

        return {
            "success": True,
            "metrics": {
                "total_applicants": total,
                "shortlisted_count": shortlisted,
                "average_match": avg_score,
                "top_candidate": top_cand,
                "top_score": top_score
            },
            "jd_profile": jd_profile,
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
