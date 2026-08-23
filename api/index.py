"""
FastAPI Backend Serverless API for AI Resume Screening System (Vercel Ready)
"""

import os
import json
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.parser import extract_document_text
from core.extractor import parse_candidate_profile, parse_job_description
from core.matcher import rank_candidates
from utils.exporter import export_to_csv, export_to_excel, export_to_pdf

app = FastAPI(
    title="AI Resume Screening API",
    description="NLP-Powered Candidate Ranking & Resume Screening Serverless Backend",
    version="1.0.0"
)

# Enable CORS for local testing & Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_DATA_DIR = os.path.join(BASE_DIR, "sample_data")
PUBLIC_DIR = os.path.join(BASE_DIR, "public")

@app.get("/api/health")
def health_check():
    """Health check endpoint for Vercel monitoring."""
    return {
        "status": "online",
        "service": "AI Resume Screening API",
        "version": "1.0.0"
    }

@app.get("/api/sample-data")
def get_sample_data():
    """Returns available sample Job Descriptions and Resumes for 1-click demo."""
    jds = []
    resumes = []
    
    jd_dir = os.path.join(SAMPLE_DATA_DIR, "job_descriptions")
    if os.path.exists(jd_dir):
        for f in sorted(os.listdir(jd_dir)):
            if f.endswith(".txt"):
                path = os.path.join(jd_dir, f)
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                name_clean = f.replace("_jd.txt", "").replace("_", " ").title()
                jds.append({
                    "id": f,
                    "title": name_clean,
                    "content": content
                })
                
    resume_dir = os.path.join(SAMPLE_DATA_DIR, "resumes")
    if os.path.exists(resume_dir):
        for f in sorted(os.listdir(resume_dir)):
            if f.endswith(".pdf"):
                name_clean = f.replace(".pdf", "").replace("_", " ").title()
                resumes.append({
                    "id": f,
                    "filename": f,
                    "display_name": name_clean
                })
                
    return {
        "job_descriptions": jds,
        "sample_resumes": resumes
    }

@app.post("/api/analyze")
async def analyze_candidates(
    jd_text: str = Form(...),
    weights_json: Optional[str] = Form(None),
    sample_resumes: Optional[str] = Form(None), # Comma separated list of sample filenames
    files: List[UploadFile] = File([])
):
    """
    Main evaluation pipeline:
    Parses JD and candidates (uploaded files + sample selection), calculates scores,
    and returns ranked candidate leaderboard.
    """
    if not jd_text or not jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description text is required.")
        
    weights = {
        "skill_weight": 0.45,
        "semantic_weight": 0.35,
        "exp_weight": 0.10,
        "edu_weight": 0.10
    }
    if weights_json:
        try:
            parsed_w = json.loads(weights_json)
            weights.update(parsed_w)
        except Exception:
            pass

    # 1. Parse Job Description
    jd_profile = parse_job_description(jd_text)

    parsed_candidates = []

    # 2. Parse User Uploaded Resume Files
    for file in files:
        if not file.filename:
            continue
        content = await file.read()
        extracted_text = extract_document_text(content, file.filename)
        if extracted_text:
            profile = parse_candidate_profile(extracted_text, filename=file.filename)
            parsed_candidates.append(profile)

    # 3. Parse Selected Sample Resumes
    if sample_resumes:
        sample_ids = [s.strip() for s in sample_resumes.split(",") if s.strip()]
        resume_dir = os.path.join(SAMPLE_DATA_DIR, "resumes")
        for sample_filename in sample_ids:
            # Skip if already uploaded by same name
            if any(c["filename"] == sample_filename for c in parsed_candidates):
                continue
            path = os.path.join(resume_dir, sample_filename)
            if os.path.exists(path):
                with open(path, "rb") as f:
                    file_bytes = f.read()
                extracted_text = extract_document_text(file_bytes, sample_filename)
                if extracted_text:
                    profile = parse_candidate_profile(extracted_text, filename=sample_filename)
                    parsed_candidates.append(profile)

    if not parsed_candidates:
        raise HTTPException(status_code=400, detail="No valid resume files or sample resumes provided.")

    # 4. Rank Candidates
    ranked = rank_candidates(parsed_candidates, jd_profile, weights)

    # Prepare executive summary metrics
    total = len(ranked)
    shortlisted = len([c for c in ranked if c.get("final_score", 0) >= 50.0])
    avg_score = round(sum(c.get("final_score", 0) for c in ranked) / total, 1) if total > 0 else 0.0
    top_score = ranked[0].get("final_score", 0) if ranked else 0

    return {
        "jd_profile": {
            "required_skills": jd_profile.get("skills", []),
            "min_experience_years": jd_profile.get("min_experience_years", 0.0),
            "required_education": jd_profile.get("required_education", [])
        },
        "summary": {
            "total_evaluated": total,
            "shortlisted_count": shortlisted,
            "avg_match_score": avg_score,
            "top_match_score": top_score
        },
        "leaderboard": ranked
    }

@app.post("/api/export")
async def export_report(
    export_format: str = Form(...), # "csv" or "excel" or "pdf"
    leaderboard_json: str = Form(...)
):
    """Generates downloadable CSV, Excel, or PDF report from current leaderboard payload."""
    try:
        ranked_candidates = json.loads(leaderboard_json)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid leaderboard JSON: {e}")

    if export_format == "csv":
        csv_bytes = export_to_csv(ranked_candidates)
        return Response(
            content=csv_bytes,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=candidate_screening_report.csv"}
        )
    elif export_format == "excel":
        excel_bytes = export_to_excel(ranked_candidates)
        return Response(
            content=excel_bytes,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=candidate_screening_report.xlsx"}
        )
    elif export_format == "pdf":
        pdf_bytes = export_to_pdf(ranked_candidates)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=candidate_screening_report.pdf"}
        )
    else:
        raise HTTPException(status_code=400, detail="Unsupported export format.")

# Serve static frontend files for standalone uvicorn / local run
if os.path.exists(PUBLIC_DIR):
    app.mount("/", StaticFiles(directory=PUBLIC_DIR, html=True), name="public")
