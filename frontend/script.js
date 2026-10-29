// Global Chart Instances
let donutChartInstance = null;
let divergingChartInstance = null;
let currentStep = 1;
let autoSwitchOnSubmit = true;
let currentSelectedCountry = "canada";

// Country-Specific UI Configuration
const COUNTRY_UI_CONFIGS = {
    canada: {
        flag: "",
        name: "Canada",
        currency: "CAD",
        currencySymbol: "$",
        skillLabel: "Occupation Skill / TEER Category *",
        skillOptions: [
            { val: "TEER 0", text: "TEER 0 (Management Occupations)" },
            { val: "TEER 1", text: "TEER 1 (Professional - IT, Eng, Health)" },
            { val: "TEER 2", text: "TEER 2 (Technical & Supervisory)" },
            { val: "TEER 3", text: "TEER 3 (Intermediate Skilled)" },
            { val: "TEER 4/5", text: "TEER 4/5 (Trades & General Labor)" }
        ],
        jobOfferLabel: "Valid Canadian Employment Offer *",
        sponsorLabel: "LMIA / Sponsorship Support *",
        sponsorEmployerText: "Canadian Employer",
        salaryLabel: "Offered Salary (Annual CAD $) *",
        annualIncomeLabel: "Current Annual Income (CAD $)",
        fundsLabel: "Available Settlement Funds (CAD $) *",
        fundsHelp: "IRCC LICO Single Applicant Requirement ≈ $14,690 CAD",
        debtLabel: "Outstanding Liabilities / Debt (CAD $)",
        prevVisaLabel: "Prior Canadian Visa Issued",
        prevWorkLabel: "Prior Canadian Work Experience",
        prevStudyLabel: "Prior Canadian Study Experience",
        secondLangLabel: "French Language Proficiency"
    },
    australia: {
        flag: "",
        name: "Australia",
        currency: "AUD",
        currencySymbol: "A$",
        skillLabel: "ANZSCO Occupation Skill Level *",
        skillOptions: [
            { val: "ANZSCO Skill Level 1", text: "ANZSCO Level 1 (Managers & Degree Professionals)" },
            { val: "ANZSCO Skill Level 2", text: "ANZSCO Level 2 (Technicians & Associate Professionals)" }
        ],
        jobOfferLabel: "Valid Australian Employment Offer *",
        sponsorLabel: "Australian State / Employer Nomination *",
        sponsorEmployerText: "Australian Sponsor",
        salaryLabel: "Offered Salary (Annual AUD A$) *",
        annualIncomeLabel: "Current Annual Income (AUD A$)",
        fundsLabel: "Available Settlement Funds (AUD A$) *",
        fundsHelp: "Home Affairs Settlement Reserve ≈ $20,000 AUD",
        debtLabel: "Outstanding Liabilities / Debt (AUD A$)",
        prevVisaLabel: "Prior Australian Visa Issued",
        prevWorkLabel: "Prior Australian Work Experience",
        prevStudyLabel: "Prior Australian Study Experience",
        secondLangLabel: "Community / Second Language Credential"
    },
    uk: {
        flag: "",
        name: "United Kingdom",
        currency: "GBP",
        currencySymbol: "£",
        skillLabel: "UK Job RQF Skill Level *",
        skillOptions: [
            { val: "RQF Level 6", text: "RQF Level 6 (Degree Level / Professional)" },
            { val: "RQF Level 7", text: "RQF Level 7 (Master's Level Specialist)" },
            { val: "RQF Level 8", text: "RQF Level 8 (Doctoral Level / Research)" },
            { val: "RQF Level 4", text: "RQF Level 4 (Higher National / Associate)" },
            { val: "RQF Level 3", text: "RQF Level 3 (A-Level Equivalent / Skilled Trade)" }
        ],
        jobOfferLabel: "Valid UK Job Offer *",
        sponsorLabel: "Certificate of Sponsorship (CoS) *",
        sponsorEmployerText: "UK Licensed Employer",
        salaryLabel: "Offered Salary (Annual GBP £) *",
        annualIncomeLabel: "Current Annual Income (GBP £)",
        fundsLabel: "Available Maintenance Funds (GBP £) *",
        fundsHelp: "Home Office Maintenance Requirement ≈ £1,270 GBP",
        debtLabel: "Outstanding Liabilities / Debt (GBP £)",
        prevVisaLabel: "Prior UK Visa Issued",
        prevWorkLabel: "Prior UK Work Experience",
        prevStudyLabel: "Prior UK Study Experience",
        secondLangLabel: "Second Language Competency (CEFR)"
    },
    germany: {
        flag: "",
        name: "Germany",
        currency: "EUR",
        currencySymbol: "€",
        skillLabel: "German Profession Classification *",
        skillOptions: [
            { val: "Standard Academic Profession", text: "Standard Academic Profession (Degree Required)" },
            { val: "MINT Shortage Occupation", text: "MINT Shortage Occupation (Math, IT, Engineering, Medicine)" }
        ],
        jobOfferLabel: "Valid German Employment Contract *",
        sponsorLabel: "German Employer / ZAV Approval *",
        sponsorEmployerText: "German Employer",
        salaryLabel: "Offered Salary (Annual EUR €) *",
        annualIncomeLabel: "Current Annual Income (EUR €)",
        fundsLabel: "Available Settlement Funds (EUR €) *",
        fundsHelp: "German Blocked Account / Living Fund ≈ €11,904 EUR",
        debtLabel: "Outstanding Liabilities / Debt (EUR €)",
        prevVisaLabel: "Prior German / Schengen Visa Issued",
        prevWorkLabel: "Prior German Work Experience",
        prevStudyLabel: "Prior German University Experience",
        secondLangLabel: "German Language Level (A1 - C1)"
    }
};

