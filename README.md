# 🎯 Elythra — AI Resume Screening & Candidate Ranking System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Sentence--Transformers](https://img.shields.io/badge/SBERT-all--MiniLM--L6--v2-8A2BE2?logo=huggingface&logoColor=white)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
[![License](https://img.shields.io/badge/License-Academic%20%2F%20MIT-green)](LICENSE)

An enterprise-grade, NLP & Deep Learning-powered **AI Resume Screening and Candidate Ranking Decision-Support System** featuring a **Dual-Engine Architecture** (Classic TF-IDF & Deep Neural SBERT Transformers) with an interactive Streamlit recruiter command dashboard.

Developed as a VII-Semester Capstone Project (**CSET400C**) at **Bennett University**.

---

## 📌 Problem Statement & Objective

Recruitment teams receive hundreds of resumes for every job opening. Manual screening:
- Consumes **15–20 hours per job listing** (recruiters spend only 6–10 seconds per resume during initial triage).
- Is prone to **unconscious human bias** and **evaluator fatigue**.
- Relies on superficial keyword matching (`Ctrl+F`), frequently disqualifying top-tier talent whose resumes use synonyms or non-identical technical phrasing.

### 💡 The Solution: Elythra
An intelligent decision-support tool that:
1. Ingests Job Descriptions and candidate resumes in diverse formats (**PDF, DOCX, TXT**).
2. Extracts candidate information: **Contact Details, Skills, Work Experience, and Educational Qualifications**.
3. Employs a **Dual Matching AI Engine** allowing recruiters to dynamically switch between **Fast TF-IDF Baseline** and **Deep Neural SBERT (`all-MiniLM-L6-v2`)** embeddings.
4. Ranks applicants on an interactive leaderboard with transparent scoring, visual component gauges, and color-coded skill gap badges.
5. Generates one-click export reports in **CSV, Multi-Tab Excel (.xlsx)**, and **Branded Executive PDF** formats.

---

## 🤖 Dual Matching Engine Architecture

Recruiters and evaluators can switch matching engines on the fly from the sidebar:

```
                      ┌────────────────────────────────────────┐
                      │    Input: Resume Text + JD Text        │
                      └──────────────────┬─────────────────────┘
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
   ┌───────────────────────────────┐           ┌───────────────────────────────┐
   │    ⚡ Fast Baseline (TF-IDF)  │           │   🧠 Deep Neural AI (SBERT)   │
   │  • Sublinear N-gram (1-2)     │           │  • all-MiniLM-L6-v2 (384-d)   │
   │  • Lexical word importance    │           │  • Dense semantic embeddings  │
   │  • Latency: ~1.2 ms per doc   │           │  • Latency: ~18.5 ms per doc  │
   │  • Best for exact terminology │           │  • Understands synonyms & ctx │
   └───────────────┬───────────────┘           └───────────────┬───────────────┘
                   │                                           │
                   └─────────────────────┬─────────────────────┘
                                         ▼
                      ┌────────────────────────────────────────┐
                      │     Cosine Similarity Score (0-100)    │
                      └──────────────────┬─────────────────────┘
                                         │
   ┌─────────────────────────────────────┴─────────────────────────────────────┐
   ▼                                     ▼                                     ▼
🧩 Skill Overlap (45-50%)      ⏳ Experience Match (10-20%)   🎓 Education Match (10-20%)
   500+ Taxonomy Jaccard                 Tenure vs Requirement        Degree Level Verification
   └─────────────────────────────────────┬─────────────────────────────────────┘
                                         ▼
                      ┌────────────────────────────────────────┐
                      │   Composite Match Score & Leaderboard  │
                      └────────────────────────────────────────┘
```

### Mathematical Formulation
$$\mathbf{Score}_{\text{Composite}} = (w_{\text{skill}} \times S_{\text{Skill}}) + (w_{\text{semantic}} \times S_{\text{Semantic}}) + (w_{\text{exp}} \times S_{\text{Experience}}) + (w_{\text{edu}} \times S_{\text{Education}})$$

Where $S_{\text{Semantic}}$ is computed dynamically based on the active engine:
* **TF-IDF Engine:** Cosine similarity of sparse TF-IDF vectors scaled to $0 - 100$.
* **SBERT Engine:** Cosine similarity of 384-dimensional dense contextual embeddings from `all-MiniLM-L6-v2` with automated fallback.

---

## 📊 Model Comparison: TF-IDF vs SBERT

| Metric / Attribute | ⚡ TF-IDF + Cosine Similarity | 🧠 SBERT (`all-MiniLM-L6-v2`) |
| :--- | :--- | :--- |
| **Model Type** | Statistical Bag-of-Words / N-gram | Deep Bidirectional Transformer |
| **Embedding Dimension** | 5,000 (Sparse) | 384 (Dense) |
| **Synonym Understanding** | ❌ No (Exact word match only) | ✅ Yes (Full semantic awareness) |
| **Contextual Transferability** | ❌ None | ✅ High (Relates PyTorch $\leftrightarrow$ Deep Learning) |
| **Inference Latency** | ~1.2 ms / candidate | ~18.5 ms / candidate |
| **Memory Footprint** | Negligible (< 1 MB) | ~80 MB RAM |
| **Offline Execution** | ✅ Yes | ✅ Yes (Cached locally) |
| **Best Use Case** | High-volume fast initial triage | High-accuracy technical shortlisting |

---

## 🏗️ System Architecture & Codebase Layout

```
Capstone/
├── app.py                             # Main Streamlit web dashboard & recruiter command center
├── requirements.txt                   # Complete dependencies (including sentence-transformers)
├── test_pipeline.py                   # Automated end-to-end integration & scoring test
├── benchmark_kaggle.py                # Batch evaluation script on Kaggle resume dataset
├── MODEL_COMPARISON_REPORT.md         # Comprehensive architectural comparison & benchmark report
├── core/
│   ├── skills_database.py             # 500+ categorized skill taxonomy (Languages, Cloud, AI/ML, etc.)
│   ├── text_cleaner.py                # Regex NER extraction (Email, Phone, Links, Education, Experience)
│   ├── parser.py                      # Multi-format document parser (PDF, DOCX, TXT)
│   ├── extractor.py                   # Structured profile extraction for Resumes and JDs
│   └── matcher.py                     # Dual-model scoring engine (TF-IDF + SBERT Transformer)
├── sample_data/
│   ├── job_descriptions/              # 15+ Preloaded industry Job Descriptions
│   │   ├── senior_python_backend_jd.txt
│   │   ├── data_scientist_ai_engineer_jd.txt
│   │   └── teacher_jd.txt ...
│   └── resumes/                       # 10+ Multi-domain candidate PDF resumes
│       ├── rahul_sharma_senior_python_lead.pdf
│       ├── priya_patel_ai_data_scientist.pdf
│       └── amit_verma_fullstack_developer.pdf ...
└── utils/
    ├── visualizer.py                  # Plotly gauges, breakdown bars & distribution charts
    ├── exporter.py                    # CSV, Multi-Tab Excel, and Executive PDF report generators
    └── landing_page.py                # Modern glassmorphism landing portal & auth
```

---

## ⚡ Key Highlights & Capabilities

- **Dual-Model Interactive Switcher:** Recruiter can toggle between Fast TF-IDF and SBERT on the fly.
- **500+ Skills Taxonomy:** Normalized skill mapper across 10 technical domains (Languages, Cloud, Web, AI/ML, DevOps, Databases, Testing, etc.).
- **Configurable Algorithm Weightage:** Recruiter can tune sliders for Skill Overlap, Semantic Match, Experience, and Education weights.
- **Transparent Skill Gap Badges:** Displays green badges for 🟢 **Matched Skills** and red badges for 🔴 **Missing Skills**.
- **Real-Time Live Search:** Filter applicants instantly by skill name, candidate name, degree, or email.
- **One-Click Export Center:**
  - 📄 **Executive PDF Summary:** Professional branded evaluation report with header metrics and skill gap breakdown.
  - 📊 **Multi-Tab Excel (.xlsx):** Shortlisted candidates, full leaderboard, and comprehensive skill matrices.
  - 📑 **Clean CSV Export:** Portable data export for HR ATS integration.
- **Instant Demo Mode:** Pre-configured with realistic resumes and role profiles for instant evaluation and defense presentations.

---

## 🛠️ Technology Stack

| Category | Technologies / Libraries |
| :--- | :--- |
| **Language & Runtime** | Python 3.10+ |
| **Deep Learning & NLP** | `sentence-transformers` (`all-MiniLM-L6-v2`), `transformers`, `torch`, `scikit-learn` |
| **Text Parsing & Regex** | `pypdf`, `python-docx`, Regular Expressions (`re`) |
| **Data Manipulation** | `pandas`, `numpy`, `openpyxl` |
| **Web Dashboard** | `Streamlit` (Dynamic State & Session Management) |
| **Visualizations** | `plotly` (Score Gauges, Component Bars, Domain Charts) |
| **PDF Generation** | `reportlab` |

---

## 🚀 Quickstart: Running Locally

### 1. Clone the Repository
```bash
git clone https://github.com/amanverma0001/AI-Resume-Screening-Candidate-Ranking-System.git
cd AI-Resume-Screening-Candidate-Ranking-System
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Recruiter Dashboard
```bash
streamlit run app.py
```
Open your browser and navigate to: **`http://localhost:8501`**

---

## 🧪 Automated Testing & Verification

Run the end-to-end integration test to verify document parsers, regex extractors, both AI matching models, and report exporters:
```bash
python test_pipeline.py
```

Expected output:
```
1. Parsing Job Description... Done
2. Parsing Resumes... (10 candidates extracted)
3. Ranking Candidates against JD... Leaderboard generated
4. Testing Export Functionality... CSV, Excel, and PDF bytes verified
All pipeline tests PASSED successfully!
```

---

## 👥 Authors & Academic Context

* **Developer:** **Amandeep Verma**  
  * Enrollment: Bennett University, School of Computer Science Engineering & Technology  
  * Course: **CSET400C — Capstone Project (2026–27)**
* **Course Coordinator & Guide:** **Dr. Jabir Ali** (Associate Professor, CSE)
