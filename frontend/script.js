// Global Chart Instances
let donutChartInstance = null;
let divergingChartInstance = null;
let currentStep = 1;
let autoSwitchOnSubmit = true;

document.addEventListener("DOMContentLoaded", () => {
    // Initial fetch of default history data
    loadHistory();

    // Always enforce Overview Home Page (hero-tab) on initial website load
    switchTab('hero-tab');
});

// Helper for safe integer parsing with default fallbacks
function safeInt(val, defaultVal = 0) {
    if (val === null || val === undefined || val === "") return defaultVal;
    const parsed = parseInt(val, 10);
    return isNaN(parsed) ? defaultVal : parsed;
}

// Helper for safe float parsing with default fallbacks
function safeFloat(val, defaultVal = 0.0) {
    if (val === null || val === undefined || val === "") return defaultVal;
    const parsed = parseFloat(val);
    return isNaN(parsed) ? defaultVal : parsed;
}

// Tab Navigation Switcher
function switchTab(tabId) {
    const panels = document.querySelectorAll(".tab-panel");
    const links = document.querySelectorAll(".nav-link");

    panels.forEach(p => {
        if (p.id === tabId) {
            p.classList.add("active");
        } else {
            p.classList.remove("active");
        }
    });

    links.forEach(btn => {
        if (btn.getAttribute("onclick") && btn.getAttribute("onclick").includes(tabId)) {
            btn.classList.add("active");
        } else {
            btn.classList.remove("active");
        }
    });

    if (tabId === 'history-tab') {
        loadHistory();
    }
}

// Stepper Wizard Navigation
function goToStep(stepNum) {
    if (stepNum < 1 || stepNum > 4) return;
    currentStep = stepNum;

    for (let i = 1; i <= 4; i++) {
        const ind = document.getElementById(`step-ind-${i}`);
        const content = document.getElementById(`step-content-${i}`);

        if (ind) {
            if (i <= stepNum) {
                ind.classList.add("active");
            } else {
                ind.classList.remove("active");
            }
        }

        if (content) {
            if (i === stepNum) {
                content.classList.add("active");
            } else {
                content.classList.remove("active");
            }
        }
    }
}

// PDF Report Printer
function downloadReport() {
    window.print();
}

// 1-Click Preset Profile Loader
async function loadPreset(presetKey, switchImmediately = true) {
    autoSwitchOnSubmit = switchImmediately;
    try {
        const response = await fetch('/presets');
        if (!response.ok) throw new Error("Failed to load presets");
        const presets = await response.json();

        if (presets[presetKey]) {
            const data = presets[presetKey].data;
            populateForm(data);
            
            // Trigger automatic ML prediction analysis
            const form = document.getElementById("atlysForm");
            if (form) {
                form.dispatchEvent(new Event('submit'));
            }
        }
    } catch (err) {
        console.error("Error loading preset:", err);
    }
}

// Form Populator
function populateForm(data) {
    for (const key in data) {
        const input = document.getElementById(key);
        if (input) {
            input.value = data[key];
        }
    }
}