function selectDestinationCountry(countryKey) {
    currentSelectedCountry = countryKey.toLowerCase();
    
    // Update hidden form input
    const targetInput = document.getElementById("target_country");
    if (targetInput) targetInput.value = currentSelectedCountry;

    // Toggle active card styles across all galleries
    document.querySelectorAll(".motionsites-card, .country-pill-card").forEach(card => {
        card.classList.remove("active");
    });
    const activePill = document.getElementById(`country-pill-${currentSelectedCountry}`);
    if (activePill) activePill.classList.add("active");
    const activeHeroPill = document.getElementById(`country-hero-${currentSelectedCountry}`);
    if (activeHeroPill) activeHeroPill.classList.add("active");

    // Dynamically update form labels and dropdowns
    const cfg = COUNTRY_UI_CONFIGS[currentSelectedCountry];
    if (!cfg) return;

    // Update labels
    const lblTeer = document.getElementById("lbl_teer_category");
    if (lblTeer) lblTeer.textContent = cfg.skillLabel;

    const lblJobOffer = document.getElementById("lbl_job_offer");
    if (lblJobOffer) lblJobOffer.textContent = cfg.jobOfferLabel;

    const lblSponsor = document.getElementById("lbl_employer_sponsorship");
    if (lblSponsor) lblSponsor.textContent = cfg.sponsorLabel;

    const lblSalary = document.getElementById("lbl_offered_salary");
    if (lblSalary) lblSalary.textContent = cfg.salaryLabel;

    const lblAnnualInc = document.getElementById("lbl_annual_income");
    if (lblAnnualInc) lblAnnualInc.textContent = cfg.annualIncomeLabel;

    const lblFunds = document.getElementById("lbl_settlement_funds");
    if (lblFunds) lblFunds.textContent = cfg.fundsLabel;

    const helpFunds = document.getElementById("help_settlement_funds");
    if (helpFunds) helpFunds.textContent = cfg.fundsHelp;

    const lblDebt = document.getElementById("lbl_outstanding_debt");
    if (lblDebt) lblDebt.textContent = cfg.debtLabel;

    const lblPrevVisa = document.getElementById("lbl_prev_visa");
    if (lblPrevVisa) lblPrevVisa.textContent = cfg.prevVisaLabel;

    const lblPrevWork = document.getElementById("lbl_prev_work");
    if (lblPrevWork) lblPrevWork.textContent = cfg.prevWorkLabel;

    const lblPrevStudy = document.getElementById("lbl_prev_study");
    if (lblPrevStudy) lblPrevStudy.textContent = cfg.prevStudyLabel;

    const lblSecondLang = document.getElementById("lbl_second_language");
    if (lblSecondLang) lblSecondLang.textContent = cfg.secondLangLabel;

    const optEmployer = document.getElementById("opt_sponsor_employer");
    if (optEmployer) optEmployer.textContent = cfg.sponsorEmployerText;

    // Rebuild skill options dropdown
    const teerSelect = document.getElementById("teer_category");
    if (teerSelect && cfg.skillOptions) {
        teerSelect.innerHTML = "";
        cfg.skillOptions.forEach((opt, idx) => {
            const optElem = document.createElement("option");
            optElem.value = opt.val;
            optElem.textContent = opt.text;
            if (idx === 0) optElem.selected = true;
            teerSelect.appendChild(optElem);
        });
    }
}

