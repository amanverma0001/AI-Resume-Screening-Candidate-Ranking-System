"""
AI Resume Screening and Candidate Ranking System
Interactive Streamlit Recruiter Dashboard
"""

import os
import streamlit as st
import pandas as pd
from core.parser import parse_pdf, parse_docx, parse_txt, extract_document_text
from core.extractor import parse_candidate_profile, parse_job_description
from core.matcher import rank_candidates
from utils.visualizer import (
    create_score_gauge,
    create_breakdown_bar,
    create_leaderboard_chart,
    create_category_distribution_chart
)
from utils.exporter import export_to_csv, export_to_excel, export_to_pdf
from utils.landing_page import render_landing_page

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume Screening & Ranking System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Global CSS to eliminate top blank space ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Completely eliminate top empty blank space */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 1400px !important;
    }
    
    #MainMenu, footer {
        visibility: hidden !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Session Authentication Check & Landing Page Gatekeeper ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "registered_users" not in st.session_state:
    st.session_state.registered_users = {}

if not st.session_state.authenticated:
    render_landing_page()
    st.stop()


# --- Custom Styling & CSS Design System ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    @keyframes headerGradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes headerPulseGlow {
        0% { box-shadow: 0 10px 25px -4px rgba(79, 70, 229, 0.4); border-color: rgba(99, 102, 241, 0.4); }
        50% { box-shadow: 0 16px 38px 4px rgba(168, 85, 247, 0.75); border-color: rgba(168, 85, 247, 0.85); }
        100% { box-shadow: 0 10px 25px -4px rgba(79, 70, 229, 0.4); border-color: rgba(99, 102, 241, 0.4); }
    }

    @keyframes shimmerSweep {
        0% { transform: translateX(-100%) rotate(25deg); }
        25% { transform: translateX(250%) rotate(25deg); }
        100% { transform: translateX(250%) rotate(25deg); }
    }

    .main-header {
        background: linear-gradient(-45deg, #0F172A, #1E1B4B, #312E81, #4338CA, #6366F1, #7C3AED, #0EA5E9);
        background-size: 350% 350%;
        animation: headerGradientShift 8s ease infinite, headerPulseGlow 4s infinite ease-in-out;
        padding: 30px 36px;
        border-radius: 20px;
        color: white;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.25);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 50%;
        height: 200%;
        background: linear-gradient(
            to right,
            rgba(255, 255, 255, 0) 0%,
            rgba(255, 255, 255, 0.3) 50%,
            rgba(255, 255, 255, 0) 100%
        );
        transform: rotate(25deg);
        animation: shimmerSweep 6s infinite ease-in-out;
        pointer-events: none;
    }
    
    .main-header h1 {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        color: #FFFFFF;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        font-size: 1.05rem;
        color: #C7D2FE;
        margin: 6px 0 0 0;
    }
    
    @keyframes kpiPulseGlow {
        0% { box-shadow: 0 6px 20px -2px rgba(99, 102, 241, 0.4); border-color: rgba(99, 102, 241, 0.5); }
        50% { box-shadow: 0 14px 32px 4px rgba(168, 85, 247, 0.8); border-color: rgba(168, 85, 247, 0.9); }
        100% { box-shadow: 0 6px 20px -2px rgba(99, 102, 241, 0.4); border-color: rgba(99, 102, 241, 0.5); }
    }

    /* Base Card Styles */
    .kpi-card, .section-card {
        background-color: var(--secondary-background-color, #FFFFFF);
        border: 1px solid rgba(99, 102, 241, 0.4);
        border-radius: 16px;
        padding: 22px 24px;
        animation: kpiPulseGlow 4s infinite ease-in-out;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 18px 36px 6px rgba(168, 85, 247, 0.85) !important;
    }
    
    .kpi-title {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-color, #64748B);
        opacity: 0.8;
        margin-bottom: 4px;
    }
    
    .kpi-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: var(--text-color, #0F172A);
    }
    
    .kpi-sub {
        font-size: 0.8rem;
        color: var(--text-color, #94A3B8);
        opacity: 0.75;
        margin-top: 4px;
    }

    .badge-matched {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 3px 2px;
    }

    .badge-missing {
        display: inline-block;
        background: rgba(239, 68, 68, 0.15);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 3px 2px;
    }

    .badge-generic {
        display: inline-block;
        background: rgba(99, 102, 241, 0.12);
        color: var(--text-color, #334155);
        border: 1px solid rgba(99, 102, 241, 0.25);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 3px 2px;
    }

    .fit-tag-strong {
        background: #10B981;
        color: white;
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.82rem;
    }

    .fit-tag-mod {
        background: #F59E0B;
        color: white;
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.82rem;
    }

    .fit-tag-low {
        background: #EF4444;
        color: white;
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.82rem;
    }

    .card-title-text {
        color: var(--text-color, #0F172A) !important;
        margin: 0;
        font-weight: 800;
        font-size: 1.6rem;
    }

    .card-sub-text {
        color: var(--text-color, #64748B) !important;
        opacity: 0.8;
        margin: 4px 0 0 0;
    }

    .kpi-card, .section-card {
        background-color: var(--secondary-background-color, #FFFFFF) !important;
        color: var(--text-color, #0F172A) !important;
    }

    .kpi-title {
        color: var(--text-color, #64748B) !important;
        opacity: 0.75;
    }

    .kpi-value {
        color: var(--text-color, #0F172A) !important;
    }

    .kpi-sub {
        color: var(--text-color, #94A3B8) !important;
        opacity: 0.7;
    }

    /* Red Accent Colors for Sliders, Values, Tabs & Radio Buttons */
    div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"] {
        background-color: #FF4B4B !important;
        border-color: #FF4B4B !important;
    }

    div[data-testid="stSlider"] div[data-testid="stThumbValue"] {
        color: #FF4B4B !important;
        font-weight: 700 !important;
    }

    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
        background-color: #FF4B4B !important;
    }

    /* Tab bar active indicator and text */
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #FF4B4B !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #FF4B4B !important;
        font-weight: 700 !important;
    }

    div[data-baseweb="tab-highlight"] {
        background-color: #FF4B4B !important;
    }

    /* Radio button active dot */
    div[data-baseweb="radio"] input:checked + div,
    div[data-baseweb="radio"] div[aria-checked="true"] {
        background-color: #FF4B4B !important;
        border-color: #FF4B4B !important;
    }

    div[data-baseweb="radio"] div[aria-checked="true"] > div {
        background-color: #FF4B4B !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Header Banner ---
st.markdown("""
<div class="main-header">
    <div style="position: relative; z-index: 2;">
        <h1 style="display: flex; align-items: center; gap: 12px;">
            <span>🎯</span>
            <span style="background: linear-gradient(to right, #FFFFFF, #E0E7FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI Resume Screening & Candidate Ranking System</span>
        </h1>
        <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px;">
            <span style="background: rgba(255, 255, 255, 0.18); backdrop-filter: blur(10px); padding: 5px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.3); color: #F8FAFC;">✨ Automated NLP Screening</span>
            <span style="background: rgba(255, 255, 255, 0.18); backdrop-filter: blur(10px); padding: 5px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.3); color: #F8FAFC;">🟢 Skill Gap Analysis</span>
            <span style="background: rgba(255, 255, 255, 0.18); backdrop-filter: blur(10px); padding: 5px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.3); color: #F8FAFC;">⚡ Multi-Factor Weighted Scoring</span>
            <span style="background: rgba(255, 255, 255, 0.18); backdrop-filter: blur(10px); padding: 5px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.3); color: #F8FAFC;">📊 Excel / CSV Export</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Preloaded Demo Paths ---
BASE_DIR = os.path.dirname(__file__)
SAMPLE_JD_DIR = os.path.join(BASE_DIR, "sample_data", "job_descriptions")
SAMPLE_RESUME_DIR = os.path.join(BASE_DIR, "sample_data", "resumes")

PRELOADED_JDS = {
    "Senior Python Backend Developer (4+ Yrs)": "senior_python_backend_jd.txt",
    "Data Scientist & AI / ML Engineer (3+ Yrs)": "data_scientist_ai_engineer_jd.txt",
    "English Teacher & Literature Educator (3+ Yrs)": "english_teacher_jd.txt"
}

# --- Sidebar Controls ---
with st.sidebar:
    st.markdown("""
    <style>
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 8px 22px -4px rgba(99, 102, 241, 0.4); }
        50% { box-shadow: 0 14px 32px 2px rgba(168, 85, 247, 0.7); }
        100% { box-shadow: 0 8px 22px -4px rgba(99, 102, 241, 0.4); }
    }
    .moving-banner {
        background: linear-gradient(-45deg, #1E1B4B, #312E81, #4338CA, #6366F1, #8B5CF6, #3B82F6);
        background-size: 300% 300%;
        animation: gradientShift 7s ease infinite, pulseGlow 4s infinite ease-in-out;
        padding: 24px 18px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        position: relative;
    }
    </style>
    <div class="moving-banner">
        <div style="width: 56px; height: 56px; background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(12px); border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.4);">
            <span style="font-size: 28px;">⚡</span>
        </div>
        <div style="font-size: 1.3rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.01em;">AI Screener Pro</div>
        <div style="font-size: 0.78rem; color: #E0E7FF; font-weight: 500; margin-top: 3px;">Recruiter Command Center</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🎛️ Operation Controls")
    
    app_mode = st.radio(
        "Select Operation Mode:",
        ["✨ 1-Click Instant Demo", "📁 Upload Custom Files"],
        help="Use Instant Demo for instant presentation or Upload Custom Files for your own documents."
    )
    
    st.markdown("---")
    with st.expander("⚙️ Advanced Scoring Settings", expanded=False):
        st.caption("Fine-tune algorithm weightage for specific hiring preferences")
        w_skill = st.slider("Skill Overlap Weight", min_value=0, max_value=100, value=60, step=5, format="%d%%")
        w_exp = st.slider("Experience Weight", min_value=0, max_value=100, value=20, step=5, format="%d%%")
        w_edu = st.slider("Education Weight", min_value=0, max_value=100, value=20, step=5, format="%d%%")
        
        # Normalize weights
        total_w = float(w_skill + w_exp + w_edu)
        if total_w > 0:
            weights = {
                "skill_weight": w_skill / total_w,
                "semantic_weight": 0.0,
                "exp_weight": w_exp / total_w,
                "edu_weight": w_edu / total_w
            }
        else:
            weights = {"skill_weight": 0.60, "semantic_weight": 0.0, "exp_weight": 0.20, "edu_weight": 0.20}

    shortlist_threshold = st.slider("Shortlist Cutoff Score (%)", min_value=30, max_value=90, value=50, step=5)
    
    user = st.session_state.get("user_info") or {"name": "Recruiter", "role": "Talent Specialist", "organization": "Edufyi Tech"}
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 12px 14px; margin-top: 16px; margin-bottom: 10px;">
        <div style="font-size: 0.72rem; color: #94A3B8; font-weight: 700; text-transform: uppercase;">👤 Active Recruiter</div>
        <div style="font-weight: 800; color: #F8FAFC; font-size: 0.95rem; margin-top: 2px;">{user.get('name', 'Recruiter')}</div>
        <div style="font-size: 0.78rem; color: #FF4B4B; margin-top: 2px; font-weight: 600;">{user.get('role', 'Talent Specialist')} • {user.get('organization', 'Enterprise')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Sign Out (Landing Page)", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_info = None
        st.rerun()

    st.markdown("---")
    st.caption("AI Resume Screening System v2.0 • Built with Python, NLP & Streamlit")

# --- Processing & Data Preparation ---
jd_text = ""
candidates_profiles = []

if app_mode == "✨ 1-Click Instant Demo":
    selected_jd_name = st.selectbox("Select Target Job Description Role:", list(PRELOADED_JDS.keys()))
        
    jd_filename = PRELOADED_JDS[selected_jd_name]
    jd_filepath = os.path.join(SAMPLE_JD_DIR, jd_filename)
    if os.path.exists(jd_filepath):
        jd_text = parse_txt(jd_filepath)
        
    # Load all sample PDF resumes
    if os.path.exists(SAMPLE_RESUME_DIR):
        for fname in sorted(os.listdir(SAMPLE_RESUME_DIR)):
            if fname.endswith('.pdf'):
                fpath = os.path.join(SAMPLE_RESUME_DIR, fname)
                text = parse_pdf(fpath)
                profile = parse_candidate_profile(text, filename=fname)
                candidates_profiles.append(profile)

else: # Upload Custom Files
    col_upload_jd, col_upload_res = st.columns(2)
    with col_upload_jd:
        st.subheader("1. Job Description")
        jd_input_method = st.radio("Input JD As:", ["Paste Text", "Upload File (PDF / DOCX / TXT)"], horizontal=True)
        if jd_input_method == "Paste Text":
            jd_text = st.text_area("Paste Job Description here:", height=200, placeholder="Paste requirements, skills, experience needed...")
        else:
            uploaded_jd = st.file_uploader("Upload Job Description", type=["pdf", "docx", "txt"])
            if uploaded_jd:
                jd_text = extract_document_text(uploaded_jd, uploaded_jd.name)
                
    with col_upload_res:
        st.subheader("2. Candidate Resumes")
        uploaded_resumes = st.file_uploader(
            "Upload Multiple Resumes (PDF, DOCX, TXT)",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )
        if uploaded_resumes:
            for up_file in uploaded_resumes:
                res_text = extract_document_text(up_file, up_file.name)
                profile = parse_candidate_profile(res_text, filename=up_file.name)
                candidates_profiles.append(profile)

# --- Analysis & Dashboard Rendering ---
if not jd_text.strip():
    st.warning("⚠️ Please provide a Job Description (paste text or choose a demo role) to begin screening.")
    st.stop()

if not candidates_profiles:
    st.warning("⚠️ Please upload at least one resume or use Demo Mode to view ranking results.")
    st.stop()

# Parse JD
jd_profile = parse_job_description(jd_text)

# Rank Candidates
ranked_candidates = rank_candidates(candidates_profiles, jd_profile, weights)

# Filter shortlisted
shortlisted_candidates = [c for c in ranked_candidates if c["final_score"] >= shortlist_threshold]

# --- Section 1: Executive KPI Metric Cards ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Applicants</div>
        <div class="kpi-value">{len(ranked_candidates)}</div>
        <div class="kpi-sub">Resumes Parsed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Shortlisted Candidates</div>
        <div class="kpi-value" style="color: #10B981;">{len(shortlisted_candidates)}</div>
        <div class="kpi-sub">Match Score &ge; {shortlist_threshold}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_score = round(sum(c["final_score"] for c in ranked_candidates) / len(ranked_candidates), 1)
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Average Match</div>
        <div class="kpi-value" style="color: #4F46E5;">{avg_score}%</div>
        <div class="kpi-sub">Across All Candidates</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    top_candidate = ranked_candidates[0] if ranked_candidates else None
    top_name = top_candidate["candidate_name"] if top_candidate else "N/A"
    top_score = top_candidate["final_score"] if top_candidate else 0
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Top Match</div>
        <div class="kpi-value" style="color: #0EA5E9; font-size: 1.5rem;">{top_name[:15]}</div>
        <div class="kpi-sub">{top_score}% Match Score</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Section 2: Job Description Skills Summary ---
with st.expander("🔍 **View Detected Job Description Requirements**", expanded=False):
    c_jd1, c_jd2 = st.columns([3, 1])
    with c_jd1:
        st.markdown(f"**Required Skills Detected ({len(jd_profile['skills'])}):**")
        skills_html = "".join([f'<span class="badge-matched">{s}</span>' for s in jd_profile["skills"]])
        st.markdown(skills_html if skills_html else "No specific skills detected.", unsafe_allow_html=True)
    with c_jd2:
        st.markdown(f"**Min Experience:** {jd_profile['min_experience_years']} Years")
        st.markdown(f"**Education:** {', '.join(jd_profile['required_education']) if jd_profile['required_education'] else 'Any Degree'}")

# --- Section 3: Visual Analytics & Leaderboard ---
tab_ranking, tab_analytics, tab_inspector, tab_export = st.tabs([
    "🏆 Candidate Leaderboard",
    "📊 Comparative Analytics",
    "👤 Deep-Dive Candidate Inspector",
    "📥 Export Center"
])

with tab_ranking:
    col_lead_head, col_lead_filter = st.columns([2, 1])
    with col_lead_head:
        st.subheader("🎯 Ranked Applicant Leaderboard")
    with col_lead_filter:
        show_only_shortlisted = st.checkbox(f"Show Only Shortlisted (≥ {shortlist_threshold}%)", value=False)
    
    # 🔍 Instant Keyword & Skill Search Bar
    search_query = st.text_input(
        "🔍 Instant Keyword & Skill Search:",
        placeholder="Type any skill (e.g. Python, Docker, PyTorch), candidate name, degree, or email...",
        help="Filters the leaderboard in real time based on your search query."
    )
    
    # Filtering logic
    base_candidates = shortlisted_candidates if show_only_shortlisted else ranked_candidates
    
    if search_query.strip():
        q_clean = search_query.strip().lower()
        display_candidates = []
        for c in base_candidates:
            all_text_search = (
                c["candidate_name"].lower() + " " +
                c["email"].lower() + " " +
                " ".join(c["matched_skills"]).lower() + " " +
                " ".join(c["total_candidate_skills"]).lower() + " " +
                " ".join(c["education"]).lower() + " " +
                c["filename"].lower()
            )
            if q_clean in all_text_search:
                display_candidates.append(c)
        st.caption(f"🔎 Found **{len(display_candidates)}** candidates matching *'{search_query}'*")
    else:
        display_candidates = base_candidates
    
    if not display_candidates:
        st.warning(f"No candidates match your criteria. Try adjusting the search query or lowering the Cutoff Score in the sidebar.")
    else:
        table_data = []
        for c in display_candidates:
            is_shortlisted = "✅ Shortlisted" if c['final_score'] >= shortlist_threshold else "❌ Below Cutoff"
            table_data.append({
                "Rank": f"#{c['rank']}",
                "Candidate Name": c["candidate_name"],
                "Match Score": c['final_score'],
                "Shortlisted Status": is_shortlisted,
                "Fit Status": c["fit_status"],
                "Matched Skills": f"{len(c['matched_skills'])} / {len(jd_profile['skills'])}",
                "Experience": f"{c['experience_years']} yrs",
                "Education": ", ".join(c["education"]),
                "Email": c["email"],
                "File": c["filename"]
            })
        df_table = pd.DataFrame(table_data)
        
        st.dataframe(
            df_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Match Score": st.column_config.ProgressColumn(
                    "Match Score",
                    help="Overall Weighted Score",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100
                )
            }
        )

with tab_analytics:
    st.subheader("📊 Recruiter Analytics")
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        fig_leaderboard = create_leaderboard_chart(ranked_candidates)
        st.plotly_chart(fig_leaderboard, use_container_width=True)
    with col_chart2:
        if top_candidate:
            fig_category = create_category_distribution_chart(top_candidate.get("skills_by_category", {}))
            st.plotly_chart(fig_category, use_container_width=True)

def render_formatted_resume_paper(candidate: dict) -> str:
    name = candidate.get("candidate_name", "Candidate Profile")
    email = candidate.get("email", "")
    phone = candidate.get("phone", "")
    linkedin = candidate.get("linkedin", "")
    github = candidate.get("github", "")
    exp = candidate.get("experience_years", 0)
    education = ", ".join(candidate.get("education", []))
    raw_text = candidate.get("raw_text", "")
    
    contact_items = []
    if email and email != "Not detected":
        contact_items.append(f"📧 {email}")
    if phone and phone != "Not detected":
        contact_items.append(f"📱 {phone}")
    if linkedin:
        contact_items.append(f"🔗 {linkedin}")
    if github:
        contact_items.append(f"💻 {github}")
        
    contact_html = " &nbsp;|&nbsp; ".join(contact_items) if contact_items else "No direct contact details"
    
    formatted_paragraphs = []
    for line in raw_text.split('\n'):
        line_clean = line.strip()
        if not line_clean:
            continue
        if line_clean.isupper() and len(line_clean) < 45:
            formatted_paragraphs.append(f'<h4 style="color: #6366F1; margin: 18px 0 8px 0; border-bottom: 2px solid rgba(99,102,241,0.25); padding-bottom: 4px; font-size: 0.95rem; letter-spacing: 0.05em; text-transform: uppercase;">{line_clean}</h4>')
        elif line_clean.startswith("Email:") or line_clean.startswith("Phone:"):
            continue
        elif line_clean == name:
            continue
        else:
            formatted_paragraphs.append(f'<p style="margin: 6px 0; line-height: 1.6; font-size: 0.9rem; color: var(--text-color, #334155); opacity: 0.9;">{line_clean}</p>')
            
    body_content_html = "".join(formatted_paragraphs)
    
    return f"""
    <div style="
        background-color: var(--secondary-background-color, #FFFFFF);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 16px;
        padding: 28px 32px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
        font-family: 'Plus Jakarta Sans', sans-serif;
        margin-top: 14px;
    ">
        <!-- Resume Paper Header -->
        <div style="border-bottom: 2px solid rgba(99, 102, 241, 0.3); padding-bottom: 14px; margin-bottom: 18px;">
            <h1 style="margin: 0; font-size: 1.7rem; font-weight: 800; color: var(--text-color, #0F172A);">{name}</h1>
            <div style="font-size: 0.85rem; color: var(--text-color, #64748B); opacity: 0.9; margin-top: 6px;">
                {contact_html}
            </div>
            <div style="font-size: 0.85rem; color: #6366F1; font-weight: 600; margin-top: 8px;">
                🎓 <b>Education:</b> {education} &nbsp;|&nbsp; ⏳ <b>Total Experience:</b> {exp} Years
            </div>
        </div>
        
        <!-- Formatted Resume Body -->
        <div>
            {body_content_html}
        </div>
    </div>
    """

with tab_inspector:
    st.subheader("👤 Individual Candidate Deep Dive")
    
    cand_names = [f"Rank #{c['rank']} - {c['candidate_name']} ({c['final_score']}%)" for c in ranked_candidates]
    selected_idx = st.selectbox("Select Candidate to Inspect:", range(len(ranked_candidates)), format_func=lambda i: cand_names[i])
    
    selected_cand = ranked_candidates[selected_idx]
    
    # Candidate Header Card
    st.markdown(f"""
    <div class="section-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 class="card-title-text">{selected_cand['candidate_name']}</h2>
                <p class="card-sub-text">
                    📧 {selected_cand['email']} &nbsp;|&nbsp; 📱 {selected_cand['phone']} &nbsp;|&nbsp; 📄 {selected_cand['filename']}
                </p>
                <p class="card-sub-text">
                    🎓 <b>Education:</b> {', '.join(selected_cand['education'])} &nbsp;|&nbsp; ⏳ <b>Experience:</b> {selected_cand['experience_years']} Years
                </p>
            </div>
            <div>
                <span class="fit-tag-{'strong' if selected_cand['fit_status'] == 'Strong Fit' else ('mod' if selected_cand['fit_status'] == 'Moderate Fit' else 'low')}">
                    {selected_cand['fit_status']} ({selected_cand['final_score']}%)
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Visual Breakdown & Gauges
    c_g1, c_g2 = st.columns(2)
    with c_g1:
        st.plotly_chart(create_score_gauge(selected_cand["final_score"]), use_container_width=True)
    with c_g2:
        st.plotly_chart(create_breakdown_bar(selected_cand), use_container_width=True)
        
    st.markdown("---")
    
    # Matched vs Missing Skills Badges
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        st.markdown(f"#### 🟢 Matched Skills ({len(selected_cand['matched_skills'])})")
        if selected_cand["matched_skills"]:
            matched_html = "".join([f'<span class="badge-matched">✅ {s}</span>' for s in selected_cand["matched_skills"]])
            st.markdown(matched_html, unsafe_allow_html=True)
        else:
            st.info("No direct skill matches found with the JD.")
            
    with col_s2:
        st.markdown(f"#### 🔴 Missing Skills / Skill Gap ({len(selected_cand['missing_skills'])})")
        if selected_cand["missing_skills"]:
            missing_html = "".join([f'<span class="badge-missing">❌ {s}</span>' for s in selected_cand["missing_skills"]])
            st.markdown(missing_html, unsafe_allow_html=True)
        else:
            st.success("Candidate matches 100% of required JD skills!")

    st.markdown("<br>", unsafe_allow_html=True)

    # 📄 Built-in Formatted Resume Paper Viewer Accordion
    with st.expander(f"📄 **View Formatted Resume Document ({selected_cand['candidate_name']})**", expanded=False):
        raw_text_val = selected_cand.get("raw_text", "")
        c_meta1, c_meta2, c_meta3 = st.columns(3)
        with c_meta1:
            st.metric("Total Characters", f"{len(raw_text_val):,}")
        with c_meta2:
            st.metric("Total Words", f"{len(raw_text_val.split()):,}")
        with c_meta3:
            st.metric("Source File", selected_cand.get("filename", "N/A"))
            
        st.markdown(render_formatted_resume_paper(selected_cand), unsafe_allow_html=True)

with tab_export:
    st.subheader("📥 Export Screening Results")
    st.markdown("Download candidate evaluations, rank scores, matched skills, and gap analysis for HR records.")
    
    st.markdown("##### 1. Export All Applicants (CSV, Excel & Branded PDF Report)")
    csv_bytes = export_to_csv(ranked_candidates)
    excel_bytes = export_to_excel(ranked_candidates, jd_profile["skills"])
    pdf_bytes = export_to_pdf(ranked_candidates, jd_title=selected_jd_name if app_mode == "✨ 1-Click Instant Demo" else "Job Position", jd_skills=jd_profile["skills"])
    
    c_exp1, c_exp2, c_exp3 = st.columns(3)
    with c_exp1:
        st.download_button(
            label="📄 Download CSV Report",
            data=csv_bytes,
            file_name="all_candidate_rankings.csv",
            mime="text/csv",
            use_container_width=True
        )
    with c_exp2:
        st.download_button(
            label="📊 Download Excel Report (.xlsx)",
            data=excel_bytes,
            file_name="all_candidate_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    with c_exp3:
        st.download_button(
            label="📕 Download Branded PDF Report",
            data=pdf_bytes,
            file_name="candidate_evaluation_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"##### 2. Export Only Shortlisted Candidates (Score ≥ {shortlist_threshold}%)")
    if shortlisted_candidates:
        short_csv_bytes = export_to_csv(shortlisted_candidates)
        short_excel_bytes = export_to_excel(shortlisted_candidates, jd_profile["skills"])
        short_pdf_bytes = export_to_pdf(shortlisted_candidates, jd_title=f"{selected_jd_name if app_mode == '✨ 1-Click Instant Demo' else 'Job Position'} (Shortlisted)", jd_skills=jd_profile["skills"])
        
        c_short1, c_short2, c_short3 = st.columns(3)
        with c_short1:
            st.download_button(
                label=f"🟢 Download Shortlisted CSV",
                data=short_csv_bytes,
                file_name="shortlisted_candidates.csv",
                mime="text/csv",
                use_container_width=True
            )
        with c_short2:
            st.download_button(
                label=f"📊 Download Shortlisted Excel (.xlsx)",
                data=short_excel_bytes,
                file_name="shortlisted_candidates_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        with c_short3:
            st.download_button(
                label=f"📕 Download Shortlisted PDF Report",
                data=short_pdf_bytes,
                file_name="shortlisted_evaluation_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.info("No candidates meet the current shortlist threshold.")
