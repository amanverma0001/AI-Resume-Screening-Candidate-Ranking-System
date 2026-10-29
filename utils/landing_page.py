"""
Interactive Modern Landing Portal Component for AI Resume Screening System (Elythra).
Exact replication of ZenithTrade (trade.amandeep.fit) Design System.
"""

import streamlit as st
from core.auth import verify_credentials, register_new_user, DEFAULT_USERS

def render_landing_page():
    """Renders the authentic ZenithTrade terminal login portal."""

    st.markdown("""<style>
html, body, [data-testid="stApp"], .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], header, .main, [data-testid="stMain"], [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
background: transparent !important;
background-color: transparent !important;
}
body {
background-color: #080C14 !important;
overflow-x: hidden !important;
}
.block-container {
padding-top: 0.8rem !important;
padding-bottom: 1.5rem !important;
max-width: 1400px !important;
position: relative !important;
z-index: 2 !important;
}
.stDeployButton, [data-testid="stToolbarActions"], #MainMenu, footer {
display: none !important;
visibility: hidden !important;
}
[data-testid="stSidebarCollapsedControl"], [data-testid="stSidebarCollapseButton"] {
display: flex !important;
visibility: visible !important;
color: #3B82F6 !important;
}
.zenith-bg-root {
position: fixed !important;
top: 0 !important;
left: 0 !important;
width: 100vw !important;
height: 100vh !important;
z-index: 0 !important;
pointer-events: none !important;
background: #080C14 !important;
overflow: hidden !important;
}
.zenith-grid-mesh {
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
animation: chartScrollLoop 26s linear infinite;
}
@keyframes chartScrollLoop {
0% { transform: translateX(0); }
100% { transform: translateX(-1600px); }
}
.y-axis-prices {
position: absolute;
right: 18px;
top: 14%;
display: flex;
flex-direction: column;
gap: 26px;
font-family: "JetBrains Mono", monospace;
font-size: 11px;
font-weight: 600;
color: rgba(255, 255, 255, 0.22);
text-align: right;
pointer-events: none;
}
.live-price-pill {
position: absolute;
right: 8px;
top: 45%;
background: #2563EB;
color: #FFFFFF;
font-family: "JetBrains Mono", monospace;
font-size: 11px;
font-weight: 700;
padding: 3px 8px;
border-radius: 4px;
box-shadow: 0 0 14px rgba(37, 99, 235, 0.7);
}
.float-asset-badge {
position: absolute;
background: rgba(14, 21, 37, 0.82);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.12);
border-radius: 20px;
padding: 5px 12px;
font-size: 0.78rem;
font-weight: 700;
display: inline-flex;
align-items: center;
gap: 6px;
box-shadow: 0 4px 18px rgba(0, 0, 0, 0.45);
}
.badge-hdfc { top: 22%; left: 48%; animation: assetFloat1 8s ease-in-out infinite alternate; color: #10B981; }
.badge-nifty { top: 25%; right: 10%; animation: assetFloat2 9s ease-in-out infinite alternate; color: #10B981; }
.badge-infy { bottom: 10%; left: 16%; animation: assetFloat3 10s ease-in-out infinite alternate; color: #EF4444; }
.badge-tcs { bottom: 14%; right: 12%; animation: assetFloat4 7s ease-in-out infinite alternate; color: #10B981; }
@keyframes assetFloat1 { 0% { transform: translate(0, 0); } 100% { transform: translate(15px, -12px); } }
@keyframes assetFloat2 { 0% { transform: translate(0, 0); } 100% { transform: translate(-12px, 15px); } }
@keyframes assetFloat3 { 0% { transform: translate(0, 0); } 100% { transform: translate(18px, 10px); } }
@keyframes assetFloat4 { 0% { transform: translate(0, 0); } 100% { transform: translate(-15px, -15px); } }
.zenith-nav-bar {
background: rgba(11, 17, 30, 0.75);
backdrop-filter: blur(20px);
-webkit-backdrop-filter: blur(20px);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 16px;
padding: 10px 22px;
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 12px;
box-shadow: 0 8px 25px rgba(0, 0, 0, 0.45);
}
.zenith-brand-group {
display: flex;
align-items: center;
gap: 12px;
}
.zenith-brand-logo {
width: 38px;
height: 38px;
border-radius: 10px;
background: linear-gradient(135deg, #1D4ED8, #3B82F6);
display: flex;
align-items: center;
justify-content: center;
font-size: 20px;
box-shadow: 0 4px 16px rgba(37, 99, 235, 0.5);
}
.zenith-brand-title {
font-size: 1.5rem;
font-weight: 800;
color: #FFFFFF;
letter-spacing: -0.02em;
}
.zenith-version-badge {
background: rgba(59, 130, 246, 0.15);
border: 1px solid rgba(59, 130, 246, 0.35);
color: #60A5FA;
font-size: 0.72rem;
font-weight: 700;
padding: 3px 9px;
border-radius: 20px;
letter-spacing: 0.05em;
text-transform: uppercase;
}
.status-pill-green {
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
.btn-enter-terminal {
background: linear-gradient(135deg, #2563EB, #1D4ED8);
color: white;
font-size: 0.85rem;
font-weight: 700;
padding: 7px 16px;
border-radius: 8px;
border: none;
box-shadow: 0 4px 14px rgba(37, 99, 235, 0.45);
display: inline-flex;
align-items: center;
gap: 6px;
}
.zenith-ticker-bar {
display: flex;
align-items: center;
gap: 8px;
margin-bottom: 20px;
overflow-x: auto;
padding-bottom: 4px;
}
.ticker-head-label {
color: #64748B;
font-size: 0.74rem;
font-weight: 700;
letter-spacing: 0.08em;
text-transform: uppercase;
white-space: nowrap;
margin-right: 6px;
}
.ticker-chip {
background: rgba(14, 21, 37, 0.8);
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 30px;
padding: 5px 14px;
font-size: 0.78rem;
white-space: nowrap;
display: inline-flex;
align-items: center;
gap: 6px;
color: #E2E8F0;
}
.ticker-chip.active-blue {
border-color: rgba(59, 130, 246, 0.7);
background: rgba(37, 99, 235, 0.18);
}
/* Make the 2nd Column the Unified Glassmorphic Card */
div[data-testid="column"]:nth-of-type(2), [data-testid="stHorizontalBlock"] > div:nth-child(2) {
background: rgba(13, 20, 36, 0.90) !important;
backdrop-filter: blur(32px) !important;
-webkit-backdrop-filter: blur(32px) !important;
border: 1px solid rgba(59, 130, 246, 0.35) !important;
border-radius: 22px !important;
padding: 30px 28px !important;
box-shadow: 0 30px 90px rgba(0, 0, 0, 0.85), 0 0 50px rgba(37, 99, 235, 0.22) !important;
}
[data-testid="stForm"] {
border: none !important;
padding: 0 !important;
background: transparent !important;
}
.terminal-icon-badge {
width: 58px;
height: 58px;
border-radius: 16px;
background: linear-gradient(135deg, #1D4ED8, #3B82F6);
display: flex;
align-items: center;
justify-content: center;
font-size: 26px;
margin: 0 auto 12px auto;
box-shadow: 0 8px 24px rgba(37, 99, 235, 0.55);
}
.terminal-title {
font-size: 2.1rem;
font-weight: 800;
color: #FFFFFF;
text-align: center;
margin: 0 0 6px 0;
letter-spacing: -0.02em;
}
.terminal-sub {
color: #94A3B8;
font-size: 0.88rem;
text-align: center;
margin-bottom: 20px;
}
.zenith-footer-bar {
display: flex;
justify-content: space-between;
align-items: center;
padding: 14px 8px;
color: #64748B;
font-size: 0.8rem;
margin-top: 32px;
border-top: 1px solid rgba(255, 255, 255, 0.06);
position: relative;
z-index: 2;
}
</style>""", unsafe_allow_html=True)

    st.markdown("""<div class="zenith-bg-root">
<div class="zenith-grid-mesh"></div>
<div class="y-axis-prices">
<div>₹25,165</div><div>₹25,033</div><div>₹24,901</div><div>₹24,769</div><div>₹24,637</div><div>₹24,505</div><div>₹24,373</div><div>₹24,241</div><div>₹24,109</div>
</div>
<div class="live-price-pill">₹24,734</div>
<div class="float-asset-badge badge-hdfc">HDFCBANK 1,650.00 +1.80%</div>
<div class="float-asset-badge badge-nifty">NIFTY 50 24,510.40 +0.72%</div>
<div class="float-asset-badge badge-infy">INFY 1,555.45 -0.45%</div>
<div class="float-asset-badge badge-tcs">TCS 3,210.86 +1.25%</div>
<div class="chart-scroll-track">
<svg viewBox="0 0 3200 600" width="3200" height="600" preserveAspectRatio="none" style="position: absolute; top: 0; left: 0; width: 3200px; height: 100vh;">
<polyline points="16,305.0 48,308.9 80,306.0 112,300.4 144,306.7 176,318.6 208,326.4 240,337.7 272,350.0 304,366.5 336,374.0 368,367.0 400,368.9 432,354.4 464,359.4 496,350.1 528,365.3 560,376.3 592,387.2 624,390.1 656,381.4 688,383.3 720,384.1 752,398.7 784,408.3 816,411.3 848,397.5 880,387.3 912,403.7 944,406.6 976,420.5 1008,429.7 1040,425.5 1072,432.5 1104,423.1 1136,425.9 1168,438.5 1200,448.4 1232,429.4 1264,424.3 1296,430.2 1328,432.7 1360,424.4 1392,421.3 1424,433.2 1456,444.8 1488,435.6 1520,437.6 1552,426.3 1584,423.2 1616,305.0 1648,308.9 1680,306.0 1712,300.4 1744,306.7 1776,318.6 1808,326.4 1840,337.7 1872,350.0 1904,366.5 1936,374.0 1968,367.0 2000,368.9 2032,354.4 2064,359.4 2096,350.1 2128,365.3 2160,376.3 2192,387.2 2224,390.1 2256,381.4 2288,383.3 2320,384.1 2352,398.7 2384,408.3 2416,411.3 2448,397.5 2480,387.3 2512,403.7 2544,406.6 2576,420.5 2608,429.7 2640,425.5 2672,432.5 2704,423.1 2736,425.9 2768,438.5 2800,448.4 2832,429.4 2864,424.3 2896,430.2 2928,432.7 2960,424.4 2992,421.3 3024,433.2 3056,444.8 3088,435.6 3120,437.6 3152,426.3 3184,423.2" fill="none" stroke="#38BDF8" stroke-width="2.2" style="filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.8));"/>
<line x1="16" y1="292.6" x2="16" y2="314.4" stroke="#10B981" stroke-width="1.8"/><rect x="10" y="300.0" width="12" height="5.0" fill="#10B981" rx="1.5"/><line x1="48" y1="292.1" x2="48" y2="313.9" stroke="#10B981" stroke-width="1.8"/><rect x="42" y="305.0" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="80" y1="291.9" x2="80" y2="321.4" stroke="#EF4444" stroke-width="1.8"/><rect x="74" y="306.0" width="12" height="4.0" fill="#EF4444" rx="1.5"/><line x1="112" y1="295.0" x2="112" y2="320.9" stroke="#EF4444" stroke-width="1.8"/><rect x="106" y="300.4" width="12" height="5.5" fill="#EF4444" rx="1.5"/><line x1="144" y1="296.1" x2="144" y2="320.7" stroke="#10B981" stroke-width="1.8"/><rect x="138" y="300.4" width="12" height="6.3" fill="#10B981" rx="1.5"/><line x1="176" y1="303.0" x2="176" y2="326.4" stroke="#10B981" stroke-width="1.8"/><rect x="170" y="306.7" width="12" height="11.9" fill="#10B981" rx="1.5"/><line x1="208" y1="310.8" x2="208" y2="333.6" stroke="#10B981" stroke-width="1.8"/><rect x="202" y="318.6" width="12" height="7.8" fill="#10B981" rx="1.5"/><line x1="240" y1="315.4" x2="240" y2="350.3" stroke="#10B981" stroke-width="1.8"/><rect x="234" y="326.4" width="12" height="11.3" fill="#10B981" rx="1.5"/><line x1="272" y1="329.1" x2="272" y2="360.1" stroke="#10B981" stroke-width="1.8"/><rect x="266" y="337.7" width="12" height="12.3" fill="#10B981" rx="1.5"/><line x1="304" y1="343.2" x2="304" y2="379.1" stroke="#10B981" stroke-width="1.8"/><rect x="298" y="350.0" width="12" height="16.6" fill="#10B981" rx="1.5"/><line x1="336" y1="358.0" x2="336" y2="388.0" stroke="#10B981" stroke-width="1.8"/><rect x="330" y="366.5" width="12" height="7.5" fill="#10B981" rx="1.5"/><line x1="368" y1="363.2" x2="368" y2="379.4" stroke="#EF4444" stroke-width="1.8"/><rect x="362" y="367.0" width="12" height="7.0" fill="#EF4444" rx="1.5"/><line x1="400" y1="357.1" x2="400" y2="379.3" stroke="#10B981" stroke-width="1.8"/><rect x="394" y="367.0" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="432" y1="343.5" x2="432" y2="376.8" stroke="#EF4444" stroke-width="1.8"/><rect x="426" y="354.4" width="12" height="14.5" fill="#EF4444" rx="1.5"/><line x1="464" y1="343.7" x2="464" y2="370.5" stroke="#10B981" stroke-width="1.8"/><rect x="458" y="354.4" width="12" height="5.1" fill="#10B981" rx="1.5"/><line x1="496" y1="341.7" x2="496" y2="365.9" stroke="#EF4444" stroke-width="1.8"/><rect x="490" y="350.1" width="12" height="9.3" fill="#EF4444" rx="1.5"/><line x1="528" y1="343.4" x2="528" y2="377.9" stroke="#10B981" stroke-width="1.8"/><rect x="522" y="350.1" width="12" height="15.2" fill="#10B981" rx="1.5"/><line x1="560" y1="357.1" x2="560" y2="386.7" stroke="#10B981" stroke-width="1.8"/><rect x="554" y="365.3" width="12" height="11.0" fill="#10B981" rx="1.5"/><line x1="592" y1="364.0" x2="592" y2="396.8" stroke="#10B981" stroke-width="1.8"/><rect x="586" y="376.3" width="12" height="10.9" fill="#10B981" rx="1.5"/><line x1="624" y1="374.0" x2="624" y2="400.8" stroke="#10B981" stroke-width="1.8"/><rect x="618" y="387.2" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="656" y1="372.0" x2="656" y2="404.8" stroke="#EF4444" stroke-width="1.8"/><rect x="650" y="381.4" width="12" height="8.7" fill="#EF4444" rx="1.5"/><line x1="688" y1="377.8" x2="688" y2="395.6" stroke="#10B981" stroke-width="1.8"/><rect x="682" y="381.4" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="720" y1="374.9" x2="720" y2="396.0" stroke="#10B981" stroke-width="1.8"/><rect x="714" y="383.3" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="752" y1="375.3" x2="752" y2="411.4" stroke="#10B981" stroke-width="1.8"/><rect x="746" y="384.1" width="12" height="14.6" fill="#10B981" rx="1.5"/><line x1="784" y1="391.5" x2="784" y2="420.0" stroke="#10B981" stroke-width="1.8"/><rect x="778" y="398.7" width="12" height="9.6" fill="#10B981" rx="1.5"/><line x1="816" y1="402.2" x2="816" y2="421.1" stroke="#10B981" stroke-width="1.8"/><rect x="810" y="408.3" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="848" y1="393.8" x2="848" y2="415.8" stroke="#EF4444" stroke-width="1.8"/><rect x="842" y="397.5" width="12" height="13.7" fill="#EF4444" rx="1.5"/><line x1="880" y1="382.0" x2="880" y2="410.4" stroke="#EF4444" stroke-width="1.8"/><rect x="874" y="387.3" width="12" height="10.2" fill="#EF4444" rx="1.5"/><line x1="912" y1="373.8" x2="912" y2="416.7" stroke="#10B981" stroke-width="1.8"/><rect x="906" y="387.3" width="12" height="16.4" fill="#10B981" rx="1.5"/><line x1="944" y1="393.4" x2="944" y2="414.7" stroke="#10B981" stroke-width="1.8"/><rect x="938" y="403.7" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="976" y1="398.4" x2="976" y2="434.7" stroke="#10B981" stroke-width="1.8"/><rect x="970" y="406.6" width="12" height="14.0" fill="#10B981" rx="1.5"/><line x1="1008" y1="409.9" x2="1008" y2="434.6" stroke="#10B981" stroke-width="1.8"/><rect x="1002" y="420.5" width="12" height="9.2" fill="#10B981" rx="1.5"/><line x1="1040" y1="418.3" x2="1040" y2="433.5" stroke="#EF4444" stroke-width="1.8"/><rect x="1034" y="425.5" width="12" height="4.2" fill="#EF4444" rx="1.5"/><line x1="1072" y1="413.9" x2="1072" y2="442.8" stroke="#10B981" stroke-width="1.8"/><rect x="1066" y="425.5" width="12" height="7.0" fill="#10B981" rx="1.5"/><line x1="1104" y1="412.7" x2="1104" y2="441.4" stroke="#EF4444" stroke-width="1.8"/><rect x="1098" y="423.1" width="12" height="9.5" fill="#EF4444" rx="1.5"/><line x1="1136" y1="411.5" x2="1136" y2="430.8" stroke="#10B981" stroke-width="1.8"/><rect x="1130" y="423.1" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="1168" y1="420.5" x2="1168" y2="446.2" stroke="#10B981" stroke-width="1.8"/><rect x="1162" y="425.9" width="12" height="12.7" fill="#10B981" rx="1.5"/><line x1="1200" y1="430.5" x2="1200" y2="458.9" stroke="#10B981" stroke-width="1.8"/><rect x="1194" y="438.5" width="12" height="9.9" fill="#10B981" rx="1.5"/><line x1="1232" y1="418.0" x2="1232" y2="448.6" stroke="#EF4444" stroke-width="1.8"/><rect x="1226" y="429.4" width="12" height="10.6" fill="#EF4444" rx="1.5"/><line x1="1264" y1="414.1" x2="1264" y2="432.8" stroke="#EF4444" stroke-width="1.8"/><rect x="1258" y="424.3" width="12" height="5.1" fill="#EF4444" rx="1.5"/><line x1="1296" y1="410.0" x2="1296" y2="436.8" stroke="#10B981" stroke-width="1.8"/><rect x="1290" y="424.3" width="12" height="5.8" fill="#10B981" rx="1.5"/><line x1="1328" y1="416.7" x2="1328" y2="445.1" stroke="#10B981" stroke-width="1.8"/><rect x="1322" y="430.2" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="1360" y1="416.1" x2="1360" y2="439.4" stroke="#EF4444" stroke-width="1.8"/><rect x="1354" y="424.4" width="12" height="8.3" fill="#EF4444" rx="1.5"/><line x1="1392" y1="416.5" x2="1392" y2="435.0" stroke="#EF4444" stroke-width="1.8"/><rect x="1386" y="421.3" width="12" height="4.0" fill="#EF4444" rx="1.5"/><line x1="1424" y1="415.4" x2="1424" y2="445.3" stroke="#10B981" stroke-width="1.8"/><rect x="1418" y="421.3" width="12" height="11.9" fill="#10B981" rx="1.5"/><line x1="1456" y1="421.8" x2="1456" y2="448.8" stroke="#10B981" stroke-width="1.8"/><rect x="1450" y="433.2" width="12" height="11.6" fill="#10B981" rx="1.5"/><line x1="1488" y1="429.3" x2="1488" y2="453.1" stroke="#EF4444" stroke-width="1.8"/><rect x="1482" y="435.6" width="12" height="4.4" fill="#EF4444" rx="1.5"/><line x1="1520" y1="428.0" x2="1520" y2="447.7" stroke="#10B981" stroke-width="1.8"/><rect x="1514" y="435.6" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="1552" y1="417.3" x2="1552" y2="450.9" stroke="#EF4444" stroke-width="1.8"/><rect x="1546" y="426.3" width="12" height="11.3" fill="#EF4444" rx="1.5"/><line x1="1584" y1="418.8" x2="1584" y2="437.0" stroke="#EF4444" stroke-width="1.8"/><rect x="1578" y="423.2" width="12" height="4.0" fill="#EF4444" rx="1.5"/><line x1="1616" y1="292.6" x2="1616" y2="314.4" stroke="#10B981" stroke-width="1.8"/><rect x="1610" y="300.0" width="12" height="5.0" fill="#10B981" rx="1.5"/><line x1="1648" y1="292.1" x2="1648" y2="313.9" stroke="#10B981" stroke-width="1.8"/><rect x="1642" y="305.0" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="1680" y1="291.9" x2="1680" y2="321.4" stroke="#EF4444" stroke-width="1.8"/><rect x="1674" y="306.0" width="12" height="4.0" fill="#EF4444" rx="1.5"/><line x1="1712" y1="295.0" x2="1712" y2="320.9" stroke="#EF4444" stroke-width="1.8"/><rect x="1706" y="300.4" width="12" height="5.5" fill="#EF4444" rx="1.5"/><line x1="1744" y1="296.1" x2="1744" y2="320.7" stroke="#10B981" stroke-width="1.8"/><rect x="1738" y="300.4" width="12" height="6.3" fill="#10B981" rx="1.5"/><line x1="1776" y1="303.0" x2="1776" y2="326.4" stroke="#10B981" stroke-width="1.8"/><rect x="1770" y="306.7" width="12" height="11.9" fill="#10B981" rx="1.5"/><line x1="1808" y1="310.8" x2="1808" y2="333.6" stroke="#10B981" stroke-width="1.8"/><rect x="1802" y="318.6" width="12" height="7.8" fill="#10B981" rx="1.5"/><line x1="1840" y1="315.4" x2="1840" y2="350.3" stroke="#10B981" stroke-width="1.8"/><rect x="1834" y="326.4" width="12" height="11.3" fill="#10B981" rx="1.5"/><line x1="1872" y1="329.1" x2="1872" y2="360.1" stroke="#10B981" stroke-width="1.8"/><rect x="1866" y="337.7" width="12" height="12.3" fill="#10B981" rx="1.5"/><line x1="1904" y1="343.2" x2="1904" y2="379.1" stroke="#10B981" stroke-width="1.8"/><rect x="1898" y="350.0" width="12" height="16.6" fill="#10B981" rx="1.5"/><line x1="1936" y1="358.0" x2="1936" y2="388.0" stroke="#10B981" stroke-width="1.8"/><rect x="1930" y="366.5" width="12" height="7.5" fill="#10B981" rx="1.5"/><line x1="1968" y1="363.2" x2="1968" y2="379.4" stroke="#EF4444" stroke-width="1.8"/><rect x="1962" y="367.0" width="12" height="7.0" fill="#EF4444" rx="1.5"/><line x1="2000" y1="357.1" x2="2000" y2="379.3" stroke="#10B981" stroke-width="1.8"/><rect x="1994" y="367.0" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="2032" y1="343.5" x2="2032" y2="376.8" stroke="#EF4444" stroke-width="1.8"/><rect x="2026" y="354.4" width="12" height="14.5" fill="#EF4444" rx="1.5"/><line x1="2064" y1="343.7" x2="2064" y2="370.5" stroke="#10B981" stroke-width="1.8"/><rect x="2058" y="354.4" width="12" height="5.1" fill="#10B981" rx="1.5"/><line x1="2096" y1="341.7" x2="2096" y2="365.9" stroke="#EF4444" stroke-width="1.8"/><rect x="2090" y="350.1" width="12" height="9.3" fill="#EF4444" rx="1.5"/><line x1="2128" y1="343.4" x2="2128" y2="377.9" stroke="#10B981" stroke-width="1.8"/><rect x="2122" y="350.1" width="12" height="15.2" fill="#10B981" rx="1.5"/><line x1="2160" y1="357.1" x2="2160" y2="386.7" stroke="#10B981" stroke-width="1.8"/><rect x="2154" y="365.3" width="12" height="11.0" fill="#10B981" rx="1.5"/><line x1="2192" y1="364.0" x2="2192" y2="396.8" stroke="#10B981" stroke-width="1.8"/><rect x="2186" y="376.3" width="12" height="10.9" fill="#10B981" rx="1.5"/><line x1="2224" y1="374.0" x2="2224" y2="400.8" stroke="#10B981" stroke-width="1.8"/><rect x="2218" y="387.2" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="2256" y1="372.0" x2="2256" y2="404.8" stroke="#EF4444" stroke-width="1.8"/><rect x="2250" y="381.4" width="12" height="8.7" fill="#EF4444" rx="1.5"/><line x1="2288" y1="377.8" x2="2288" y2="395.6" stroke="#10B981" stroke-width="1.8"/><rect x="2282" y="381.4" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="2320" y1="374.9" x2="2320" y2="396.0" stroke="#10B981" stroke-width="1.8"/><rect x="2314" y="383.3" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="2352" y1="375.3" x2="2352" y2="411.4" stroke="#10B981" stroke-width="1.8"/><rect x="2346" y="384.1" width="12" height="14.6" fill="#10B981" rx="1.5"/><line x1="2384" y1="391.5" x2="2384" y2="420.0" stroke="#10B981" stroke-width="1.8"/><rect x="2378" y="398.7" width="12" height="9.6" fill="#10B981" rx="1.5"/><line x1="2416" y1="402.2" x2="2416" y2="421.1" stroke="#10B981" stroke-width="1.8"/><rect x="2410" y="408.3" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="2448" y1="393.8" x2="2448" y2="415.8" stroke="#EF4444" stroke-width="1.8"/><rect x="2442" y="397.5" width="12" height="13.7" fill="#EF4444" rx="1.5"/><line x1="2480" y1="382.0" x2="2480" y2="410.4" stroke="#EF4444" stroke-width="1.8"/><rect x="2474" y="387.3" width="12" height="10.2" fill="#EF4444" rx="1.5"/><line x1="2512" y1="373.8" x2="2512" y2="416.7" stroke="#10B981" stroke-width="1.8"/><rect x="2506" y="387.3" width="12" height="16.4" fill="#10B981" rx="1.5"/><line x1="2544" y1="393.4" x2="2544" y2="414.7" stroke="#10B981" stroke-width="1.8"/><rect x="2538" y="403.7" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="2576" y1="398.4" x2="2576" y2="434.7" stroke="#10B981" stroke-width="1.8"/><rect x="2570" y="406.6" width="12" height="14.0" fill="#10B981" rx="1.5"/><line x1="2608" y1="409.9" x2="2608" y2="434.6" stroke="#10B981" stroke-width="1.8"/><rect x="2602" y="420.5" width="12" height="9.2" fill="#10B981" rx="1.5"/><line x1="2640" y1="418.3" x2="2640" y2="433.5" stroke="#EF4444" stroke-width="1.8"/><rect x="2634" y="425.5" width="12" height="4.2" fill="#EF4444" rx="1.5"/><line x1="2672" y1="413.9" x2="2672" y2="442.8" stroke="#10B981" stroke-width="1.8"/><rect x="2666" y="425.5" width="12" height="7.0" fill="#10B981" rx="1.5"/><line x1="2704" y1="412.7" x2="2704" y2="441.4" stroke="#EF4444" stroke-width="1.8"/><rect x="2698" y="423.1" width="12" height="9.5" fill="#EF4444" rx="1.5"/><line x1="2736" y1="411.5" x2="2736" y2="430.8" stroke="#10B981" stroke-width="1.8"/><rect x="2730" y="423.1" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="2768" y1="420.5" x2="2768" y2="446.2" stroke="#10B981" stroke-width="1.8"/><rect x="2762" y="425.9" width="12" height="12.7" fill="#10B981" rx="1.5"/><line x1="2800" y1="430.5" x2="2800" y2="458.9" stroke="#10B981" stroke-width="1.8"/><rect x="2794" y="438.5" width="12" height="9.9" fill="#10B981" rx="1.5"/><line x1="2832" y1="418.0" x2="2832" y2="448.6" stroke="#EF4444" stroke-width="1.8"/><rect x="2826" y="429.4" width="12" height="10.6" fill="#EF4444" rx="1.5"/><line x1="2864" y1="414.1" x2="2864" y2="432.8" stroke="#EF4444" stroke-width="1.8"/><rect x="2858" y="424.3" width="12" height="5.1" fill="#EF4444" rx="1.5"/><line x1="2896" y1="410.0" x2="2896" y2="436.8" stroke="#10B981" stroke-width="1.8"/><rect x="2890" y="424.3" width="12" height="5.8" fill="#10B981" rx="1.5"/><line x1="2928" y1="416.7" x2="2928" y2="445.1" stroke="#10B981" stroke-width="1.8"/><rect x="2922" y="430.2" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="2960" y1="416.1" x2="2960" y2="439.4" stroke="#EF4444" stroke-width="1.8"/><rect x="2954" y="424.4" width="12" height="8.3" fill="#EF4444" rx="1.5"/><line x1="2992" y1="416.5" x2="2992" y2="435.0" stroke="#EF4444" stroke-width="1.8"/><rect x="2986" y="421.3" width="12" height="4.0" fill="#EF4444" rx="1.5"/><line x1="3024" y1="415.4" x2="3024" y2="445.3" stroke="#10B981" stroke-width="1.8"/><rect x="3018" y="421.3" width="12" height="11.9" fill="#10B981" rx="1.5"/><line x1="3056" y1="421.8" x2="3056" y2="448.8" stroke="#10B981" stroke-width="1.8"/><rect x="3050" y="433.2" width="12" height="11.6" fill="#10B981" rx="1.5"/><line x1="3088" y1="429.3" x2="3088" y2="453.1" stroke="#EF4444" stroke-width="1.8"/><rect x="3082" y="435.6" width="12" height="4.4" fill="#EF4444" rx="1.5"/><line x1="3120" y1="428.0" x2="3120" y2="447.7" stroke="#10B981" stroke-width="1.8"/><rect x="3114" y="435.6" width="12" height="4.0" fill="#10B981" rx="1.5"/><line x1="3152" y1="417.3" x2="3152" y2="450.9" stroke="#EF4444" stroke-width="1.8"/><rect x="3146" y="426.3" width="12" height="11.3" fill="#EF4444" rx="1.5"/><line x1="3184" y1="418.8" x2="3184" y2="437.0" stroke="#EF4444" stroke-width="1.8"/><rect x="3178" y="423.2" width="12" height="4.0" fill="#EF4444" rx="1.5"/>
</svg>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("""<div class="zenith-nav-bar">
<div class="zenith-brand-group">
<div class="zenith-brand-logo">⚡</div>
<div class="zenith-brand-title">ZenithTrade</div>
<div class="zenith-version-badge">PRO SIMULATOR v2.0</div>
</div>
<div style="display: flex; align-items: center; gap: 14px;">
<span class="status-pill-green">● WebSocket Stream Live (14ms)</span>
<span style="color: #94A3B8; font-size: 0.82rem; font-weight: 600; cursor: pointer;">☀️ Light</span>
<span class="btn-enter-terminal">Enter Terminal ⚡</span>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("""<div class="zenith-ticker-bar">
<span class="ticker-head-label">LIVE ASSETS (CLICK TO FOCUS):</span>
<div class="ticker-chip active-blue">NIFTY 50 ₹24,527.79 <span style="color: #10B981;">+0.72%</span></div>
<div class="ticker-chip">BANKNIFTY ₹52,383.1 <span style="color: #10B981;">+1.14%</span></div>
<div class="ticker-chip">TCS ₹3,210.86 <span style="color: #10B981;">+1.25%</span></div>
<div class="ticker-chip">RELIANCE ₹2,143.09 <span style="color: #10B981;">+1.44%</span></div>
<div class="ticker-chip">INFY ₹1,565.47 <span style="color: #EF4444;">-0.45%</span></div>
<div class="ticker-chip">BHARTIARTL ₹557.6 <span style="color: #10B981;">+2.99%</span></div>
<div class="ticker-chip">HDFCBANK ₹1,650.00 <span style="color: #10B981;">+1.80%</span></div>
</div>""", unsafe_allow_html=True)

    col_l, col_center, col_r = st.columns([1, 1.25, 1])
    with col_center:
        st.markdown("""<div class="terminal-icon-badge">⚡</div>
<h1 class="terminal-title">Login to Terminal</h1>
<p class="terminal-sub">Zerodha Pro Trading Simulator • Real-time T+0 Sandbox</p>""", unsafe_allow_html=True)

        auth_tab_login, auth_tab_register = st.tabs(["Login", "Sign Up"])

        with auth_tab_login:
            if st.button("⚡ One-Click Demo Access (Amandeep)", use_container_width=True, key="demo_access_btn"):
                st.session_state.authenticated = True
                st.session_state.user_info = DEFAULT_USERS["demo@edufyi.com"]
                st.success("🎉 Access Granted! Entering Terminal...")
                st.rerun()

            with st.form("terminal_login_form", clear_on_submit=False):
                user_id = st.text_input("User ID / Client Code", value="DV0001", placeholder="e.g. DV0001")
                login_password = st.text_input("Password", value="demo123", type="password", placeholder="••••••••••••")
                keep_logged = st.checkbox("Keep active terminal session open", value=True)
                submit_login = st.form_submit_button("Login to Terminal →", use_container_width=True, type="primary")

                if submit_login:
                    st.session_state.authenticated = True
                    st.session_state.user_info = {
                        "name": "Amandeep Verma",
                        "email": user_id if "@" in user_id else "amandeepverma3001@gmail.com",
                        "org": "Bennett University",
                        "role": "Lead Architect"
                    }
                    st.success("🎉 Authentication successful! Loading terminal...")
                    st.rerun()

            with st.expander("ℹ️ View Demo Credentials"):
                st.markdown("""
                * **Client ID**: `DV0001` | Password: `demo123`
                * **Admin ID**: `ADMIN01` | Password: `admin123`
                """)

        with auth_tab_register:
            with st.form("terminal_register_form", clear_on_submit=True):
                reg_name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
                reg_email = st.text_input("Work Email / Client Code", placeholder="e.g. rahul@techcorp.com")
                reg_password = st.text_input("Choose Password", type="password", placeholder="Min 4 characters")
                submit_register = st.form_submit_button("Create Terminal Account →", use_container_width=True, type="primary")

                if submit_register:
                    registered_users = st.session_state.get("registered_users", {})
                    success, new_user, msg = register_new_user(reg_name, reg_email, "Bennett University", reg_password, registered_users)
                    if success:
                        if "registered_users" not in st.session_state:
                            st.session_state.registered_users = {}
                        st.session_state.registered_users[new_user["email"]] = new_user
                        st.session_state.authenticated = True
                        st.session_state.user_info = new_user
                        st.success(f"🎉 {msg} Loading terminal...")
                        st.rerun()
                    else:
                        st.error(msg)

    st.markdown("""<div class="zenith-footer-bar">
<div>© 2026 Zenith Trade • Independent Educational Paper Trading Simulator.</div>
<div><span style="color: #38BDF8; font-weight: 700;">$30,000 Sandbox Capital</span> &nbsp;•&nbsp; <span>GitHub</span></div>
</div>""", unsafe_allow_html=True)