function selectDestinationCountryAndGo(countryKey) {
    selectDestinationCountry(countryKey);
    switchTab('wizard-tab');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Theme Mode Switcher (Dark & Light Theme)
function setAppTheme(theme, save = true) {
    const root = document.documentElement;
    const body = document.body;
    const selectedTheme = (theme === 'light') ? 'light' : 'dark';

    root.setAttribute('data-theme', selectedTheme);
    body.setAttribute('data-theme', selectedTheme);

    if (save) {
        localStorage.setItem('canvisa_theme', selectedTheme);
    }

    // Update active state on drawer toggle buttons
    const btnDark = document.getElementById('themeBtnDark');
    const btnLight = document.getElementById('themeBtnLight');
    if (btnDark && btnLight) {
        if (selectedTheme === 'light') {
            btnDark.classList.remove('active');
            btnLight.classList.add('active');
        } else {
            btnLight.classList.remove('active');
            btnDark.classList.add('active');
        }
    }

    // Dispatch custom event for charts or dynamic components if needed
    window.dispatchEvent(new CustomEvent('canvisa_theme_changed', { detail: { theme: selectedTheme } }));
}

document.addEventListener("DOMContentLoaded", () => {
    // Restore user theme preference (supports ?theme=light or defaults to dark)
    const initialUrlParams = new URLSearchParams(window.location.search);
    const themeParam = initialUrlParams.get('theme');
    const savedTheme = (themeParam === 'light' || themeParam === 'dark') ? themeParam : (localStorage.getItem('canvisa_theme') || 'dark');
    setAppTheme(savedTheme, false);

    // Initial fetch of default history data
    loadHistory();

    // Check existing auth session
    initAuthSession();

    // Set default destination country
    selectDestinationCountry('canada');

    // Check for direct tab in URL (e.g. ?tab=results or #results-tab)
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get('tab');
    const hashTab = window.location.hash ? window.location.hash.replace('#', '') : null;
    const targetTab = tabParam ? (tabParam.endsWith('-tab') ? tabParam : `${tabParam}-tab`) : hashTab;

    if (targetTab && document.getElementById(targetTab)) {
        switchTab(targetTab);
        if (targetTab === 'results-tab' && !window.lastAnalyzedData) {
            loadPreset('moderate_profile', true);
        }
    } else {
        // Default to Overview Home Page (hero-tab)
        switchTab('hero-tab');
    }

    // Listen for language changes and re-render dashboard if results are active
    window.addEventListener('canvisa_language_changed', () => {
        if (window.lastAnalyzedData) {
            renderDashboardView(window.lastAnalyzedData);
        }
    });

    // Close profile dropdown when clicking outside
    document.addEventListener('click', (e) => {
        const wrapper = document.getElementById('userProfileWrapper');
        if (wrapper && !wrapper.contains(e.target)) {
            closeUserProfileDropdown();
        }
    });
});


// Trust Modules Information Modal (Interactive Module Details)
const TRUST_MODULES_DATA = {
    standards: {
        icon: "•",
        badge: "OFFICIAL CANADIAN STANDARDS",
        title: "Official Standards & NOC TEER Classification",
        summary: "How Immigration, Refugees and Citizenship Canada (IRCC) evaluates work visas and skill levels.",
        points: [
            {
                icon: "•",
                title: "Canada NOC 2021 TEER Categories",
                desc: "Canada classifies every occupation into 6 TEER levels (0 to 5) based on Training, Education, and Experience. Professional and managerial jobs (TEER 0, 1, and 2) have significantly higher visa approval odds."
            },
            {
                icon: "•",
                title: "Job Offer & LMIA Verification",
                desc: "Evaluates whether your Canadian job offer is backed by an approved Labour Market Impact Assessment (LMIA) or an active LMIA-exempt code confirming a genuine labor need."
            },
            {
                icon: "•",
                title: "LICO Settlement Funds Baseline",
                desc: "Checks your liquid bank savings against the mandatory Low Income Cut-Off (LICO) thresholds (e.g. $14,690+ CAD for a single applicant) to ensure financial self-sufficiency."
            },
            {
                icon: "•",
                title: "Language Benchmark (CLB 7+)",
                desc: "Translates IELTS / CELPIP scores into Canadian Language Benchmarks (CLB), requiring a minimum CLB 7.0 for skilled worker pathways."
            }
        ],
        actionText: "Check My Eligibility Now →",
        actionTab: "wizard-tab"
    },
    prediction: {
        icon: "•",
        badge: "INSTANT AI PREDICTION",
        title: "Instant Prediction & Factor Breakdown",
        summary: "Real-time AI analysis giving you immediate probability scores and actionable explanations.",
        points: [
            {
                icon: "•",
                title: "Sub-Second Inferences (<0.2 ms)",
                desc: "Our high-speed machine learning pipeline processes all 30 applicant profile attributes simultaneously, providing instant results without waiting."
            },
            {
                icon: "•",
                title: "Dual-Probability Percentage",
                desc: "Calculates precise percentage chances for both approval and refusal so you can see exactly where you stand."
            },
            {
                icon: "•",
                title: "Clear Strengths & Risk Penalties",
                desc: "Pinpoints the exact factors boosting your score (e.g. valid job offer, advanced degrees) and flags penalties (like missing ECA credential evaluation or prior refusals)."
            },
            {
                icon: "•",
                title: "Personalized Action Plan",
                desc: "Provides step-by-step suggestions on what to improve before submitting an actual visa application to maximize your chances."
            }
        ],
        actionText: "Try a Sample Case →",
        actionPreset: "strong_profile"
    },
    accuracy: {
        icon: "✓",
        badge: "VERIFIED STANDARDS",
        title: "Official Immigration Guidelines & Criteria",
        summary: "Evaluates your visa eligibility using official immigration standards and practical requirements.",
        points: [
            {
                icon: "•",
                title: "Official Immigration Criteria",
                desc: "Evaluates your education, work experience, language proficiency, and proof of funds directly against statutory benchmarks."
            },
            {
                icon: "•",
                title: "Clear Risk Levels",
                desc: "Categorizes your application into Low, Medium, or High Risk so you clearly understand your approval chances."
            },
            {
                icon: "•",
                title: "Fair & Objective Scoring",
                desc: "Evaluates every profile objectively and consistently without bias across nationalities, professions, and backgrounds."
            },
            {
                icon: "•",
                title: "Practical Next Steps",
                desc: "Highlights exactly which factors boost your score and what improvements (like higher IELTS or job offer) make the biggest difference."
            }
        ],
        actionText: "Start My Free Check →",
        actionTab: "wizard-tab"
    }
};

function openTrustModal(moduleKey) {
    const data = TRUST_MODULES_DATA[moduleKey];
    if (!data) return;

    const contentElem = document.getElementById("trustModalContent");
    if (!contentElem) return;

    const pointsHtml = data.points.map(pt => `
        <div class="trust-modal-point">
            <span class="trust-modal-point-icon">${pt.icon}</span>
            <div>
                <strong>${pt.title}</strong>
                <p>${pt.desc}</p>
            </div>
        </div>
    `).join("");

    let actionBtnHtml = "";
    if (data.actionTab) {
        actionBtnHtml = `<button class="btn-trust-modal-cta" onclick="closeTrustModal(); switchTab('${data.actionTab}');">${data.actionText}</button>`;
    } else if (data.actionPreset) {
        actionBtnHtml = `<button class="btn-trust-modal-cta" onclick="closeTrustModal(); loadPreset('${data.actionPreset}');">${data.actionText}</button>`;
    }

    contentElem.innerHTML = `
        <div class="trust-modal-header">
            <div class="trust-modal-icon">${data.icon}</div>
            <div>
                <span class="panel-section-badge">${data.badge}</span>
                <h3 class="trust-modal-title">${data.title}</h3>
                <p class="trust-modal-subtitle">${data.summary}</p>
            </div>
        </div>
        <div class="trust-modal-points">
            ${pointsHtml}
        </div>
        <div class="trust-modal-actions">
            <button class="btn-trust-modal-close" onclick="closeTrustModal()">Close</button>
            ${actionBtnHtml}
        </div>
    `;

    const overlay = document.getElementById("trustModalOverlay");
    if (overlay) {
        overlay.classList.add("active");
        document.body.style.overflow = "hidden";
    }
}

function closeTrustModal() {
    const overlay = document.getElementById("trustModalOverlay");
    if (overlay) {
        overlay.classList.remove("active");
        document.body.style.overflow = "";
    }
}

function openTermsModal() {
    const contentElem = document.getElementById("trustModalContent");
    if (!contentElem) return;

    contentElem.innerHTML = `
        <div class="trust-modal-header">
            <div class="trust-modal-icon">§</div>
            <div>
                <span class="panel-section-badge">LEGAL NOTICE & COMPLIANCE</span>
                <h3 class="trust-modal-title">Terms & Conditions of Academic Evaluation</h3>
                <p class="trust-modal-subtitle">Official Terms of Use for CanVisa AI Decision Support Engine</p>
            </div>
        </div>
        <div class="trust-modal-points">
            <div class="trust-modal-point">
                <span class="trust-modal-point-icon">•</span>
                <div>
                    <strong>Decision Support & Self-Assessment Tool</strong>
                    <p>CanVisa is an intelligent decision-support tool designed to help applicants assess their visa chances and understand requirements before applying.</p>
                </div>
            </div>
            <div class="trust-modal-point">
                <span class="trust-modal-point-icon">•</span>
                <div>
                    <strong>Advisory Guidance Only</strong>
                    <p>All score estimates and factor breakdowns are guidance indicators to help you plan. They do NOT constitute formal or legally binding immigration decisions. Official visa decisions are made exclusively by authorized government visa officers.</p>
                </div>
            </div>
            <div class="trust-modal-point">
                <span class="trust-modal-point-icon">•</span>
                <div>
                    <strong>Applicant Privacy & Synthetic Data Protection</strong>
                    <p>Applicant profiles processed in memory are analyzed in real time. Historical benchmarks are derived exclusively from synthesized and anonymized multi-country visa datasets.</p>
                </div>
            </div>
        </div>
        <div class="trust-modal-actions">
            <button class="btn-trust-modal-close" onclick="closeTrustModal()">Acknowledge & Close</button>
        </div>
    `;

    const overlay = document.getElementById("trustModalOverlay");
    if (overlay) {
        overlay.classList.add("active");
        document.body.style.overflow = "hidden";
    }
}

function handleTrustOverlayClick(e) {
    if (e.target && e.target.id === "trustModalOverlay") {
        closeTrustModal();
    }
}

// Authentication Modal & Session Management (Option 2)
function openLoginModal() {
    const modal = document.getElementById("loginModalOverlay");
    if (modal) {
        modal.classList.add("active");
        document.body.style.overflow = "hidden";
        setTimeout(() => {
            const emailInput = document.getElementById("authEmail");
            if (emailInput && !sessionStorage.getItem("canvisa_user")) emailInput.focus();
        }, 150);
    }
}

function closeLoginModal() {
    const modal = document.getElementById("loginModalOverlay");
    if (modal) {
        modal.classList.remove("active");
        document.body.style.overflow = "";
    }
}

function handleLoginOverlayClick(e) {
    if (e.target && e.target.id === "loginModalOverlay") {
        closeLoginModal();
    }
}

function initAuthSession() {
    let user = null;
    try {
        const stored = sessionStorage.getItem("canvisa_user") || localStorage.getItem("canvisa_user");
        if (stored) user = JSON.parse(stored);
    } catch (e) {
        console.warn("Failed to parse stored user:", e);
    }
    updateNavAuthUI(user);
    updateProfileCircleUI(user);
}

function updateNavAuthUI(user) {
    const authBtn = document.getElementById("navAuthBtn");
    const authIcon = document.getElementById("navAuthIcon");
    const authLabel = document.getElementById("navAuthLabel");
    if (authBtn && authLabel) {
        if (user) {
            authBtn.classList.add("logged-in");
            if (authIcon) authIcon.innerHTML = "G";
            authLabel.textContent = user.name || "Evaluator";
            authBtn.onclick = handleProfileLogout;
        } else {
            authBtn.classList.remove("logged-in");
            if (authIcon) authIcon.innerHTML = "";
            authLabel.textContent = "Sign In";
            authBtn.onclick = openLoginModal;
        }
    }

    // Also update drawer auth button if present
    const drawerBtn = document.getElementById("drawerAuthBtn");
    const drawerIcon = document.getElementById("drawerAuthIcon");
    const drawerLabel = document.getElementById("drawerAuthLabel");
    if (drawerBtn && drawerLabel) {
        if (user) {
            if (drawerIcon) drawerIcon.innerHTML = "";
            drawerLabel.textContent = "Log Out";
            drawerBtn.onclick = (e) => {
                e.preventDefault();
                handleProfileLogout();
            };
        } else {
            if (drawerIcon) drawerIcon.innerHTML = "";
            drawerLabel.textContent = "Sign In";
            drawerBtn.onclick = null;
            drawerBtn.href = "/login";
        }
    }

    updateProfileCircleUI(user);
}

// Update Taskbar Profile Circle and Session Dropdown UI
function updateProfileCircleUI(user) {
    const avatarInitial = document.getElementById("userAvatarInitial");
    const statusDot = document.getElementById("userStatusDot");
    const dropdownAvatar = document.getElementById("profileDropdownAvatar");
    const dropdownName = document.getElementById("profileDropdownName");
    const dropdownEmail = document.getElementById("profileDropdownEmail");
    const dropdownStatus = document.getElementById("profileDropdownStatus");
    const dropdownRole = document.getElementById("profileDropdownRole");
    const dropdownSessionId = document.getElementById("profileDropdownSessionId");
    const logoutBtn = document.getElementById("profileLogoutBtn");
    const logoutLabel = document.getElementById("profileLogoutLabel");
    const profileBtn = document.getElementById("userProfileBtn");

    if (!avatarInitial || !profileBtn) return;

    if (user && (user.name || user.email)) {
        const displayName = (user.name || user.email.split("@")[0] || "User").trim();
        const initial = displayName.charAt(0).toUpperCase() || "U";

        avatarInitial.textContent = initial;
        if (statusDot) {
            statusDot.classList.remove("offline");
            statusDot.title = "Session Status: Active (Online)";
        }
        if (dropdownAvatar) dropdownAvatar.textContent = initial;
        if (dropdownName) dropdownName.textContent = displayName;
        if (dropdownEmail) dropdownEmail.textContent = user.email || "applicant@canvisa.app";
        if (dropdownStatus) {
            dropdownStatus.textContent = "Active Session";
            dropdownStatus.className = "detail-badge";
        }
        if (dropdownRole) dropdownRole.textContent = user.role || "Verified Applicant";
        if (dropdownSessionId) {
            const shortToken = user.token ? String(user.token).slice(-6).toUpperCase() : "99A4";
            dropdownSessionId.textContent = "SYS-" + shortToken;
        }
        if (logoutLabel) logoutLabel.textContent = "Log Out";
        if (logoutBtn) {
            logoutBtn.onclick = handleProfileLogout;
            logoutBtn.className = "profile-btn-logout";
        }
        profileBtn.title = `Logged in as ${displayName} (${user.email || ''}) — Click for account details`;
    } else {
        avatarInitial.textContent = "G";
        if (statusDot) {
            statusDot.classList.add("offline");
            statusDot.title = "Session: Guest / Not Signed In";
        }
        if (dropdownAvatar) dropdownAvatar.textContent = "G";
        if (dropdownName) dropdownName.textContent = "Guest Evaluator";
        if (dropdownEmail) dropdownEmail.textContent = "Not logged in";
        if (dropdownStatus) {
            dropdownStatus.textContent = "Guest Mode";
            dropdownStatus.className = "detail-badge badge-guest";
        }
        if (dropdownRole) dropdownRole.textContent = "Standard Visitor";
        if (dropdownSessionId) dropdownSessionId.textContent = "GUEST-TEMP";
        if (logoutLabel) logoutLabel.textContent = "Sign In / Log In";
        if (logoutBtn) {
            logoutBtn.onclick = () => { window.location.href = "/login"; };
            logoutBtn.className = "profile-btn-logout profile-btn-login";
        }
        profileBtn.title = "Guest Session — Click to view account details or sign in";
    }
}

// Toggle Taskbar Profile Dropdown
function toggleUserProfileDropdown(event) {
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    const dropdown = document.getElementById("userProfileDropdown");
    const btn = document.getElementById("userProfileBtn");
    if (!dropdown) return;

    if (typeof closeLanguageDropdown === "function") {
        closeLanguageDropdown();
    }

    const isOpen = dropdown.classList.contains("open");
    if (isOpen) {
        dropdown.classList.remove("open");
        if (btn) btn.classList.remove("active");
    } else {
        dropdown.classList.add("open");
        if (btn) btn.classList.add("active");
    }
}

function closeUserProfileDropdown() {
    const dropdown = document.getElementById("userProfileDropdown");
    const btn = document.getElementById("userProfileBtn");
    if (dropdown) dropdown.classList.remove("open");
    if (btn) btn.classList.remove("active");
}

// User Logout Action
function handleProfileLogout() {
    if (confirm("Are you sure you want to log out of CanVisa?")) {
        sessionStorage.removeItem("canvisa_user");
        localStorage.removeItem("canvisa_user");
        closeUserProfileDropdown();
        updateNavAuthUI(null);
        window.location.href = "/login";
    }
}

function loginAsGuest() {
    const guestUser = {
        name: "Jury Evaluator",
        email: "panel.guest@academic-review.edu",
        role: "Academic Reviewer",
        token: "demo_guest_jwt_" + Date.now()
    };
    sessionStorage.setItem("canvisa_user", JSON.stringify(guestUser));
    updateNavAuthUI(guestUser);
    closeLoginModal();
    // Smooth transition into assessment
    switchTab('wizard-tab');
}

function handleAuthSubmit(e) {
    e.preventDefault();
    const email = document.getElementById("authEmail").value.trim();
    const remember = document.getElementById("authRemember").checked;

    const authUser = {
        name: email.split("@")[0].replace(".", " "),
        email: email,
        role: "Evaluator",
        token: "auth_token_" + Date.now()
    };

    if (remember) {
        localStorage.setItem("canvisa_user", JSON.stringify(authUser));
    }
    sessionStorage.setItem("canvisa_user", JSON.stringify(authUser));
    updateNavAuthUI(authUser);
    closeLoginModal();
    switchTab('wizard-tab');
}

function logoutUser() {
    handleProfileLogout();
}

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

// Sidebar Drawer (Corner Sliding Menu) Controls
function toggleSidebarDrawer() {
    const drawer = document.getElementById("sidebarDrawer");
    const overlay = document.getElementById("sidebarDrawerOverlay");
    if (!drawer) return;
    const isOpen = drawer.classList.contains("active");
    if (isOpen) {
        closeSidebarDrawer();
    } else {
        openSidebarDrawer();
    }
}

function openSidebarDrawer() {
    const drawer = document.getElementById("sidebarDrawer");
    const overlay = document.getElementById("sidebarDrawerOverlay");
    if (drawer) drawer.classList.add("active");
    if (overlay) overlay.classList.add("active");
    document.body.style.overflow = "hidden";
}

function closeSidebarDrawer() {
    const drawer = document.getElementById("sidebarDrawer");
    const overlay = document.getElementById("sidebarDrawerOverlay");
    if (drawer) drawer.classList.remove("active");
    if (overlay) overlay.classList.remove("active");
    document.body.style.overflow = "";
}

function switchTabFromDrawer(tabId) {
    switchTab(tabId);
    closeSidebarDrawer();
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

    // Update active drawer nav item
    document.querySelectorAll(".drawer-nav-item").forEach(item => {
        item.classList.remove("active");
    });
    const drawerActive = document.querySelector(`.drawer-nav-item[onclick*="${tabId}"]`);
    if (drawerActive) drawerActive.classList.add("active");

    // Smooth scroll to top of page upon tab switch
    window.scrollTo({ top: 0, behavior: "smooth" });

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

// Fullscreen Mode Toggle Helper
function toggleFullScreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {
            console.warn(`Fullscreen error: ${err.message}`);
        });
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
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

// WHAT-IF SIMULATOR ENGINE
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
        medical_flag: safeInt(formData.get("medical_flag"), 0),
        target_country: formData.get("target_country") || currentSelectedCountry || "canada",
        occupation_skill_level: formData.get("teer_category") || "TEER 1"
    };

    const submitBtn = document.getElementById("btnCalculateChances") || form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn ? submitBtn.innerHTML : "Calculate My Visa Approval Chances";

    try {
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `⏳ Analyzing Profile with AI...`;
            submitBtn.style.opacity = "0.75";
        }

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
        renderDashboardView(data);
        switchTab('results-tab');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
        console.error("Analysis Error:", err);
        alert(`Analysis Error: ${err.message}`);
    } finally {
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
            submitBtn.style.opacity = "";
        }
    }
}

