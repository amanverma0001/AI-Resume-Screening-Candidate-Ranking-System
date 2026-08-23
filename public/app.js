/**
 * Client Application Logic for AI Resume Screening System (Vercel Ready)
 */

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const selectSampleJd = document.getElementById("select-sample-jd");
    const textareaJd = document.getElementById("jd-text");
    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("file-input");
    const fileCountLabel = document.getElementById("file-count-label");
    
    const btnAnalyze = document.getElementById("btn-analyze");
    const btnSpinner = document.getElementById("btn-spinner");
    const btnText = document.getElementById("btn-text");
    const btnDemo = document.getElementById("btn-demo-load");
    
    const kpiSection = document.getElementById("kpi-section");
    const resultsCard = document.getElementById("results-card");
    const leaderboardBody = document.getElementById("leaderboard-body");
    
    const kpiTotal = document.getElementById("kpi-total");
    const kpiShortlisted = document.getElementById("kpi-shortlisted");
    const kpiAvg = document.getElementById("kpi-avg");
    const kpiTop = document.getElementById("kpi-top");
    
    const btnExportCsv = document.getElementById("btn-export-csv");
    const btnExportExcel = document.getElementById("btn-export-excel");
    
    const modalDetail = document.getElementById("modal-detail");
    const btnCloseModal = document.getElementById("btn-close-modal");
    
    // Sliders
    const sliderSkill = document.getElementById("weight-skill");
    const sliderSemantic = document.getElementById("weight-semantic");
    const sliderExp = document.getElementById("weight-exp");
    const sliderEdu = document.getElementById("weight-edu");
    const sliderThreshold = document.getElementById("filter-threshold");
    
    let uploadedFiles = [];
    let sampleResumesToInclude = [];
    let currentLeaderboard = [];
    let sampleDataCache = null;

    // Update Slider Labels
    const setupSliders = () => {
        sliderSkill.addEventListener("input", (e) => document.getElementById("val-skill").innerText = `${e.target.value}%`);
        sliderSemantic.addEventListener("input", (e) => document.getElementById("val-semantic").innerText = `${e.target.value}%`);
        sliderExp.addEventListener("input", (e) => document.getElementById("val-exp").innerText = `${e.target.value}%`);
        sliderEdu.addEventListener("input", (e) => document.getElementById("val-edu").innerText = `${e.target.value}%`);
        sliderThreshold.addEventListener("input", (e) => {
            document.getElementById("val-threshold").innerText = `${e.target.value}%`;
            filterLeaderboard();
        });
    };
    setupSliders();

    // Fetch Sample Data from API
    const loadSampleData = async () => {
        try {
            const res = await fetch("/api/sample-data");
            if (!res.ok) return;
            sampleDataCache = await res.json();
            
            if (sampleDataCache.job_descriptions) {
                sampleDataCache.job_descriptions.forEach(jd => {
                    const opt = document.createElement("option");
                    opt.value = jd.id;
                    opt.textContent = jd.title;
                    selectSampleJd.appendChild(opt);
                });
            }
        } catch (err) {
            console.warn("Sample data load notice:", err);
        }
    };
    loadSampleData();

    // Handle Sample JD Selection
    selectSampleJd.addEventListener("change", (e) => {
        const selectedId = e.target.value;
        if (!selectedId || !sampleDataCache) return;
        const found = sampleDataCache.job_descriptions.find(j => j.id === selectedId);
        if (found) {
            textareaJd.value = found.content;
        }
    });

    // File Drag & Drop
    dropzone.addEventListener("click", () => fileInput.click());
    
    dropzone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropzone.classList.add("dragover");
    });
    
    dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
    
    dropzone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropzone.classList.remove("dragover");
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFiles(e.dataTransfer.files);
        }
    });
    
    fileInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFiles(e.target.files);
        }
    });

    const handleFiles = (files) => {
        uploadedFiles = Array.from(files);
        fileCountLabel.innerHTML = `<strong>${uploadedFiles.length} file(s) selected:</strong> ` + 
            uploadedFiles.map(f => f.name).join(", ");
    };

    // 1-Click Demo Trigger
    btnDemo.addEventListener("click", () => {
        if (sampleDataCache && sampleDataCache.job_descriptions.length > 0) {
            const firstJd = sampleDataCache.job_descriptions[0];
            textareaJd.value = firstJd.content;
            selectSampleJd.value = firstJd.id;
        } else {
            textareaJd.value = `Senior Python Backend Developer (4+ Years Exp)
Key Requirements:
- Python, Django, FastAPI, Flask, REST APIs
- PostgreSQL, Redis, MongoDB, Docker, Kubernetes
- AWS (EC2, S3, RDS), CI/CD, Microservices architecture`;
        }

        if (sampleDataCache && sampleDataCache.sample_resumes) {
            sampleResumesToInclude = sampleDataCache.sample_resumes.map(r => r.filename);
            fileCountLabel.innerHTML = `⚡ <strong>10 Sample Resumes Selected</strong> (Senior Lead, Fullstack, AI Scientist, DevOps, etc.)`;
        }

        runAnalysis();
    });

    // Run Analysis Pipeline
    const runAnalysis = async () => {
        const jdText = textareaJd.value.trim();
        if (!jdText) {
            alert("Please enter or select a Job Description.");
            return;
        }

        if (uploadedFiles.length === 0 && sampleResumesToInclude.length === 0) {
            if (sampleDataCache && sampleDataCache.sample_resumes) {
                sampleResumesToInclude = sampleDataCache.sample_resumes.map(r => r.filename);
            } else {
                alert("Please upload at least one resume file or click 1-Click Live Demo.");
                return;
            }
        }

        // Show Spinner
        btnSpinner.classList.remove("hidden");
        btnText.innerText = "Analyzing Candidates & Ranking...";
        btnAnalyze.disabled = true;

        const formData = new FormData();
        formData.append("jd_text", jdText);

        const weights = {
            skill_weight: parseFloat(sliderSkill.value) / 100.0,
            semantic_weight: parseFloat(sliderSemantic.value) / 100.0,
            exp_weight: parseFloat(sliderExp.value) / 100.0,
            edu_weight: parseFloat(sliderEdu.value) / 100.0
        };
        formData.append("weights_json", JSON.stringify(weights));

        if (sampleResumesToInclude.length > 0) {
            formData.append("sample_resumes", sampleResumesToInclude.join(","));
        }

        for (let i = 0; i < uploadedFiles.length; i++) {
            formData.append("files", uploadedFiles[i]);
        }

        try {
            const res = await fetch("/api/analyze", {
                method: "POST",
                body: formData
            });

            if (!res.ok) {
                const errData = await res.json();
                alert(errData.detail || "Evaluation error occurred.");
                return;
            }

            const data = await res.json();
            currentLeaderboard = data.leaderboard || [];

            renderSummaryMetrics(data.summary);
            filterLeaderboard();

            kpiSection.classList.remove("hidden");
            resultsCard.classList.remove("hidden");
            resultsCard.scrollIntoView({ behavior: "smooth" });

        } catch (err) {
            alert("Connection failed: " + err.message);
        } finally {
            btnSpinner.classList.add("hidden");
            btnText.innerText = "🚀 Run AI Screening & Rank Candidates";
            btnAnalyze.disabled = false;
        }
    };

    btnAnalyze.addEventListener("click", runAnalysis);

    // Render KPI Metrics
    const renderSummaryMetrics = (summary) => {
        kpiTotal.innerText = summary.total_evaluated || 0;
        kpiShortlisted.innerText = summary.shortlisted_count || 0;
        kpiAvg.innerText = `${summary.avg_match_score || 0}%`;
        kpiTop.innerText = `${summary.top_match_score || 0}%`;
    };

    // Render Leaderboard Table with Filters
    const filterLeaderboard = () => {
        const threshold = parseFloat(sliderThreshold.value);
        leaderboardBody.innerHTML = "";

        const filtered = currentLeaderboard.filter(c => c.final_score >= threshold);

        if (filtered.length === 0) {
            leaderboardBody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 2rem; color: var(--text-muted);">No candidates match the selected threshold (${threshold}%). Try lowering the slider.</td></tr>`;
            return;
        }

        filtered.forEach((c) => {
            const tr = document.createElement("tr");
            
            let badgeClass = "badge-low";
            if (c.fit_status === "Strong Fit") badgeClass = "badge-strong";
            else if (c.fit_status === "Moderate Fit") badgeClass = "badge-moderate";

            const skillsMatchedBadges = c.matched_skills.slice(0, 4).map(s => 
                `<span class="badge badge-skill">${s}</span>`
            ).join(" ") + (c.matched_skills.length > 4 ? ` <span style="font-size:0.75rem; color: var(--text-muted);">+${c.matched_skills.length - 4} more</span>` : "");

            tr.innerHTML = `
                <td><strong>#${c.rank}</strong></td>
                <td><strong>${c.candidate_name}</strong><br/><span style="font-size:0.75rem; color: var(--text-muted);">${c.filename}</span></td>
                <td><strong style="font-size: 1rem; color: ${c.fit_color};">${c.final_score}%</strong></td>
                <td><span class="badge ${badgeClass}">${c.fit_status}</span></td>
                <td>${skillsMatchedBadges}</td>
                <td>${c.experience_years} Years</td>
                <td><button class="btn btn-secondary btn-detail" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;">Inspect</button></td>
            `;

            tr.querySelector(".btn-detail").addEventListener("click", (e) => {
                e.stopPropagation();
                openDetailModal(c);
            });

            leaderboardBody.appendChild(tr);
        });
    };

    // Open Inspector Modal
    const openDetailModal = (candidate) => {
        document.getElementById("modal-candidate-name").innerText = `Rank #${candidate.rank} — ${candidate.candidate_name}`;
        document.getElementById("modal-email").innerText = candidate.email;
        document.getElementById("modal-phone").innerText = candidate.phone;
        document.getElementById("modal-exp").innerText = `${candidate.experience_years} Years`;
        document.getElementById("modal-edu").innerText = candidate.education.join(", ");

        const matchedDiv = document.getElementById("modal-matched-skills");
        matchedDiv.innerHTML = candidate.matched_skills.map(s => `<span class="badge badge-skill">${s}</span>`).join(" ") || "None";

        const missingDiv = document.getElementById("modal-missing-skills");
        missingDiv.innerHTML = candidate.missing_skills.map(s => `<span class="badge badge-missing">${s}</span>`).join(" ") || "None";

        // Render Plotly Gauge Chart
        const gaugeData = [{
            type: "indicator",
            mode: "gauge+number",
            value: candidate.final_score,
            title: { text: "Overall Fit Match", font: { size: 14, color: "#F9FAFB" } },
            number: { suffix: "%", font: { color: candidate.fit_color, size: 24 } },
            gauge: {
                axis: { range: [0, 100], tickcolor: "#6B7280" },
                bar: { color: candidate.fit_color },
                bgcolor: "rgba(31, 41, 55, 0.5)",
                borderwidth: 1,
                bordercolor: "rgba(255,255,255,0.1)",
                steps: [
                    { range: [0, 45], color: "rgba(239, 68, 68, 0.2)" },
                    { range: [45, 70], color: "rgba(245, 158, 11, 0.2)" },
                    { range: [70, 100], color: "rgba(16, 185, 129, 0.2)" }
                ]
            }
        }];

        const gaugeLayout = {
            margin: { t: 30, b: 10, l: 30, r: 30 },
            paper_bgcolor: "rgba(0,0,0,0)",
            font: { color: "#F9FAFB", family: "Inter, sans-serif" }
        };

        Plotly.newPlot("plotly-gauge", gaugeData, gaugeLayout, { responsive: true, displayModeBar: false });

        modalDetail.classList.remove("hidden");
    };

    btnCloseModal.addEventListener("click", () => modalDetail.classList.add("hidden"));
    modalDetail.addEventListener("click", (e) => {
        if (e.target === modalDetail) modalDetail.classList.add("hidden");
    });

    // Handle CSV Export
    btnExportCsv.addEventListener("click", async () => {
        if (currentLeaderboard.length === 0) return;
        const formData = new FormData();
        formData.append("export_format", "csv");
        formData.append("leaderboard_json", JSON.stringify(currentLeaderboard));

        const res = await fetch("/api/export", { method: "POST", body: formData });
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "candidate_ranking_report.csv";
        a.click();
    });

    // Handle Excel Export
    btnExportExcel.addEventListener("click", async () => {
        if (currentLeaderboard.length === 0) return;
        const formData = new FormData();
        formData.append("export_format", "excel");
        formData.append("leaderboard_json", JSON.stringify(currentLeaderboard));

        const res = await fetch("/api/export", { method: "POST", body: formData });
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "candidate_ranking_report.xlsx";
        a.click();
    });
});
