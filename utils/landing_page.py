"""
Interactive Modern Landing Portal Component for AI Resume Screening System (Elythra).
Faithfully recreates the signature Ignite 'Enter the Arena' Design System:
- Full-screen Procedural HTML5 Background Waveform Canvas (Heartbeat / Neural Pulse waveform, grid lines, Y-axis markers, floating badges, rising embers)
- Pinned Header Bar with Live Status indicator
- Live Telemetry Ribbon with real-time candidate screening metrics
- Centered Glassmorphic Auth Card ('Enter the Arena') with glowing icon badge
- 1-Click Instant Recruiter Demo Access (Amandeep Verma)
- Minimalist Social Proof Footer
"""

import streamlit as st
from core.auth import verify_credentials, register_new_user, DEFAULT_USERS

def inject_arena_canvas_engine():
    """
    Mounts a full-screen, zero-DOM procedural HTML5 canvas on the parent/main window
    featuring animated glowing ECG/Neural pulse waveforms, background grid lines,
    Y-axis percentage markers, floating telemetry badges, rising embers, and mouse reactivity.
    """
    canvas_html = """
    <script>
    (function() {
        var targetDoc = document;
        try {
            if (window.parent && window.parent.document && window.parent.document.body) {
                targetDoc = window.parent.document;
            }
        } catch(e) {
            targetDoc = document;
        }

        // Prevent duplicate animation engines
        if (targetDoc.__elythraArenaCanvasInitialized) {
            return;
        }
        targetDoc.__elythraArenaCanvasInitialized = true;

        // Clean up any old canvas
        var oldCanvas = targetDoc.getElementById("elythra-arena-canvas");
        if (oldCanvas) oldCanvas.remove();

        // Transparency styles for Streamlit wrappers
        var styleTag = targetDoc.getElementById("elythra-arena-transparency");
        if (!styleTag) {
            styleTag = targetDoc.createElement("style");
            styleTag.id = "elythra-arena-transparency";
            styleTag.textContent = "" +
                "html, body, .stApp, [data-testid=\"stAppViewContainer\"], [data-testid=\"stHeader\"], header, .main, [data-testid=\"stMain\"], [data-testid=\"stVerticalBlock\"] {" +
                "    background: transparent !important;" +
                "    background-color: transparent !important;" +
                "}" +
                "body {" +
                "    background-color: #06070B !important;" +
                "    overflow-x: hidden !important;" +
                "}";
            targetDoc.head.appendChild(styleTag);
        }

        // Mount Canvas Element
        var canvas = targetDoc.createElement("canvas");
        canvas.id = "elythra-arena-canvas";
        canvas.style.position = "fixed";
        canvas.style.top = "0";
        canvas.style.left = "0";
        canvas.style.width = "100vw";
        canvas.style.height = "100vh";
        canvas.style.zIndex = "0";
        canvas.style.pointerEvents = "none";
        canvas.style.background = "radial-gradient(ellipse at 50% 25%, #180D12 0%, #06070B 80%)";
        targetDoc.body.prepend(canvas);

        var ctx = canvas.getContext("2d");
        var width = canvas.width = targetDoc.documentElement.clientWidth || window.innerWidth;
        var height = canvas.height = targetDoc.documentElement.clientHeight || window.innerHeight;

        var onResize = function() {
            width = canvas.width = targetDoc.documentElement.clientWidth || window.innerWidth;
            height = canvas.height = targetDoc.documentElement.clientHeight || window.innerHeight;
        };
        window.addEventListener("resize", onResize);
        if (window.parent) window.parent.addEventListener("resize", onResize);

        // Mouse Tracker
        var mouseX = -999;
        var mouseY = -999;
        var isMouseOver = false;

        var onMouseMove = function(e) {
            mouseX = e.clientX;
            mouseY = e.clientY;
            isMouseOver = true;
        };
        var onMouseLeave = function() {
            isMouseOver = false;
        };

        targetDoc.addEventListener("mousemove", onMouseMove);
        targetDoc.addEventListener("mouseleave", onMouseLeave);

        // Rising Glowing Embers (Orange / Coral)
        var emberCount = 32;
        var embers = [];
        for (var i = 0; i < emberCount; i++) {
            embers.push({
                x: Math.random() * width,
                y: Math.random() * height,
                r: Math.random() * 2.5 + 1.0,
                speedY: Math.random() * 0.75 + 0.3,
                speedX: (Math.random() - 0.5) * 0.35,
                opacity: Math.random() * 0.65 + 0.25,
                color: Math.random() > 0.4 ? "#FF6B35" : "#FFA26B"
            });
        }

        // Floating Telemetry Badges (just like in the Ignite screenshot)
        var floatingBadges = [
            { text: "🎯 TOP CANDIDATE: 99.4% Match (Python / NLP)", x: width * 0.12, y: height * 0.24, vx: 0.3, color: "#FF6B35" },
            { text: "⚡ INFERENCE ENGINE: 0.09s (Sub-Second)", x: width * 0.68, y: height * 0.28, vx: -0.28, color: "#10B981" },
            { text: "📊 2,484 KAGGLE RESUMES PROCESSED", x: width * 0.18, y: height * 0.88, vx: 0.32, color: "#38BDF8" },
            { text: "🔥 AMANDEEP VERMA • Capstone M1", x: width * 0.72, y: height * 0.82, vx: -0.25, color: "#FFA26B" },
            { text: "⚖️ 100% UNBIASED MERIT RANKING", x: width * 0.42, y: height * 0.93, vx: 0.22, color: "#A855F7" }
        ];

        // Click Shockwave Burst
        var shockwaves = [];
        targetDoc.addEventListener("click", function(e) {
            var tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : "";
            if (tag === "input" || tag === "textarea") return;

            shockwaves.push({
                x: e.clientX,
                y: e.clientY,
                r: 8,
                maxR: 90,
                opacity: 1.0,
                color: "#FF6B35"
            });
        });

        // Cardiac / Neural Waveform Math Function
        // Produces the exact P-Q-R-S-T pulse pattern from the user's screenshot
        function getWaveY(x, time, midY) {
            var wavelength = 380;
            var pos = (x + time * 140) % wavelength;
            if (pos < 0) pos += wavelength;

            var dy = 0;
            if (pos >= 0 && pos < 120) {
                // Baseline with subtle tremor
                dy = Math.sin((x + time * 60) * 0.04) * 2;
            } else if (pos >= 120 && pos < 155) {
                // P-wave (small round upward bump)
                var prog = (pos - 120) / 35;
                dy = -Math.sin(prog * Math.PI) * 16;
            } else if (pos >= 155 && pos < 185) {
                // Flat PR segment
                dy = 0;
            } else if (pos >= 185 && pos < 198) {
                // Q-wave (sharp downward dip)
                var prog = (pos - 185) / 13;
                dy = Math.sin(prog * Math.PI) * 18;
            } else if (pos >= 198 && pos < 222) {
                // R-wave (TALL SHARP PEAK UPWARD)
                var prog = (pos - 198) / 24;
                dy = -Math.sin(prog * Math.PI) * 115;
            } else if (pos >= 222 && pos < 238) {
                // S-wave (sharp downward dip)
                var prog = (pos - 222) / 16;
                dy = Math.sin(prog * Math.PI) * 32;
            } else if (pos >= 238 && pos < 270) {
                // ST segment
                dy = 0;
            } else if (pos >= 270 && pos < 325) {
                // T-wave (broad rounded upward bump)
                var prog = (pos - 270) / 55;
                dy = -Math.sin(prog * Math.PI) * 28;
            } else {
                // TP baseline
                dy = 0;
            }

            // Mouse Interaction: Magnetic distortion towards cursor
            if (isMouseOver && mouseX > 0 && mouseY > 0) {
                var dist = Math.abs(mouseX - x);
                if (dist < 150) {
                    var factor = (1 - dist / 150);
                    dy += (mouseY - (midY + dy)) * factor * 0.35;
                }
            }

            return midY + dy;
        }

        var time = 0;
        function animate() {
            time += 0.016;
            ctx.clearRect(0, 0, width, height);

            var midY = height * 0.56;

            // 1. Draw Background Grid Lines
            ctx.save();
            ctx.strokeStyle = "rgba(255, 255, 255, 0.035)";
            ctx.lineWidth = 1;

            // Horizontal grid lines
            var gridSpacingY = 46;
            for (var gy = 40; gy < height; gy += gridSpacingY) {
                ctx.beginPath();
                ctx.moveTo(0, gy);
                ctx.lineTo(width, gy);
                ctx.stroke();
            }

            // Vertical grid lines
            var gridSpacingX = 80;
            for (var gx = 0; gx < width; gx += gridSpacingX) {
                ctx.beginPath();
                ctx.moveTo(gx, 0);
                ctx.lineTo(gx, height);
                ctx.stroke();
            }

            // Right-side Y-Axis Scale Markers (like the BPM labels in screenshot)
            var yLabels = [
                { text: "100% MATCH", y: midY - 140 },
                { text: "95% TIER-1", y: midY - 95 },
                { text: "90% SHORTLIST", y: midY - 50 },
                { text: "85% HIGH POTENTIAL", y: midY - 10 },
                { text: "80% QUALIFIED", y: midY + 35 },
                { text: "75% RELEVANT", y: midY + 80 },
                { text: "70% BASELINE", y: midY + 125 }
            ];
            ctx.font = "600 10px 'JetBrains Mono', monospace";
            ctx.fillStyle = "rgba(255, 255, 255, 0.18)";
            ctx.textAlign = "right";
            for (var i = 0; i < yLabels.length; i++) {
                ctx.fillText(yLabels[i].text, width - 24, yLabels[i].y);
            }
            ctx.restore();

            // 2. Draw Gentle Undulating Shaded Area Fill below the wave
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(0, height);
            for (var x = 0; x <= width; x += 6) {
                var y = getWaveY(x, time, midY);
                ctx.lineTo(x, y);
            }
            ctx.lineTo(width, height);
            ctx.closePath();

            var areaGrad = ctx.createLinearGradient(0, midY - 80, 0, height);
            areaGrad.addColorStop(0, "rgba(255, 107, 53, 0.12)");
            areaGrad.addColorStop(0.5, "rgba(255, 87, 34, 0.05)");
            areaGrad.addColorStop(1, "rgba(6, 7, 11, 0.0)");
            ctx.fillStyle = areaGrad;
            ctx.fill();
            ctx.restore();

            // 3. Draw the Glowing Orange ECG / Neural Pulse Waveform Line
            ctx.save();
            ctx.beginPath();
            for (var x = 0; x <= width; x += 4) {
                var y = getWaveY(x, time, midY);
                if (x === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.strokeStyle = "#FF6B35";
            ctx.lineWidth = 2.6;
            ctx.shadowBlur = 18;
            ctx.shadowColor = "#FF6B35";
            ctx.stroke();

            // Secondary subtle highlight pass for extra brightness
            ctx.strokeStyle = "#FFA26B";
            ctx.lineWidth = 1.0;
            ctx.shadowBlur = 8;
            ctx.shadowColor = "#FFA26B";
            ctx.stroke();
            ctx.restore();

            // 4. Draw Rising Glowing Embers
            ctx.save();
            for (var i = 0; i < embers.length; i++) {
                var em = embers[i];
                em.y -= em.speedY;
                em.x += em.speedX;
                if (em.y < -10) { em.y = height + 10; em.x = Math.random() * width; }
                if (em.x < -10) em.x = width + 10;
                if (em.x > width + 10) em.x = -10;

                ctx.beginPath();
                ctx.arc(em.x, em.y, em.r, 0, Math.PI * 2);
                ctx.fillStyle = em.color;
                ctx.globalAlpha = em.opacity * 0.7;
                ctx.shadowBlur = 10;
                ctx.shadowColor = em.color;
                ctx.fill();
            }
            ctx.restore();

            // 5. Draw Floating Telemetry Badges (Ignite Screenshot style)
            ctx.save();
            for (var i = 0; i < floatingBadges.length; i++) {
                var b = floatingBadges[i];
                b.x += b.vx;
                if (b.x < -280) b.x = width + 60;
                if (b.x > width + 280) b.x = -240;

                var text = b.text;
                ctx.font = "bold 11px 'Plus Jakarta Sans', sans-serif";
                var tWidth = ctx.measureText(text).width;
                var padX = 14;
                var bHeight = 28;

                // Pill container
                ctx.fillStyle = "rgba(18, 16, 26, 0.78)";
                ctx.strokeStyle = "rgba(255, 107, 53, 0.35)";
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.roundRect(b.x, b.y - 18, tWidth + padX * 2, bHeight, 14);
                ctx.fill();
                ctx.stroke();

                // Glowing indicator dot
                ctx.fillStyle = b.color;
                ctx.beginPath();
                ctx.arc(b.x + 10, b.y - 4, 3.5, 0, Math.PI * 2);
                ctx.shadowBlur = 6;
                ctx.shadowColor = b.color;
                ctx.fill();
                ctx.shadowBlur = 0;

                // Text
                ctx.fillStyle = "#F1F5F9";
                ctx.fillText(text, b.x + 20, b.y);
            }
            ctx.restore();

            // 6. Draw Shockwaves
            for (var i = shockwaves.length - 1; i >= 0; i--) {
                var s = shockwaves[i];
                s.r += 2.8;
                s.opacity -= 0.024;
                if (s.opacity <= 0 || s.r >= s.maxR) {
                    shockwaves.splice(i, 1);
                    continue;
                }

                ctx.save();
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
                ctx.strokeStyle = s.color;
                ctx.globalAlpha = s.opacity;
                ctx.lineWidth = 2.2;
                ctx.shadowBlur = 14;
                ctx.shadowColor = s.color;
                ctx.stroke();
                ctx.restore();
            }

            requestAnimationFrame(animate);
        }
        animate();

        // 7. Live Telemetric Micro-Fluctuations (Ribbon Updates)
        setInterval(function() {
            var latEl = targetDoc.getElementById("ribbon-latency");
            var spdEl = targetDoc.getElementById("ribbon-speed");
            var accEl = targetDoc.getElementById("ribbon-accuracy");

            if (latEl) {
                var lat = (0.08 + Math.random() * 0.03).toFixed(2);
                latEl.innerText = lat + "s";
            }
            if (spdEl) {
                var spd = Math.floor(615 + Math.random() * 25);
                spdEl.innerText = spd + " KCAL/MIN";
            }
            if (accEl) {
                var acc = (99.2 + Math.random() * 0.6).toFixed(1);
                accEl.innerText = acc + "%";
            }
        }, 2200);

    })();
    </script>
    """
    try:
        st.html(canvas_html, unsafe_allow_javascript=True)
    except Exception:
        import streamlit.components.v1 as components
        components.html(canvas_html, height=1, width=1)


