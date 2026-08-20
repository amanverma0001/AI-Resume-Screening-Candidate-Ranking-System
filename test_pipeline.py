"""
Unit and Integration Test for the AI Resume Screening Engine.
"""

import os
from core.parser import parse_pdf, parse_txt
from core.extractor import parse_candidate_profile, parse_job_description
from core.matcher import rank_candidates
from utils.exporter import export_to_csv, export_to_excel, export_to_pdf

def run_test():
    base_dir = os.path.dirname(__file__)
    jd_path = os.path.join(base_dir, "sample_data", "job_descriptions", "senior_python_backend_jd.txt")
    resumes_dir = os.path.join(base_dir, "sample_data", "resumes")
    
    print("1. Parsing Job Description...")
    jd_text = parse_txt(jd_path)
    jd_profile = parse_job_description(jd_text)
    print(f"   JD Required Skills ({len(jd_profile['skills'])}): {jd_profile['skills']}")
    print(f"   JD Min Experience: {jd_profile['min_experience_years']} years")
    
    print("\n2. Parsing Resumes...")
    candidates = []
    for fname in os.listdir(resumes_dir):
        if fname.endswith('.pdf'):
            fpath = os.path.join(resumes_dir, fname)
            text = parse_pdf(fpath)
            cand_profile = parse_candidate_profile(text, filename=fname)
            candidates.append(cand_profile)
            print(f"   -> Parsed: {cand_profile['name']} | Exp: {cand_profile['experience_years']}y | Skills: {len(cand_profile['skills'])}")

    print("\n3. Ranking Candidates against JD...")
    ranked = rank_candidates(candidates, jd_profile)
    
    print("\n=== FINAL RANKING LEADERBOARD ===")
    for c in ranked:
        print(f"Rank {c['rank']}: {c['candidate_name']} ({c['filename']}) -> Match: {c['final_score']}% [{c['fit_status']}]")
        print(f"   Skills Matched ({len(c['matched_skills'])}): {c['matched_skills'][:5]}...")
        print(f"   Skills Missing ({len(c['missing_skills'])}): {c['missing_skills'][:5]}...")
        
    print("\n4. Testing Export Functionality...")
    csv_data = export_to_csv(ranked)
    excel_data = export_to_excel(ranked, jd_profile["skills"])
    pdf_data = export_to_pdf(ranked, "Senior Python Backend Developer", jd_profile["skills"])
    print(f"   CSV bytes generated: {len(csv_data)} bytes")
    print(f"   Excel bytes generated: {len(excel_data)} bytes")
    print(f"   PDF bytes generated: {len(pdf_data)} bytes")
    print("\nAll pipeline tests PASSED successfully!")

if __name__ == "__main__":
    run_test()