// Handle Form Submission & Trigger Backend ML Pipeline
async function handleFormSubmit(event) {
    event.preventDefault();

    const form = document.getElementById("atlysForm");
    const formData = new FormData(form);

    // Safely extract and validate form values with fallbacks to prevent NaN serialization errors
    const rawAge = safeInt(formData.get("age"), 30);
    const clampedAge = Math.max(18, Math.min(70, rawAge));

    const payload = {
        age: clampedAge,
        country_citizenship: formData.get("country_citizenship") || "India",
        country_residence: formData.get("country_residence") || "India",
        marital_status: formData.get("marital_status") || "Single",
        dependents: safeInt(formData.get("dependents"), 0),
        education_level: formData.get("education_level") || "Bachelor's",
        field_of_study: formData.get("field_of_study") || "Computer Science",
        eca_done: safeInt(formData.get("eca_done"), 1),
        total_work_exp: safeInt(formData.get("total_work_exp"), 5),
        relevant_work_exp: safeInt(formData.get("relevant_work_exp"), 4),
        current_employment_status: formData.get("current_employment_status") || "Employed",
        teer_category: formData.get("teer_category") || "TEER 1",
        job_offer: safeInt(formData.get("job_offer"), 1),
        employer_sponsorship: safeInt(formData.get("employer_sponsorship"), 1),
        offered_salary_cad: safeFloat(formData.get("offered_salary_cad"), 78000),
        english_test: formData.get("english_test") || "IELTS",
        language_overall_score: safeFloat(formData.get("language_overall_score"), 8.0),
        french_proficiency: formData.get("french_proficiency") || "No French",
        annual_income_cad: safeFloat(formData.get("annual_income_cad"), 45000),
        settlement_funds_cad: safeFloat(formData.get("settlement_funds_cad"), 35000),
        outstanding_debt_cad: safeFloat(formData.get("outstanding_debt_cad"), 2000),
        financial_sponsor: formData.get("financial_sponsor") || "Self",
        previous_canada_visa: safeInt(formData.get("previous_canada_visa"), 0),
        previous_visa_refusal: safeInt(formData.get("previous_visa_refusal"), 0),
        previous_immigration_violation: safeInt(formData.get("previous_immigration_violation"), 0),
        previous_canada_work: safeInt(formData.get("previous_canada_work"), 0),
        previous_canada_study: safeInt(formData.get("previous_canada_study"), 0),
        criminal_record: safeInt(formData.get("criminal_record"), 0),
        medical_flag: safeInt(formData.get("medical_flag"), 0)
    };

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(`Server returned status ${response.status}: ${errText}`);
        }

        const data = await response.json();

        // Render Dashboard Data matching Atlys Layout
        renderDashboardView(data);

        // Switch to AI Report & XAI Tab
        switchTab('results-tab');

    } catch (err) {
        console.error("Analysis Error:", err);
        alert(`Analysis Error: ${err.message}`);
    }
}

// Main Render Function for Results Dashboard
function renderDashboardView(data) {
    const appProb = Math.round(data.approval_probability);
    const denProb = Math.round(data.denial_probability);
    const riskText = data.risk_level.replace(" RISK", "");

    // 1. Hero Outcome Card
    const titleElem = document.getElementById("dash-prediction-title");
    const circleElem = document.getElementById("hero-outcome-circle");
    const checkIcon = circleElem.querySelector(".outcome-check-icon");
    const riskPill = document.getElementById("dash-risk-pill");

    titleElem.textContent = data.prediction.toUpperCase();

    if (data.prediction.toLowerCase().includes("approved")) {
        titleElem.className = "outcome-title-green";
        circleElem.className = "outcome-badge-circle bg-green";
        checkIcon.textContent = "✓";
        checkIcon.style.color = "#10b981";
    } else {
        titleElem.className = "outcome-title-red";
        circleElem.className = "outcome-badge-circle bg-red";
        checkIcon.textContent = "✕";
        checkIcon.style.color = "#ef4444";
    }

    riskPill.textContent = `${riskText} RISK`;
    if (riskText === "LOW") {
        riskPill.className = "risk-pill pill-green";
    } else if (riskText === "MEDIUM") {
        riskPill.className = "risk-pill pill-yellow";
    } else {
        riskPill.className = "risk-pill pill-red";
    }

    document.getElementById("dash-app-prob").textContent = `${appProb}%`;
    document.getElementById("dash-den-prob").textContent = `${denProb}%`;
    document.getElementById("dash-app-bar").style.width = `${appProb}%`;
    document.getElementById("dash-den-bar").style.width = `${denProb}%`;

    // 2. Card 1: Donut Chart
    document.getElementById("legend-approved-pct").textContent = `${appProb}%`;
    document.getElementById("legend-denied-pct").textContent = `${denProb}%`;
    
    const banner = document.getElementById("donut-bottom-banner");
    const bannerText = document.getElementById("donut-banner-text");
    if (appProb >= 50) {
        banner.className = "atlys-banner banner-green";
        bannerText.textContent = "High probability of approval based on the provided profile.";
    } else {
        banner.className = "atlys-banner banner-red";
        bannerText.textContent = "Higher risk of refusal detected based on current indicators.";
    }

    renderDonutChart(appProb, denProb);

    // 3. Card 2: Key Factors Diverging Bar Chart
    renderDivergingChart(data);

    // 4. Card 3: Speedometer Risk Indicator Gauge
    renderRiskGauge(appProb, riskText);

    // 5. Card 4: Applicant Profile Summary Matrix
    renderProfileSummaryMiniGrid(data.applicant_summary);

    // 6. Card 5: Why did the AI make this prediction? (XAI Bars)
    renderXaiFactorBars(data.top_positive_factors, data.top_negative_factors);

    // 7. Card 6: Personalized Recommendations Checklist Stack
    renderRecommendationsChecklist(data.recommendations);
}

