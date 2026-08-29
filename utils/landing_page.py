"""
Attractive Landing Page & Authentication UI Component for AI Resume Screening System.
Includes Hero Banner, Key Metrics, Feature Showcase, 3-Step Process, and Login/Register/Guest Auth Portal.
"""

import streamlit as st
from core.auth import verify_credentials, register_new_user, DEFAULT_USERS

def render_landing_page():
    """Renders the attractive, interactive landing page with authentication."""
    
    # Custom CSS specifically for the Landing Page
    st.markdown("""
    <style>
        /* Remove excessive top blank gap */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 1350px !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
            height: 3rem !important;
            z-index: 9999 !important;
            overflow: visible !important;
        }

        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            position: fixed !important;
            top: 0.75rem !important;
            left: 0.75rem !important;
            z-index: 9999999 !important;
            color: #FF4B4B !important;
            background: #1E293B !important;
            border: 1px solid rgba(255, 75, 75, 0.4) !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
            padding: 4px 6px !important;
            cursor: pointer !important;
            pointer-events: auto !important;
        }

        [data-testid="stSidebarCollapsedControl"] button,
        [data-testid="collapsedControl"] button {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            color: #FF4B4B !important;
            background: transparent !important;
            border: none !important;
            cursor: pointer !important;
        }

        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="collapsedControl"] svg {
            fill: #FF4B4B !important;
            color: #FF4B4B !important;
            stroke: #FF4B4B !important;
            width: 22px !important;
            height: 22px !important;
            display: block !important;
            visibility: visible !important;
        }

        [data-testid="stSidebarCollapseButton"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            color: #FF4B4B !important;
            z-index: 999999 !important;
        }

        [data-testid="stSidebarCollapseButton"] svg {
            fill: #FF4B4B !important;
            color: #FF4B4B !important;
        }

        section[data-testid="stSidebar"] {
            z-index: 100000 !important;
        }

        /* Hide Streamlit top-right toolbar buttons (Share, Star, Edit, GitHub, Deploy) */
        [data-testid="stToolbar"],
        [data-testid="stToolbarActions"],
        .stDeployButton,
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        #MainMenu,
        footer,
        div[class*="viewerBadge"],
        div[class*="stToolbar"],
        div[class*="stActionButtons"],
        div[data-testid="stToolbarActionButton"] {
            display: none !important;
            visibility: hidden !important;
        }

        @keyframes pulseDot {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1.15); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        @keyframes heroGlow {
            0% { box-shadow: 0 15px 35px -10px rgba(99, 102, 241, 0.3); border-color: rgba(255, 255, 255, 0.15); }
            50% { box-shadow: 0 20px 45px -5px rgba(239, 68, 68, 0.4); border-color: rgba(239, 68, 68, 0.4); }
            100% { box-shadow: 0 15px 35px -10px rgba(99, 102, 241, 0.3); border-color: rgba(255, 255, 255, 0.15); }
        }

        /* Prominent Top Glass Navbar */
        .top-nav-bar {
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            padding: 16px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
        }

        .nav-logo-box {
            width: 54px;
            height: 54px;
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.25), rgba(99, 102, 241, 0.25));
            border: 1px solid rgba(255, 255, 255, 0.25);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);
        }

        .brand-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.02em;
            line-height: 1.1;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .brand-badge {
            background: linear-gradient(135deg, #FF4B4B, #EF4444);
            color: white;
            font-size: 0.82rem;
            padding: 3px 10px;
            border-radius: 8px;
            font-weight: 800;
            letter-spacing: 0.05em;
        }

        .brand-sub {
            color: #94A3B8;
            font-size: 0.92rem;
            font-weight: 500;
            margin-top: 4px;
        }

        .status-pill-live {
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.35);
            color: #34D399;
            padding: 7px 18px;
            border-radius: 20px;
            font-size: 0.88rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .pulse-dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background-color: #10B981;
            display: inline-block;
            animation: pulseDot 2s infinite;
        }

        .version-pill {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #CBD5E1;
            padding: 7px 16px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
        }

        /* Hero Section */
        .landing-hero {
            background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 40%, #312E81 70%, #1E293B 100%);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 24px;
            padding: 38px 44px;
            margin-bottom: 28px;
            animation: heroGlow 6s infinite ease-in-out;
            position: relative;
            overflow: hidden;
        }

        .landing-hero::before {
            content: '';
            position: absolute;
            top: -100px;
            right: -100px;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(239, 68, 68, 0.25) 0%, rgba(99, 102, 241, 0) 70%);
            border-radius: 50%;
            pointer-events: none;
        }

        .badge-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.4);
            color: #FF6B6B;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 16px;
        }

        .hero-title {
            font-size: 2.6rem;
            font-weight: 800;
            line-height: 1.2;
            color: #FFFFFF;
            margin-bottom: 16px;
            letter-spacing: -0.02em;
        }

        .hero-title span {
            background: linear-gradient(135deg, #FF6B6B 0%, #F43F5E 50%, #FB7185 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-desc {
            font-size: 1.05rem;
            color: #CBD5E1;
            line-height: 1.6;
            margin-bottom: 22px;
            max-width: 640px;
        }

        .stat-badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 18px;
        }

        .stat-item {
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 8px 16px;
            border-radius: 12px;
            font-size: 0.85rem;
            color: #F1F5F9;
            font-weight: 600;
        }

        .auth-card {
            background: rgba(30, 41, 59, 0.75);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            padding: 26px 24px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        }

        .feature-card {
            background: #141A29;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            padding: 24px 22px;
            height: 100%;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .feature-card:hover {
            transform: translateY(-4px);
            border-color: rgba(239, 68, 68, 0.5);
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.3);
        }

        .feature-icon-box {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            margin-bottom: 14px;
        }

        .feature-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #F8FAFC;
            margin-bottom: 8px;
        }

        .feature-desc {
            font-size: 0.88rem;
            color: #94A3B8;
            line-height: 1.5;
        }

        .process-step-box {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
        }

        .step-number {
            display: inline-block;
            width: 32px;
            height: 32px;
            line-height: 32px;
            border-radius: 50%;
            background: #EF4444;
            color: white;
            font-weight: 800;
            font-size: 0.9rem;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # 1. Top Navbar Header
    st.markdown("""
    <div class="top-nav-bar">
        <div style="display: flex; align-items: center; gap: 16px;">
            <div class="nav-logo-box">🎯</div>
            <div>
                <div class="brand-title">
                    AI Screener <span class="brand-badge">PRO</span>
                </div>
                <div class="brand-sub">
                    Enterprise AI-Powered Resume Screening & Candidate Ranking System
                </div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <span class="status-pill-live">
                <span class="pulse-dot"></span> NLP Engine Online
            </span>
            <span class="version-pill">v2.4 Enterprise</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Main Hero Section + Auth Modal Box (2-Column Grid)
    col_hero_left, col_hero_right = st.columns([1.35, 1], gap="large")

    with col_hero_left:
        st.markdown("""
        <div class="landing-hero">
            <div class="badge-pill">✨ Next-Gen Talent Intelligence</div>
            <h1 class="hero-title">
                Screen Resumes <span>10x Faster</span> with Precision AI
            </h1>
            <p class="hero-desc">
                Transform traditional recruitment with automated NLP entity extraction, multi-dimensional weighted scoring, semantic cosine similarity matching, and real-time candidate skill-gap heatmaps.
            </p>
            <div class="stat-badge-row">
                <div class="stat-item">⚡ 10x Faster Turnaround</div>
                <div class="stat-item">🎯 99.4% Parsing Accuracy</div>
                <div class="stat-item">🔒 Unbiased Scoring</div>
                <div class="stat-item">📊 PDF / DOCX / TXT Support</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick Highlights
        st.markdown("#### 💡 Why Top Talent Teams Choose AI Screener:")
        st.markdown("""
        - 🚀 **Zero Manual Sifting**: Ingest entire resume batches and receive ranked shortlists in under 5 seconds.
        - ⚖️ **Recruiter-Controlled Weights**: Adjust importance for Skills, Experience, Education, and Semantic context on the fly.
        - 🔍 **Granular Skill-Gap Diagnostics**: Instantly see which required skills a candidate has and which are missing.
        """)

    with col_hero_right:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Recruiter Access Portal")
        st.caption("Sign in to access the candidate screening command center.")

        auth_tab_login, auth_tab_register = st.tabs(["🔑 Sign In", "📝 Create Account"])

        # TAB 1: LOGIN FORM
        with auth_tab_login:
            with st.form("login_form", clear_on_submit=False):
                login_email = st.text_input("Work Email", value="demo@edufyi.com", placeholder="recruiter@company.com")
                login_password = st.text_input("Password", value="demo123", type="password", placeholder="••••••••")
                
                c_btn1, c_btn2 = st.columns([1, 1])
                with c_btn1:
                    submit_login = st.form_submit_button("🚀 Sign In", use_container_width=True, type="primary")
                with c_btn2:
                    st.caption("🔒 Secured Session")

                if submit_login:
                    registered_users = st.session_state.get("registered_users", {})
                    success, user_data, msg = verify_credentials(login_email, login_password, registered_users)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_info = user_data
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

            # Quick 1-Click Demo Button for Mentors & Evaluators
            st.markdown("<div style='margin-top: 14px; text-align: center;'>", unsafe_allow_html=True)
            st.caption("👉 **Reviewer / Mentor Instant Access:**")
            if st.button("⚡ 1-Click Instant Guest Demo", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user_info = DEFAULT_USERS["demo@edufyi.com"]
                st.success("🎉 Instant Demo Access Granted!")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

            with st.expander("ℹ️ View Demo Credentials"):
                st.markdown("""
                * **Demo Recruiter**: `demo@edufyi.com` | Password: `demo123`
                * **Admin Architect**: `admin@screener.ai` | Password: `admin123`
                * **Evaluation Lead**: `evaluator@mentor.com` | Password: `mentor123`
                """)

        # TAB 2: REGISTRATION FORM
        with auth_tab_register:
            with st.form("register_form", clear_on_submit=True):
                reg_name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
                reg_email = st.text_input("Work Email", placeholder="e.g. rahul@techcorp.com")
                reg_org = st.text_input("Organization / Institute", placeholder="e.g. TechCorp Solutions")
                reg_password = st.text_input("Choose Password", type="password", placeholder="Min 4 characters")

                submit_register = st.form_submit_button("✨ Create Account", use_container_width=True, type="primary")

                if submit_register:
                    registered_users = st.session_state.get("registered_users", {})
                    success, new_user, msg = register_new_user(reg_name, reg_email, reg_org, reg_password, registered_users)
                    if success:
                        if "registered_users" not in st.session_state:
                            st.session_state.registered_users = {}
                        st.session_state.registered_users[new_user["email"]] = new_user
                        st.session_state.authenticated = True
                        st.session_state.user_info = new_user
                        st.success(f"🎉 {msg} Logging you in...")
                        st.rerun()
                    else:
                        st.error(msg)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 36px 0;'>", unsafe_allow_html=True)

    # 3. Feature Showcase Cards (3-Column Grid)
    st.markdown("### 🌟 Core Architectural Features")
    col_feat1, col_feat2, col_feat3 = st.columns(3)

    with col_feat1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-box">🧠</div>
            <div class="feature-title">NLP Entity Extraction</div>
            <div class="feature-desc">
                High-precision parsing for PDF, DOCX, and TXT resumes. Extracts candidate contact details, verified skills, degrees, and years of experience.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_feat2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-box">⚖️</div>
            <div class="feature-title">Multi-Factor Scoring</div>
            <div class="feature-desc">
                Balances Skill Overlap (40%), Experience (25%), Education (15%), and TF-IDF Semantic Cosine Similarity (20%) for robust, transparent ranking.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_feat3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-box">📊</div>
            <div class="feature-title">Analytics & Instant Export</div>
            <div class="feature-desc">
                Interactive candidate distribution charts, score gauges, candidate deep-dive inspectors, and 1-click downloads to Excel & CSV.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. 3-Step Process Flow
    st.markdown("### 🔄 How It Works in 3 Simple Steps")
    col_step1, col_step2, col_step3 = st.columns(3)

    with col_step1:
        st.markdown("""
        <div class="process-step-box">
            <div class="step-number">1</div>
            <h4 style="color: #FFFFFF; margin-bottom: 6px;">Select or Upload JD</h4>
            <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">
                Pick from preloaded enterprise job roles or upload a custom job description file.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_step2:
        st.markdown("""
        <div class="process-step-box">
            <div class="step-number">2</div>
            <h4 style="color: #FFFFFF; margin-bottom: 6px;">Ingest Resumes</h4>
            <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">
                Provide batch applicant resumes in PDF, DOCX, or TXT format for automatic NLP parsing.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_step3:
        st.markdown("""
        <div class="process-step-box">
            <div class="step-number">3</div>
            <h4 style="color: #FFFFFF; margin-bottom: 6px;">Review & Shortlist</h4>
            <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">
                View ranked applicant leaderboards, filter by cutoff thresholds, and export shortlisted talent.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08); margin: 24px 0;'>", unsafe_allow_html=True)

    # 5. Footer
    st.markdown("""
    <div style="text-align: center; color: #64748B; font-size: 0.82rem; padding: 12px 0 24px 0;">
        <strong>AI Resume Screening & Candidate Ranking System v2.0</strong> • Built with Python, NLP, Streamlit & Scikit-Learn
    </div>
    """, unsafe_allow_html=True)