// Main Render Function for Results Dashboard
function renderDashboardView(data) {
    const appProb = Math.round(data.approval_probability);
    const denProb = Math.round(data.denial_probability);
    const riskText = data.risk_level.replace(" RISK", "");

    window.lastAnalyzedData = data;

    // 0. Country Header Details & Dossier Meta
    const cName = data.country_name || "Canada";
    const cFlag = data.country_flag || "🍁";
    
    const caseTitleElem = document.getElementById("dash-case-title");
    if (caseTitleElem) {
        caseTitleElem.textContent = `${cFlag} ${cName.toUpperCase()} • DECISION SUPPORT`;
    }
    const countrySubElem = document.getElementById("dash-country-subtitle");
    if (countrySubElem) {
        countrySubElem.textContent = `Evaluated against official ${cName} immigration standards and dedicated AI models.`;
    }

    // Case ID and Date
    const caseIdElem = document.getElementById("dash-case-id");
    if (caseIdElem) {
        caseIdElem.textContent = data.id ? `CV-${String(data.id).padStart(5, '0')}` : "CV-00127";
    }
    const caseDateElem = document.getElementById("dash-case-date");
    if (caseDateElem) {
        caseDateElem.textContent = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }

    // 1. Hero Outcome Card (Left Column)
    const titleElem = document.getElementById("dash-prediction-title");
    const riskPill = document.getElementById("dash-risk-pill");
    const descElem = document.getElementById("dash-outcome-desc");
    const isApproved = data.prediction.toLowerCase().includes("approved");

    if (titleElem) {
        titleElem.textContent = isApproved ? "Likely Approved" : "Likely Denied";
        titleElem.className = isApproved ? "outcome-headline outcome-title-green" : "outcome-headline outcome-title-red";
    }

    if (riskPill) {
        if (riskText === "LOW") {
            riskPill.innerHTML = '<span class="risk-dot"></span> LOW RISK';
            riskPill.className = "risk-pill pill-green";
        } else if (riskText === "MEDIUM") {
            riskPill.innerHTML = '<span class="risk-dot"></span> MEDIUM RISK';
            riskPill.className = "risk-pill pill-yellow";
        } else {
            riskPill.innerHTML = '<span class="risk-dot"></span> HIGH RISK';
            riskPill.className = "risk-pill pill-red";
        }
    }

    if (descElem) {
        if (isApproved) {
            descElem.textContent = "The model leans toward approval for the submitted profile. Inspect the evidence signals and suggested checks before treating this as a plan.";
        } else {
            descElem.textContent = "The model indicates material refusal risks under current immigration thresholds. Review the limiting factors and action checklist below to improve eligibility.";
        }
    }

    // 2. Probability Card (Right Column)
    const appProbElem = document.getElementById("dash-app-prob");
    if (appProbElem) appProbElem.textContent = `${appProb}%`;

    const refinedProbElem = document.getElementById("dash-refined-prob");
    if (refinedProbElem) refinedProbElem.textContent = `${appProb}%`;

    const bandTextElem = document.getElementById("dash-band-text");
    if (bandTextElem) bandTextElem.textContent = `${riskText} RISK`;

    // Probability Scale Bar & Thumb
    const scaleMarker = document.getElementById("dash-scale-marker");
    if (scaleMarker) scaleMarker.textContent = `${appProb}%`;

    const appFill = document.getElementById("dash-app-bar");
    if (appFill) appFill.style.width = `${appProb}%`;

    const scaleThumb = document.getElementById("dash-scale-thumb");
    if (scaleThumb) scaleThumb.style.left = `${appProb}%`;

    // 3. Mini Factor Signals (in Right Probability Card)
    renderFactorSignalsMini(data);

    // 4. Intelligence Meta Grid (4 Cards)
    const metaFlag = document.getElementById("meta-country-flag");
    const metaName = document.getElementById("meta-country-name");
    const metaCat = document.getElementById("meta-visa-category");
    const metaModel = document.getElementById("meta-model-name");
    const metaGenDate = document.getElementById("meta-gen-date");

    if (metaFlag) metaFlag.textContent = cFlag;
    if (metaName) metaName.textContent = cName;
    if (metaCat) {
        const catMap = {
            canada: "NOC 2021 • MIA / PR",
            australia: "SUBCLASS 189 • ANZSCO",
            uk: "SKILLED WORKER • RQF",
            germany: "EU BLUE CARD • MINT"
        };
        metaCat.textContent = catMap[data.target_country] || "SKILLED VISA CATEGORY";
    }
    if (metaModel) metaModel.textContent = data.model_used || "Random Forest Classifier • CanVisa prototype";
    if (metaGenDate) metaGenDate.textContent = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

    // 5. Explainability Workspace: Diverging SHAP Bars & Global Chart
    renderShapDivergingBars(data);
    renderDivergingChart(data);

    // 6. Profile Audit Matrix & Collapsible Accordions
    renderInputAudit(data.applicant_summary, cName);

    // 7. Personalized Action Plan Checklist
    renderActionPlan(data.recommendations);
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
            devicePixelRatio: Math.max(2, window.devicePixelRatio || 2),
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
    const bgColors = values.map(v => v >= 0 ? '#4f46e5' : '#dc2626');

    divergingChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: bgColors,
                borderRadius: 5,
                barThickness: 12
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            devicePixelRatio: Math.max(2, window.devicePixelRatio || 2),
            plugins: {
                legend: { display: false },
                tooltip: {
                    titleFont: { family: "'Plus Jakarta Sans', sans-serif", size: 12, weight: '700' },
                    bodyFont: { family: "'Plus Jakarta Sans', sans-serif", size: 11, weight: '600' }
                }
            },
            scales: {
                x: {
                    min: -0.2,
                    max: 0.3,
                    grid: { color: '#e2e8f0', drawBorder: false },
                    ticks: {
                        color: '#334155',
                        font: { family: "'Plus Jakarta Sans', sans-serif", size: 11, weight: '600' }
                    },
                    title: {
                        display: true,
                        text: 'Impact on Prediction',
                        color: '#0f172a',
                        font: { family: "'Plus Jakarta Sans', sans-serif", size: 11, weight: '800' }
                    }
                },
                y: {
                    grid: { display: false },
                    ticks: {
                        color: '#0f172a',
                        font: { family: "'Plus Jakarta Sans', sans-serif", size: 11, weight: '700' }
                    }
                }
            }
        }
    });
}