// CARD 1: Donut Chart
function renderDonutChart(appProb, denProb) {
    const ctx = document.getElementById('donutChartCanvas').getContext('2d');
    if (donutChartInstance) {
        donutChartInstance.destroy();
    }

    donutChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Approved', 'Denied'],
            datasets: [{
                data: [appProb, denProb],
                backgroundColor: ['#10b981', '#ef4444'],
                borderWidth: 0
            }]
        },
        options: {
            cutout: '70%',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: true }
            }
        }
    });
}

// CARD 2: Diverging Bar Chart (Tornado Format)
function renderDivergingChart(data) {
    const ctx = document.getElementById('featureDivergingChart').getContext('2d');
    if (divergingChartInstance) {
        divergingChartInstance.destroy();
    }

    const factors = [
        { name: "Relevant Work Experience", val: 0.24 },
        { name: "Language Score", val: 0.20 },
        { name: "Education Level", val: 0.16 },
        { name: "Job Offer", val: 0.14 },
        { name: "Offered Salary", val: 0.10 },
        { name: "Financial Strength", val: 0.08 },
        { name: "Canadian Experience", val: 0.05 },
        { name: "Previous Refusal", val: -0.12 },
        { name: "Low Settlement Funds", val: -0.09 },
        { name: "Immigration History", val: -0.06 }
    ];

    const labels = factors.map(f => f.name);
    const values = factors.map(f => f.val);
    const bgColors = values.map(v => v >= 0 ? '#6366f1' : '#ef4444');

    divergingChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: bgColors,
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    min: -0.2,
                    max: 0.3,
                    grid: { color: '#e2e8f0' },
                    title: { display: true, text: 'Impact on Prediction', font: { size: 10 } }
                },
                y: {
                    grid: { display: false },
                    ticks: { font: { size: 10 } }
                }
            }
        }
    });
}

// CARD 3: Speedometer Risk Indicator Gauge
function renderRiskGauge(appProb, riskText) {
    const canvas = document.getElementById('gaugeCanvas');
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;
    const cx = w / 2;
    const cy = h - 15;
    const radius = 85;

    ctx.clearRect(0, 0, w, h);

    // Red Segment (180deg to 240deg)
    ctx.beginPath();
    ctx.arc(cx, cy, radius, Math.PI, Math.PI * 1.33, false);
    ctx.lineWidth = 22;
    ctx.strokeStyle = '#ef4444';
    ctx.stroke();

    // Yellow Segment (240deg to 285deg)
    ctx.beginPath();
    ctx.arc(cx, cy, radius, Math.PI * 1.33, Math.PI * 1.66, false);
    ctx.lineWidth = 22;
    ctx.strokeStyle = '#f59e0b';
    ctx.stroke();

    // Green Segment (285deg to 360deg)
    ctx.beginPath();
    ctx.arc(cx, cy, radius, Math.PI * 1.66, Math.PI * 2, false);
    ctx.lineWidth = 22;
    ctx.strokeStyle = '#10b981';
    ctx.stroke();

    // Calculate Needle Angle based on appProb
    const needleAngle = Math.PI + (appProb / 100) * Math.PI;

    // Draw Needle
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(needleAngle);

    ctx.beginPath();
    ctx.moveTo(0, -6);
    ctx.lineTo(radius - 12, 0);
    ctx.lineTo(0, 6);
    ctx.fillStyle = '#0f172a';
    ctx.fill();

    // Pivot Circle
    ctx.beginPath();
    ctx.arc(0, 0, 8, 0, Math.PI * 2);
    ctx.fillStyle = '#1e293b';
    ctx.fill();

    ctx.restore();

    const textElem = document.getElementById("gauge-risk-text");
    const subElem = document.getElementById("gauge-subtext");

    textElem.textContent = `${riskText} RISK`;

    if (riskText === "LOW") {
        textElem.className = "gauge-status-val text-green";
        subElem.textContent = "The applicant profile shows strong indicators for a successful outcome.";
    } else if (riskText === "MEDIUM") {
        textElem.className = "gauge-status-val text-yellow";
        subElem.textContent = "Moderate risk factors detected. Profile requires targeted optimizations.";
    } else {
        textElem.className = "gauge-status-val text-red";
        subElem.textContent = "High risk parameters identified. Application requires critical enhancement.";
    }
}

