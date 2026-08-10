/**
 * AI Driven Immigration Decision Support System
 * Client JavaScript Orchestrator
 */

// Presets data cache
let presetCache = {};

// Fetch presets on page load
document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/presets")
        .then(res => res.json())
        .then(data => {
            presetCache = data;
        })
        .catch(err => console.log("Preset fetch status:", err));
});

/**
 * Load test preset data into applicant form
 */
function loadPreset(key) {
    if (!presetCache[key]) {
        console.warn("Preset key not found:", key);
        return;
    }

    const data = presetCache[key].data;

    // Prefill form fields
    for (const [field, val] of Object.entries(data)) {
        const el = document.getElementById(field);
        if (el) {
            el.value = val;
        }
    }

    // Auto-submit form to showcase immediate prediction result
    const form = document.getElementById("visaForm");
    if (form) {
        form.submit();
    }
}

/**
 * Real-Time Interactive What-If Simulator
 */
function runSimulation() {
    const bankVal = document.getElementById("simBank").value;
    const ieltsVal = document.getElementById("simIelts").value;
    const salaryVal = document.getElementById("simSalary").value;

    // Update slider label UI text
    document.getElementById("simBankVal").innerText = `$${Number(bankVal).toLocaleString()}`;
    document.getElementById("simIeltsVal").innerText = ieltsVal;
    document.getElementById("simSalaryVal").innerText = `$${Number(salaryVal).toLocaleString()}`;

    // Collect current form data
    const payload = {
        age: parseInt(document.getElementById("age").value || 30),
        salary: parseInt(salaryVal),
        experience: parseInt(document.getElementById("experience").value || 3),
        ielts_score: parseFloat(ieltsVal),
        bank_balance: parseInt(bankVal),
        education: document.getElementById("education").value,
        job_role: document.getElementById("job_role").value,
        sponsorship: document.getElementById("sponsorship").value,
        international_experience: document.getElementById("international_experience").value,
        criminal_record: document.getElementById("criminal_record").value,
        employment_type: document.getElementById("employment_type").value,
        country: document.getElementById("country").value
    };

    // Send AJAX prediction request
    fetch("/api/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(result => {
        if (result && result.approval_probability !== undefined) {
            const probEl = document.getElementById("simProbVal");
            probEl.innerText = `${result.approval_probability}%`;
            
            // Dynamic color toggle based on probability score
            if (result.approval_probability >= 50) {
                probEl.className = "text-emerald";
            } else {
                probEl.className = "text-rose";
            }
        }
    })
    .catch(err => console.error("Simulation error:", err));
}
