# 🎯 AI Resume Screening & Candidate Ranking System

An enterprise-grade, NLP-powered **AI Resume Screening and Candidate Ranking System** built with Python, Natural Language Processing (NLP), Machine Learning matching algorithms, and an interactive Streamlit recruiter dashboard.

---

## 📌 Problem Statement & Objective
Companies receive hundreds of resumes for every job posting. Manually reviewing and comparing these resumes is tedious, time-consuming, and prone to human bias and oversight.

**Objective**: Develop an intelligent decision-support tool that:
1. Ingests Job Descriptions and multiple applicant resumes (PDF, DOCX, TXT).
2. Extracts candidate information: **Contact Details, Skills, Work Experience, and Educational Qualifications**.
3. Compares candidate qualifications against the job description using **Semantic TF-IDF Cosine Similarity** and **Skill Gap Overlap**.
4. Ranks applicants on a leaderboard with transparent scoring and color-coded skill badges.
5. Enables recruiters to export shortlisted candidates to CSV and Excel reports in one click.

---

## 🏗️ System Architecture

```
Elythra project/
├── app.py                             # Main Streamlit web dashboard & recruiter UI
├── requirements.txt                   # Project dependencies
├── test_pipeline.py                   # Automated end-to-end integration test
├── core/
│   ├── skills_database.py             # 500+ categorized skill taxonomy (Languages, Cloud, ML, etc.)
│   ├── text_cleaner.py                # Regex extraction (Email, Phone, Links, Education, Experience)
│   ├── parser.py                      # Multi-format document parser (PDF, DOCX, TXT)
│   ├── extractor.py                   # Structured profile extraction for Resumes and JDs
│   └── matcher.py                     # Multi-factor weighted ranking & TF-IDF similarity engine
├── sample_data/
│   ├── job_descriptions/              # Preloaded industry Job Descriptions
│   │   ├── senior_python_backend_jd.txt
│   │   └── data_scientist_ai_engineer_jd.txt
│   ├── resumes/                       # 6 Realistic pre-generated PDF resumes
│   │   ├── rahul_sharma_senior_python_lead.pdf
│   │   ├── priya_patel_ai_data_scientist.pdf
│   │   ├── amit_verma_fullstack_developer.pdf
│   │   ├── sneha_reddy_junior_python_dev.pdf
│   │   ├── rohit_kumar_devops_cloud_eng.pdf
│   │   └── vikram_singh_sales_marketing.pdf
│   └── generate_sample_resumes.py     # Resume generation script using ReportLab
└── utils/
    ├── visualizer.py                  # Plotly gauges, breakdown bars & radar charts
    └── exporter.py                    # CSV and multi-sheet Excel report generators
```

---

## ⚡ Core Features

- **Multi-Format Ingestion**: Supports `.pdf`, `.docx`, and `.txt` files with automated text sanitization.
- **500+ Skills Taxonomy**: Recognizes skills across 10 domains (Programming Languages, Web & Frontend, Backend Frameworks, AI/ML & Data Science, Cloud & DevOps, Databases, Testing, etc.).
- **Multi-Factor Weighted Scoring Algorithm**:
  - 🧩 **Skill Overlap (45%)**: Direct matching between required JD skills and candidate skills.
  - 🧠 **Semantic Text Similarity (35%)**: TF-IDF N-gram vectorization and Cosine Similarity.
  - ⏳ **Experience Match (10%)**: Candidate work experience compared to minimum job requirements.
  - 🎓 **Education Match (10%)**: Verification of degree level (B.Tech, M.Tech, MS, BCA, MCA, etc.).
- **Skill Gap Analysis**: Visual color-coded badges for 🟢 **Matched Skills** vs 🔴 **Missing Skills**.
- **Interactive Recruiter Dashboard**:
  - Executive KPI summary cards (Total Resumes, Shortlisted, Avg Match %, Top Match).
  - Configurable threshold sliders and scoring weight customizer.
  - Candidate deep-dive inspector with Plotly gauge charts and skill breakdown bars.
- **1-Click Instant Demo Mode**: Pre-loaded roles and resumes for seamless live demonstrations.
- **Data Export Center**: One-click export to CSV and multi-tab Excel (`.xlsx`) spreadsheets.

---

## 🛠️ Technology Stack

| Category | Technologies / Libraries |
| :--- | :--- |
| **Programming Language** | Python 3.10+ |
| **NLP & Text Processing** | `scikit-learn` (TF-IDF, Cosine Similarity), `re` (Regex NER), `pypdf`, `python-docx` |
| **Data Manipulation** | `pandas`, `numpy`, `openpyxl` |
| **Interactive Dashboard & UI** | `Streamlit` |
| **Data Visualizations** | `plotly` (Gauges, Horizontal Bar Charts, Distribution Plots) |
| **PDF Generation** | `reportlab` |

---

## 🚀 How to Run the Project Locally

### 1. Clone or Open the Workspace
```bash
cd "Elythra project"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Application
```bash
streamlit run app.py
```

Open your browser and navigate to: `http://localhost:8501`

---

## 🧪 Running Automated Tests
To verify all parsers, extractors, and scoring algorithms:
```bash
python test_pipeline.py
```