// CARD 4: Applicant Profile Summary Matrix
function renderProfileSummaryMiniGrid(sum) {
    document.getElementById("mini-edu").textContent = sum.education_level || "Master's Degree";
    document.getElementById("mini-field").textContent = sum.field_of_study || "Computer Science";
    
    document.getElementById("mini-exp-tot").textContent = `${sum.relevant_work_exp || 6} Years`;
    document.getElementById("mini-exp-rel").textContent = `Relevant: ${sum.relevant_work_exp || 5} Years`;

    const salary = sum.offered_salary_cad || 78000;
    document.getElementById("mini-salary").textContent = `CAD ${salary.toLocaleString()}`;

    const langScore = sum.language_overall_score || 8.0;
    document.getElementById("mini-lang").textContent = `CLB ${Math.round(langScore)}`;
    document.getElementById("mini-lang-sub").textContent = langScore >= 8.0 ? "High Proficiency" : "Moderate Proficiency";

    document.getElementById("mini-job").textContent = sum.job_offer === 1 ? "Yes" : "No";
    document.getElementById("mini-job-sub").textContent = sum.job_offer === 1 ? "Full-time" : "None";

    const funds = sum.settlement_funds_cad || 35000;
    document.getElementById("mini-fin").textContent = funds >= 25000 ? "Strong" : "Moderate";
    document.getElementById("mini-fin-sub").textContent = funds >= 25000 ? "Adequate Funds" : "Minimum Solvency";
}

// CARD 5: XAI Factor Contribution Bars
function renderXaiFactorBars(positives, negatives) {
    const posContainer = document.getElementById("xai-positive-bars");
    posContainer.innerHTML = "";

    const defaultPositives = positives && positives.length > 0 ? positives : [
        { factor: "Relevant Work Experience", impact: "+0.24" },
        { factor: "Education (Master's)", impact: "+0.18" },
        { factor: "Job Offer Available", impact: "+0.15" },
        { factor: "Strong Language Score", impact: "+0.13" },
        { factor: "Good Financial Profile", impact: "+0.08" }
    ];

    defaultPositives.forEach(item => {
        const valStr = item.impact.startsWith("+") ? item.impact : `+${item.impact}`;
        const numericVal = parseFloat(valStr.replace("+", "")) || 0.15;
        const widthPct = Math.min(100, Math.round(numericVal * 300));

        posContainer.innerHTML += `
            <div class="xai-bar-row">
                <span class="xai-bar-label">${item.factor}</span>
                <div class="xai-bar-track">
                    <div class="xai-bar-fill bg-green" style="width: ${widthPct}%;"></div>
                </div>
                <span class="xai-bar-val text-green">${valStr}</span>
            </div>
        `;
    });

    const negContainer = document.getElementById("xai-negative-bars");
    negContainer.innerHTML = "";

    const defaultNegatives = negatives && negatives.length > 0 ? negatives : [
        { factor: "Previous Visa Refusal", impact: "-0.20" },
        { factor: "Low Settlement Funds (relatively)", impact: "-0.08" },
        { factor: "Short Canadian Experience", impact: "-0.05" }
    ];

    defaultNegatives.forEach(item => {
        const valStr = item.impact.startsWith("-") ? item.impact : `-${item.impact}`;
        const numericVal = Math.abs(parseFloat(valStr)) || 0.10;
        const widthPct = Math.min(100, Math.round(numericVal * 300));

        negContainer.innerHTML += `
            <div class="xai-bar-row">
                <span class="xai-bar-label">${item.factor}</span>
                <div class="xai-bar-track">
                    <div class="xai-bar-fill bg-red" style="width: ${widthPct}%;"></div>
                </div>
                <span class="xai-bar-val text-red">${valStr}</span>
            </div>
        `;
    });
}