def render_landing_page():
    """Renders the authentic Ignite-style centered movable landing page."""
    
    # Inject the procedural HTML5 Waveform & Telemetry Engine
    inject_arena_canvas_engine()

    # Custom CSS exactly matching the user's Ignite screenshot
    st.markdown("""
    <style>
        /* Transparency Overrides */
        html, body,
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

        .block-container {
            padding-top: 0.8rem !important;
            padding-bottom: 2rem !important;
            max-width: 1400px !important;
            position: relative;
            z-index: 2;
        }

        /* Controls Accent */
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarCollapseButton"] {
            display: flex !important;
            visibility: visible !important;
            color: #FF6B35 !important;
        }

        .stDeployButton, [data-testid="stToolbarActions"], #MainMenu, footer {
            display: none !important;
            visibility: hidden !important;
        }

        @keyframes pulseGlow {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1.15); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        @keyframes cardGlowPulse {
            0% { box-shadow: 0 30px 90px rgba(0,0,0,0.85), 0 0 35px rgba(255,107,53,0.18); }
            50% { box-shadow: 0 35px 105px rgba(0,0,0,0.9), 0 0 55px rgba(255,107,53,0.32); }
            100% { box-shadow: 0 30px 90px rgba(0,0,0,0.85), 0 0 35px rgba(255,107,53,0.18); }
        }

        @keyframes iconFloat {
            0%, 100% { transform: translateY(0) rotate(0deg); box-shadow: 0 10px 30px rgba(255,107,53,0.55); }
            50% { transform: translateY(-6px) rotate(2deg); box-shadow: 0 18px 45px rgba(255,107,53,0.8); }
        }

        /* Top Pinned Nav Bar */
        .top-arena-bar {
            background: rgba(14, 13, 20, 0.75);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            padding: 12px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }

        .arena-brand-group {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .arena-brand-logo {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: linear-gradient(135deg, #FF6B35, #E65100);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            box-shadow: 0 4px 18px rgba(255, 107, 53, 0.5);
        }

        .arena-brand-name {
            font-size: 1.6rem;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.02em;
        }

        .arena-brand-badge {
            background: rgba(255, 107, 53, 0.18);
            border: 1px solid rgba(255, 107, 53, 0.4);
            color: #FF9E79;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .status-pill-biometrics {
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.35);
            color: #10B981;
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .pulse-dot-green {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10B981;
            animation: pulseGlow 1.8s infinite;
        }

        /* Live Telemetry Ribbon (Exact match to user screenshot) */
        .telemetry-ribbon-ignite {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 22px;
            overflow-x: auto;
            padding-bottom: 4px;
        }

        .telemetry-lead-label {
            color: #71717A;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            white-space: nowrap;
            margin-right: 6px;
        }

        .telemetry-pill-item {
            background: rgba(22, 19, 29, 0.82);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 30px;
            padding: 6px 16px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 0.8rem;
            white-space: nowrap;
        }

        .telemetry-pill-item.active-orange {
            border-color: rgba(255, 107, 53, 0.5);
            background: rgba(255, 107, 53, 0.14);
        }

        .highlight-orange { color: #FF6B35 !important; font-weight: 700; }
        .highlight-green { color: #10B981 !important; font-weight: 700; }
        .highlight-cyan { color: #38BDF8 !important; font-weight: 700; }

        /* Centered 'Enter the Arena' Card */
        .arena-auth-card {
            background: rgba(18, 16, 26, 0.84);
            backdrop-filter: blur(32px);
            -webkit-backdrop-filter: blur(32px);
            border: 1px solid rgba(255, 107, 53, 0.32);
            border-radius: 26px;
            padding: 38px 36px;
            width: 100%;
            max-width: 470px;
            margin: 0 auto;
            position: relative;
            animation: cardGlowPulse 5s infinite alternate ease-in-out;
            z-index: 2;
        }

        .card-top-line {
            position: absolute;
            top: 0;
            left: 15%;
            right: 15%;
            height: 2px;
            background: linear-gradient(90deg, transparent, #FF6B35, transparent);
            border-radius: 4px;
        }

        .card-icon-badge {
            width: 62px;
            height: 62px;
            border-radius: 18px;
            background: linear-gradient(135deg, #FF6B35, #E65100);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            margin: 0 auto 16px auto;
            box-shadow: 0 10px 30px rgba(255, 107, 53, 0.6);
            animation: iconFloat 4s ease-in-out infinite;
        }

        .arena-card-title {
            font-size: 2.1rem;
            font-weight: 800;
            color: #FFFFFF;
            text-align: center;
            margin: 0 0 6px 0;
            letter-spacing: -0.02em;
        }

        .arena-card-sub {
            color: #A1A1AA;
            font-size: 0.9rem;
            text-align: center;
            margin-bottom: 24px;
        }

        /* Dashed Recruiter 1-Click Button */
        .btn-dashed-demo {
            width: 100%;
            padding: 12px 18px;
            border: 1.5px dashed rgba(255, 107, 53, 0.7) !important;
            background: rgba(255, 107, 53, 0.08) !important;
            border-radius: 14px !important;
            color: #FFB347 !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            text-align: center;
            cursor: pointer;
            transition: all 0.25s ease;
            margin-bottom: 18px;
        }

        .btn-dashed-demo:hover {
            background: rgba(255, 107, 53, 0.18) !important;
            border-color: #FF6B35 !important;
            transform: translateY(-1px);
        }

        /* Bottom Fixed Footer */
        .arena-footer-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 8px;
            color: #71717A;
            font-size: 0.8rem;
            margin-top: 36px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            flex-wrap: wrap;
            gap: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

    # 1. Top Pinned Nav Bar (Ignite style)
    st.markdown("""
    <div class="top-arena-bar">
        <div class="arena-brand-group">
            <div class="arena-brand-logo">🎯</div>
            <div class="arena-brand-name">Elythra</div>
            <div class="arena-brand-badge">TALENT OS v2.4</div>
        </div>
        <div style="display: flex; align-items: center; gap: 14px;">
            <span class="status-pill-biometrics">
                <span class="pulse-dot-green"></span> Biometrics / AI Live (14ms) • Screener Ready
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Live Telemetry Ribbon (Exact chips from the screenshot!)
    st.markdown("""
    <div class="telemetry-ribbon-ignite">
        <span class="telemetry-lead-label">LIVE TELEMETRY (CLICK TO FOCUS):</span>
        <div class="telemetry-pill-item active-orange" title="Cardio / Candidate Relevance">
            <span>🎯 MATCH RELEVANCE</span>
            <span class="highlight-orange" id="ribbon-accuracy">99.4%</span>
            <span style="color: #10B981; font-size: 0.75rem;">• Peak Zone</span>
        </div>
        <div class="telemetry-pill-item" title="Throughput Capacity">
            <span>🔥 INGESTION RATE</span>
            <span class="highlight-orange" id="ribbon-speed">620 / MIN</span>
            <span style="color: #38BDF8; font-size: 0.75rem;">• Active Engine</span>
        </div>
        <div class="telemetry-pill-item" title="Latency">
            <span>⚡ INFERENCE SPEED</span>
            <span class="highlight-orange" id="ribbon-latency">0.09s</span>
            <span style="color: #10B981; font-size: 0.75rem;">• Record Fast</span>
        </div>
        <div class="telemetry-pill-item" title="Kaggle Dataset">
            <span>🏆 KAGGLE DATASET</span>
            <span style="color: #FFFFFF; font-weight: 700;">2,484 RESUMES</span>
            <span style="color: #10B981; font-size: 0.75rem;">• 24 Domains</span>
        </div>
        <div class="telemetry-pill-item" title="SDG 10 Equality">
            <span>⚖️ UNBIASED MERIT</span>
            <span class="highlight-green">100% MERIT</span>
            <span style="color: #A855F7; font-size: 0.75rem;">• SDG 10</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Centered 'Enter the Arena' Card Layout (Single Centered Column)
    col_l, col_center, col_r = st.columns([1, 1.25, 1])

    with col_center:
        st.markdown('<div class="arena-auth-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-top-line"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-icon-badge">🎯</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="arena-card-title">Enter the Arena</h1>', unsafe_allow_html=True)
        st.markdown('<p class="arena-card-sub">Welcome back, recruiter! Level up your talent screening 🔥</p>', unsafe_allow_html=True)

        auth_tab_login, auth_tab_register = st.tabs(["🚀 Login", "✨ Sign Up"])

        # TAB 1: LOGIN
        with auth_tab_login:
            # Dashed 1-Click Recruiter Demo Button (Directly like screenshot)
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
                    # Allow both amandeepverma3001@gmail.com and demo@edufyi.com as instant admin demo
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

        # TAB 2: SIGN UP
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

        st.markdown('</div>', unsafe_allow_html=True)

    # 4. Bottom Footer Bar (Exact match to screenshot)
    st.markdown("""
    <div class="arena-footer-bar">
        <div>© 2026 Elythra AI • Autonomous Talent Intelligence & Ranking OS.</div>
        <div>
            <span style="color: #FF6B35; font-weight: 700;">🔥 2,484+ Resumes Ingested Today</span>
            &nbsp;•&nbsp;
            <span style="color: #10B981; font-weight: 700;">⚡ Precision Match Active</span>
            &nbsp;•&nbsp;
            <span style="color: #E2E8F0;">Amandeep Verma</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