// CARD 3: Speedometer Risk Indicator Gauge
function renderRiskGauge(appProb, riskText) {
    const canvas = document.getElementById('gaugeCanvas');
    const dpr = Math.max(2, window.devicePixelRatio || 2);
    
    // High DPI Canvas crispness scaling
    canvas.width = 240 * dpr;
    canvas.height = 130 * dpr;
    canvas.style.width = '240px';
    canvas.style.height = '130px';

    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);

    const w = 240;
    const h = 130;
    const cx = w / 2;
    const cy = h - 15;
    const radius = 85;

    ctx.clearRect(0, 0, w, h);

    // Red Segment (180deg to 240deg)
    ctx.beginPath();
    ctx.arc(cx, cy, radius, Math.PI, Math.PI * 1.33, false);
    ctx.lineWidth = 20;
    ctx.strokeStyle = '#ef4444';
    ctx.stroke();

    // Yellow Segment (240deg to 285deg)
    ctx.beginPath();
    ctx.arc(cx, cy, radius, Math.PI * 1.33, Math.PI * 1.66, false);
    ctx.lineWidth = 20;
    ctx.strokeStyle = '#f59e0b';
    ctx.stroke();

    // Green Segment (285deg to 360deg)
    ctx.beginPath();
    ctx.arc(cx, cy, radius, Math.PI * 1.66, Math.PI * 2, false);
    ctx.lineWidth = 20;
    ctx.strokeStyle = '#10b981';
    ctx.stroke();

    // Calculate Needle Angle based on appProb
    const needleAngle = Math.PI + (appProb / 100) * Math.PI;

    // Draw Needle
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(needleAngle);

    ctx.beginPath();
    ctx.moveTo(0, -5);
    ctx.lineTo(radius - 12, 0);
    ctx.lineTo(0, 5);
    ctx.fillStyle = '#0f172a';
    ctx.fill();

    // Pivot Circle
    ctx.beginPath();
    ctx.arc(0, 0, 7, 0, Math.PI * 2);
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