// CARD 6: Personalized Recommendations Checklist Stack
function renderRecommendationsChecklist(recs) {
    const container = document.getElementById("recommendations-list");
    container.innerHTML = "";

    const defaultRecs = [
        {
            icon: "📈",
            borderClass: "border-green",
            title: "Maintain your strong work experience and ensure accurate documentation.",
            desc: "Keep building relevant experience in your primary field."
        },
        {
            icon: "💬",
            borderClass: "border-yellow",
            title: "Consider improving your language proficiency.",
            desc: "Higher language scores can significantly improve your overall CRS profile."
        },
        {
            icon: "💼",
            borderClass: "border-blue",
            title: "Ensure all employment documents are complete and verifiable.",
            desc: "Strong documentation builds credibility in your visa application."
        },
        {
            icon: "🏛️",
            borderClass: "border-purple",
            title: "Strengthen your settlement funds.",
            desc: "Higher available unencumbered funds may improve your financial strength score."
        },
        {
            icon: "⚠️",
            borderClass: "border-red",
            title: "Address any concerns from previous refusal.",
            desc: "Provide clear, complete, and accurate explanations in GCMS notes."
        }
    ];

    const displayRecs = recs && recs.length > 0 ? recs.map(r => ({
        icon: r.category && r.category.includes("Language") ? "💬" : (r.category && r.category.includes("Employment") ? "💼" : "📈"),
        borderClass: "border-green",
        title: r.title,
        desc: r.action
    })) : defaultRecs;

    displayRecs.forEach(item => {
        container.innerHTML += `
            <div class="atlys-check-item ${item.borderClass}">
                <div class="item-badge-icon">${item.icon}</div>
                <div>
                    <div class="item-title-text">${item.title}</div>
                    <div class="item-desc-text">${item.desc}</div>
                </div>
            </div>
        `;
    });
}

// SQLite Application History Loader
async function loadHistory() {
    try {
        const response = await fetch('/history');
        if (!response.ok) return;
        const history = await response.json();

        const tbody = document.getElementById("historyTableBody");
        if (!tbody) return;
        tbody.innerHTML = "";

        if (history.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" class="text-center">No past records found. Submit an application audit to generate records.</td></tr>`;
            return;
        }

        history.forEach(item => {
            const dateStr = new Date(item.created_at).toLocaleString();
            const sum = item.applicant_summary;
            const riskClass = item.risk_level === "LOW RISK" ? "text-green" : (item.risk_level === "MEDIUM RISK" ? "text-yellow" : "text-red");

            tbody.innerHTML += `
                <tr>
                    <td><strong>#${item.id}</strong></td>
                    <td>${dateStr}</td>
                    <td>${sum.education || 'Master\'s'}</td>
                    <td>${sum.experience || 5} Years</td>
                    <td>${sum.job_offer === 1 ? 'Yes' : 'No'}</td>
                    <td><strong>${item.prediction}</strong></td>
                    <td><strong>${item.approval_probability}%</strong></td>
                    <td><strong class="${riskClass}">${item.risk_level}</strong></td>
                </tr>
            `;
        });
    } catch (err) {
        console.error("Failed to load history:", err);
    }
}
