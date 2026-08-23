/**
 * Client Application Logic matching Streamlit app.py
 */

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const optDemo = document.getElementById("opt-demo");
    const optUpload = document.getElementById("opt-upload");
    const sectionDemo = document.getElementById("section-demo-controls");
    const sectionUpload = document.getElementById("section-upload-controls");
    const selectRole = document.getElementById("select-role");
    
    const toggleAdvanced = document.getElementById("toggle-advanced");
    const bodyAdvanced = document.getElementById("body-advanced");
    
    const sliderSkill = document.getElementById("w-skill");
    const sliderExp = document.getElementById("w-exp");
    const sliderEdu = document.getElementById("w-edu");
    const sliderCutoff = document.getElementById("slider-cutoff");
    
    const valSkill = document.getElementById("val-skill");
    const valExp = document.getElementById("val-exp");
    const valEdu = document.getElementById("val-edu");
    const valCutoff = document.getElementById("val-cutoff");
    const labelChkCutoff = document.getElementById("label-chk-cutoff");
    
    const kpiTotal = document.getElementById("kpi-total");
    const kpiShortlisted = document.getElementById("kpi-shortlisted");
    const kpiShortlistedSub = document.getElementById("kpi-shortlisted-sub");
    const kpiAvg = document.getElementById("kpi-avg");
    const kpiTop = document.getElementById("kpi-top");
    const kpiTopSub = document.getElementById("kpi-top-sub");
    
    const toggleJdReq = document.getElementById("toggle-jd-req");
    const bodyJdReq = document.getElementById("body-jd-req");
    const jdSkillsBadges = document.getElementById("jd-skills-badges");
    const jdMinExp = document.getElementById("jd-min-exp");
    const jdEdu = document.getElementById("jd-edu");
    
    const tabBtns = document.querySelectorAll(".tab-btn");
    const chkOnlyShortlisted = document.getElementById("chk-only-shortlisted");
    const inputSearch = document.getElementById("input-search");
    const tableBody = document.getElementById("table-body-leaderboard");
    
    const inspectorSelect = document.getElementById("inspector-cand-select");
    const inspName = document.getElementById("insp-name");
    const inspContact = document.getElementById("insp-contact");
    const inspEduExp = document.getElementById("insp-edu-exp");
    const inspFitTag = document.getElementById("insp-fit-tag");
    const inspMatched = document.getElementById("insp-matched-skills");
    const inspMissing = document.getElementById("insp-missing-skills");
    
    const toggleResumePaper = document.getElementById("toggle-resume-paper");
    const bodyResumePaper = document.getElementById("body-resume-paper");
    const resumePaperContent = document.getElementById("resume-paper-content");
    
    let currentCandidates = [];
    let currentJdProfile = null;
    let sampleDataCache = null;

    // Operation Controls Switch
    optDemo.addEventListener("click", () => {
        optDemo.classList.add("active");
        optUpload.classList.remove("active");
        optDemo.querySelector("input").checked = true;
        sectionDemo.classList.remove("hidden");
        sectionUpload.classList.add("hidden");
        runDemoAnalysis();
    });

    optUpload.addEventListener("click", () => {
        optUpload.classList.add("active");
        optDemo.classList.remove("active");
        optUpload.querySelector("input").checked = true;
        sectionUpload.classList.remove("hidden");
        sectionDemo.classList.add("hidden");
    });

    // Accordions
    toggleAdvanced.addEventListener("click", () => bodyAdvanced.classList.toggle("open"));
    toggleJdReq.addEventListener("click", () => bodyJdReq.classList.toggle("open"));
    toggleResumePaper.addEventListener("click", () => bodyResumePaper.classList.toggle("open"));

    // Sliders Event Handlers
    sliderSkill.addEventListener("input", (e) => {
        valSkill.innerText = `${e.target.value}%`;
        runDemoAnalysis();
    });
    sliderExp.addEventListener("input", (e) => {
        valExp.innerText = `${e.target.value}%`;
        runDemoAnalysis();
    });
    sliderEdu.addEventListener("input", (e) => {
        valEdu.innerText = `${e.target.value}%`;
        runDemoAnalysis();
    });
    sliderCutoff.addEventListener("input", (e) => {
        const val = e.target.value;
        valCutoff.innerText = val;
        labelChkCutoff.innerText = val;
        kpiShortlistedSub.innerText = `Match Score ≥ ${val}%`;
        renderDashboard();
    });

    // Role Select Handler
    selectRole.addEventListener("change", () => runDemoAnalysis());

    // Fetch Sample Data & Run Default Analysis
    const initData = async () => {
        try {
            const res = await fetch("/api/sample-data");
            if (!res.ok) return;
            sampleDataCache = await res.json();
            runDemoAnalysis();
        } catch (e) {
            console.warn("Init error:", e);
        }
    };
    initData();

    // Run Demo Analysis
    const runDemoAnalysis = async () => {
        if (!sampleDataCache) return;

        const roleTitle = selectRole.value;
        let jdContent = "";
        
        // Find matching JD
        if (sampleDataCache.job_descriptions) {
            const found = sampleDataCache.job_descriptions.find(j => 
                roleTitle.toLowerCase().includes(j.title.toLowerCase()) || j.title.toLowerCase().includes("python")
            );
            if (found) jdContent = found.content;
        }

        if (!jdContent) {
            jdContent = `Senior Python Backend Developer (4+ Years Exp)
Requirements: Python, Django, FastAPI, Flask, REST APIs, PostgreSQL, Redis, Docker, Kubernetes, AWS, Microservices`;
        }

        const sampleResumesList = sampleDataCache.sample_resumes ? 
            sampleDataCache.sample_resumes.map(r => r.filename).join(",") : "";

        const wSkillVal = parseFloat(sliderSkill.value);
        const wExpVal = parseFloat(sliderExp.value);
        const wEduVal = parseFloat(sliderEdu.value);
        const totalW = wSkillVal + wExpVal + wEduVal;
        
        const weights = {
            skill_weight: totalW > 0 ? wSkillVal / totalW : 0.6,
            semantic_weight: 0.0,
            exp_weight: totalW > 0 ? wExpVal / totalW : 0.2,
            edu_weight: totalW > 0 ? wEduVal / totalW : 0.2
        };

        const formData = new FormData();
        formData.append("jd_text", jdContent);
        formData.append("weights_json", JSON.stringify(weights));
        if (sampleResumesList) formData.append("sample_resumes", sampleResumesList);

        try {
            const res = await fetch("/api/analyze", { method: "POST", body: formData });
            if (!res.ok) return;
            const data = await res.json();
            
            currentCandidates = data.leaderboard || [];
            currentJdProfile = data.jd_profile || {};

            renderDashboard();

        } catch (err) {
            console.error("Analysis failed:", err);
        }
    };

    // Render Full Dashboard
    const renderDashboard = () => {
        if (currentCandidates.length === 0) return;

        const cutoff = parseFloat(sliderCutoff.value);
        const shortlisted = currentCandidates.filter(c => c.final_score >= cutoff);
        const total = currentCandidates.length;
        const avg = roundVal(currentCandidates.reduce((acc, c) => acc + c.final_score, 0) / total);
        const topCandidate = currentCandidates[0];

        // 1. KPI Cards
        kpiTotal.innerText = total;
        kpiShortlisted.innerText = shortlisted.length;
        kpiAvg.innerText = `${avg}%`;
        if (topCandidate) {
            kpiTop.innerText = topCandidate.candidate_name;
            kpiTopSub.innerText = `${topCandidate.final_score}% Match Score`;
        }

        // 2. JD Requirements Accordion
        if (currentJdProfile && currentJdProfile.required_skills) {
            jdSkillsBadges.innerHTML = currentJdProfile.required_skills.map(s => 
                `<span class="badge-matched">${s}</span>`
            ).join("");
            jdMinExp.innerText = currentJdProfile.min_experience_years || 4.0;
            jdEdu.innerText = currentJdProfile.required_education.length ? currentJdProfile.required_education.join(", ") : "B.Tech / MCA";
        }

        // 3. Render Table
        renderLeaderboardTable();

        // 4. Render Inspector Dropdown & Content
        renderInspector();

        // 5. Render Analytics Charts
        renderAnalyticsCharts();
    };

    const roundVal = (v) => Math.round(v * 10) / 10;

    // Leaderboard Table Search & Filtering
    const renderLeaderboardTable = () => {
        const cutoff = parseFloat(sliderCutoff.value);
        const query = inputSearch.value.trim().lowerCase ? inputSearch.value.trim().toLowerCase() : "";
        const onlyShortlisted = chkOnlyShortlisted.checked;

        tableBody.innerHTML = "";

        let list = currentCandidates;
        if (onlyShortlisted) {
            list = list.filter(c => c.final_score >= cutoff);
        }

        if (query) {
            list = list.filter(c => {
                const fullText = (
                    c.candidate_name + " " +
                    c.email + " " +
                    c.matched_skills.join(" ") + " " +
                    c.education.join(" ") + " " +
                    c.filename
                ).toLowerCase();
                return fullText.includes(query);
            });
        }

        if (list.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="9" style="text-align: center; padding: 2rem; color: #9CA3AF;">No candidates match your criteria. Try adjusting the search query or lowering the Cutoff Score in the sidebar.</td></tr>`;
            return;
        }

        list.forEach(c => {
            const isShortlisted = c.final_score >= cutoff;
            const shortTag = isShortlisted 
                ? `<span class="badge-shortlisted-true">✅ Shortlisted</span>` 
                : `<span class="badge-shortlisted-false">❌ Below Cutoff</span>`;

            const expStr = typeof c.experience_years === "number" ? `${c.experience_years.toFixed(1)} yrs` : `${c.experience_years} yrs`;
            const reqSkillsCount = (currentJdProfile && currentJdProfile.required_skills) ? currentJdProfile.required_skills.length : 31;

            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><strong>#${c.rank}</strong></td>
                <td><strong>${c.candidate_name}</strong></td>
                <td>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div class="table-score-bar-bg">
                            <div class="table-score-bar-fill" style="width: ${c.final_score}%;"></div>
                        </div>
                        <strong style="font-size: 0.88rem;">${c.final_score}%</strong>
                    </div>
                </td>
                <td>${shortTag}</td>
                <td><span class="fit-status-text">${c.fit_status}</span></td>
                <td>${c.matched_skills.length} / ${reqSkillsCount}</td>
                <td>${expStr}</td>
                <td>${c.education.join(", ")}</td>
                <td>${c.email}</td>
            `;
            tableBody.appendChild(tr);
        });
    };

    inputSearch.addEventListener("input", renderLeaderboardTable);
    chkOnlyShortlisted.addEventListener("change", renderLeaderboardTable);

    // Inspector Rendering
    const renderInspector = () => {
        inspectorSelect.innerHTML = "";
        currentCandidates.forEach((c, idx) => {
            const opt = document.createElement("option");
            opt.value = idx;
            opt.textContent = `Rank #${c.rank} - ${c.candidate_name} (${c.final_score}%)`;
            inspectorSelect.appendChild(opt);
        });

        if (currentCandidates.length > 0) {
            updateInspectorDetails(currentCandidates[0]);
        }
    };

    inspectorSelect.addEventListener("change", (e) => {
        const idx = parseInt(e.target.value);
        if (currentCandidates[idx]) {
            updateInspectorDetails(currentCandidates[idx]);
        }
    });

    const updateInspectorDetails = (c) => {
        inspName.innerText = c.candidate_name;
        inspContact.innerText = `📧 ${c.email} | 📱 ${c.phone} | 📄 ${c.filename}`;
        inspEduExp.innerText = `🎓 Education: ${c.education.join(", ")} | ⏳ Experience: ${c.experience_years} Years`;

        let fitClass = "fit-tag-low";
        if (c.fit_status === "Strong Fit") fitClass = "fit-tag-strong";
        else if (c.fit_status === "Moderate Fit") fitClass = "fit-tag-mod";
        inspFitTag.className = fitClass;
        inspFitTag.innerText = `${c.fit_status} (${c.final_score}%)`;

        inspMatched.innerHTML = c.matched_skills.map(s => `<span class="badge-matched">✅ ${s}</span>`).join("") || "None";
        inspMissing.innerHTML = c.missing_skills.map(s => `<span class="badge-missing">❌ ${s}</span>`).join("") || "None";

        // Plotly Gauge
        const gaugeData = [{
            type: "indicator",
            mode: "gauge+number",
            value: c.final_score,
            title: { text: "Overall Fit Score", font: { size: 14, color: "#F8FAFC" } },
            number: { suffix: "%", font: { color: c.fit_color || "#10B981", size: 26 } },
            gauge: {
                axis: { range: [0, 100], tickcolor: "#94A3B8" },
                bar: { color: c.fit_color || "#10B981" },
                bgcolor: "rgba(30, 41, 59, 0.5)",
                bordercolor: "rgba(255,255,255,0.1)",
                steps: [
                    { range: [0, 45], color: "rgba(239, 68, 68, 0.25)" },
                    { range: [45, 70], color: "rgba(245, 158, 11, 0.25)" },
                    { range: [70, 100], color: "rgba(16, 185, 129, 0.25)" }
                ]
            }
        }];
        Plotly.newPlot("insp-gauge-chart", gaugeData, { margin: { t: 30, b: 10, l: 30, r: 30 }, paper_bgcolor: "rgba(0,0,0,0)", font: { color: "#F8FAFC", family: "Plus Jakarta Sans" } }, { responsive: true, displayModeBar: false });

        // Plotly Breakdown Bar
        const breakdownData = [{
            x: [c.skill_score, c.exp_score, c.edu_score],
            y: ["Skills Overlap", "Experience Match", "Education Match"],
            type: "bar",
            orientation: "h",
            marker: { color: ["#6366F1", "#8B5CF6", "#0EA5E9"] }
        }];
        Plotly.newPlot("insp-breakdown-chart", breakdownData, { title: { text: "Score Breakdown", font: { size: 14, color: "#F8FAFC" } }, margin: { t: 30, b: 30, l: 110, r: 30 }, paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)", font: { color: "#F8FAFC", family: "Plus Jakarta Sans" } }, { responsive: true, displayModeBar: false });

        // Resume Paper Content
        renderResumePaperContent(c);
    };

    const renderResumePaperContent = (c) => {
        const lines = (c.raw_text || "").split("\n").filter(l => l.strip ? l.strip() : l.trim());
        let html = `
            <div style="border-bottom: 2px solid rgba(99, 102, 241, 0.3); padding-bottom: 14px; margin-bottom: 18px;">
                <h1 style="margin: 0; font-size: 1.7rem; font-weight: 800; color: #0F172A;">${c.candidate_name}</h1>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 6px;">
                    📧 ${c.email} &nbsp;|&nbsp; 📱 ${c.phone}
                </div>
                <div style="font-size: 0.85rem; color: #6366F1; font-weight: 600; margin-top: 8px;">
                    🎓 <b>Education:</b> ${c.education.join(", ")} &nbsp;|&nbsp; ⏳ <b>Total Experience:</b> ${c.experience_years} Years
                </div>
            </div>
            <div>
        `;

        lines.forEach(l => {
            const clean = l.trim();
            if (clean.isupper() && clean.length < 45) {
                html += `<h4 style="color: #6366F1; margin: 18px 0 8px 0; border-bottom: 2px solid rgba(99,102,241,0.25); padding-bottom: 4px; font-size: 0.95rem; text-transform: uppercase;">${clean}</h4>`;
            } else {
                html += `<p style="margin: 6px 0; line-height: 1.6; font-size: 0.9rem; color: #334155;">${clean}</p>`;
            }
        });

        html += `</div>`;
        resumePaperContent.innerHTML = html;
    };

    // Comparative Analytics Charts
    const renderAnalyticsCharts = () => {
        const names = currentCandidates.map(c => c.candidate_name).reverse();
        const scores = currentCandidates.map(c => c.final_score).reverse();
        const colors = currentCandidates.map(c => c.fit_color || "#10B981").reverse();

        const barData = [{
            x: scores,
            y: names,
            type: "bar",
            orientation: "h",
            marker: { color: colors }
        }];

        Plotly.newPlot("chart-leaderboard-bar", barData, {
            title: { text: "Candidate Ranking Scores (%)", font: { size: 14, color: "#F8FAFC" } },
            margin: { t: 40, b: 30, l: 120, r: 30 },
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "rgba(0,0,0,0)",
            font: { color: "#F8FAFC", family: "Plus Jakarta Sans" }
        }, { responsive: true, displayModeBar: false });

        if (currentCandidates[0] && currentCandidates[0].skills_by_category) {
            const cats = Object.keys(currentCandidates[0].skills_by_category);
            const counts = cats.map(k => currentCandidates[0].skills_by_category[k].length);

            const pieData = [{
                labels: cats,
                values: counts,
                type: "pie",
                hole: 0.4
            }];

            Plotly.newPlot("chart-category-dist", pieData, {
                title: { text: "Top Candidate Skill Distribution", font: { size: 14, color: "#F8FAFC" } },
                margin: { t: 40, b: 30, l: 30, r: 30 },
                paper_bgcolor: "rgba(0,0,0,0)",
                font: { color: "#F8FAFC", family: "Plus Jakarta Sans" }
            }, { responsive: true, displayModeBar: false });
        }
    };

    // Tabs Navigation
    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            tabBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            const target = btn.dataset.tab;
            document.getElementById("tab-content-ranking").classList.toggle("hidden", target !== "ranking");
            document.getElementById("tab-content-analytics").classList.toggle("hidden", target !== "analytics");
            document.getElementById("tab-content-inspector").classList.toggle("hidden", target !== "inspector");
            document.getElementById("tab-content-export").classList.toggle("hidden", target !== "export");

            if (target === "analytics") renderAnalyticsCharts();
        });
    });

    // Custom File Upload Run Button
    document.getElementById("btn-run-custom").addEventListener("click", async () => {
        const jdText = document.getElementById("custom-jd-text").value.trim();
        const filesInput = document.getElementById("custom-files-input");

        if (!jdText) {
            alert("Please paste a Job Description.");
            return;
        }

        const formData = new FormData();
        formData.append("jd_text", jdText);

        const wSkillVal = parseFloat(sliderSkill.value);
        const wExpVal = parseFloat(sliderExp.value);
        const wEduVal = parseFloat(sliderEdu.value);
        const totalW = wSkillVal + wExpVal + wEduVal;
        
        const weights = {
            skill_weight: totalW > 0 ? wSkillVal / totalW : 0.6,
            semantic_weight: 0.0,
            exp_weight: totalW > 0 ? wExpVal / totalW : 0.2,
            edu_weight: totalW > 0 ? wEduVal / totalW : 0.2
        };
        formData.append("weights_json", JSON.stringify(weights));

        if (filesInput.files && filesInput.files.length > 0) {
            for (let i = 0; i < filesInput.files.length; i++) {
                formData.append("files", filesInput.files[i]);
            }
        } else {
            alert("Please select at least one resume file.");
            return;
        }

        try {
            const res = await fetch("/api/analyze", { method: "POST", body: formData });
            if (!res.ok) return;
            const data = await res.json();
            currentCandidates = data.leaderboard || [];
            currentJdProfile = data.jd_profile || {};
            renderDashboard();
        } catch (err) {
            alert("Analysis failed: " + err.message);
        }
    });

    // Export Handlers
    const exportData = async (format, candidatesOnlyShortlisted = false) => {
        let payload = currentCandidates;
        if (candidatesOnlyShortlisted) {
            const cutoff = parseFloat(sliderCutoff.value);
            payload = payload.filter(c => c.final_score >= cutoff);
        }

        if (payload.length === 0) {
            alert("No candidates available for export.");
            return;
        }

        const formData = new FormData();
        formData.append("export_format", format);
        formData.append("leaderboard_json", JSON.stringify(payload));

        const res = await fetch("/api/export", { method: "POST", body: formData });
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `candidate_report_${candidatesOnlyShortlisted ? 'shortlisted' : 'all'}.${format === 'excel' ? 'xlsx' : format}`;
        a.click();
    };

    document.getElementById("btn-exp-all-csv").addEventListener("click", () => exportData("csv", false));
    document.getElementById("btn-exp-all-excel").addEventListener("click", () => exportData("excel", false));
    document.getElementById("btn-exp-all-pdf").addEventListener("click", () => exportData("pdf", false));

    document.getElementById("btn-exp-short-csv").addEventListener("click", () => exportData("csv", true));
    document.getElementById("btn-exp-short-excel").addEventListener("click", () => exportData("excel", true));
    document.getElementById("btn-exp-short-pdf").addEventListener("click", () => exportData("pdf", true));
});
