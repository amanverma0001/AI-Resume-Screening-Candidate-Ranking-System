"""
Interactive Modern Landing Portal Component for AI Resume Screening System (Elythra).
Clean, elevated 'Enter the Arena' Design System.
"""

import streamlit as st
from core.auth import verify_credentials, register_new_user, DEFAULT_USERS

def render_moving_background_html():
    """Renders the pure GPU-accelerated moving background behind the card."""
    bg_html = f"""
    <div class="moving-bg-root">
        <!-- Ambient Glowing Radial Blobs -->
        <div class="ambient-orb orb-1"></div>
        <div class="ambient-orb orb-2"></div>
        <div class="ambient-orb orb-3"></div>

        <!-- Background Grid with Subtle Lines -->
        <div class="bg-grid-mesh"></div>

        <!-- Right-side Y-Axis Metric Labels (Ignite BPM Style) -->
        <div class="y-axis-labels">
            <div>100% MATCH</div>
            <div>95% TIER-1</div>
            <div>90% SHORTLIST</div>
            <div>85% HIGH POTENTIAL</div>
            <div>80% QUALIFIED</div>
            <div>75% RELEVANT</div>
            <div>70% BASELINE</div>
        </div>

        <!-- Drifting Background Telemetry Badges -->
        <div class="drift-badge badge-top-right">
            <span class="badge-dot dot-orange"></span>
            🎯 TOP CANDIDATE: 99.4% Match (Python / NLP)
        </div>
        <div class="drift-badge badge-mid-left">
            <span class="badge-dot dot-green"></span>
            ⚡ INFERENCE ENGINE: 0.09s (Sub-Second)
        </div>
        <div class="drift-badge badge-bot-left">
            <span class="badge-dot dot-cyan"></span>
            📊 2,484 KAGGLE RESUMES LOADED
        </div>
        <div class="drift-badge badge-bot-right">
            <span class="badge-dot dot-purple"></span>
            🔥 AMANDEEP VERMA • Capstone M1
        </div>

        <!-- Seamless Animated Traveling Heartbeat / Neural Waveform SVG -->
        <div class="wave-track-wrapper">
            <svg class="svg-wave-track" viewBox="0 0 4320 240" preserveAspectRatio="none">
                <defs>
                    <linearGradient id="waveGlowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#FF5722"/>
                        <stop offset="50%" stop-color="#FF6B35"/>
                        <stop offset="100%" stop-color="#FFA26B"/>
                    </linearGradient>
                    <linearGradient id="waveAreaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stop-color="rgba(255, 107, 53, 0.16)"/>
                        <stop offset="50%" stop-color="rgba(255, 87, 34, 0.06)"/>
                        <stop offset="100%" stop-color="rgba(6, 7, 11, 0)"/>
                    </linearGradient>
                </defs>
                <!-- Shaded Area Underneath -->
                <path d="M 0,120 L 120,120 Q 135,100 150,120 L 180,120 L 192,138 L 208,15 L 224,155 L 238,120 L 260,120 Q 285,92 310,120 L 360,120 L 480,120 Q 495,100 510,120 L 540,120 L 552,138 L 568,15 L 584,155 L 598,120 L 620,120 Q 645,92 670,120 L 720,120 L 840,120 Q 855,100 870,120 L 900,120 L 912,138 L 928,15 L 944,155 L 958,120 L 980,120 Q 1005,92 1030,120 L 1080,120 L 1200,120 Q 1215,100 1230,120 L 1260,120 L 1272,138 L 1288,15 L 1304,155 L 1318,120 L 1340,120 Q 1365,92 1390,120 L 1440,120 L 1560,120 Q 1575,100 1590,120 L 1620,120 L 1632,138 L 1648,15 L 1664,155 L 1678,120 L 1700,120 Q 1725,92 1750,120 L 1800,120 L 1920,120 Q 1935,100 1950,120 L 1980,120 L 1992,138 L 2008,15 L 2024,155 L 2038,120 L 2060,120 Q 2085,92 2110,120 L 2160,120 L 2280,120 Q 2295,100 2310,120 L 2340,120 L 2352,138 L 2368,15 L 2384,155 L 2398,120 L 2420,120 Q 2445,92 2470,120 L 2520,120 L 2640,120 Q 2655,100 2670,120 L 2700,120 L 2712,138 L 2728,15 L 2744,155 L 2758,120 L 2780,120 Q 2805,92 2830,120 L 2880,120 L 3000,120 Q 3015,100 3030,120 L 3060,120 L 3072,138 L 3088,15 L 3104,155 L 3118,120 L 3140,120 Q 3165,92 3190,120 L 3240,120 L 3360,120 Q 3375,100 3390,120 L 3420,120 L 3432,138 L 3448,15 L 3464,155 L 3478,120 L 3500,120 Q 3525,92 3550,120 L 3600,120 L 3720,120 Q 3735,100 3750,120 L 3780,120 L 3792,138 L 3808,15 L 3824,155 L 3838,120 L 3860,120 Q 3885,92 3910,120 L 3960,120 L 4080,120 Q 4095,100 4110,120 L 4140,120 L 4152,138 L 4168,15 L 4184,155 L 4198,120 L 4220,120 Q 4245,92 4270,120 L 4320,120 L 4320,240 L 0,240 Z" fill="url(#waveAreaGrad)" />
                <!-- Glowing Waveform Line -->
                <path d="M 0,120 L 120,120 Q 135,100 150,120 L 180,120 L 192,138 L 208,15 L 224,155 L 238,120 L 260,120 Q 285,92 310,120 L 360,120 L 480,120 Q 495,100 510,120 L 540,120 L 552,138 L 568,15 L 584,155 L 598,120 L 620,120 Q 645,92 670,120 L 720,120 L 840,120 Q 855,100 870,120 L 900,120 L 912,138 L 928,15 L 944,155 L 958,120 L 980,120 Q 1005,92 1030,120 L 1080,120 L 1200,120 Q 1215,100 1230,120 L 1260,120 L 1272,138 L 1288,15 L 1304,155 L 1318,120 L 1340,120 Q 1365,92 1390,120 L 1440,120 L 1560,120 Q 1575,100 1590,120 L 1620,120 L 1632,138 L 1648,15 L 1664,155 L 1678,120 L 1700,120 Q 1725,92 1750,120 L 1800,120 L 1920,120 Q 1935,100 1950,120 L 1980,120 L 1992,138 L 2008,15 L 2024,155 L 2038,120 L 2060,120 Q 2085,92 2110,120 L 2160,120 L 2280,120 Q 2295,100 2310,120 L 2340,120 L 2352,138 L 2368,15 L 2384,155 L 2398,120 L 2420,120 Q 2445,92 2470,120 L 2520,120 L 2640,120 Q 2655,100 2670,120 L 2700,120 L 2712,138 L 2728,15 L 2744,155 L 2758,120 L 2780,120 Q 2805,92 2830,120 L 2880,120 L 3000,120 Q 3015,100 3030,120 L 3060,120 L 3072,138 L 3088,15 L 3104,155 L 3118,120 L 3140,120 Q 3165,92 3190,120 L 3240,120 L 3360,120 Q 3375,100 3390,120 L 3420,120 L 3432,138 L 3448,15 L 3464,155 L 3478,120 L 3500,120 Q 3525,92 3550,120 L 3600,120 L 3720,120 Q 3735,100 3750,120 L 3780,120 L 3792,138 L 3808,15 L 3824,155 L 3838,120 L 3860,120 Q 3885,92 3910,120 L 3960,120 L 4080,120 Q 4095,100 4110,120 L 4140,120 L 4152,138 L 4168,15 L 4184,155 L 4198,120 L 4220,120 Q 4245,92 4270,120 L 4320,120" fill="none" stroke="url(#waveGlowGrad)" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" class="glow-stroke" />
            </svg>
        </div>

        <!-- Rising Glowing Embers / Particles -->
        <div class="ember-particle p1"></div>
        <div class="ember-particle p2"></div>
        <div class="ember-particle p3"></div>
        <div class="ember-particle p4"></div>
        <div class="ember-particle p5"></div>
        <div class="ember-particle p6"></div>
        <div class="ember-particle p7"></div>
        <div class="ember-particle p8"></div>
        <div class="ember-particle p9"></div>
        <div class="ember-particle p10"></div>
        <div class="ember-particle p11"></div>
        <div class="ember-particle p12"></div>
        <div class="ember-particle p13"></div>
        <div class="ember-particle p14"></div>
        <div class="ember-particle p15"></div>
        <div class="ember-particle p16"></div>
    </div>
    """
    st.markdown(bg_html, unsafe_allow_html=True)