// MINI FACTOR SIGNALS (Inside Right Outcome Probability Card)
function renderFactorSignalsMini(data) {
    const container = document.getElementById("prob-factor-signals");
    if (!container) return;
    container.innerHTML = "";

    const positives = (data.top_positive_factors && data.top_positive_factors.length > 0)
        ? data.top_positive_factors
        : [
            { factor: "Language Overall Score", impact: "+0.194" },
            { factor: "Annual Salary (USD)", impact: "+0.135" },
            { factor: "Job Offer Supported", impact: "+0.098" }
        ];

    const negatives = (data.top_negative_factors && data.top_negative_factors.length > 0)
        ? data.top_negative_factors
        : [
            { factor: "Settlement Funds USD", impact: "-0.103" },
            { factor: "Previous Visa Refusal", impact: "-0.080" }
        ];

    // Combine top signals (up to 4 items)
    const combined = [];
    if (positives[0]) combined.push({ ...positives[0], isPos: true });
    if (negatives[0]) combined.push({ ...negatives[0], isPos: false });
    if (positives[1]) combined.push({ ...positives[1], isPos: true });
    if (negatives[1]) combined.push({ ...negatives[1], isPos: false });

    combined.forEach(item => {
        const valStr = String(item.impact || "+0.15");
        const isPos = item.isPos || !valStr.startsWith("-");
        const cleanVal = parseFloat(valStr.replace(/[^0-9.-]/g, "")) || 0.15;
        const widthPct = Math.min(100, Math.max(15, Math.round(Math.abs(cleanVal) * 350)));

        container.innerHTML += `
            <div class="factor-signal-row">
                <span class="factor-signal-name" title="${item.factor}">${item.factor}</span>
                <div class="factor-signal-bar-track">
                    <div class="factor-signal-bar-fill ${isPos ? 'fill-pos' : 'fill-neg'}" style="width: ${widthPct}%;"></div>
                </div>
                <span class="factor-signal-val ${isPos ? 'val-pos' : 'val-neg'}">${valStr.startsWith('+') || valStr.startsWith('-') ? valStr : (isPos ? '+' + valStr : '-' + valStr)}</span>
            </div>
        `;
    });
}

// EXPLAINABILITY WORKSPACE: Diverging Case-Specific SHAP Bars
function renderShapDivergingBars(data) {
    const container = document.getElementById("shap-diverging-list");
    if (!container) return;
    container.innerHTML = "";

    const positives = (data.top_positive_factors && data.top_positive_factors.length > 0)
        ? data.top_positive_factors
        : [
            { factor: "language overall score", impact: "+0.194" },
            { factor: "annual salary (usd)", impact: "+0.135" },
            { factor: "job_offer", impact: "+0.098" }
        ];

    const negatives = (data.top_negative_factors && data.top_negative_factors.length > 0)
        ? data.top_negative_factors
        : [
            { factor: "settlement funds usd", impact: "-0.103" },
            { factor: "previous visa refusal", impact: "-0.103" }
        ];

    const allFactors = [];
    positives.forEach(p => allFactors.push({ ...p, isPos: true }));
    negatives.forEach(n => allFactors.push({ ...n, isPos: false }));

    allFactors.forEach(item => {
        const valStr = String(item.impact || "+0.10");
        const isPos = item.isPos || !valStr.startsWith("-");
        const numVal = Math.abs(parseFloat(valStr.replace(/[^0-9.-]/g, ""))) || 0.12;
        // Bar length as percentage of half the track (max 45%)
        const widthPct = Math.min(46, Math.max(8, Math.round(numVal * 200)));
        const displayScore = isPos 
            ? (valStr.startsWith("+") ? valStr : `+${valStr}`) 
            : (valStr.startsWith("-") ? valStr : `-${valStr}`);

        container.innerHTML += `
            <div class="shap-bar-row">
                <span class="shap-bar-name" title="${item.factor}">${item.factor.toLowerCase()}</span>
                <div class="shap-diverging-track">
                    <div class="shap-track-zero-line"></div>
                    <div class="shap-bar-segment ${isPos ? 'pos' : 'neg'}" style="width: ${widthPct}%;"></div>
                </div>
                <span class="shap-bar-score ${isPos ? 'score-pos' : 'score-neg'}">${displayScore}</span>
            </div>
        `;
    });

    // Populate Rule-Based Compliance tab details
    const sum = data.applicant_summary || {};
    const fundsDesc = document.getElementById("rule-funds-desc");
    if (fundsDesc) {
        const funds = sum.settlement_funds_cad || 35000;
        fundsDesc.textContent = funds >= 14690 
            ? `Meets IRCC baseline settlement threshold ($${funds.toLocaleString()} CAD vs $14,690 CAD requirement).`
            : `Below recommended IRCC settlement baseline ($${funds.toLocaleString()} CAD). Additional reserves recommended.`;
    }

    const langDesc = document.getElementById("rule-lang-desc");
    if (langDesc) {
        const lang = sum.language_overall_score || 8.0;
        langDesc.textContent = lang >= 7.0
            ? `Exceeds minimum language benchmark (${lang} vs CLB 7.0 standard for high-skilled pathways).`
            : `Language score (${lang}) is borderline. Retaking IELTS/CELPIP can yield +15-20 CRS points.`;
    }

    const jobDesc = document.getElementById("rule-job-desc");
    if (jobDesc) {
        jobDesc.textContent = (sum.job_offer === 1 || sum.job_offer === "1" || sum.job_offer === true)
            ? "Job offer confirmed with genuine employer alignment."
            : "No validated local job offer recorded. Secondary points streams may be required.";
    }

    const admDesc = document.getElementById("rule-adm-desc");
    if (admDesc) {
        admDesc.textContent = (sum.previous_visa_refusal === 1 || sum.previous_visa_refusal === "1")
            ? "Prior visa refusal detected on record. GCMS explanation note required."
            : "No previous visa refusals or criminal/medical flags identified.";
    }
}

