document.addEventListener("DOMContentLoaded", () => {
    let currentJdProfile = null;
    let currentRankedList = [];
    let sampleJds = {};

    // Elements
    const labelModeDemo = document.getElementById("label-mode-demo");
    const labelModeCustom = document.getElementById("label-mode-custom");
    const customUploadSection = document.getElementById("custom-upload-section");
    const selectJdRole = document.getElementById("select-jd-role");
    const btnRunAnalysis = document.getElementById("btn-run-analysis");

    const sliderSkill = document.getElementById("slider-w-skill");
    const sliderExp = document.getElementById("slider-w-exp");
    const sliderEdu = document.getElementById("slider-w-edu");
    const sliderSem = document.getElementById("slider-w-sem");
    const sliderCutoff = document.getElementById("slider-cutoff");

    const labelSkill = document.getElementById("label-w-skill");
    const labelExp = document.getElementById("label-w-exp");
    const labelEdu = document.getElementById("label-w-edu");
    const labelSem = document.getElementById("label-w-sem");
    const labelCutoff = document.getElementById("label-cutoff");
    const labelChkCutoff = document.getElementById("label-chk-cutoff");
    const kpiSubCutoff = document.getElementById("kpi-sub-cutoff");

    const chkOnlyShortlisted = document.getElementById("chk-only-shortlisted");
    const inputSearch = document.getElementById("input-search");
    const tableBody = document.getElementById("table-body-leaderboard");

    // Accordions
    const accHeaderWeights = document.getElementById("acc-header-weights");
    const accBodyWeights = document.getElementById("acc-body-weights");
    const accArrowWeights = document.getElementById("acc-arrow-weights");

    const accHeaderJd = document.getElementById("acc-header-jd");
    const accBodyJd = document.getElementById("acc-body-jd");
    const accArrowJd = document.getElementById("acc-arrow-jd");

    // Charts references
    let chartLeaderboard = null;
    let chartCategory = null;

    // Toggle accordions
    const setupAccordion = (header, body, arrow) => {
        header.addEventListener("click", () => {
            const isOpen = body.classList.contains("open");
            if (isOpen) {
                body.classList.remove("open");
                arrow.textContent = "▼";
            } else {
                body.classList.add("open");
                arrow.textContent = "▲";
            }
        });
    };
    setupAccordion(accHeaderWeights, accBodyWeights, accArrowWeights);
    setupAccordion(accHeaderJd, accBodyJd, accArrowJd);

    // Mode Switch
    labelModeDemo.addEventListener("click", () => {
        labelModeDemo.classList.add("active");
        labelModeCustom.classList.remove("active");
        customUploadSection.classList.add("hidden");
        selectJdRole.parentElement.classList.remove("hidden");
        triggerAnalysis();
    });

    labelModeCustom.addEventListener("click", () => {
        labelModeCustom.classList.add("active");
        labelModeDemo.classList.remove("active");
        customUploadSection.classList.remove("hidden");
        selectJdRole.parentElement.classList.add("hidden");
    });

    // Sliders event listeners
    const bindSlider = (slider, label, isPercent = true) => {
        slider.addEventListener("input", (e) => {
            label.textContent = isPercent ? `${e.target.value}%` : e.target.value;
            if (slider === sliderCutoff) {
                labelChkCutoff.textContent = e.target.value;
                kpiSubCutoff.textContent = e.target.value;
                renderLeaderboardTable();
                updateKpiMetrics();
            } else {
                triggerAnalysis();
            }
        });
    };
    bindSlider(sliderSkill, labelSkill);
    bindSlider(sliderExp, labelExp);
    bindSlider(sliderEdu, labelEdu);
    bindSlider(sliderSem, labelSem);
    bindSlider(sliderCutoff, labelCutoff, false);

    // Role selector change
    selectJdRole.addEventListener("change", () => {
        triggerAnalysis();
    });

    // Tab navigation
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabContents = {
        "tab-leaderboard": document.getElementById("tab-content-leaderboard"),
        "tab-analytics": document.getElementById("tab-content-analytics"),
        "tab-inspector": document.getElementById("tab-content-inspector"),
        "tab-export": document.getElementById("tab-content-export")
    };

    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            tabButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            const target = btn.getAttribute("data-tab");
            Object.keys(tabContents).forEach(k => {
                if (k === target) {
                    tabContents[k].classList.remove("hidden");
                } else {
                    tabContents[k].classList.add("hidden");
                }
            });

            if (target === "tab-analytics") {
                renderAnalyticsCharts();
            } else if (target === "tab-inspector") {
                populateInspectorSelect();
            }
        });
    });

    // Fetch initial sample data and trigger first analysis
    fetch("/api/sample-data")
        .then(res => res.json())
        .then(data => {
            sampleJds = data.job_descriptions || {};
            triggerAnalysis();
        })
        .catch(err => {
            console.error("Failed to load sample data:", err);
            triggerAnalysis();
        });

    function triggerAnalysis() {
        const isDemo = labelModeDemo.classList.contains("active");
        const formData = new FormData();

        const skillW = parseFloat(sliderSkill.value) / 100.0;
        const expW = parseFloat(sliderExp.value) / 100.0;
        const eduW = parseFloat(sliderEdu.value) / 100.0;
        const semW = parseFloat(sliderSem.value) / 100.0;
        const cutoff = parseFloat(sliderCutoff.value);

        formData.append("skill_weight", skillW);
        formData.append("experience_weight", expW);
        formData.append("education_weight", eduW);
        formData.append("semantic_weight", semW);
        formData.append("cutoff_score", cutoff);

        if (isDemo) {
            formData.append("use_sample_resumes", "true");
            const selectedRole = selectJdRole.value;
            let jdContent = sampleJds[selectedRole];
            if (!jdContent) {
                const firstKey = Object.keys(sampleJds)[0];
                jdContent = sampleJds[firstKey] || "Senior Python Backend Developer with 4+ years of experience in Django, FastAPI, Docker, PostgreSQL.";
            }
            formData.append("jd_text", jdContent);
        } else {
            formData.append("use_sample_resumes", "false");
            const jdFileInput = document.getElementById("input-jd-file");
            const resumeFileInput = document.getElementById("input-resumes-files");

            if (!jdFileInput.files || jdFileInput.files.length === 0) {
                alert("Please select a Job Description (.txt) file.");
                return;
            }
            if (!resumeFileInput.files || resumeFileInput.files.length === 0) {
                alert("Please select at least one resume file.");
                return;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                formData.append("jd_text", e.target.result);
                for (let i = 0; i < resumeFileInput.files.length; i++) {
                    formData.append("files", resumeFileInput.files[i]);
                }
                sendAnalysisRequest(formData);
            };
            reader.readAsText(jdFileInput.files[0]);
            return;
        }

        sendAnalysisRequest(formData);
    }

    function sendAnalysisRequest(formData) {
        fetch("/api/analyze", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("Analysis Error: " + data.error);
                return;
            }
            currentJdProfile = data.jd_profile;
            currentRankedList = data.ranked_candidates || [];

            updateKpiMetrics();
            renderJdProfile(currentJdProfile);
            renderLeaderboardTable();
            populateInspectorSelect();
        })
        .catch(err => {
            console.error("API error:", err);
        });
    }

    btnRunAnalysis.addEventListener("click", () => {
        triggerAnalysis();
    });

    function updateKpiMetrics() {
        const cutoff = parseFloat(sliderCutoff.value);
        const total = currentRankedList.length;
        const shortlisted = currentRankedList.filter(c => c.final_score >= cutoff).length;
        const avg = total > 0 ? (currentRankedList.reduce((acc, c) => acc + c.final_score, 0) / total).toFixed(1) : "0.0";
        const top = total > 0 ? currentRankedList[0].candidate_name : "N/A";
        const topScore = total > 0 ? currentRankedList[0].final_score.toFixed(1) : "0.0";

        document.getElementById("kpi-total").textContent = total;
        document.getElementById("kpi-shortlisted").textContent = shortlisted;
        document.getElementById("kpi-avg").textContent = `${avg}%`;
        document.getElementById("kpi-top").textContent = top;
        document.getElementById("kpi-top-score").textContent = topScore;
    }

    function renderJdProfile(profile) {
        if (!profile) return;
        document.getElementById("jd-role-detected").textContent = profile.detected_role || "Software Developer";
        document.getElementById("jd-exp-detected").textContent = `${profile.required_experience_years || 4.0} Years`;
        document.getElementById("jd-skills-count").textContent = `${profile.required_skills ? profile.required_skills.length : 0} Skills`;

        const container = document.getElementById("jd-skills-tags-container");
        container.innerHTML = "";
        (profile.required_skills || []).forEach(skill => {
            const span = document.createElement("span");
            span.className = "header-pill";
            span.style.background = "rgba(99, 102, 241, 0.2)";
            span.style.border = "1px solid rgba(99, 102, 241, 0.4)";
            span.textContent = skill;
            container.appendChild(span);
        });
    }

    function renderLeaderboardTable() {
        const cutoff = parseFloat(sliderCutoff.value);
        const showOnlyShort = chkOnlyShortlisted.checked;
        const searchVal = inputSearch.value.trim().toLowerCase();

        tableBody.innerHTML = "";

        let list = [...currentRankedList];
        if (showOnlyShort) {
            list = list.filter(c => c.final_score >= cutoff);
        }

        if (searchVal) {
            list = list.filter(c => {
                const name = (c.candidate_name || "").toLowerCase();
                const email = (c.email || "").toLowerCase();
                const skills = (c.matched_skills || []).join(" ").toLowerCase();
                const edu = (c.education || []).join(" ").toLowerCase();
                return name.includes(searchVal) || email.includes(searchVal) || skills.includes(searchVal) || edu.includes(searchVal);
            });
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
    }

    chkOnlyShortlisted.addEventListener("change", renderLeaderboardTable);
    inputSearch.addEventListener("input", renderLeaderboardTable);

    function renderAnalyticsCharts() {
        const barCanvas = document.getElementById("chart-leaderboard-bar");
        const pieCanvas = document.getElementById("chart-category-dist");

        if (chartLeaderboard) chartLeaderboard.destroy();
        if (chartCategory) chartCategory.destroy();

        const top10 = currentRankedList.slice(0, 10);
        const names = top10.map(c => c.candidate_name);
        const scores = top10.map(c => c.final_score);

        barCanvas.innerHTML = `<canvas id="canvas-bar"></canvas>`;
        chartLeaderboard = new Chart(document.getElementById("canvas-bar"), {
            type: "bar",
            data: {
                labels: names,
                datasets: [{
                    label: "Match Score (%)",
                    data: scores,
                    backgroundColor: "rgba(99, 102, 241, 0.8)",
                    borderColor: "#6366F1",
                    borderWidth: 1,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: "#F8FAFC" } },
                    title: { display: true, text: "Top Candidate Match Scores", color: "#F8FAFC", font: { size: 14 } }
                },
                scales: {
                    x: { ticks: { color: "#94A3B8" }, grid: { color: "rgba(255,255,255,0.06)" } },
                    y: { ticks: { color: "#94A3B8" }, grid: { color: "rgba(255,255,255,0.06)" }, min: 0, max: 100 }
                }
            }
        });

        const strongFitCount = currentRankedList.filter(c => c.fit_status === "Strong Fit").length;
        const modFitCount = currentRankedList.filter(c => c.fit_status === "Moderate Fit").length;
        const lowFitCount = currentRankedList.filter(c => c.fit_status === "Low Fit").length;

        pieCanvas.innerHTML = `<canvas id="canvas-pie"></canvas>`;
        chartCategory = new Chart(document.getElementById("canvas-pie"), {
            type: "doughnut",
            data: {
                labels: ["Strong Fit (>=70%)", "Moderate Fit (50-69%)", "Low Fit (<50%)"],
                datasets: [{
                    data: [strongFitCount, modFitCount, lowFitCount],
                    backgroundColor: ["#10B981", "#F59E0B", "#EF4444"],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: "#F8FAFC" } },
                    title: { display: true, text: "Candidate Fit Tier Breakdown", color: "#F8FAFC", font: { size: 14 } }
                }
            }
        });
    }

    const inspectorSelect = document.getElementById("inspector-cand-select");
    function populateInspectorSelect() {
        inspectorSelect.innerHTML = "";
        currentRankedList.forEach(c => {
            const opt = document.createElement("option");
            opt.value = c.candidate_name;
            opt.textContent = `#${c.rank} - ${c.candidate_name} (${c.final_score}%)`;
            inspectorSelect.appendChild(opt);
        });
        renderInspectorDetails();
    }

    inspectorSelect.addEventListener("change", renderInspectorDetails);

    function renderInspectorDetails() {
        const selectedName = inspectorSelect.value;
        const cand = currentRankedList.find(c => c.candidate_name === selectedName);
        if (!cand) return;

        document.getElementById("insp-name").textContent = cand.candidate_name;
        document.getElementById("insp-email").textContent = cand.email;
        document.getElementById("insp-phone").textContent = cand.phone || "+91 0000000000";
        document.getElementById("insp-exp").textContent = `${cand.experience_years} Yrs Exp`;
        document.getElementById("insp-score").textContent = `${cand.final_score}%`;
        document.getElementById("insp-fit").textContent = cand.fit_status;

        const matchedCountSpan = document.getElementById("insp-matched-count");
        const missingCountSpan = document.getElementById("insp-missing-count");
        const matchedContainer = document.getElementById("insp-matched-tags");
        const missingContainer = document.getElementById("insp-missing-tags");

        matchedContainer.innerHTML = "";
        missingContainer.innerHTML = "";

        const matched = cand.matched_skills || [];
        const missing = cand.missing_skills || [];

        matchedCountSpan.textContent = matched.length;
        missingCountSpan.textContent = missing.length;

        matched.forEach(s => {
            const span = document.createElement("span");
            span.className = "badge-matched";
            span.textContent = s;
            matchedContainer.appendChild(span);
        });

        missing.forEach(s => {
            const span = document.createElement("span");
            span.className = "badge-missing";
            span.textContent = s;
            missingContainer.appendChild(span);
        });

        document.getElementById("insp-resume-text").textContent = cand.raw_text || "Parsed resume details ready.";
    }

    // Export handlers
    document.getElementById("btn-export-csv").addEventListener("click", () => {
        exportRankings("csv");
    });
    document.getElementById("btn-export-excel").addEventListener("click", () => {
        exportRankings("excel");
    });

    function exportRankings(format) {
        const formData = new FormData();
        formData.append("data", JSON.stringify(currentRankedList));
        formData.append("format", format);

        fetch("/api/export", {
            method: "POST",
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = format === "csv" ? "candidate_rankings.csv" : "candidate_rankings.xlsx";
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(err => alert("Export failed: " + err));
    }
});