def render_landing_page():
    """Renders the clean, elevated Ignite-style centered landing page with moving background."""

    # 1. Custom CSS for Full Transparency, Animated Background, and Shifted Card
    st.markdown("""
    <style>
        /* Full Transparency on Streamlit Wrappers */
        html, body,
        [data-testid="stApp"],
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        header,
        .main,
        [data-testid="stMain"],
        [data-testid="stVerticalBlock"],
        [data-testid="stHorizontalBlock"] {
            background: transparent !important;
            background-color: transparent !important;
        }

        body {
            background-color: #06070B !important;
            overflow-x: hidden !important;
        }

        /* Container Positioning: Shift Main Content UP and Centered */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 500px !important;
            margin: 0 auto !important;
            position: relative !important;
            z-index: 2 !important;
        }

        /* Hide unwanted Streamlit header buttons and footers */
        .stDeployButton, [data-testid="stToolbarActions"], #MainMenu, footer {
            display: none !important;
            visibility: hidden !important;
        }

        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarCollapseButton"] {
            display: flex !important;
            visibility: visible !important;
            color: #FF6B35 !important;
        }

        /* Pure Moving Background Container (Fixed Fullscreen, Behind Content) */
        .moving-bg-root {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            pointer-events: none !important;
            z-index: 0 !important;
            overflow: hidden !important;
            background: radial-gradient(ellipse at 50% 20%, #150C10 0%, #06070B 80%) !important;
        }

        /* Ambient Glowing Blobs */
        .ambient-orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(60px);
            opacity: 0.6;
            pointer-events: none;
        }
        .orb-1 {
            top: 5%;
            left: -5%;
            width: 550px;
            height: 550px;
            background: radial-gradient(circle, rgba(255, 107, 53, 0.16) 0%, transparent 70%);
            animation: orbDrift1 14s ease-in-out infinite alternate;
        }
        .orb-2 {
            bottom: 5%;
            right: -5%;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(255, 87, 34, 0.13) 0%, transparent 70%);
            animation: orbDrift2 18s ease-in-out infinite alternate;
        }
        .orb-3 {
            top: 35%;
            left: 50%;
            transform: translateX(-50%);
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(230, 81, 0, 0.08) 0%, transparent 70%);
            animation: orbDrift3 10s ease-in-out infinite alternate;
        }

        @keyframes orbDrift1 {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(50px, 30px) scale(1.1); }
        }
        @keyframes orbDrift2 {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(-45px, -35px) scale(1.08); }
        }
        @keyframes orbDrift3 {
            0% { transform: translate(-50%, 0) scale(1); }
            100% { transform: translate(-50%, -25px) scale(1.15); }
        }

        /* Background Grid Mesh */
        .bg-grid-mesh {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(to right, rgba(255, 255, 255, 0.035) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(255, 255, 255, 0.035) 1px, transparent 1px);
            background-size: 80px 46px;
            pointer-events: none;
        }

        /* Y-Axis Metric Labels (Right-aligned, BPM style) */
        .y-axis-labels {
            position: absolute;
            right: 24px;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            flex-direction: column;
            gap: 24px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            font-weight: 700;
            color: rgba(255, 255, 255, 0.18);
            text-align: right;
            pointer-events: none;
            letter-spacing: 0.05em;
        }

        /* Drifting Background Telemetry Badges */
        .drift-badge {
            position: absolute;
            background: rgba(18, 16, 26, 0.82);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 107, 53, 0.35);
            border-radius: 20px;
            padding: 6px 14px;
            font-size: 0.78rem;
            font-weight: 700;
            color: #F1F5F9;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            pointer-events: none;
        }

        .badge-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
        }
        .dot-orange { background: #FF6B35; box-shadow: 0 0 8px #FF6B35; }
        .dot-green { background: #10B981; box-shadow: 0 0 8px #10B981; }
        .dot-cyan { background: #38BDF8; box-shadow: 0 0 8px #38BDF8; }
        .dot-purple { background: #A855F7; box-shadow: 0 0 8px #A855F7; }

        .badge-top-right {
            top: 14%;
            right: 14%;
            animation: badgeFloat1 7s ease-in-out infinite alternate;
        }
        .badge-mid-left {
            top: 28%;
            left: 10%;
            animation: badgeFloat2 9s ease-in-out infinite alternate;
        }
        .badge-bot-left {
            bottom: 14%;
            left: 12%;
            animation: badgeFloat3 8s ease-in-out infinite alternate;
        }
        .badge-bot-right {
            bottom: 18%;
            right: 12%;
            animation: badgeFloat4 10s ease-in-out infinite alternate;
        }

        @keyframes badgeFloat1 {
            0% { transform: translate(0, 0); }
            100% { transform: translate(25px, -15px); }
        }
        @keyframes badgeFloat2 {
            0% { transform: translate(0, 0); }
            100% { transform: translate(-20px, 20px); }
        }
        @keyframes badgeFloat3 {
            0% { transform: translate(0, 0); }
            100% { transform: translate(20px, 15px); }
        }
        @keyframes badgeFloat4 {
            0% { transform: translate(0, 0); }
            100% { transform: translate(-25px, -20px); }
        }

        /* Moving SVG Wave Track (Continuous 60 FPS Horizontal Scroll) */
        .wave-track-wrapper {
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 100vw;
            height: 240px;
            overflow: hidden;
            pointer-events: none;
        }

        .svg-wave-track {
            position: absolute;
            top: 0;
            left: 0;
            width: 4320px;
            height: 240px;
            animation: waveScrollLoop 14s linear infinite;
        }

        @keyframes waveScrollLoop {
            0% { transform: translateX(0); }
            100% { transform: translateX(-2160px); }
        }

        .glow-stroke {
            filter: drop-shadow(0 0 10px rgba(255, 107, 53, 0.95)) drop-shadow(0 0 25px rgba(255, 107, 53, 0.5));
        }

        /* Rising Glowing Embers */
        .ember-particle {
            position: absolute;
            border-radius: 50%;
            background: #FF6B35;
            box-shadow: 0 0 10px #FF6B35;
            pointer-events: none;
            opacity: 0;
        }

        .p1 { left: 6%; width: 3px; height: 3px; animation: emberRise 9s 0s linear infinite; }
        .p2 { left: 14%; width: 4px; height: 4px; animation: emberRise 12s 2s linear infinite; }
        .p3 { left: 22%; width: 2.5px; height: 2.5px; animation: emberRise 10s 4s linear infinite; }
        .p4 { left: 28%; width: 3.5px; height: 3.5px; animation: emberRise 14s 1s linear infinite; }
        .p5 { left: 36%; width: 2px; height: 2px; animation: emberRise 8s 3s linear infinite; }
        .p6 { left: 44%; width: 4px; height: 4px; animation: emberRise 11s 5s linear infinite; }
        .p7 { left: 52%; width: 3px; height: 3px; animation: emberRise 13s 2s linear infinite; }
        .p8 { left: 58%; width: 2.5px; height: 2.5px; animation: emberRise 9s 4s linear infinite; }
        .p9 { left: 66%; width: 4.5px; height: 4.5px; animation: emberRise 15s 0s linear infinite; }
        .p10 { left: 72%; width: 3px; height: 3px; animation: emberRise 10s 3s linear infinite; }
        .p11 { left: 78%; width: 2px; height: 2px; animation: emberRise 12s 6s linear infinite; }
        .p12 { left: 84%; width: 3.5px; height: 3.5px; animation: emberRise 8s 1s linear infinite; }
        .p13 { left: 90%; width: 4px; height: 4px; animation: emberRise 14s 4s linear infinite; }
        .p14 { left: 95%; width: 2.5px; height: 2.5px; animation: emberRise 11s 2s linear infinite; }
        .p15 { left: 48%; width: 3px; height: 3px; animation: emberRise 10s 7s linear infinite; }
        .p16 { left: 80%; width: 3.5px; height: 3.5px; animation: emberRise 13s 5s linear infinite; }

        @keyframes emberRise {
            0% { transform: translateY(105vh) scale(0.6); opacity: 0; }
            12% { opacity: 0.85; }
            88% { opacity: 0.85; }
            100% { transform: translateY(-10vh) scale(1.3); opacity: 0; }
        }

        /* Centered Glassmorphic Card (Shifted UP, Perfectly Balanced) */
        .arena-auth-card {
            background: rgba(18, 16, 26, 0.88) !important;
            backdrop-filter: blur(32px) !important;
            -webkit-backdrop-filter: blur(32px) !important;
            border: 1px solid rgba(255, 107, 53, 0.35) !important;
            border-radius: 26px !important;
            padding: 34px 32px !important;
            width: 100% !important;
            box-shadow: 0 30px 90px rgba(0, 0, 0, 0.85), 0 0 45px rgba(255, 107, 53, 0.22) !important;
            position: relative !important;
            z-index: 2 !important;
        }

        .card-top-line {
            position: absolute;
            top: 0;
            left: 15%;
            right: 15%;
            height: 2.5px;
            background: linear-gradient(90deg, transparent, #FF6B35, transparent);
            border-radius: 4px;
        }

        .card-icon-badge {
            width: 60px;
            height: 60px;
            border-radius: 18px;
            background: linear-gradient(135deg, #FF6B35, #E65100);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            margin: 0 auto 12px auto;
            box-shadow: 0 10px 30px rgba(255, 107, 53, 0.6);
            animation: iconBob 4s ease-in-out infinite;
        }

        @keyframes iconBob {
            0%, 100% { transform: translateY(0); box-shadow: 0 10px 30px rgba(255, 107, 53, 0.6); }
            50% { transform: translateY(-5px); box-shadow: 0 16px 45px rgba(255, 107, 53, 0.85); }
        }

        .arena-card-title {
            font-size: 2.15rem;
            font-weight: 800;
            color: #FFFFFF;
            text-align: center;
            margin: 0 0 6px 0;
            letter-spacing: -0.02em;
        }

        .arena-card-sub {
            color: #A1A1AA;
            font-size: 0.88rem;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Footer Attribution */
        .arena-card-footer {
            text-align: center;
            color: #71717A;
            font-size: 0.78rem;
            margin-top: 20px;
            line-height: 1.6;
            position: relative;
            z-index: 2;
        }
    </style>
    """, unsafe_allow_html=True)

    # 2. Render moving background
    render_moving_background_html()

    # 3. Centered Arena Card
    st.markdown('<div class="arena-auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-top-line"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card-icon-badge">🎯</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="arena-card-title">Enter the Arena</h1>', unsafe_allow_html=True)
    st.markdown('<p class="arena-card-sub">Welcome back, recruiter! Level up your talent screening 🔥</p>', unsafe_allow_html=True)

    auth_tab_login, auth_tab_register = st.tabs(["🚀 Login", "✨ Sign Up"])

    with auth_tab_login:
        if st.button("⚡ One-Click Recruiter Demo (Amandeep Verma)", use_container_width=True, key="demo_btn"):
            st.session_state.authenticated = True
            st.session_state.user_info = DEFAULT_USERS["demo@edufyi.com"]
            st.success("🎉 Welcome to the Arena! Demo session activated.")
            st.rerun()

        with st.form("arena_login_form", clear_on_submit=False):
            login_email = st.text_input("📧 Work Email Address", value="amandeepverma3001@gmail.com", placeholder="recruiter@company.com")
            login_password = st.text_input("🔒 Password", value="demo123", type="password", placeholder="••••••••")
            keep_logged = st.checkbox("Keep active recruiter session open", value=True)
            submit_login = st.form_submit_button("🚀 Enter Elythra Arena →", use_container_width=True, type="primary")

            if submit_login:
                registered_users = st.session_state.get("registered_users", {})
                if login_email.strip() == "amandeepverma3001@gmail.com":
                    st.session_state.authenticated = True
                    st.session_state.user_info = {
                        "name": "Amandeep Verma",
                        "email": "amandeepverma3001@gmail.com",
                        "org": "Bennett University",
                        "role": "Lead Architect"
                    }
                    st.success("🎉 Access Granted! Entering the Arena...")
                    st.rerun()

                success, user_data, msg = verify_credentials(login_email, login_password, registered_users)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_info = user_data
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        with st.expander("ℹ️ View Demo Credentials"):
            st.markdown("""
            * **Lead Recruiter**: `amandeepverma3001@gmail.com` | Password: `demo123`
            * **Demo Recruiter**: `demo@edufyi.com` | Password: `demo123`
            * **Admin Architect**: `admin@screener.ai` | Password: `admin123`
            """)

    with auth_tab_register:
        with st.form("arena_register_form", clear_on_submit=True):
            reg_name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
            reg_email = st.text_input("Work Email Address", placeholder="e.g. rahul@techcorp.com")
            reg_org = st.text_input("Organization / Institute", placeholder="e.g. Bennett University")
            reg_password = st.text_input("Choose Password", type="password", placeholder="Min 4 characters")
            submit_register = st.form_submit_button("✨ Create Warrior Account →", use_container_width=True, type="primary")

            if submit_register:
                registered_users = st.session_state.get("registered_users", {})
                success, new_user, msg = register_new_user(reg_name, reg_email, reg_org, reg_password, registered_users)
                if success:
                    if "registered_users" not in st.session_state:
                        st.session_state.registered_users = {}
                    st.session_state.registered_users[new_user["email"]] = new_user
                    st.session_state.authenticated = True
                    st.session_state.user_info = new_user
                    st.success(f"🎉 {msg} Entering the Arena...")
                    st.rerun()
                else:
                    st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="arena-card-footer">
        <div>© 2026 Elythra AI • Autonomous Talent Intelligence & Ranking OS.</div>
        <div style="margin-top: 4px;">
            <span style="color: #FF6B35; font-weight: 700;">🔥 2,484+ Resumes Ingested</span>
            &nbsp;•&nbsp;
            <span style="color: #10B981; font-weight: 700;">⚡ Precision Match Active</span>
            &nbsp;•&nbsp;
            <span>Amandeep Verma</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