// INPUT AUDIT (Profile Summary Matrix & Collapsible Accordions)
function renderInputAudit(sum, countryName) {
    if (!sum) sum = {};

    // 1. Top 6 Summary Pills
    const pCountry = document.getElementById("audit-pill-country");
    const pEdu = document.getElementById("audit-pill-edu");
    const pExp = document.getElementById("audit-pill-exp");
    const pJob = document.getElementById("audit-pill-job");
    const pLang = document.getElementById("audit-pill-lang");
    const pFunds = document.getElementById("audit-pill-funds");

    if (pCountry) pCountry.textContent = countryName || "Canada";
    if (pEdu) pEdu.textContent = sum.education_level ? sum.education_level.replace(" Degree", "") : "Master's";
    if (pExp) pExp.textContent = `${sum.relevant_work_exp || 5} years`;
    if (pJob) pJob.textContent = (sum.job_offer === 1 || sum.job_offer === "1" || sum.job_offer === true) ? "Yes" : "No";
    if (pLang) pLang.textContent = String(sum.language_overall_score || "8.5");
    if (pFunds) {
        const fVal = sum.settlement_funds_cad || 55000;
        pFunds.textContent = `$${Number(fVal).toLocaleString()}`;
    }

    // 2. Accordion 1: Personal & Destination
    setFieldText("audit-val-age", `${sum.age || 29} years`);
    setFieldText("audit-val-citizenship", sum.citizenship || "India");
    setFieldText("audit-val-residence", sum.current_residence || sum.citizenship || "India");
    setFieldText("audit-val-marital", sum.marital_status || "Single");
    setFieldText("audit-val-dependents", String(sum.dependents ?? 0));
    setFieldText("audit-val-dest", countryName || "Canada");

    // 3. Accordion 2: Education & Credentials
    setFieldText("audit-val-edulevel", sum.education_level || "Master's Degree");
    setFieldText("audit-val-field", sum.field_of_study || "Computer Science");
    setFieldText("audit-val-tier", sum.institution_tier || "Tier 1 Accredited");

    // 4. Accordion 3: Work & Offer
    setFieldText("audit-val-exptot", `${sum.total_work_exp || 6} Years`);
    setFieldText("audit-val-exprel", `${sum.relevant_work_exp || 5} Years`);
    setFieldText("audit-val-joboffer", (sum.job_offer === 1 || sum.job_offer === "1") ? "Supported (Full-time)" : "None");
    setFieldText("audit-val-localexp", `${sum.previous_canada_work || 0} Years`);
    setFieldText("audit-val-skillteer", sum.occupation_skill_level || "TEER 1 (Professional)");

    // 5. Accordion 4: Language & Finances
    setFieldText("audit-val-langscore", `CLB ${sum.language_overall_score || 8.5} (English)`);
    const salary = sum.offered_salary_cad || sum.annual_income_cad || 78000;
    setFieldText("audit-val-salary", `CAD $${Number(salary).toLocaleString()}`);
    const funds = sum.settlement_funds_cad || 55000;
    setFieldText("audit-val-funds", `CAD $${Number(funds).toLocaleString()}`);
    setFieldText("audit-val-sponsor", sum.financial_sponsor || "Self-Funded");

    // 6. Accordion 5: Admissibility
    setFieldText("audit-val-refusal", (sum.previous_visa_refusal === 1 || sum.previous_visa_refusal === "1") ? "1 Prior Refusal" : "None");
    setFieldText("audit-val-police", (sum.criminal_record === 1 || sum.criminal_record === "1") ? "Record Flagged" : "Clear Record");
    setFieldText("audit-val-medical", (sum.medical_flag === 1 || sum.medical_flag === "1") ? "Review Needed" : "Passed / No Flags");
}

function setFieldText(elemId, val) {
    const el = document.getElementById(elemId);
    if (el) el.textContent = val;
}

// SUGGESTED ACTION PLAN (Interactive Checklist with Progress)
function renderActionPlan(recs) {
    const container = document.getElementById("recommendations-list");
    if (!container) return;
    container.innerHTML = "";

    const defaultRecs = [
        {
            priority: "HIGH",
            category: "EMPLOYMENT",
            title: "Verify employment offer evidence",
            action: "Check that employer and position details are current and consistent with NOC TEER descriptions.",
            rationale: "Rule-based criteria only"
        },
        {
            priority: "MEDIUM",
            category: "LANGUAGE",
            title: "Review language-test validity",
            action: "Confirm test month and expiry date before relying on it (must be within 2 years of submission).",
            rationale: "Static statutory rule"
        },
        {
            priority: "HIGH",
            category: "FINANCIAL",
            title: "Recheck settlement-fund documentation",
            action: "Review balances, ownership, and document dates to satisfy official LICO proof-of-funds rules.",
            rationale: "Rule-based criteria only"
        }
    ];

    const displayRecs = (recs && recs.length > 0) ? recs.slice(0, 3).map((r, idx) => ({
        priority: (r.priority && r.priority.toLowerCase().includes("high")) ? "HIGH" : "MEDIUM",
        category: (r.category && r.category.toLowerCase().includes("lang")) ? "LANGUAGE" : (r.category && r.category.toLowerCase().includes("employ") ? "EMPLOYMENT" : "FINANCIAL"),
        title: r.title || `Action Step ${idx + 1}`,
        action: r.action || "Ensure statutory compliance with relevant guidelines.",
        rationale: r.rationale || "Rule-based criteria only"
    })) : defaultRecs;

    displayRecs.forEach((item, idx) => {
        const isHigh = item.priority === "HIGH";
        container.innerHTML += `
            <div class="action-plan-card" id="action-card-${idx}">
                <div>
                    <div class="card-tags-row">
                        <span class="act-badge-priority ${isHigh ? 'priority-high' : 'priority-med'}">${item.priority}</span>
                        <span class="act-badge-cat">${item.category}</span>
                    </div>
                    <h4 class="act-card-title">${item.title}</h4>
                    <p class="act-card-desc">${item.action}</p>
                    <span class="act-rationale-pill">Rationale: ${item.rationale}</span>
                </div>
                <label class="act-checkbox-wrap">
                    <input type="checkbox" onchange="toggleActionReviewed(this)">
                    <span>Mark reviewed</span>
                </label>
            </div>
        `;
    });

    updateActionPlanProgress();
}

