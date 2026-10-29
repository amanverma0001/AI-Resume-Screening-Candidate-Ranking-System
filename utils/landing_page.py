"""
Interactive Modern Landing Portal Component for AI Resume Screening System (Elythra).
Compact, zero-scroll centered panel with pure 60 FPS moving resume candidate match stream background.
"""

import streamlit as st
from core.auth import verify_credentials, register_new_user, DEFAULT_USERS

def render_landing_page():
    """Renders the compact, zero-scroll recruiter command center."""

    st.markdown("""<style>
/* 1. SCROLLING 100% OFF & FULL TRANSPARENCY */
html, body, [data-testid="stApp"], .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], header, .main, [data-testid="stMain"], [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
background: transparent !important;
background-color: transparent !important;
overflow: hidden !important;
overflow-y: hidden !important;
overflow-x: hidden !important;
height: 100vh !important;
max-height: 100vh !important;
}
body {
background-color: #080C14 !important;
}
/* 2. CENTERED BLOCK CONTAINER (NO SCROLL, PURE VERTICAL CENTERING) */
.block-container {
padding: 0 !important;
max-width: 420px !important;
height: 100vh !important;
display: flex !important;
flex-direction: column !important;
justify-content: center !important;
align-items: center !important;
margin: 0 auto !important;
position: relative !important;
z-index: 2 !important;
}
.stDeployButton, [data-testid="stToolbarActions"], #MainMenu, footer {
display: none !important;
visibility: hidden !important;
}
[data-testid="stSidebarCollapsedControl"], [data-testid="stSidebarCollapseButton"] {
display: none !important;
visibility: hidden !important;
}
/* 3. FULLSCREEN MOVING BACKGROUND (CANDIDATE SIMILARITY STREAM) */
.resume-bg-root {
position: fixed !important;
top: 0 !important;
left: 0 !important;
width: 100vw !important;
height: 100vh !important;
z-index: 0 !important;
pointer-events: none !important;
background: radial-gradient(ellipse at 50% 25%, #0F192C 0%, #080C14 85%) !important;
overflow: hidden !important;
}
.resume-grid-mesh {
position: absolute;
top: 0;
left: 0;
width: 100%;
height: 100%;
background-image: linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(to bottom, rgba(255, 255, 255, 0.035) 1px, transparent 1px);
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
right: 18px;
top: 14%;
display: flex;
flex-direction: column;
gap: 24px;
font-family: "JetBrains Mono", monospace;
font-size: 10px;
font-weight: 700;
color: rgba(255, 255, 255, 0.18);
text-align: right;
pointer-events: none;
letter-spacing: 0.04em;
}
.live-match-pill {
position: absolute;
right: 8px;
top: 48%;
background: linear-gradient(135deg, #10B981, #059669);
color: #FFFFFF;
font-family: "JetBrains Mono", monospace;
font-size: 10px;
font-weight: 800;
padding: 3px 8px;
border-radius: 4px;
box-shadow: 0 0 14px rgba(16, 185, 129, 0.65);
}
.float-resume-badge {
position: absolute;
background: rgba(14, 21, 37, 0.85);
backdrop-filter: blur(12px);
-webkit-backdrop-filter: blur(12px);
border: 1px solid rgba(56, 189, 248, 0.28);
border-radius: 18px;
padding: 5px 12px;
font-size: 0.74rem;
font-weight: 700;
display: inline-flex;
align-items: center;
gap: 6px;
box-shadow: 0 4px 18px rgba(0, 0, 0, 0.5);
}
.badge-top-cand { top: 16%; left: 8%; animation: resumeBadgeFloat1 8s ease-in-out infinite alternate; color: #10B981; }
.badge-nlp-speed { top: 22%; right: 10%; animation: resumeBadgeFloat2 9s ease-in-out infinite alternate; color: #38BDF8; }
.badge-dataset { bottom: 12%; left: 8%; animation: resumeBadgeFloat3 10s ease-in-out infinite alternate; color: #A855F7; }
.badge-architect { bottom: 16%; right: 10%; animation: resumeBadgeFloat4 7s ease-in-out infinite alternate; color: #10B981; }
@keyframes resumeBadgeFloat1 { 0% { transform: translate(0, 0); } 100% { transform: translate(16px, -12px); } }
@keyframes resumeBadgeFloat2 { 0% { transform: translate(0, 0); } 100% { transform: translate(-14px, 16px); } }
@keyframes resumeBadgeFloat3 { 0% { transform: translate(0, 0); } 100% { transform: translate(18px, 12px); } }
@keyframes resumeBadgeFloat4 { 0% { transform: translate(0, 0); } 100% { transform: translate(-16px, -14px); } }
/* 4. COMPACT CARD CONTAINER (FITS 100% IN VIEWPORT) */
div[data-testid="stVerticalBlockBorderWrapper"] {
background: rgba(13, 20, 36, 0.92) !important;
backdrop-filter: blur(28px) !important;
-webkit-backdrop-filter: blur(28px) !important;
border: 1px solid rgba(59, 130, 246, 0.35) !important;
border-radius: 20px !important;
padding: 22px 24px !important;
box-shadow: 0 25px 70px rgba(0, 0, 0, 0.85), 0 0 45px rgba(37, 99, 235, 0.22) !important;
width: 100% !important;
max-width: 410px !important;
margin: 0 auto !important;
}
[data-testid="stForm"] {
border: none !important;
padding: 0 !important;
background: transparent !important;
}
.compact-icon-badge {
width: 44px;
height: 44px;
border-radius: 12px;
background: linear-gradient(135deg, #1D4ED8, #3B82F6);
display: flex;
align-items: center;
justify-content: center;
font-size: 20px;
margin: 0 auto 6px auto;
box-shadow: 0 6px 18px rgba(37, 99, 235, 0.5);
}
.compact-title {
font-size: 1.45rem;
font-weight: 800;
color: #FFFFFF;
text-align: center;
margin: 0 0 2px 0;
letter-spacing: -0.02em;
line-height: 1.2;
}
.compact-sub {
color: #94A3B8;
font-size: 0.8rem;
text-align: center;
margin-bottom: 12px;
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

    st.markdown("""<div class="resume-bg-root">
<div class="resume-grid-mesh"></div>
<div class="y-axis-talent-tiers">
<div>100% TIER-1 ELITE</div><div>95% EXCEPTIONAL</div><div>90% SHORTLISTED</div><div>85% HIGH POTENTIAL</div><div>80% QUALIFIED</div><div>75% COMPETENT</div><div>70% BASELINE</div>
</div>
<div class="live-match-pill">99.4% MATCH</div>
<div class="float-resume-badge badge-top-cand">📄 Rahul Sharma • Full Stack • 98.4% Match</div>
<div class="float-resume-badge badge-nlp-speed">⚡ NLP Parser • 0.09s Sub-Second</div>
<div class="float-resume-badge badge-dataset">📊 2,484 Kaggle Resumes • 24 Domains</div>
<div class="float-resume-badge badge-architect">📄 Amandeep Verma • AI Architect • 99.8%</div>
<div class="chart-scroll-track">
<svg viewBox="0 0 3200 600" width="3200" height="600" preserveAspectRatio="none" style="position: absolute; top: 0; left: 0; width: 3200px; height: 100vh;">
<defs>
<linearGradient id="resumeAreaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="rgba(56, 189, 248, 0.18)"/>
<stop offset="50%" stop-color="rgba(16, 185, 129, 0.07)"/>
<stop offset="100%" stop-color="rgba(8, 12, 20, 0)"/>
</linearGradient>
</defs>
<path d="M 0,320 L 0,300.0 L 8,295.8 L 16,291.9 L 24,288.1 L 32,284.6 L 40,281.2 L 48,278.0 L 56,275.1 L 64,272.4 L 72,269.9 L 80,267.6 L 88,265.5 L 96,263.6 L 104,261.9 L 112,260.4 L 120,259.0 L 128,257.9 L 136,256.9 L 144,256.0 L 152,255.3 L 160,254.7 L 168,254.2 L 176,253.8 L 184,253.5 L 192,253.3 L 200,253.2 L 208,253.1 L 216,253.1 L 224,253.1 L 232,253.1 L 240,253.1 L 248,253.2 L 256,253.3 L 264,253.4 L 272,253.4 L 280,253.5 L 288,253.6 L 296,253.6 L 304,253.7 L 312,253.7 L 320,253.8 L 328,253.8 L 336,253.9 L 344,253.9 L 352,254.0 L 360,254.1 L 368,254.2 L 376,254.3 L 384,254.5 L 392,254.7 L 400,255.0 L 408,255.3 L 416,255.8 L 424,256.3 L 432,256.9 L 440,257.5 L 448,258.3 L 456,259.2 L 464,260.2 L 472,261.3 L 480,262.6 L 488,263.9 L 496,265.4 L 504,267.0 L 512,268.8 L 520,270.6 L 528,272.6 L 536,274.7 L 544,276.9 L 552,279.3 L 560,281.7 L 568,284.2 L 576,286.8 L 584,289.4 L 592,292.1 L 600,294.9 L 608,297.7 L 616,300.5 L 624,303.3 L 632,306.1 L 640,308.9 L 648,311.6 L 656,314.3 L 664,317.0 L 672,319.5 L 680,321.9 L 688,324.3 L 696,326.5 L 704,328.5 L 712,330.5 L 720,332.2 L 728,333.8 L 736,335.3 L 744,336.5 L 752,337.6 L 760,338.5 L 768,339.2 L 776,339.6 L 784,340.0 L 792,340.1 L 800,340.0 L 808,339.8 L 816,339.3 L 824,338.8 L 832,338.0 L 840,337.2 L 848,336.2 L 856,335.1 L 864,333.9 L 872,332.6 L 880,331.3 L 888,329.9 L 896,328.5 L 904,327.1 L 912,325.7 L 920,324.3 L 928,323.0 L 936,321.8 L 944,320.7 L 952,319.6 L 960,318.7 L 968,318.0 L 976,317.4 L 984,317.0 L 992,316.8 L 1000,316.8 L 1008,317.0 L 1016,317.5 L 1024,318.2 L 1032,319.1 L 1040,320.3 L 1048,321.7 L 1056,323.4 L 1064,325.3 L 1072,327.4 L 1080,329.8 L 1088,332.5 L 1096,335.3 L 1104,338.4 L 1112,341.6 L 1120,345.1 L 1128,348.7 L 1136,352.4 L 1144,356.3 L 1152,360.2 L 1160,364.3 L 1168,368.4 L 1176,372.6 L 1184,376.7 L 1192,380.9 L 1200,385.0 L 1208,389.0 L 1216,393.0 L 1224,396.8 L 1232,400.6 L 1240,404.1 L 1248,407.4 L 1256,410.6 L 1264,413.5 L 1272,416.2 L 1280,418.6 L 1288,420.7 L 1296,422.5 L 1304,424.0 L 1312,425.2 L 1320,426.0 L 1328,426.5 L 1336,426.6 L 1344,426.4 L 1352,425.8 L 1360,424.9 L 1368,423.6 L 1376,422.0 L 1384,420.0 L 1392,417.7 L 1400,415.1 L 1408,412.2 L 1416,409.0 L 1424,405.4 L 1432,401.7 L 1440,397.7 L 1448,393.4 L 1456,389.0 L 1464,384.4 L 1472,379.6 L 1480,374.7 L 1488,369.7 L 1496,364.6 L 1504,359.4 L 1512,354.1 L 1520,348.9 L 1528,343.7 L 1536,338.4 L 1544,333.3 L 1552,328.2 L 1560,323.2 L 1568,318.3 L 1576,313.5 L 1584,308.8 L 1592,304.3 L 1600,300.0 L 1608,295.8 L 1616,291.9 L 1624,288.1 L 1632,284.6 L 1640,281.2 L 1648,278.0 L 1656,275.1 L 1664,272.4 L 1672,269.9 L 1680,267.6 L 1688,265.5 L 1696,263.6 L 1704,261.9 L 1712,260.4 L 1720,259.0 L 1728,257.9 L 1736,256.9 L 1744,256.0 L 1752,255.3 L 1760,254.7 L 1768,254.2 L 1776,253.8 L 1784,253.5 L 1792,253.3 L 1800,253.2 L 1808,253.1 L 1816,253.1 L 1824,253.1 L 1832,253.1 L 1840,253.1 L 1848,253.2 L 1856,253.3 L 1864,253.4 L 1872,253.4 L 1880,253.5 L 1888,253.6 L 1896,253.6 L 1904,253.7 L 1912,253.7 L 1920,253.8 L 1928,253.8 L 1936,253.9 L 1944,253.9 L 1952,254.0 L 1960,254.1 L 1968,254.2 L 1976,254.3 L 1984,254.5 L 1992,254.7 L 2000,255.0 L 2008,255.3 L 2016,255.8 L 2024,256.3 L 2032,256.9 L 2040,257.5 L 2048,258.3 L 2056,259.2 L 2064,260.2 L 2072,261.3 L 2080,262.6 L 2088,263.9 L 2096,265.4 L 2104,267.0 L 2112,268.8 L 2120,270.6 L 2128,272.6 L 2136,274.7 L 2144,276.9 L 2152,279.3 L 2160,281.7 L 2168,284.2 L 2176,286.8 L 2184,289.4 L 2192,292.1 L 2200,294.9 L 2208,297.7 L 2216,300.5 L 2224,303.3 L 2232,306.1 L 2240,308.9 L 2248,311.6 L 2256,314.3 L 2264,317.0 L 2272,319.5 L 2280,321.9 L 2288,324.3 L 2296,326.5 L 2304,328.5 L 2312,330.5 L 2320,332.2 L 2328,333.8 L 2336,335.3 L 2344,336.5 L 2352,337.6 L 2360,338.5 L 2368,339.2 L 2376,339.6 L 2384,340.0 L 2392,340.1 L 2400,340.0 L 2408,339.8 L 2416,339.3 L 2424,338.8 L 2432,338.0 L 2440,337.2 L 2448,336.2 L 2456,335.1 L 2464,333.9 L 2472,332.6 L 2480,331.3 L 2488,329.9 L 2496,328.5 L 2504,327.1 L 2512,325.7 L 2520,324.3 L 2528,323.0 L 2536,321.8 L 2544,320.7 L 2552,319.6 L 2560,318.7 L 2568,318.0 L 2576,317.4 L 2584,317.0 L 2592,316.8 L 2600,316.8 L 2608,317.0 L 2616,317.5 L 2624,318.2 L 2632,319.1 L 2640,320.3 L 2648,321.7 L 2656,323.4 L 2664,325.3 L 2672,327.4 L 2680,329.8 L 2688,332.5 L 2696,335.3 L 2704,338.4 L 2712,341.6 L 2720,345.1 L 2728,348.7 L 2736,352.4 L 2744,356.3 L 2752,360.2 L 2760,364.3 L 2768,368.4 L 2776,372.6 L 2784,376.7 L 2792,380.9 L 2800,385.0 L 2808,389.0 L 2816,393.0 L 2824,396.8 L 2832,400.6 L 2840,404.1 L 2848,407.4 L 2856,410.6 L 2864,413.5 L 2872,416.2 L 2880,418.6 L 2888,420.7 L 2896,422.5 L 2904,424.0 L 2912,425.2 L 2920,426.0 L 2928,426.5 L 2936,426.6 L 2944,426.4 L 2952,425.8 L 2960,424.9 L 2968,423.6 L 2976,422.0 L 2984,420.0 L 2992,417.7 L 3000,415.1 L 3008,412.2 L 3016,409.0 L 3024,405.4 L 3032,401.7 L 3040,397.7 L 3048,393.4 L 3056,389.0 L 3064,384.4 L 3072,379.6 L 3080,374.7 L 3088,369.7 L 3096,364.6 L 3104,359.4 L 3112,354.1 L 3120,348.9 L 3128,343.7 L 3136,338.4 L 3144,333.3 L 3152,328.2 L 3160,323.2 L 3168,318.3 L 3176,313.5 L 3184,308.8 L 3192,304.3 L 3200,300.0 L 3200,600 L 0,600 Z" fill="url(#resumeAreaGrad)"/>
<polyline points="0,300.0 8,295.8 16,291.9 24,288.1 32,284.6 40,281.2 48,278.0 56,275.1 64,272.4 72,269.9 80,267.6 88,265.5 96,263.6 104,261.9 112,260.4 120,259.0 128,257.9 136,256.9 144,256.0 152,255.3 160,254.7 168,254.2 176,253.8 184,253.5 192,253.3 200,253.2 208,253.1 216,253.1 224,253.1 232,253.1 240,253.1 248,253.2 256,253.3 264,253.4 272,253.4 280,253.5 288,253.6 296,253.6 304,253.7 312,253.7 320,253.8 328,253.8 336,253.9 344,253.9 352,254.0 360,254.1 368,254.2 376,254.3 384,254.5 392,254.7 400,255.0 408,255.3 416,255.8 424,256.3 432,256.9 440,257.5 448,258.3 456,259.2 464,260.2 472,261.3 480,262.6 488,263.9 496,265.4 504,267.0 512,268.8 520,270.6 528,272.6 536,274.7 544,276.9 552,279.3 560,281.7 568,284.2 576,286.8 584,289.4 592,292.1 600,294.9 608,297.7 616,300.5 624,303.3 632,306.1 640,308.9 648,311.6 656,314.3 664,317.0 672,319.5 680,321.9 688,324.3 696,326.5 704,328.5 712,330.5 720,332.2 728,333.8 736,335.3 744,336.5 752,337.6 760,338.5 768,339.2 776,339.6 784,340.0 792,340.1 800,340.0 808,339.8 816,339.3 824,338.8 832,338.0 840,337.2 848,336.2 856,335.1 864,333.9 872,332.6 880,331.3 888,329.9 896,328.5 904,327.1 912,325.7 920,324.3 928,323.0 936,321.8 944,320.7 952,319.6 960,318.7 968,318.0 976,317.4 984,317.0 992,316.8 1000,316.8 1008,317.0 1016,317.5 1024,318.2 1032,319.1 1040,320.3 1048,321.7 1056,323.4 1064,325.3 1072,327.4 1080,329.8 1088,332.5 1096,335.3 1104,338.4 1112,341.6 1120,345.1 1128,348.7 1136,352.4 1144,356.3 1152,360.2 1160,364.3 1168,368.4 1176,372.6 1184,376.7 1192,380.9 1200,385.0 1208,389.0 1216,393.0 1224,396.8 1232,400.6 1240,404.1 1248,407.4 1256,410.6 1264,413.5 1272,416.2 1280,418.6 1288,420.7 1296,422.5 1304,424.0 1312,425.2 1320,426.0 1328,426.5 1336,426.6 1344,426.4 1352,425.8 1360,424.9 1368,423.6 1376,422.0 1384,420.0 1392,417.7 1400,415.1 1408,412.2 1416,409.0 1424,405.4 1432,401.7 1440,397.7 1448,393.4 1456,389.0 1464,384.4 1472,379.6 1480,374.7 1488,369.7 1496,364.6 1504,359.4 1512,354.1 1520,348.9 1528,343.7 1536,338.4 1544,333.3 1552,328.2 1560,323.2 1568,318.3 1576,313.5 1584,308.8 1592,304.3 1600,300.0 1608,295.8 1616,291.9 1624,288.1 1632,284.6 1640,281.2 1648,278.0 1656,275.1 1664,272.4 1672,269.9 1680,267.6 1688,265.5 1696,263.6 1704,261.9 1712,260.4 1720,259.0 1728,257.9 1736,256.9 1744,256.0 1752,255.3 1760,254.7 1768,254.2 1776,253.8 1784,253.5 1792,253.3 1800,253.2 1808,253.1 1816,253.1 1824,253.1 1832,253.1 1840,253.1 1848,253.2 1856,253.3 1864,253.4 1872,253.4 1880,253.5 1888,253.6 1896,253.6 1904,253.7 1912,253.7 1920,253.8 1928,253.8 1936,253.9 1944,253.9 1952,254.0 1960,254.1 1968,254.2 1976,254.3 1984,254.5 1992,254.7 2000,255.0 2008,255.3 2016,255.8 2024,256.3 2032,256.9 2040,257.5 2048,258.3 2056,259.2 2064,260.2 2072,261.3 2080,262.6 2088,263.9 2096,265.4 2104,267.0 2112,268.8 2120,270.6 2128,272.6 2136,274.7 2144,276.9 2152,279.3 2160,281.7 2168,284.2 2176,286.8 2184,289.4 2192,292.1 2200,294.9 2208,297.7 2216,300.5 2224,303.3 2232,306.1 2240,308.9 2248,311.6 2256,314.3 2264,317.0 2272,319.5 2280,321.9 2288,324.3 2296,326.5 2304,328.5 2312,330.5 2320,332.2 2328,333.8 2336,335.3 2344,336.5 2352,337.6 2360,338.5 2368,339.2 2376,339.6 2384,340.0 2392,340.1 2400,340.0 2408,339.8 2416,339.3 2424,338.8 2432,338.0 2440,337.2 2448,336.2 2456,335.1 2464,333.9 2472,332.6 2480,331.3 2488,329.9 2496,328.5 2504,327.1 2512,325.7 2520,324.3 2528,323.0 2536,321.8 2544,320.7 2552,319.6 2560,318.7 2568,318.0 2576,317.4 2584,317.0 2592,316.8 2600,316.8 2608,317.0 2616,317.5 2624,318.2 2632,319.1 2640,320.3 2648,321.7 2656,323.4 2664,325.3 2672,327.4 2680,329.8 2688,332.5 2696,335.3 2704,338.4 2712,341.6 2720,345.1 2728,348.7 2736,352.4 2744,356.3 2752,360.2 2760,364.3 2768,368.4 2776,372.6 2784,376.7 2792,380.9 2800,385.0 2808,389.0 2816,393.0 2824,396.8 2832,400.6 2840,404.1 2848,407.4 2856,410.6 2864,413.5 2872,416.2 2880,418.6 2888,420.7 2896,422.5 2904,424.0 2912,425.2 2920,426.0 2928,426.5 2936,426.6 2944,426.4 2952,425.8 2960,424.9 2968,423.6 2976,422.0 2984,420.0 2992,417.7 3000,415.1 3008,412.2 3016,409.0 3024,405.4 3032,401.7 3040,397.7 3048,393.4 3056,389.0 3064,384.4 3072,379.6 3080,374.7 3088,369.7 3096,364.6 3104,359.4 3112,354.1 3120,348.9 3128,343.7 3136,338.4 3144,333.3 3152,328.2 3160,323.2 3168,318.3 3176,313.5 3184,308.8 3192,304.3 3200,300.0" fill="none" stroke="#38BDF8" stroke-width="2.6" style="filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.95)) drop-shadow(0 0 25px rgba(56, 189, 248, 0.5));"/>
<circle cx="32" cy="284.6" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="32" cy="284.6" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="96" cy="263.6" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="96" cy="263.6" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="160" cy="254.7" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="160" cy="254.7" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="224" cy="253.1" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="224" cy="253.1" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="288" cy="253.6" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="288" cy="253.6" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="352" cy="254.0" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="352" cy="254.0" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="416" cy="255.8" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="416" cy="255.8" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="480" cy="262.6" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="480" cy="262.6" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="544" cy="276.9" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="544" cy="276.9" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="608" cy="297.7" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="608" cy="297.7" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="672" cy="319.5" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="672" cy="319.5" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="736" cy="335.3" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="736" cy="335.3" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="800" cy="340.0" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="800" cy="340.0" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="864" cy="333.9" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="864" cy="333.9" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="928" cy="323.0" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="928" cy="323.0" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="992" cy="316.8" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="992" cy="316.8" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="1056" cy="323.4" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="1056" cy="323.4" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="1120" cy="345.1" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="1120" cy="345.1" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="1184" cy="376.7" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="1184" cy="376.7" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="1248" cy="407.4" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="1248" cy="407.4" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="1312" cy="425.2" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="1312" cy="425.2" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="1376" cy="422.0" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="1376" cy="422.0" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="1440" cy="397.7" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="1440" cy="397.7" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="1504" cy="359.4" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="1504" cy="359.4" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="1568" cy="318.3" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="1568" cy="318.3" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="1632" cy="284.6" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="1632" cy="284.6" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="1696" cy="263.6" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="1696" cy="263.6" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="1760" cy="254.7" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="1760" cy="254.7" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="1824" cy="253.1" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="1824" cy="253.1" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="1888" cy="253.6" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="1888" cy="253.6" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="1952" cy="254.0" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="1952" cy="254.0" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="2016" cy="255.8" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="2016" cy="255.8" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="2080" cy="262.6" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="2080" cy="262.6" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="2144" cy="276.9" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="2144" cy="276.9" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="2208" cy="297.7" r="7" fill="none" stroke="#10B981" stroke-width="1.2" opacity="0.6"/><circle cx="2208" cy="297.7" r="3.5" fill="#10B981" style="filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.8));"/><circle cx="2272" cy="319.5" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="2272" cy="319.5" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="2336" cy="335.3" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="2336" cy="335.3" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="2400" cy="340.0" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="2400" cy="340.0" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="2464" cy="333.9" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="2464" cy="333.9" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="2528" cy="323.0" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="2528" cy="323.0" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="2592" cy="316.8" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="2592" cy="316.8" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="2656" cy="323.4" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="2656" cy="323.4" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="2720" cy="345.1" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="2720" cy="345.1" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="2784" cy="376.7" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="2784" cy="376.7" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="2848" cy="407.4" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="2848" cy="407.4" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="2912" cy="425.2" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="2912" cy="425.2" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="2976" cy="422.0" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="2976" cy="422.0" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="3040" cy="397.7" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="3040" cy="397.7" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="3104" cy="359.4" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="3104" cy="359.4" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/><circle cx="3168" cy="318.3" r="7" fill="none" stroke="#38BDF8" stroke-width="1.2" opacity="0.6"/><circle cx="3168" cy="318.3" r="3.5" fill="#38BDF8" style="filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.8));"/>
</svg>
</div>
</div>""", unsafe_allow_html=True)

    with st.container(border=True):
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
