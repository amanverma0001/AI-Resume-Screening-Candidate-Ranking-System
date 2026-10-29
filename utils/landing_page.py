"""
Interactive Modern Landing Portal Component for AI Resume Screening System.
Compact, zero-scroll centered panel with rich moving resume match stream background.
Borderless form aesthetic matching Screenshot 1.
"""

import streamlit as st
from core.auth import verify_credentials, register_new_user, DEFAULT_USERS

def render_landing_page():
    """Renders the borderless, compact recruiter command center portal."""

    st.markdown("""<style>
/* 1. RESET STREAMLIT APP BACKGROUND & ELIMINATE SQUASHING */
html, body {
    margin: 0 !important;
    padding: 0 !important;
    background-color: #080C14 !important;
    overflow-x: hidden !important;
    min-height: 100vh !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

[data-testid="stApp"],
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
header,
.main,
[data-testid="stMain"] {
    background: transparent !important;
    background-color: transparent !important;
}

/* Hide deploy button, header decoration, and sidebar triggers */
header, [data-testid="stHeader"], [data-testid="stAppDeployButton"], .stDeployButton, [data-testid="stToolbarActions"], [data-testid="stToolbar"], #MainMenu,
[data-testid="stToolbarActions"],
#MainMenu,
footer,
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
    visibility: hidden !important;
}

/* 2. BACKGROUND LAYER: ZERO FLOW SPACE, FIXED BEHIND EVERYTHING */
div[data-testid="stElementContainer"]:has(.resume-bg-root),
div.stMarkdown:has(.resume-bg-root),
.resume-bg-root {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
    z-index: 0 !important;
    pointer-events: none !important;
    user-select: none !important;
    overflow: hidden !important;
    background: radial-gradient(ellipse at 50% 25%, #0F192C 0%, #080C14 85%) !important;
}

.resume-bg-root * {
    pointer-events: none !important;
    user-select: none !important;
}

.resume-grid-mesh {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        linear-gradient(to right, rgba(255, 255, 255, 0.035) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.035) 1px, transparent 1px);
    background-size: 80px 48px;
}

.chart-scroll-track {
    position: absolute;
    top: 0;
    left: 0;
    width: 3200px;
    height: 100vh;
    animation: resumeStreamScroll 26s linear infinite;
}

@keyframes resumeStreamScroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-1600px); }
}

.y-axis-talent-tiers {
    position: absolute;
    right: 22px;
    top: 15%;
    display: flex;
    flex-direction: column;
    gap: 22px;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 11px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.22);
    text-align: right;
    pointer-events: none;
    letter-spacing: 0.05em;
    z-index: 1;
}

.live-match-pill {
    position: absolute;
    right: 14px;
    top: 50%;
    background: linear-gradient(135deg, #10B981, #059669);
    color: #FFFFFF;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 11px;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 4px;
    box-shadow: 0 0 16px rgba(16, 185, 129, 0.7);
    z-index: 1;
}

.float-resume-badge {
    position: absolute;
    background: rgba(14, 21, 37, 0.88);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(56, 189, 248, 0.32);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.78rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.55);
    z-index: 1;
}

.badge-top-cand { top: 18%; left: 8%; animation: resumeBadgeFloat1 8s ease-in-out infinite alternate; color: #10B981; }
.badge-nlp-speed { top: 24%; right: 10%; animation: resumeBadgeFloat2 9s ease-in-out infinite alternate; color: #38BDF8; }
.badge-sdg { top: 52%; left: 6%; animation: resumeBadgeFloat2 8.5s ease-in-out infinite alternate; color: #38BDF8; }
.badge-dataset { bottom: 12%; left: 8%; animation: resumeBadgeFloat3 10s ease-in-out infinite alternate; color: #A855F7; }
.badge-architect { bottom: 16%; right: 10%; animation: resumeBadgeFloat4 7s ease-in-out infinite alternate; color: #10B981; }

@keyframes resumeBadgeFloat1 { 0% { transform: translate(0, 0); } 100% { transform: translate(16px, -12px); } }
@keyframes resumeBadgeFloat2 { 0% { transform: translate(0, 0); } 100% { transform: translate(-14px, 16px); } }
@keyframes resumeBadgeFloat3 { 0% { transform: translate(0, 0); } 100% { transform: translate(18px, 12px); } }
@keyframes resumeBadgeFloat4 { 0% { transform: translate(0, 0); } 100% { transform: translate(-16px, -14px); } }

.bottom-telemetry-bar {
    position: absolute;
    bottom: 12px;
    left: 0;
    width: 100%;
    text-align: center;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 11px;
    color: rgba(255, 255, 255, 0.28);
    letter-spacing: 0.12em;
    pointer-events: none;
    z-index: 1;
}

/* 3. CENTERED WORKSPACE & BORDERLESS PANEL AESTHETIC */
.block-container {
    max-width: 1240px !important;
    width: 100% !important;
    padding-top: max(24px, calc(50vh - 290px)) !important;
    padding-bottom: 24px !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    margin: 0 auto !important;
    position: relative !important;
    z-index: 10 !important;
    pointer-events: auto !important;
}

/* Center column specifically holding the login portal */
div[data-testid="column"]:nth-of-type(2) {
    position: relative !important;
    z-index: 25 !important;
    pointer-events: auto !important;
}

/* Completely borderless container */
div[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stForm"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* Icon & Header styling matching Screenshot 1 */
.compact-icon-badge {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: #2563EB;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    margin: 0 auto 10px auto;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.5);
}

.compact-title {
    font-size: 2.15rem;
    font-weight: 800;
    color: #FFFFFF;
    text-align: center;
    margin: 0 0 4px 0;
    letter-spacing: -0.025em;
    line-height: 1.2;
}

.compact-sub {
    color: #94A3B8;
    font-size: 0.92rem;
    text-align: center;
    margin-bottom: 20px;
    font-weight: 500;
}

/* Tabs styling matching Screenshot 1 */
div[data-testid="column"]:nth-of-type(2) [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12) !important;
    gap: 16px !important;
    padding-bottom: 4px !important;
    margin-bottom: 16px !important;
}

div[data-testid="column"]:nth-of-type(2) [data-baseweb="tab"] {
    background: transparent !important;
    color: #94A3B8 !important;
    font-size: 0.94rem !important;
    font-weight: 600 !important;
    padding: 6px 4px !important;
    border: none !important;
    cursor: pointer !important;
}

div[data-testid="column"]:nth-of-type(2) [data-baseweb="tab"][aria-selected="true"] {
    color: #FF4B4B !important;
}

div[data-testid="column"]:nth-of-type(2) [data-baseweb="tab-highlight"] {
    background-color: #FF4B4B !important;
    height: 3px !important;
    border-radius: 2px !important;
}

/* 4. BUTTONS & CONTROLS: GUARANTEED CLICKABLE WITH MATCHING STYLES */
div[data-testid="column"]:nth-of-type(2) button,
div[data-testid="column"]:nth-of-type(2) input,
div[data-testid="column"]:nth-of-type(2) [data-baseweb="tab"],
div[data-testid="column"]:nth-of-type(2) [data-testid="stCheckbox"],
div[data-testid="column"]:nth-of-type(2) [data-testid="stFormSubmitButton"] button {
    pointer-events: auto !important;
    cursor: pointer !important;
}

/* 1-Click Instant Demo Button matching Screenshot 1 */
div[data-testid="column"]:nth-of-type(2) .stButton > button {
    background: rgba(15, 23, 42, 0.65) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    border-radius: 8px !important;
    padding: 10px 16px !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
    width: 100% !important;
}

div[data-testid="column"]:nth-of-type(2) .stButton > button:hover {
    background: rgba(30, 41, 59, 0.85) !important;
    border-color: rgba(255, 255, 255, 0.35) !important;
}

/* Input boxes matching Screenshot 1 */
div[data-testid="column"]:nth-of-type(2) [data-testid="stTextInput"] label p {
    color: #CBD5E1 !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    margin-bottom: 4px !important;
}

div[data-testid="column"]:nth-of-type(2) [data-baseweb="input"] {
    background-color: #151D2C !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
}

div[data-testid="column"]:nth-of-type(2) [data-baseweb="input"] input {
    background-color: transparent !important;
    color: #FFFFFF !important;
    font-size: 0.92rem !important;
}

div[data-testid="column"]:nth-of-type(2) [data-baseweb="input"]:focus-within {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 1px #38BDF8 !important;
}

/* Checkbox matching Screenshot 1 */
div[data-testid="column"]:nth-of-type(2) [data-testid="stCheckbox"] label p {
    color: #E2E8F0 !important;
    font-size: 0.86rem !important;
}

div[data-testid="column"]:nth-of-type(2) [data-testid="stCheckbox"] span[data-checked="true"] {
    background-color: #FF4B4B !important;
    border-color: #FF4B4B !important;
}

/* Submit Button: Red/Coral with soft glow matching Screenshot 1 */
div[data-testid="column"]:nth-of-type(2) [data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #FF4B4B, #E11D48) !important;
    background-color: #FF4B4B !important;
    color: #FFFFFF !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 20px !important;
    box-shadow: 0 6px 24px rgba(255, 75, 75, 0.45) !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

div[data-testid="column"]:nth-of-type(2) [data-testid="stFormSubmitButton"] button:hover {
    background: linear-gradient(135deg, #FF5C5C, #F43F5E) !important;
    box-shadow: 0 8px 30px rgba(255, 75, 75, 0.65) !important;
    transform: translateY(-1px) !important;
}

.compact-hint {
    text-align: center;
    color: #64748B;
    font-size: 0.72rem;
    margin-top: 10px;
}

.compact-hint code {
    color: #38BDF8;
    background: rgba(56, 189, 248, 0.1);
    padding: 2px 5px;
    border-radius: 4px;
    font-size: 0.72rem;
}
</style>""", unsafe_allow_html=True)

    # Full Background layer with waves, glowing nodes, floating badges, ladder, and bottom ticker
    st.markdown("""<div class="resume-bg-root">
<div class="resume-grid-mesh"></div>

<div class="y-axis-talent-tiers">
<div>100% TIER-1 ELITE</div>
<div>95% EXCEPTIONAL</div>
<div>90% SHORTLISTED</div>
<div>85% HIGH POTENTIAL</div>
<div>80% QUALIFIED</div>
<div>75% COMPETENT</div>
<div>70% BASELINE</div>
</div>

<div class="live-match-pill">● 99.4% MATCH</div>

<div class="float-resume-badge badge-top-cand">📄 Rahul Sharma • Full Stack • 98.4% Match</div>
<div class="float-resume-badge badge-nlp-speed">⚡ NLP Hybrid Matcher • 0.08s Sub-Second</div>
<div class="float-resume-badge badge-sdg">⚖️ SDG-10: 100% Unbiased Merit Ranking</div>
<div class="float-resume-badge badge-dataset">📊 2,484 Kaggle Resumes • 24 Domains</div>
<div class="float-resume-badge badge-architect">📄 Amandeep Verma • AI Architect • 99.8%</div>

<div class="chart-scroll-track">
<svg viewBox="0 0 3200 900" width="3200" height="900" fill="none" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 0; left: 0; overflow: hidden !important; pointer-events: none !important;">
  <defs>
    <linearGradient id="streamGradientCyan" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00F2FE"/>
      <stop offset="30%" stop-color="#4FACFE"/>
      <stop offset="70%" stop-color="#00F2FE"/>
      <stop offset="100%" stop-color="#4FACFE"/>
    </linearGradient>
    <filter id="glowFilterCyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Flow Wave 3: Deep subtle Teal -->
  <path d="M 0 540 Q 200 580, 400 550 T 800 530 T 1200 560 T 1600 540 T 2000 580 T 2400 550 T 2800 530 T 3200 540"
        stroke="#0D9488" stroke-width="1.5" fill="none" opacity="0.35"/>

  <!-- Flow Wave 2: Violet dashed wave -->
  <path d="M 0 490 Q 200 530, 400 480 T 800 420 T 1200 490 T 1600 490 T 2000 530 T 2400 480 T 2800 420 T 3200 490"
        stroke="#8B5CF6" stroke-width="2" stroke-dasharray="6,6" fill="none" opacity="0.6"/>

  <!-- Main Flow Wave 1: Cyan-Emerald with glowing shadow -->
  <path d="M 0 520 Q 200 380, 400 420 T 800 480 T 1200 400 T 1600 520 T 2000 380 T 2400 420 T 2800 480 T 3200 400"
        stroke="url(#streamGradientCyan)" stroke-width="3.5" fill="none" filter="url(#glowFilterCyan)"/>

  <!-- Vertical Telemetry Marker Lines -->
  <line x1="220" y1="380" x2="220" y2="600" stroke="#38BDF8" stroke-width="1" stroke-dasharray="3,3" opacity="0.2"/>
  <line x1="580" y1="450" x2="580" y2="600" stroke="#38BDF8" stroke-width="1" stroke-dasharray="3,3" opacity="0.2"/>
  <line x1="1180" y1="390" x2="1180" y2="600" stroke="#38BDF8" stroke-width="1" stroke-dasharray="3,3" opacity="0.2"/>
  <line x1="1820" y1="380" x2="1820" y2="600" stroke="#38BDF8" stroke-width="1" stroke-dasharray="3,3" opacity="0.2"/>
  <line x1="2180" y1="450" x2="2180" y2="600" stroke="#38BDF8" stroke-width="1" stroke-dasharray="3,3" opacity="0.2"/>
  <line x1="2780" y1="390" x2="2780" y2="600" stroke="#38BDF8" stroke-width="1" stroke-dasharray="3,3" opacity="0.2"/>

  <!-- Metric Node 1 -->
  <circle cx="220" cy="415" r="5.5" fill="#38BDF8" filter="url(#glowFilterCyan)"/>
  <circle cx="220" cy="415" r="12" fill="none" stroke="#38BDF8" stroke-width="1" opacity="0.4"/>

  <!-- Metric Node 2 (Top Shortlist) -->
  <circle cx="580" cy="452" r="7" fill="#10B981" filter="url(#glowFilterCyan)"/>
  <circle cx="580" cy="452" r="15" fill="none" stroke="#10B981" stroke-width="1" opacity="0.5"/>

  <!-- Metric Node 3 -->
  <circle cx="1180" cy="402" r="6" fill="#38BDF8" filter="url(#glowFilterCyan)"/>

  <!-- Metric Node 4 -->
  <circle cx="1820" cy="415" r="5.5" fill="#38BDF8" filter="url(#glowFilterCyan)"/>
  <circle cx="1820" cy="415" r="12" fill="none" stroke="#38BDF8" stroke-width="1" opacity="0.4"/>

  <!-- Metric Node 5 -->
  <circle cx="2180" cy="452" r="7" fill="#10B981" filter="url(#glowFilterCyan)"/>
  <circle cx="2180" cy="452" r="15" fill="none" stroke="#10B981" stroke-width="1" opacity="0.5"/>

  <!-- Metric Node 6 -->
  <circle cx="2780" cy="402" r="6" fill="#38BDF8" filter="url(#glowFilterCyan)"/>
</svg>
</div>

<div class="bottom-telemetry-bar">
AI_SCREENER // MODEL: BERT + TF-IDF // DATASET: 2,484 RESUMES // INFERENCE: 0.08S // MERIT_RANK: ACTIVE
</div>
</div>""", unsafe_allow_html=True)

    # 3-Column Architecture: Left spacer, Center login portal, Right spacer
    col_left, col_center, col_right = st.columns([1.2, 1.0, 1.2])

    with col_center:
        st.markdown("""<div class="compact-icon-badge">🎯</div>
<h1 class="compact-title">Recruiter Portal</h1>
<p class="compact-sub">AI Resume Screening & Ranking System</p>""", unsafe_allow_html=True)

        auth_tab_login, auth_tab_register = st.tabs(["🔑 Sign In", "📝 Register"])

        with auth_tab_login:
            if st.button("⚡ 1-Click Instant Demo (Amandeep Verma)", use_container_width=True, key="compact_demo_btn"):
                st.session_state.authenticated = True
                st.session_state.user_info = DEFAULT_USERS["demo@edufyi.com"]
                st.success("🎉 Welcome! Entering Command Center...")
                st.rerun()

            with st.form("compact_login_form", clear_on_submit=False):
                user_email = st.text_input("📧 Work Email", value="amandeepverma3001@gmail.com", placeholder="recruiter@company.com")
                user_pass = st.text_input("🔒 Password", value="demo123", type="password", placeholder="••••••••")
                keep_logged = st.checkbox("Keep active recruiter session open", value=True)
                submit_login = st.form_submit_button("🚀 Enter Command Center →", use_container_width=True, type="primary")

                if submit_login:
                    st.session_state.authenticated = True
                    st.session_state.user_info = {
                        "name": "Amandeep Verma",
                        "email": user_email if "@" in user_email else "amandeepverma3001@gmail.com",
                        "org": "Bennett University",
                        "role": "Lead Architect"
                    }
                    st.success("🎉 Access Granted! Loading...")
                    st.rerun()

            st.markdown("""<div class="compact-hint">
Demo Account: <code>amandeepverma3001@gmail.com</code> | Pass: <code>demo123</code>
</div>""", unsafe_allow_html=True)

        with auth_tab_register:
            with st.form("compact_register_form", clear_on_submit=True):
                reg_name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
                reg_email = st.text_input("Work Email", placeholder="e.g. rahul@techcorp.com")
                reg_password = st.text_input("Password", type="password", placeholder="Min 4 chars")
                submit_reg = st.form_submit_button("✨ Create Account →", use_container_width=True, type="primary")

                if submit_reg:
                    registered_users = st.session_state.get("registered_users", {})
                    success, new_user, msg = register_new_user(reg_name, reg_email, "Bennett University", reg_password, registered_users)
                    if success:
                        if "registered_users" not in st.session_state:
                            st.session_state.registered_users = {}
                        st.session_state.registered_users[new_user["email"]] = new_user
                        st.session_state.authenticated = True
                        st.session_state.user_info = new_user
                        st.success(f"🎉 {msg} Entering...")
                        st.rerun()
                    else:
                        st.error(msg)
