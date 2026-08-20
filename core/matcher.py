"""
Matching and Scoring Engine for AI Resume Screening.
Combines TF-IDF Semantic Cosine Similarity, Skill Overlap Analysis,
Experience Matching, and Education Matching into a Weighted Composite Score.
"""

from typing import Dict, List, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.skills_database import SKILL_MAP
from core.text_cleaner import preprocess_for_nlp

def calculate_tfidf_similarity(resume_text: str, jd_text: str) -> float:
    """
    Computes normalized cosine similarity between TF-IDF vector representations
    of the resume text and the job description.
    """
    try:
        clean_resume = preprocess_for_nlp(resume_text)
        clean_jd = preprocess_for_nlp(jd_text)
        
        if not clean_resume or not clean_jd:
            return 0.0
            
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True
        )
        
        tfidf_matrix = vectorizer.fit_transform([clean_jd, clean_resume])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Document cosine similarity rarely exceeds 0.70 even for near-identical technical resumes;
        # We apply a gentle sigmoid/linear scaling to reflect human recruiter relevance (0 to 100).
        scaled_sim = min(100.0, sim * 140.0)
        return float(np.clip(scaled_sim, 0.0, 100.0))
    except Exception as e:
        print(f"[TF-IDF Error] {e}")
        return 0.0

def match_candidate_with_jd(
    candidate_profile: Dict[str, Any],
    jd_profile: Dict[str, Any],
    weights: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Compares a candidate profile with the JD profile and computes:
      - Matched skills list
      - Missing skills list (Skill Gap)
      - Skill match %
      - TF-IDF content similarity %
      - Experience match %
      - Education match %
      - Final Weighted Overall Match Score (0 - 100)
    """
    if weights is None:
        weights = {
            "skill_weight": 0.45,
            "semantic_weight": 0.35,
            "exp_weight": 0.10,
            "edu_weight": 0.10
        }
        
    cand_skills_raw = candidate_profile.get("raw_skills_set", set())
    jd_skills_raw = jd_profile.get("raw_skills_set", set())
    
    # 1. Skill Overlap Calculation
    if jd_skills_raw:
        matched_raw = cand_skills_raw.intersection(jd_skills_raw)
        missing_raw = jd_skills_raw - cand_skills_raw
        skill_score = (len(matched_raw) / len(jd_skills_raw)) * 100.0
    else:
        matched_raw = cand_skills_raw
        missing_raw = set()
        skill_score = 100.0 if cand_skills_raw else 50.0

    matched_skills = [SKILL_MAP.get(s, s.title()) for s in sorted(matched_raw)]
    missing_skills = [SKILL_MAP.get(s, s.title()) for s in sorted(missing_raw)]
    
    # 2. Semantic Similarity Score
    semantic_score = calculate_tfidf_similarity(
        candidate_profile.get("raw_text", ""),
        jd_profile.get("raw_text", "")
    )
    
    # 3. Experience Score
    cand_exp = float(candidate_profile.get("experience_years", 0.0))
    jd_exp = float(jd_profile.get("min_experience_years", 0.0))
    
    if jd_exp > 0:
        if cand_exp >= jd_exp:
            exp_score = 100.0
        else:
            exp_score = min(100.0, (cand_exp / jd_exp) * 100.0)
    else:
        exp_score = 100.0 if cand_exp > 0 else 80.0
        
    # 4. Education Score
    cand_edu = [e.lower() for e in candidate_profile.get("education", [])]
    jd_edu = [e.lower() for e in jd_profile.get("required_education", [])]
    
    if jd_edu:
        has_match = any(e in cand_edu for e in jd_edu)
        edu_score = 100.0 if has_match else 50.0
    else:
        edu_score = 100.0 if any(e != "not specified" for e in cand_edu) else 75.0
        
    # 5. Composite Weighted Score
    final_score = (
        skill_score * weights.get("skill_weight", 0.45) +
        semantic_score * weights.get("semantic_weight", 0.35) +
        exp_score * weights.get("exp_weight", 0.10) +
        edu_score * weights.get("edu_weight", 0.10)
    )
    final_score = float(np.clip(final_score, 0.0, 100.0))
    
    # Determine Fit Badge
    if final_score >= 70.0:
        fit_status = "Strong Fit"
        fit_color = "#10B981" # Emerald Green
    elif final_score >= 45.0:
        fit_status = "Moderate Fit"
        fit_color = "#F59E0B" # Amber Yellow
    else:
        fit_status = "Low Fit"
        fit_color = "#EF4444" # Rose Red
        
    return {
        "candidate_name": candidate_profile.get("name", "Unknown"),
        "filename": candidate_profile.get("filename", ""),
        "email": candidate_profile.get("email", ""),
        "phone": candidate_profile.get("phone", ""),
        "linkedin": candidate_profile.get("linkedin"),
        "github": candidate_profile.get("github"),
        "experience_years": cand_exp,
        "education": candidate_profile.get("education", []),
        "final_score": round(final_score, 1),
        "skill_score": round(skill_score, 1),
        "semantic_score": round(semantic_score, 1),
        "exp_score": round(exp_score, 1),
        "edu_score": round(edu_score, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_candidate_skills": candidate_profile.get("skills", []),
        "fit_status": fit_status,
        "fit_color": fit_color,
        "skills_by_category": candidate_profile.get("skills_by_category", {}),
        "raw_text": candidate_profile.get("raw_text", "")
    }

def rank_candidates(
    candidates_data: List[Dict[str, Any]],
    jd_profile: Dict[str, Any],
    weights: Dict[str, float] = None
) -> List[Dict[str, Any]]:
    """
    Ranks a list of parsed candidate profiles against the JD profile.
    Returns sorted list from highest score to lowest.
    """
    scored_candidates = []
    for cand in candidates_data:
        match_res = match_candidate_with_jd(cand, jd_profile, weights)
        scored_candidates.append(match_res)
        
    # Sort descending by final score
    scored_candidates.sort(key=lambda x: x["final_score"], reverse=True)
    
    # Assign Rank numbers
    for idx, item in enumerate(scored_candidates, 1):
        item["rank"] = idx
        
    return scored_candidates