function toggleActionReviewed(checkbox) {
    const card = checkbox.closest('.action-plan-card');
    if (card) {
        if (checkbox.checked) {
            card.classList.add('reviewed');
        } else {
            card.classList.remove('reviewed');
        }
    }
    updateActionPlanProgress();
}

function updateActionPlanProgress() {
    const total = document.querySelectorAll('#recommendations-list input[type="checkbox"]').length || 3;
    const checked = document.querySelectorAll('#recommendations-list input[type="checkbox"]:checked').length;
    
    const textElem = document.getElementById("action-progress-text");
    if (textElem) textElem.textContent = `${checked}/${total} reviewed`;

    const barElem = document.getElementById("action-progress-bar");
    if (barElem) {
        const pct = total > 0 ? Math.round((checked / total) * 100) : 0;
        barElem.style.width = `${pct}%`;
    }
}

// DASHBOARD SECTION SMOOTH JUMP NAVIGATION
function scrollToDashSection(sectionId) {
    const target = document.getElementById(sectionId);
    if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    // Update active jump pill
    document.querySelectorAll('.dash-jump-nav .jump-pill').forEach(pill => {
        pill.classList.remove('active');
    });
    const activePill = document.getElementById(`pill-${sectionId}`);
    if (activePill) activePill.classList.add('active');
}

// EXPLAINABILITY WORKSPACE TAB SWITCHER
function switchXaiTab(tabKey) {
    document.querySelectorAll('.xai-tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.xai-tab-panel').forEach(panel => {
        panel.classList.remove('active');
        panel.style.display = 'none';
    });

    const activeBtn = document.getElementById(`tab-btn-${tabKey}`);
    if (activeBtn) activeBtn.classList.add('active');

    const activePanel = document.getElementById(`xai-panel-${tabKey}`);
    if (activePanel) {
        activePanel.classList.add('active');
        activePanel.style.display = 'block';
    }
}

// AUDIT ACCORDION TOGGLE
function toggleAuditAcc(accId) {
    const item = document.getElementById(accId);
    if (item) {
        item.classList.toggle('open');
    }
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

// Admin Modal Handlers & Telemetry Diagnostics
function openAdminModal() {
    const modal = document.getElementById("adminModal");
    if (modal) {
        modal.classList.add("active");
        document.body.style.overflow = "hidden";
    }
}

function closeAdminModal() {
    const modal = document.getElementById("adminModal");
    if (modal) {
        modal.classList.remove("active");
        document.body.style.overflow = "";
    }
}

function closeAdminModalOnOverlay(event) {
    if (event.target && event.target.id === "adminModal") {
        closeAdminModal();
    }
}

async function testModelHealth() {
    try {
        const response = await fetch('/health');
        if (!response.ok) throw new Error("Health check failed");
        const data = await response.json();
        alert(`System Diagnostic Output:\nStatus: ${data.status.toUpperCase()}\nEngine: ${data.ml_engine}\nBackend: ${data.backend}\nSystem: ${data.system}`);
    } catch (err) {
        alert(`Diagnostic Error: ${err.message}`);
    }
}

// Interactive Scenario Modeling & What-If Simulation Sandbox
let originalAppProb = null;

function simulateChange(scenarioType, boostAmount) {
    const appProbElem = document.getElementById("dash-app-prob");
    const denProbElem = document.getElementById("dash-den-prob");
    const appFillElem = document.getElementById("dash-app-bar");
    const denFillElem = document.getElementById("dash-den-bar");
    const legendAppElem = document.getElementById("legend-approved-pct");
    const legendDenElem = document.getElementById("legend-denied-pct");
    const feedbackElem = document.getElementById("sim-feedback-message");
    
    if (!appProbElem) return;

    if (originalAppProb === null) {
        originalAppProb = parseInt(appProbElem.textContent.replace('%', '')) || 86;
    }

    let targetProb;
    let label;

    if (scenarioType === 'reset') {
        targetProb = originalAppProb;
        label = "Reset profile to original calculation.";
    } else {
        const boost = parseInt(boostAmount) || 8;
        targetProb = Math.min(99, Math.max(10, originalAppProb + boost));
        label = `${scenarioType}: +${boost}% boost (New Chance of Approval: ${targetProb}%).`;
    }

    const targetDen = 100 - targetProb;
    const riskCategory = targetProb >= 75 ? "LOW" : (targetProb >= 50 ? "MEDIUM" : "HIGH");

    appProbElem.textContent = `${targetProb}%`;
    if (denProbElem) denProbElem.textContent = `${targetDen}%`;
    if (appFillElem) appFillElem.style.width = `${targetProb}%`;
    if (denFillElem) denFillElem.style.width = `${targetDen}%`;
    if (legendAppElem) legendAppElem.textContent = `${targetProb}%`;
    if (legendDenElem) legendDenElem.textContent = `${targetDen}%`;

    const refinedProbElem = document.getElementById("dash-refined-prob");
    if (refinedProbElem) refinedProbElem.textContent = `${targetProb}%`;
    const bandTextElem = document.getElementById("dash-band-text");
    if (bandTextElem) bandTextElem.textContent = `${riskCategory} RISK`;
    const scaleMarker = document.getElementById("dash-scale-marker");
    if (scaleMarker) scaleMarker.textContent = `${targetProb}%`;
    const scaleThumb = document.getElementById("dash-scale-thumb");
    if (scaleThumb) scaleThumb.style.left = `${targetProb}%`;

    // Re-render Donut
    if (typeof renderDonutChart === 'function') {
        renderDonutChart(targetProb, targetDen);
    }

    // Re-render Risk Gauge
    if (typeof renderRiskGauge === 'function') {
        renderRiskGauge(targetProb, riskCategory);
    }

    // Update banner
    const banner = document.getElementById("donut-bottom-banner");
    const bannerText = document.getElementById("donut-banner-text");
    if (banner && bannerText) {
        if (targetProb >= 50) {
            banner.className = "atlys-banner banner-green";
            bannerText.textContent = `High probability of approval (${targetProb}%) based on simulated parameter adjustments.`;
        } else {
            banner.className = "atlys-banner banner-red";
            bannerText.textContent = `Statutory review recommended (${targetProb}%). Profile requires targeted credential enhancement.`;
        }
    }

    if (feedbackElem) {
        feedbackElem.textContent = label;
        feedbackElem.classList.remove("hidden");
        feedbackElem.style.display = "block";
    }
}


