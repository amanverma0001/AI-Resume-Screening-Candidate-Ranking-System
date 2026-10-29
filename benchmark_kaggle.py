"""
Kaggle Dataset Benchmark & Stress Testing Script for Elythra ATS.
Evaluates parsing speed, accuracy, and ranking across real-world Kaggle resumes.
"""

import os
import sys
import time
import glob
import pandas as pd

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.parser import parse_pdf
from core.extractor import parse_candidate_profile, parse_job_description
from core.matcher import rank_candidates

def run_benchmark(category="INFORMATION-TECHNOLOGY", limit=50, jd_filename="senior_python_backend_jd.txt"):
    print("=" * 70)
    print("   ELYTHRA AI ATS - KAGGLE DATASET BENCHMARKING HARNESS")
    print("=" * 70)

    # 1. Load Job Description
    jd_path = os.path.join(BASE_DIR, "sample_data", "job_descriptions", jd_filename)
    if not os.path.exists(jd_path):
        print(f"[Error] Job description not found at: {jd_path}")
        return

    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    jd_profile = parse_job_description(jd_text)
    print(f"\n[1] Target Job Profile: {jd_filename.replace('_', ' ').replace('.txt', '').title()}")
    print(f"    Required Skills ({len(jd_profile['skills'])}): {', '.join(jd_profile['skills'][:8])}...")
    print(f"    Min Experience Required: {jd_profile['min_experience_years']} years")
    print(f"    Education Required: {', '.join(jd_profile['required_education']) or 'Any'}")

    # 2. Locate Kaggle PDF Resumes
    pdf_dir = os.path.join(BASE_DIR, "dataset", "kaggle_resumes_pdf", category)
    if not os.path.exists(pdf_dir):
        print(f"[Error] Category directory not found: {pdf_dir}")
        return

    pdf_files = sorted(glob.glob(os.path.join(pdf_dir, "*.pdf")))
    if limit and limit > 0:
        pdf_files = pdf_files[:limit]

    total_resumes = len(pdf_files)
    print(f"\n[2] Ingesting {total_resumes} Real Kaggle Resumes from Category: '{category}'")

    # 3. Processing & Benchmarking
    parsed_candidates = []
    parse_start = time.time()
    successful = 0
    failed = 0

    print("\n[3] Executing Parsing & Feature Extraction Pipeline...")
    for idx, p in enumerate(pdf_files, 1):
        fname = os.path.basename(p)
        try:
            raw_text = parse_pdf(p)
            if not raw_text or len(raw_text.strip()) < 20:
                failed += 1
                continue
            profile = parse_candidate_profile(raw_text, filename=fname)
            parsed_candidates.append(profile)
            successful += 1
        except Exception as e:
            failed += 1

        if idx % 10 == 0 or idx == total_resumes:
            sys.stdout.write(f"\r    Processed: {idx}/{total_resumes} resumes ({(idx/total_resumes)*100:.0f}%)")
            sys.stdout.flush()

    parse_time = time.time() - parse_start
    print(f"\n    Completed extraction: {successful} successful, {failed} failed in {parse_time:.2f}s")

    # 4. Scoring & Ranking
    rank_start = time.time()
    ranked_candidates = rank_candidates(parsed_candidates, jd_profile)
    rank_time = time.time() - rank_start
    total_time = parse_time + rank_time

    # 5. Benchmark Performance Metrics
    avg_latency = total_time / successful if successful else 0
    throughput = (successful / total_time) * 60 if total_time > 0 else 0

    print("\n" + "=" * 70)
    print("   BENCHMARK PERFORMANCE SUMMARY")
    print("=" * 70)
    print(f" • Total Real Resumes Processed : {successful}")
    print(f" • Total Ingestion & Scoring Time : {total_time:.2f} seconds")
    print(f" • Average Latency Per Resume   : {avg_latency:.3f} seconds (Target: < 1.5s)")
    print(f" • Throughput                     : {throughput:.1f} resumes / minute")
    print(f" • Parsing Success Rate           : {(successful/total_resumes)*100:.1f}%")

    # 6. Fit Distribution
    strong_fit = sum(1 for c in ranked_candidates if c['fit_status'] == 'Strong Fit')
    mod_fit = sum(1 for c in ranked_candidates if c['fit_status'] == 'Moderate Fit')
    low_fit = sum(1 for c in ranked_candidates if c['fit_status'] == 'Low Fit')

    print(f"\n Candidate Classification Distribution:")
    print(f"   🟢 Strong Fit (Score >= 70%)   : {strong_fit} candidates ({(strong_fit/successful)*100:.1f}%)")
    print(f"   🟡 Moderate Fit (45% - 69%)    : {mod_fit} candidates ({(mod_fit/successful)*100:.1f}%)")
    print(f"   🔴 Low Fit (Score < 45%)       : {low_fit} candidates ({(low_fit/successful)*100:.1f}%)")

    # 7. Print Top 10 Leaderboard
    print("\n" + "=" * 70)
    print("   TOP 10 SHORTLISTED CANDIDATES (LEADERBOARD)")
    print("=" * 70)
    print(f"{'Rank':<5} | {'Candidate / File':<20} | {'Score':<8} | {'Skills%':<8} | {'TF-IDF%':<8} | {'Status'}")
    print("-" * 70)
    for c in ranked_candidates[:10]:
        print(f"{c['rank']:<5} | {c['filename']:<20} | {c['final_score']:<7.1f}% | {c['skill_score']:<7.1f}% | {c['semantic_score']:<7.1f}% | {c['fit_status']}")

    # 8. Save CSV Output for Teacher Review
    export_rows = []
    for c in ranked_candidates:
        export_rows.append({
            "Rank": c["rank"],
            "Resume_ID": c["filename"],
            "Final_Score": c["final_score"],
            "Skill_Score": c["skill_score"],
            "Semantic_TFIDF_Score": c["semantic_score"],
            "Experience_Score": c["exp_score"],
            "Education_Score": c["edu_score"],
            "Fit_Status": c["fit_status"],
            "Matched_Skills": ", ".join(c["matched_skills"]),
            "Missing_Skills": ", ".join(c["missing_skills"]),
            "Detected_Experience_Yrs": c["experience_years"]
        })

    out_csv = os.path.join(BASE_DIR, "dataset", "kaggle_benchmark_results.csv")
    pd.DataFrame(export_rows).to_csv(out_csv, index=False)
    print(f"\n[4] Complete Benchmark Leaderboard saved to: {out_csv}")
    print("=" * 70)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Benchmark Elythra with Kaggle Resumes")
    parser.add_argument("--category", default="INFORMATION-TECHNOLOGY", help="Kaggle resume category folder")
    parser.add_argument("--limit", type=int, default=50, help="Number of resumes to test (default: 50)")
    parser.add_argument("--jd", default="senior_python_backend_jd.txt", help="Job description file")
    args = parser.parse_args()

    run_benchmark(category=args.category, limit=args.limit, jd_filename=args.jd)
