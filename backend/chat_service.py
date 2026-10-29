"""
CanVisa — Advanced Immigration Intelligence AI (Atlas Engine)
Powered by:
- Semantic Vector Retrieval (TF-IDF Cosine Similarity across 25+ Comprehensive Immigration Domains)
- Real-time Candidate Profile & CRS Evaluator Engine
- Cloud LLM Integration (Gemini REST API fallback if GEMINI_API_KEY is present)
- Adaptive Immigration Regulatory Synthesizer for arbitrary open-ended questions
- Multilingual Support (English, Kannada, Hindi)
"""

import os
import re
import json
from typing import Dict, Any, List, Optional
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================================
# 1. BROAD IMMIGRATION SCOPE & INTENT CLASSIFICATION
# =========================================================================

VISA_DOMAIN_TERMS = [
    # General immigration terms
    "visa", "permit", "pr", "permanent residency", "residence", "immigrate", "immigration", "relocate",
    "move", "citizenship", "passport", "embassy", "consulate", "entry", "border", "ircc", "home office",
    "dha", "bamf", "five eyes", "gcms", "caips", "travel", "settle", "settlement", "applicant", "application",
    # Countries
    "canada", "australia", "uk", "united kingdom", "britain", "england", "germany", "schengen", "europe",
    # Status & visa types
    "work permit", "study permit", "student visa", "visitor visa", "tourist", "open work permit", "closed work permit",
    "pgwp", "sowp", "super visa", "subclass", "189", "190", "491", "482", "186", "chancenkarte", "blue card",
    "opportunity card", "cos", "lmia", "express entry", "pnp", "fsw", "cec", "fst", "crs", "eoi",
    # Evaluation & parameters
    "assess", "evaluate", "profile", "score", "points", "chance", "chances", "calculate", "cutoff", "cut off",
    "age", "education", "degree", "bachelor", "master", "phd", "diploma", "experience", "tenure", "job", "career",
    "ielts", "clb", "pte", "celpip", "toefl", "language", "english", "french", "german", "band",
    "job offer", "sponsor", "sponsorship", "employer", "company", "contract", "salary", "wage", "threshold",
    # Financials & verification
    "funds", "money", "savings", "bank", "balance", "pof", "proof of funds", "loan", "gift deed", "fee", "fees",
    "cost", "price", "refund", "wes", "eca", "credential", "medical", "police clearance", "pcc", "biometrics",
    # Edge cases & life situations
    "gap", "career gap", "refusal", "rejected", "rejection", "refused", "appeal", "spouse", "wife", "husband",
    "partner", "children", "child", "kids", "parents", "family", "dependent", "layoff", "laid off", "change employer",
    "doctor", "nurse", "healthcare", "engineer", "software", "it", "developer", "truck driver", "chef", "cook",
    "trades", "construction", "time", "processing time", "how long", "timeline", "delay", "risk", "medium risk",
    "low risk", "high risk", "moderate risk", "help", "rules", "requirements", "criteria", "eligible", "eligibility",
    # Multilingual terms (Kannada & Hindi)
    "ವೀಸಾ", "ಅರ್ಹತೆ", "ಕೆನಡಾ", "ಆಸ್ಟ್ರೇಲಿಯಾ", "ಯುಕೆ", "ಜರ್ಮನಿ", "ಉದ್ಯೋಗ", "ಉಳಿತಾಯ", "ಕುಟುಂಬ", "ಹೆಂಡತಿ", "ಮಕ್ಕಳು", "ರಿಸ್ಕ್",
    "ವಿವರ", "ನಿಯಮ", "ಮೌಲ್ಯಮಾಪನ", "ಅಂಕಗಳು", "ಪಾಯಿಂಟ್ಸ್",
    "वीजा", "पात्रता", "कनाडा", "ऑस्ट्रेलिया", "यूके", "जर्मनी", "नौकरी", "बचत", "परिवार", "पत्नी", "बच्चे", "रिस्क",
    "नियम", "मूल्यांकन", "अंक", "पॉइंट्स", "फंड्स", "जॉब ऑफर"
]

def is_visa_related(query: str) -> bool:
    q = query.lower().strip()
    if len(q) < 2:
        return False
    # Greetings & Identity
    greetings = ["hi", "hello", "hey", "help", "who are you", "what is this", "atlas", "namaste", "namaskara"]
    if any(q == g or q.startswith(g + " ") for g in greetings):
        return True
    if any(term in q for term in VISA_DOMAIN_TERMS):
        return True
    if re.search(r'\b(\d{2}\s*(?:yrs|years)|bachelor|master|phd|ielts|clb|pte|job offer)\b', q):
        return True
    return False

def detect_language(query: str, client_lang: str = "en") -> str:
    if re.search(r'[\u0C80-\u0CFF]', query):
        return "kn"
    if re.search(r'[\u0900-\u097F]', query):
        return "hi"
    if client_lang in ["kn", "hi"]:
        return client_lang
    return "en"

# =========================================================================
# 2. COMPREHENSIVE EXPERT IMMIGRATION TOPICS REPOSITORY (25 CORE DOMAINS)
# =========================================================================

KNOWLEDGE_BASE = [
    # 1. WHY MEDIUM RISK
    {
        "id": "medium_risk_why",
        "keywords": [
            "why does a profile get medium risk",
            "medium risk moderate risk reasons parameters",
            "why medium risk borderline chance",
            "ಪ್ರೊಫೈಲ್‌ಗೆ medium risk ಏಕೆ ಬರುತ್ತದೆ",
            "प्रोफाइल को medium risk क्यों मिलता है"
        ],
        "answers": {
            "en": (
                "🤔 **Why a Profile Receives Medium Risk:**\n\n"
                "A profile receives **Medium Risk (50% to 70% moderate chance)** when it satisfies statutory qualification rules but lacks competitive differentiators:\n\n"
                "1. **No Validated Job Offer:** You qualify on education and experience, but applying without an employer offer (LMIA/CoS) limits total point score.\n"
                "2. **Moderate Language Score:** Your score meets the legal cutoff (IELTS 6.5–7.0 / CLB 7), but does not reach the highest point tier (CLB 9 / IELTS 8-7-7-7).\n"
                "3. **Baseline Savings:** Your funds satisfy the legal minimum settlement requirement without an additional financial buffer.\n\n"
                "💡 **What it means:** You meet the legal criteria, but sit in the middle of the applicant pool. Boosting your language score or securing employer sponsorship quickly pushes you into **Low Risk (High Chance)**."
            ),
            "kn": (
                "🤔 **ಪ್ರೊಫೈಲ್‌ಗೆ Medium Risk ಏಕೆ ಬರುತ್ತದೆ?**\n\n"
                "ಒಬ್ಬ ಅರ್ಜಿದಾರನಿಗೆ **Medium Risk (~50% ರಿಂದ 70% ಮಧ್ಯಮ ಅವಕಾಶ)** ಬರಲು ಈ ಕೆಳಗಿನ ಮುಖ್ಯ ಕಾರಣಗಳಿವೆ:\n\n"
                "1. **ಉದ್ಯೋಗ ಆಫರ್ ಇಲ್ಲದಿರುವುದು:** ಉತ್ತಮ ಶಿಕ್ಷಣ ಮತ್ತು ಅನುಭವವಿದ್ದರೂ, ಕಂಪನಿಯಿಂದ ನೇರ ಜಾಬ್ ಆಫರ್ ಅಥವಾ ಸ್ಪಾನ್ಸರ್‌ಶಿಪ್ ಕೊರತೆ.\n"
                "2. **ಸಾಮಾನ್ಯ ಇಂಗ್ಲಿಷ್ ಅಂಕಗಳು:** ಭಾಷಾ ಸ್ಕೋರ್ ಕನಿಷ್ಠ ಅರ್ಹತೆಯನ್ನು ತಲುಪುತ್ತದೆ, ಆದರೆ ಗರಿಷ್ಠ ಅಂಕಗಳನ್ನು (IELTS 8.0+) ಗಳಿಸಲು ಸಾಕಾಗುವುದಿಲ್ಲ.\n"
                "3. **ಕನಿಷ್ಠ ಉಳಿತಾಯ:** ಬ್ಯಾಂಕ್ ಬ್ಯಾಲೆನ್ಸ್ ಸರ್ಕಾರದ ಕನಿಷ್ಠ ಮಿತಿಯಷ್ಟೇ ಇರುತ್ತದೆ.\n\n"
                "💡 ಇಂಗ್ಲಿಷ್ ಸ್ಕೋರ್ ಸ್ವಲ್ಪ ಹೆಚ್ಚಿಸಿದರೆ ಅಥವಾ ಜಾಬ್ ಆಫರ್ ಪಡೆದರೆ ನೀವು ಸುಲಭವಾಗಿ **Low Risk (ಹೆಚ್ಚಿನ ಅವಕಾಶ)** ವಲಯಕ್ಕೆ ಹೋಗಬಹುದು."
            ),
            "hi": (
                "🤔 **प्रोफाइल को Medium Risk क्यों मिलता है?**\n\n"
                "सिस्टम किसी प्रोफाइल को **Medium Risk (~50% से 70% मध्यम संभावना)** तब देता है जब कुछ मुख्य फायदों की कमी होती है:\n\n"
                "1. **जॉब ऑफर की कमी:** शिक्षा और अनुभव अच्छा है, लेकिन नियोक्ता से पक्का जॉब ऑफर या स्पॉन्सरशिप नहीं है।\n"
                "2. **मध्यम इंग्लिश स्कोर:** भाषा स्कोर बुनियादी पात्रता पूरी करता है, लेकिन टॉप पॉइंट्स (IELTS 8.0+) हासिल नहीं करता।\n"
                "3. **सीमित बैंक बचत:** बचत केवल न्यूनतम आवश्यक सीमा जितनी है, अतिरिक्त सुरक्षा फंड नहीं है।\n\n"
                "💡 जॉब ऑफर मिलने या भाषा स्कोर थोड़ा सुधारने से आप सीधे **Low Risk (उच्च संभावना)** में आ सकते हैं।"
            )
        }
    },

    # 2. HOW TO MOVE FROM MEDIUM TO LOW RISK
    {
        "id": "low_risk_how",
        "keywords": [
            "how to move from medium to low risk",
            "how to get low risk high chance",
            "improve visa chances approval tips",
            "medium ನಿಂದ low risk ಗೆ ಹೋಗುವುದು ಹೇಗೆ",
            "medium से low risk में कैसे जाएं"
        ],
        "answers": {
            "en": (
                "💡 **3 Proven Ways to Move from Medium Risk to Low Risk:**\n\n"
                "1. **Unlock the CLB 9 Multiplier:** Scoring 8.0 in Listening and 7.0 in Reading, Writing, and Speaking gives **+50 to +64 bonus CRS points** in Canada.\n"
                "2. **Target Provincial Nominee Programs (PNP):** Receiving a nomination from Ontario (OINP), Alberta (AAIP), or BC adds an instant **+600 points** guarantee.\n"
                "3. **Secure an Employer Job Offer:** A genuine LMIA job offer in Canada or Certificate of Sponsorship in the UK immediately shifts a profile to **Low Risk (High Approval Chance)**."
            ),
            "kn": (
                "💡 **Medium Risk ನಿಂದ Low Risk ಗೆ ಹೋಗಲು 3 ಸರಳ ಹಂತಗಳು:**\n\n"
                "1. **IELTS ಸ್ಕೋರ್ ಹೆಚ್ಚಿಸಿ:** CLB 9 (8-7-7-7) ಗಳಿಸಿದರೆ +50 ಕ್ಕೂ ಹೆಚ್ಚು ಬೋನಸ್ ಅಂಕಗಳು ದೊರೆಯುತ್ತವೆ.\n"
                "2. **ರಾಜ್ಯ ನಾಮನಿರ್ದೇಶನ (PNP):** ಕೆನಡಾದ ಯಾವುದೇ ರಾಜ್ಯದಿಂದ ನಾಮನಿರ್ದೇಶನ ಪಡೆದರೆ ಖಚಿತ +600 ಅಂಕಗಳು ಸಿಗುತ್ತವೆ.\n"
                "3. **ಜಾಬ್ ಆಫರ್ ಪಡೆಯಿರಿ:** ಕಂಪನಿಯಿಂದ ಮಾನ್ಯತೆ ಪಡೆದ ಉದ್ಯೋಗ ಆಫರ್ ನಿಮ್ಮ ಪ್ರೊಫೈಲ್ ಅನ್ನು ತಕ್ಷಣ Low Risk ಗೆ ತರುತ್ತದೆ."
            ),
            "hi": (
                "💡 **Medium Risk से Low Risk में जाने के 3 आसान कदम:**\n\n"
                "1. **IELTS में CLB 9 हासिल करें:** 8-7-7-7 बैंड्स लाने से सीधे +50 से +60 बोनस CRS पॉइंट्स मिलते हैं।\n"
                "2. **प्रोविंशियल नॉमिनेशन (PNP):** कनाडाई राज्य से नॉमिनेशन मिलने पर +600 पॉइंट्स की पक्की गारंटी मिलती है।\n"
                "3. **जॉब ऑफर लें:** एक वैध कंपनी जॉब ऑफर आपकी प्रोफाइल को तुरंत Low Risk (उच्च संभावना) में ले आता है।"
            )
        }
    },

    # 3. PROOF OF FUNDS (POF)
    {
        "id": "proof_of_funds_settlement",
        "keywords": [
            "what is proof of funds for canada",
            "proof of funds pof settlement funds bank balance",
            "how much money needed in bank for canada pr",
            "ಕೆನಡಾ proof of funds ಬ್ಯಾಂಕ್ ಉಳಿತಾಯ ಎಷ್ಟು ಬೇಕು",
            "कनाडा proof of funds बैंक बैलेंस कितना चाहिए"
        ],
        "answers": {
            "en": (
                "💰 **Canada Express Entry Settlement Funds (IRCC Proof of Funds 2024–2025):**\n\n"
                "Under the Federal Skilled Worker Program (FSWP), applicants must prove unencumbered liquid funds:\n\n"
                "| Family Size | Required Minimum (CAD) | Approx. USD | Approx. INR |\n"
                "| :--- | :--- | :--- | :--- |\n"
                "| **1 Applicant** | **$14,690 CAD** | ~$10,800 USD | ~₹9.1 Lakhs |\n"
                "| **2 Persons (Couple)** | **$18,288 CAD** | ~$13,450 USD | ~₹11.3 Lakhs |\n"
                "| **3 Persons** | **$22,483 CAD** | ~$16,500 USD | ~₹13.9 Lakhs |\n"
                "| **4 Persons** | **$27,297 CAD** | ~$20,050 USD | ~₹16.9 Lakhs |\n"
                "| *Each Extra Member* | +$3,958 CAD | ~$2,900 USD | ~₹2.4 Lakhs |\n\n"
                "📌 **Acceptable:** Savings accounts, Fixed Deposits (FD), cash gifts with registered Gift Deeds.\n"
                "❌ **Not Acceptable:** Real estate, jewellery, vehicles, or unverified personal loans.\n"
                "💡 **Exempt:** You do not need to show funds if you have an LMIA job offer or apply under Canadian Experience Class (CEC)."
            ),
            "kn": (
                "💰 **ಕೆನಡಾ Express Entry ಬ್ಯಾಂಕ್ ನಿಧಿ (Proof of Funds):**\n\n"
                "• **1 ವ್ಯಕ್ತಿ (ಅರ್ಜಿದಾರ ಮಾತ್ರ):** **$14,690 CAD** (~₹9.1 ಲಕ್ಷ)\n"
                "• **2 ಸದಸ್ಯರು (ದಂಪತಿ):** **$18,288 CAD** (~₹11.3 ಲಕ್ಷ)\n"
                "• **3 ಸದಸ್ಯರು:** **$22,483 CAD** (~₹13.9 ಲಕ್ಷ)\n"
                "• ಹಣವು ನಗದು ಅಥವಾ ಫಿಕ್ಸೆಡ್ ಡೆಪಾಸಿಟ್ (FD) ರೂಪದಲ್ಲಿರಬೇಕು (ರಿಯಲ್ ಎಸ್ಟೇಟ್ ಒಪ್ಪುವುದಿಲ್ಲ).\n"
                "• ನಿಮ್ಮ ಬಳಿ ಅಧಿಕೃತ ಜಾಬ್ ಆಫರ್ ಇದ್ದರೆ ಹಣ ತೋರಿಸುವ ಅಗತ್ಯವಿಲ್ಲ!"
            ),
            "hi": (
                "💰 **कनाडा Express Entry आवश्यक बैंक बैलेंस (POF):**\n\n"
                "• **1 व्यक्ति (अकेला आवेदक):** **$14,690 CAD** (~₹9.1 लाख)\n"
                "• **2 सदस्य (दंपति):** **$18,288 CAD** (~₹11.3 लाख)\n"
                "• **3 सदस्य:** **$22,483 CAD** (~₹13.9 लाख)\n"
                "• फंड्स केवल बचत खाते या FD में होने चाहिए। अचल संपत्ति मान्य नहीं है।\n"
                "• वैध जॉब ऑफर होने पर बैंक बैलेंस दिखाना अनिवार्य नहीं है।"
            )
        }
    },

    # 4. CANADA EXPRESS ENTRY & CRS
    {
        "id": "canada_express_entry_crs",
        "keywords": [
            "what are canada express entry requirements",
            "canada express entry crs score cut off points",
            "fsw cec federal skilled worker rules",
            "ಕೆನಡಾ express entry ನಿಯಮಗಳು ಯಾವುವು",
            "कनाडा express entry के नियम क्या हैं"
        ],
        "answers": {
            "en": (
                "🍁 **Canada Express Entry Core Requirements:**\n\n"
                "1. **Education:** Verified Bachelor's or Master's degree evaluated via WES/ECA.\n"
                "2. **Work Experience:** Minimum 1 continuous year of skilled work experience in TEER 0, 1, 2, or 3 within the last 10 years.\n"
                "3. **Language Benchmark:** Minimum CLB 7 (IELTS 6.0 in each band) to enter pool; CLB 9 (8-7-7-7) recommended to receive Invitation to Apply (ITA).\n"
                "4. **Settlement Savings:** Proof of Funds (CAD $14,690 for 1 person).\n\n"
                "📌 **CRS Cutoff Trends:** General draws hover around 515–530 CRS. Targeted category draws (STEM, Healthcare, French) invite candidates at lower cutoffs (430–485 CRS)."
            ),
            "kn": (
                "🍁 **ಕೆನಡಾ Express Entry ಮುಖ್ಯ ಮಾನದಂಡಗಳು:**\n\n"
                "• ಪದವಿ (WES ಮೌಲ್ಯಮಾಪನ ಮಾಡಿರಬೇಕು)\n"
                "• ಕನಿಷ್ಠ 1 ರಿಂದ 2 ವರ್ಷಗಳ ನುರಿತ ಕೆಲಸದ ಅನುಭವ\n"
                "• IELTS ನಲ್ಲಿ ಕನಿಷ್ಠ 6.0+ ಬ್ಯಾಂಡ್ಸ್\n"
                "• ಸಾಕಷ್ಟು ಬ್ಯಾಂಕ್ ಉಳಿತಾಯ ($14,690 CAD).\n"
                "• ಸಾಮಾನ್ಯ ಕಟ್‌ಆಫ್ 510+ ಅಂಕಗಳಾಗಿವೆ; STEM ಮತ್ತು Healthcare ಗೆ ಕಡಿಮೆ ಅಂಕಗಳಲ್ಲಿ PR ಸಿಗುತ್ತದೆ."
            ),
            "hi": (
                "🍁 **कनाडा Express Entry के मुख्य नियम:**\n\n"
                "• मान्यता प्राप्त विश्वविद्यालय की डिग्री (WES मूल्यांकित)\n"
                "• न्यूनतम 1 से 2 वर्ष का कुशल कार्य अनुभव\n"
                "• IELTS में न्यूनतम 6.0+ बैंड्स (CLB 7+)\n"
                "• आवश्यक बैंक बैलेंस ($14,690 CAD)\n"
                "• सामान्य कटऑफ 515+ रहता है, जबकि STEM/Healthcare में 450+ पर भी PR मिल जाता है।"
            )
        }
    },

    # 5. AUSTRALIA & UK RULES
    {
        "id": "australia_uk_rules",
        "keywords": [
            "what are the rules for australia and uk",
            "australia subclass 189 190 uk skilled worker rules",
            "how to migrate to australia and united kingdom",
            "ಆಸ್ಟ್ರೇಲಿಯಾ ಮತ್ತು ಯುಕೆ ನಿಯಮಗಳು ಯಾವುವು",
            "ऑस्ट्रेलिया और यूके के मुख्य नियम क्या हैं"
        ],
        "answers": {
            "en": (
                "🌍 **Australia & UK Skilled Immigration Rules:**\n\n"
                "🦘 **Australia (Points System):**\n"
                "• **Subclass 189:** Independent PR without state or employer sponsorship.\n"
                "• **Subclass 190:** State-nominated PR (+5 bonus points).\n"
                "• **Subclass 491:** Regional 5-year visa (+15 bonus points).\n"
                "• Must pass Skills Assessment (ACS/VETASSESS), score minimum 65 points (85+ competitive), and be under 45 years.\n\n"
                "🇬🇧 **United Kingdom (Employer Sponsored):**\n"
                "• Requires confirmed job offer with **Certificate of Sponsorship (CoS)** from a licensed sponsor.\n"
                "• **Salary Threshold:** Minimum **£38,700 per year** or occupation going rate.\n"
                "• Leads to Permanent Settlement (ILR) after 5 continuous years."
            ),
            "kn": (
                "🌍 **ಆಸ್ಟ್ರೇಲಿಯಾ ಮತ್ತು ಯುಕೆ ಮುಖ್ಯ ನಿಯಮಗಳು:**\n\n"
                "🦘 **ಆಸ್ಟ್ರೇಲಿಯಾ:**\n"
                "• ಪಾಯಿಂಟ್ಸ್ ಸಿಸ್ಟಮ್ (ವಯಸ್ಸು 45 ಕ್ಕಿಂತ ಕಡಿಮೆ, ಕನಿಷ್ಠ 65 ಅಂಕಗಳು, IELTS 7.0).\n"
                "• Subclass 189 (ಸ್ವತಂತ್ರ PR), Subclass 190 (ರಾಜ್ಯ ನಾಮನಿರ್ದೇಶಿತ PR).\n\n"
                "🇬🇧 **ಯುಕೆ:**\n"
                "• ಕಂಪನಿ ಜಾಬ್ ಆಫರ್ (CoS) ಕಡ್ಡಾಯ.\n"
                "• ಕನಿಷ್ಠ ವೇತನ ಮಿತಿ: ವಾರ್ಷಿಕ **£38,700 GBP**."
            ),
            "hi": (
                "🌍 **ऑस्ट्रेलिया और यूके के मुख्य नियम:**\n\n"
                "🦘 **ऑस्ट्रेलिया:**\n"
                "• प्वाइंट्स सिस्टम आधारित (उम्र 45 से कम, न्यूनतम 65 अंक, स्किल्स असेसमेंट)।\n"
                "• Subclass 189 (स्वतंत्र PR), Subclass 190 (राज्य नामांकित PR)।\n\n"
                "🇬🇧 **यूके:**\n"
                "• कंपनी जॉब ऑफर (CoS) अनिवार्य।\n"
                "• न्यूनतम वेतन सीमा: **£38,700 GBP प्रति वर्ष**।"
            )
        }
    },

    # 6. GERMANY OPPORTUNITY CARD & BLUE CARD
    {
        "id": "germany_chancenkarte_bluecard",
        "keywords": [
            "what is the germany opportunity card chancenkarte",
            "germany chancenkarte eu blue card rules",
            "germany job search visa 6 points",
            "ಜರ್ಮನಿ chancenkarte ಅವಕಾಶ ಕಾರ್ಡ್ ನಿಯಮಗಳೇನು",
            "जर्मनी chancenkarte के नियम क्या हैं"
        ],
        "answers": {
            "en": (
                "🇩🇪 **Germany Opportunity Card (Chancenkarte) & EU Blue Card:**\n\n"
                "1. **Chancenkarte (Opportunity Card):**\n"
                "• Allows non-EU professionals to enter Germany for up to **1 year to search for qualified work** without a pre-existing job offer.\n"
                "• Requires a minimum of **6 points** (Degree = 4 pts, 3 yrs exp = 2-3 pts, German/English skills = 1-2 pts, Age under 35 = 2 pts).\n\n"
                "2. **EU Blue Card:**\n"
                "• Requires recognized degree and employment contract with minimum gross annual salary of **€45,300 EUR** (€41,041 EUR for STEM/IT shortage fields).\n"
                "• Fast-track Permanent Residence in just **21 months** (with B1 German) or **27 months** (with basic German)."
            ),
            "kn": (
                "🇩🇪 **ಜರ್ಮನಿ Chancenkarte ಮತ್ತು EU Blue Card:**\n\n"
                "• **Chancenkarte (ಅವಕಾಶ ಕಾರ್ಡ್):** ಜಾಬ್ ಆಫರ್ ಇಲ್ಲದೆಯೇ ಜರ್ಮನಿಯಲ್ಲಿ 1 ವರ್ಷ ಕೆಲಸ ಹುಡುಕಲು ಅನುಮತಿ ನೀಡುತ್ತದೆ (ಕನಿಷ್ಠ 6 ಅಂಕಗಳು ಅಗತ್ಯ).\n"
                "• **EU Blue Card:** ಕಂಪನಿ ಉದ್ಯೋಗ ಒಪ್ಪಂದವಿರುವವರಿಗೆ ವಾರ್ಷಿಕ €45,300 (IT/STEM ಗೆ €41,041) ವೇತನ ಮಿತಿಯಲ್ಲಿ ಕೇವಲ 21 ತಿಂಗಳಲ್ಲಿ PR ನೀಡುತ್ತದೆ."
            ),
            "hi": (
                "🇩🇪 **जर्मनी Chancenkarte और EU Blue Card:**\n\n"
                "• **Chancenkarte (अपॉर्चुनिटी कार्ड):** बिना जॉब ऑफर के जर्मनी में 1 वर्ष नौकरी तलाशने का अवसर (न्यूनतम 6 अंक आवश्यक)।\n"
                "• **EU Blue Card:** डिग्री और रोजगार अनुबंध पर मात्र 21 से 27 महीनों में स्थायी निवास (PR) प्रदान करता है।"
            )
        }
    },

    # 7. FACTORS DECIDING VISA SCORE
    {
        "id": "factors_deciding_score",
        "keywords": [
            "what factors decide my visa score result",
            "how is visa eligibility score calculated",
            "factors affecting visa approval chance",
            "ಫಲಿತಾಂಶ ನಿರ್ಧರಿಸುವ ಅಂಶಗಳು ಯಾವುವು",
            "परिणाम तय करने वाले कारक क्या हैं"
        ],
        "answers": {
            "en": (
                "🔍 **6 Key Factors That Decide Your Visa Score & Eligibility:**\n\n"
                "1. **Age:** Ages 20 to 29 receive maximum points across points matrices.\n"
                "2. **Education:** Master's degrees and two or more credentials award highest points.\n"
                "3. **Language Competency:** High IELTS/PTE scores (CLB 9 / 8-7-7-7) act as points multipliers.\n"
                "4. **Skilled Work Experience:** 3+ continuous years in verified skilled occupations.\n"
                "5. **Employer Job Offer / Sponsorship:** Confirmed LMIA/CoS yields the largest single point boost.\n"
                "6. **Settlement Bank Balance:** Verifiable liquid funds proving you will not become a public charge."
            ),
            "kn": (
                "🔍 **ನಿಮ್ಮ ವೀಸಾ ಫಲಿತಾಂಶವನ್ನು ನಿರ್ಧರಿಸುವ ಮುಖ್ಯ 6 ಅಂಶಗಳು:**\n\n"
                "1. **ವಯಸ್ಸು:** 20 ರಿಂದ 29 ವರ್ಷದವರಿಗೆ ಗರಿಷ್ಠ ಅಂಕಗಳು.\n"
                "2. **ಶಿಕ್ಷಣ:** ಮಾನ್ಯತೆ ಪಡೆದ ಪದವಿ ಅಥವಾ Master's.\n"
                "3. **ಭಾಷಾ ಸ್ಕೋರ್:** IELTS 7.5+ ಹೆಚ್ಚಿನ ಪಾಯಿಂಟ್‌ಗಳನ್ನು ನೀಡುತ್ತದೆ.\n"
                "4. **ಕೆಲಸದ ಅನುಭವ:** 3+ ವರ್ಷಗಳ ನುರಿತ ಅನುಭವ.\n"
                "5. **ಜಾಬ್ ಆಫರ್:** ಕಂಪನಿಯಿಂದ ಅಧಿಕೃತ ಉದ್ಯೋಗ ಪತ್ರವಿದ್ದರೆ ಗರಿಷ್ಠ ಬೋನಸ್.\n"
                "6. **ಬ್ಯಾಂಕ್ ಉಳಿತಾಯ:** ಅಗತ್ಯವಿರುವ ಹಣಕಾಸಿನ ಪುರಾವೆ."
            ),
            "hi": (
                "🔍 **वीजा परिणाम तय करने वाले मुख्य 6 कारक:**\n\n"
                "1. **आयु:** 20 से 29 वर्ष के आवेदकों को सर्वाधिक अंक मिलते हैं।\n"
                "2. **शिक्षा:** Master's अथवा दोहरी डिग्री से अधिकतम पॉइंट्स मिलते हैं।\n"
                "3. **भाषा स्कोर:** IELTS/PTE में उच्च बैंड्स पॉइंट्स मल्टीप्लायर का काम करते हैं।\n"
                "4. **कार्य अनुभव:** 3 वर्ष या उससे अधिक का कुशल कार्य अनुभव।\n"
                "5. **जॉब ऑफर:** कंपनी से वैध जॉब ऑफर होने से स्कोर में सबसे बड़ा उछाल आता है।\n"
                "6. **बैंक बैलेंस:** देश में बसने के लिए पर्याप्त वित्तीय फंड।"
            )
        }
    },

    # 8. SPOUSE & FAMILY WORK RIGHTS
    {
        "id": "spouse_family_work_rights",
        "keywords": [
            "can my wife work in canada australia uk germany",
            "bring spouse wife husband children kids family",
            "can spouse work on work permit sowp dependent visa",
            "child schooling education rights on work permit"
        ],
        "answers": {
            "en": (
                "👨‍👩‍👧 **Spouse, Dependent & Family Immigration Rights:**\n\n"
                "• **Canada:** Spouses of skilled workers (TEER 0, 1, 2, 3) are eligible for a **Spouse Open Work Permit (SOWP)**, allowing unrestricted full-time work for any Canadian employer. Minor children can attend public schools tuition-free.\n"
                "• **Australia:** Dependants on Subclasses 189, 190, 491, or 482 receive full Australian work and study rights.\n"
                "• **United Kingdom:** Skilled Worker holders can bring a spouse and minor children; spouses have full UK employment rights.\n"
                "• **Germany:** EU Blue Card holders enjoy automatic family reunification with immediate, unrestricted employment rights for their spouse without requiring German proficiency."
            ),
            "kn": (
                "👨‍👩‍👧 **ಕುಟುಂಬ, ಸಂಗಾತಿ ಮತ್ತು ಮಕ್ಕಳ ವೀಸಾ ಹಕ್ಕುಗಳು:**\n\n"
                "• **ಕೆನಡಾ:** ನುರಿತ ವೀಸಾ ಹೊಂದಿರುವವರ ಸಂಗಾತಿಗೆ **Spouse Open Work Permit (SOWP)** ದೊರೆಯುತ್ತದೆ. ಅವರು ಯಾವುದೇ ಕಂಪನಿಯಲ್ಲಿ ಕೆಲಸ ಮಾಡಬಹುದು ಮತ್ತು ಮಕ್ಕಳಿಗೆ ಉಚಿತ ಶಾಲಾ ಶಿಕ್ಷಣ ಲಭ್ಯವಿದೆ.\n"
                "• **ಆಸ್ಟ್ರೇಲಿಯಾ, ಯುಕೆ, ಜರ್ಮನಿ:** ಸಂಗಾತಿ ಮತ್ತು ಮಕ್ಕಳು ಡಿಪೆಂಡೆಂಟ್ ವೀಸಾದಲ್ಲಿ ನಿಮ್ಮೊಂದಿಗೆ ಬರಬಹುದು ಮತ್ತು ಪೂರ್ಣಾವಧಿ ಕೆಲಸ ಮಾಡಬಹುದು."
            ),
            "hi": (
                "👨‍👩‍👧 **जीवनसाथी (पति/पत्नी) एवं बच्चों के वीजा अधिकार:**\n\n"
                "• **कनाडा:** कुशल कामगारों के जीवनसाथी को **Spouse Open Work Permit (SOWP)** मिलता है, जिससे वे किसी भी कंपनी में काम कर सकते हैं। बच्चों को मुफ्त स्कूली शिक्षा मिलती है।\n"
                "• **ऑस्ट्रेलिया, यूके, जर्मनी:** डिपेंडेंट वीजा पर जीवनसाथी को पूर्ण कार्य अधिकार प्राप्त होते हैं।"
            )
        }
    },

    # 9. TOURIST / VISITOR TO WORK PERMIT CONVERSION
    {
        "id": "visitor_to_work_permit",
        "keywords": [
            "can i convert visitor visa to work permit",
            "tourist visa to work visa in canada australia",
            "convert tourist visa change status to work",
            "can tourist apply for job offer"
        ],
        "answers": {
            "en": (
                "🔄 **Converting Visitor / Tourist Visa to Work Permit:**\n\n"
                "• **Canada:** Under temporary IRCC public policy, visitors currently in Canada who secure a genuine, positive **LMIA job offer** can apply for an employer-specific work permit from inside Canada without leaving.\n"
                "• **Australia:** Tourist visas (Subclass 600) do not allow working. If you find an employer willing to sponsor you on Subclass 482, you can apply onshore provided your tourist visa does NOT contain Condition 8503 ('No Further Stay').\n"
                "• **United Kingdom & Germany:** You cannot switch directly from standard tourist status to a skilled worker visa inside the country; you must apply from your legal residence country."
            ),
            "kn": (
                "🔄 **ಪ್ರವಾಸಿ ವೀಸಾದಿಂದ ಉದ್ಯೋಗ ವೀಸಾಗೆ ಬದಲಾವಣೆ:**\n\n"
                "• **ಕೆನಡಾ:** ಪ್ರವಾಸಿ ವೀಸಾದಲ್ಲಿರುವಾಗ ಅಧಿಕೃತ **LMIA ಜಾಬ್ ಆಫರ್** ಪಡೆದರೆ ದೇಶ ಬಿಡದೆಯೇ ವರ್ಕ್ ಪರ್ಮಿಟ್‌ಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಬಹುದು.\n"
                "• **ಆಸ್ಟ್ರೇಲಿಯಾ & ಯುಕೆ:** ಪ್ರವಾಸಿ ವೀಸಾದಲ್ಲಿ ನೇರವಾಗಿ ಕೆಲಸ ಮಾಡಲು ಅನುಮತಿ ಇಲ್ಲ; ನಿಯಮಾನುಸಾರ ಕಂಪನಿ ಸ್ಪಾನ್ಸರ್‌ಶಿಪ್ ಪಡೆದು ಬದಲಾಯಿಸಬೇಕು."
            ),
            "hi": (
                "🔄 **विजिटर / टूरिस्ट वीजा से वर्क परमिट में बदलाव:**\n\n"
                "• **कनाडा:** टूरिस्ट वीजा पर रहते हुए वैध **LMIA जॉब ऑफर** मिलने पर आप देश छोड़े बिना वर्क परमिट के लिए आवेदन कर सकते हैं।\n"
                "• **ऑस्ट्रेलिया & यूके:** टूरिस्ट वीजा पर सीधे काम करने की अनुमति नहीं होती; प्रायोजन मिलने पर उचित कानूनी प्रक्रिया से आवेदन करना होता है।"
            )
        }
    },

    # 10. OPEN VS CLOSED WORK PERMIT
    {
        "id": "open_vs_closed_work_permit",
        "keywords": [
            "difference between open and closed work permit",
            "open work permit vs employer specific closed permit",
            "can i change job on closed work permit",
            "what happens if i lose job on closed permit"
        ],
        "answers": {
            "en": (
                "📑 **Open Work Permit vs Closed (Employer-Specific) Work Permit:**\n\n"
                "• **Open Work Permit:** Not tied to any employer. You can work for any company, anywhere in Canada, and switch jobs freely. Granted to PGWP graduates, spouses of skilled workers, and PR applicants.\n"
                "• **Closed Work Permit:** Strictly tied to the specific employer, role, and location printed on the permit. Requires an LMIA/CoS.\n\n"
                "💡 **If you lose your job on a closed permit:** You retain legal status until permit expiry, but you cannot legally work for any other employer until they issue you a new LMIA and you receive a new permit."
            ),
            "kn": (
                "📑 **ಓಪನ್ ವರ್ಕ್ ಪರ್ಮಿಟ್ ಮತ್ತು ಕ್ಲೋಸ್ಡ್ ವರ್ಕ್ ಪರ್ಮಿಟ್ ವ್ಯತ್ಯಾಸ:**\n\n"
                "• **Open Work Permit:** ಯಾವುದೇ ಕಂಪನಿಯಲ್ಲಿ ಕೆಲಸ ಮಾಡುವ ಸಂಪೂರ್ಣ ಸ್ವಾತಂತ್ರ್ಯವಿರುತ್ತದೆ.\n"
                "• **Closed Work Permit:** ವೀಸಾದಲ್ಲಿ ನಮೂದಿಸಲಾದ ನಿರ್ದಿಷ್ಟ ಕಂಪನಿಯಲ್ಲಿ ಮಾತ್ರ ಕೆಲಸ ಮಾಡಬೇಕು. ಕಂಪನಿ ಬದಲಾಯಿಸಲು ಹೊಸ ಅನುಮತಿ ಬೇಕು."
            ),
            "hi": (
                "📑 **ओपन वर्क परमिट बनाम क्लोज्ड वर्क परमिट:**\n\n"
                "• **Open Work Permit:** किसी भी योग्य नियोक्ता के पास काम करने की स्वतंत्रता होती है।\n"
                "• **Closed Work Permit:** केवल परमिट पर दर्ज विशेष कंपनी से बंधा होता है। नौकरी बदलने के लिए नया LMIA व नया परमिट आवश्यक है।"
            )
        }
    },

    # 11. IT & SOFTWARE PROFESSIONALS
    {
        "id": "it_software_engineers_pathways",
        "keywords": [
            "software engineer developer it jobs canada pr",
            "tech visa pathway computer science programmer",
            "stem express entry category draws noc 21231",
            "acs skills assessment software developer australia"
        ],
        "answers": {
            "en": (
                "💻 **Immigration Pathways for IT & Software Professionals:**\n\n"
                "• **Canada (STEM Draws):** Software Engineers (NOC 21231), Developers (NOC 21232), and Data Scientists qualify for targeted **STEM Category-Based Express Entry Draws**, which invite candidates at lower CRS cutoffs (480–495) compared to general draws (520+).\n"
                "• **Australia (ACS):** Requires passing the **Australian Computer Society (ACS)** skills assessment. Competitive points totals for developers are typically 85–95 points.\n"
                "• **Germany:** IT specialists qualify for reduced EU Blue Card salary floors (€41,041 EUR) and can qualify even without a university degree if holding 3+ years of verifiable IT experience."
            ),
            "kn": (
                "💻 **ಐಟಿ ಮತ್ತು ಸಾಫ್ಟ್‌ವೇರ್ ವೃತ್ತಿಪರರ ವೀಸಾ ಮಾರ್ಗಗಳು:**\n\n"
                "• **ಕೆನಡಾ (STEM ಡ್ರಾ):** ಸಾಫ್ಟ್‌ವೇರ್ ಡೆವಲಪರ್‌ಗಳಿಗೆ ಕಡಿಮೆ CRS ಅಂಕಗಳಲ್ಲೂ (480+) ನೇರ Express Entry PR ಆಹ್ವಾನ ದೊರೆಯುತ್ತದೆ.\n"
                "• **ಆಸ್ಟ್ರೇಲಿಯಾ:** ACS ಸ್ಕಿಲ್ ಅಸೆಸ್‌ಮೆಂಟ್ ಅಗತ್ಯ; 85+ ಅಂಕಗಳು ಸ್ಪರ್ಧೆಯಲ್ಲಿ ಗೆಲ್ಲಲು ಬೇಕು.\n"
                "• **ಜರ್ಮನಿ:** ಐಟಿ ವೃತ್ತಿಪರರಿಗೆ ಕಡಿಮೆ ವೇತನ ಮಿತಿಯಲ್ಲಿ (€41,041) EU Blue Card ದೊರೆಯುತ್ತದೆ."
            ),
            "hi": (
                "💻 **आईटी एवं सॉफ्टवेयर प्रोफेशनल्स के लिए वीजा मार्ग:**\n\n"
                "• **कनाडा (STEM Category):** सॉफ्टवेयर डेवलपर्स के लिए विशेष STEM कैटेगरी ड्रॉ में कम CRS स्कोर (480–495) पर भी सीधे PR मिलता है।\n"
                "• **ऑस्ट्रेलिया:** ACS स्किल्स असेसमेंट आवश्यक है। 85+ पॉइंट्स प्रतिस्पर्धी माने जाते हैं।\n"
                "• **जर्मनी:** आईटी पेशेवरों के लिए रियायती वेतन (€41,041) पर EU Blue Card उपलब्ध है।"
            )
        }
    },

    # 12. HEALTHCARE & NURSES
    {
        "id": "healthcare_nurses_doctors",
        "keywords": [
            "nurse nursing doctor healthcare workers visa",
            "healthcare category draws express entry",
            "uk health and care worker visa nhs"
        ],
        "answers": {
            "en": (
                "🏥 **Healthcare & Nursing Immigration Fast-Tracks:**\n\n"
                "• **Canada:** Registered Nurses (NOC 31301) benefit from **Healthcare Category Draws**, where CRS cutoff scores have dropped as low as 420–460 points.\n"
                "• **United Kingdom:** The **Health and Care Worker Visa** provides fast-track 3-week processing, lower visa fees, and an exemption from the £1,035/year Immigration Health Surcharge.\n"
                "• **Australia:** Highest state demand under Subclasses 190 and 491 with priority ANMAC skills assessment."
            ),
            "kn": (
                "🏥 **ಆರೋಗ್ಯ ಮತ್ತು ನರ್ಸಿಂಗ್ ಸಿಬ್ಬಂದಿಯ ವೀಸಾ ಸೌಲಭ್ಯಗಳು:**\n\n"
                "• **ಕೆನಡಾ:** ನರ್ಸ್‌ಗಳು ಮತ್ತು ವೈದ್ಯರಿಗೆ Healthcare Category ಡ್ರಾನಲ್ಲಿ ಕೇವಲ 430-450 CRS ಅಂಕಗಳಿದ್ದರೂ PR ಸಿಗುತ್ತದೆ.\n"
                "• **ಯುಕೆ:** Health and Care Worker ವೀಸಾದಲ್ಲಿ ಶುಲ್ಕ ವಿನಾಯಿತಿ ಮತ್ತು ಕೇವಲ 3 ವಾರಗಳಲ್ಲಿ ವೇಗದ ವೀಸಾ ದೊರೆಯುತ್ತದೆ."
            ),
            "hi": (
                "🏥 **हेल्थकेयर और नर्सिंग प्रोफेशनल्स के लिए नियम:**\n\n"
                "• **कनाडा:** नर्सेज और मेडिकल स्टाफ के लिए Healthcare ड्रॉ में बहुत कम कटऑफ (430–450 CRS) पर भी PR मिलता है।\n"
                "• **यूके:** Health & Care Worker वीजा पर स्वास्थ्य अधिभार (IHS) से पूरी छूट मिलती है और 3 सप्ताह में प्रक्रिया पूरी होती है।"
            )
        }
    },

    # 13. PROCESSING TIMES
    {
        "id": "processing_times_and_timelines",
        "keywords": [
            "how long does visa take processing time timeline",
            "processing duration for canada express entry",
            "how many months weeks to get visa decision"
        ],
        "answers": {
            "en": (
                "⏱️ **Official Standard Processing Timelines (2024–2025):**\n\n"
                "• **Canada Express Entry (PR):** Approximately **5 to 6 months** from full e-APR submission.\n"
                "• **Canada Work Permit (LMIA):** Approximately **8 to 14 weeks** (or 2 weeks via Global Skills Strategy).\n"
                "• **Australia Subclass 189 / 190:** Approximately **6 to 9 months** after lodging application.\n"
                "• **UK Skilled Worker Visa:** Approximately **3 weeks** (outside UK); 5 days with Priority Service.\n"
                "• **Germany Blue Card / Chancenkarte:** Approximately **4 to 8 weeks** at your local German embassy."
            ),
            "kn": (
                "⏱️ **ವೀಸಾ ಪರಿಶೀಲನಾ ಸಮಯ (Processing Time):**\n\n"
                "• **ಕೆನಡಾ Express Entry:** ಸುಮಾರು **5 ರಿಂದ 6 ತಿಂಗಳು**.\n"
                "• **ಯುಕೆ Skilled Worker:** ಕೇವಲ **3 ವಾರಗಳು**.\n"
                "• **ಆಸ್ಟ್ರೇಲಿಯಾ Subclasses 189/190:** ಸುಮಾರು **6 ರಿಂದ 9 ತಿಂಗಳು**.\n"
                "• **ಜರ್ಮನಿ Blue Card:** ಸುಮಾರು **4 ರಿಂದ 8 ವಾರಗಳು**."
            ),
            "hi": (
                "⏱️ **वीजा प्रोसेसिंग में लगने वाला समय:**\n\n"
                "• **कनाडा Express Entry:** लगभग **5 से 6 महीने**।\n"
                "• **यूके Skilled Worker:** मात्र **3 सप्ताह**।\n"
                "• **ऑस्ट्रेलिया 189/190:** लगभग **6 से 9 महीने**।\n"
                "• **जर्मनी Blue Card:** लगभग **4 से 8 सप्ताह**।"
            )
        }
    },

    # 14. VISA FEES & REFUND POLICY
    {
        "id": "fees_and_refunds",
        "keywords": [
            "visa application fee cost how much price charges",
            "is visa fee refundable refund policy",
            "express entry fee biometric cost rprf fee"
        ],
        "answers": {
            "en": (
                "💳 **Official Visa Application Fees & Refund Policy:**\n\n"
                "• **Canada Express Entry:** Processing Fee CAD **$950** + Right of Permanent Residence Fee (RPRF) CAD **$575** + Biometrics CAD **$85** (Total ~CAD $1,610 per adult).\n"
                "• **Australia Subclass 189/190:** Primary Applicant fee is AUD **$4,765**.\n"
                "• **UK Skilled Worker:** Visa fee (£719 to £1,420) + Immigration Health Surcharge of **£1,035/year**.\n\n"
                "⚠️ **Refund Policy:** Government application processing fees are **strictly non-refundable** once processing begins, whether your visa is approved or refused."
            ),
            "kn": (
                "💳 **ವೀಸಾ ಶುಲ್ಕ ಮತ್ತು ರೀಫಂಡ್ ನಿಯಮಗಳು:**\n\n"
                "• **ಕೆನಡಾ:** ವಯಸ್ಕರಿಗೆ ಒಟ್ಟು ಶುಲ್ಕ ಸುಮಾರು CAD **$1,610**.\n"
                "• **ಆಸ್ಟ್ರೇಲಿಯಾ:** Subclass 189/190 ಶುಲ್ಕ AUD **$4,765**.\n"
                "• **ಯುಕೆ:** ವೀಸಾ ಶುಲ್ಕ £719+ ಜೊತೆಗೆ ಆರೋಗ್ಯ ವಿಮೆ (IHS) ವಾರ್ಷಿಕ £1,035.\n"
                "• **ರೀಫಂಡ್:** ಸರ್ಕಾರಿ ಅರ್ಜಿ ಶುಲ್ಕವನ್ನು **ಹಿಂತಿರುಗಿಸಲಾಗುವುದಿಲ್ಲ (Non-refundable)**."
            ),
            "hi": (
                "💳 **वीजा आवेदन शुल्क एवं रिफंड नीति:**\n\n"
                "• **कनाडा:** प्रति वयस्क कुल शुल्क लगभग CAD **$1,610**।\n"
                "• **ऑस्ट्रेलिया:** आवेदन शुल्क AUD **$4,765**।\n"
                "• **यूके:** वीजा शुल्क £719+ एवं वार्षिक IHS शुल्क £1,035।\n"
                "• **रिफंड नीति:** सरकारी वीजा शुल्क **रिफंडेबल नहीं होता**।"
            )
        }
    },

    # 15. AGE LIMITS & POINTS DECAY
    {
        "id": "age_limits_and_decay",
        "keywords": [
            "age limit for pr work visa age points decay",
            "what is maximum age to apply for canada australia",
            "can i get pr after 35 40 45 years old"
        ],
        "answers": {
            "en": (
                "🎂 **Age Limits & Points Depreciation:**\n\n"
                "• **Canada Express Entry:** Max age points (110 pts) awarded for **ages 20 to 29**. Starting at age 30, you lose **5 points per year**, reaching 0 points at age 45. There is no maximum age ban, but older applicants must compensate via PNP (+600) or high language/degree scores.\n"
                "• **Australia SkillSelect:** Strict hard limit: you must be **under 45 years of age** at the time of invitation.\n"
                "• **UK Skilled Worker & Germany Blue Card:** **No age limit** exists; eligibility is based on job offer, salary, and qualifications."
            ),
            "kn": (
                "🎂 **ವಯಸ್ಸಿನ ಮಿತಿ ಮತ್ತು ಅಂಕಗಳ ನಿಯಮ:**\n\n"
                "• **ಕೆನಡಾ:** 20 ರಿಂದ 29 ವರ್ಷದವರಿಗೆ ಗರಿಷ್ಠ (110) ಅಂಕಗಳು ದೊರೆಯುತ್ತವೆ. 30 ರ ನಂತರ ಪ್ರತಿ ವರ್ಷ 5 ಅಂಕಗಳು ಕಡಿಮೆಯಾಗುತ್ತವೆ.\n"
                "• **ಆಸ್ಟ್ರೇಲಿಯಾ:** ಕಟ್ಟುನಿಟ್ಟಿನ ನಿಯಮ: **45 ವರ್ಷಕ್ಕಿಂತ ಕಡಿಮೆ** ವಯಸ್ಸಿನವರು ಮಾತ್ರ ನುರಿತ PR ಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಬಹುದು.\n"
                "• **ಯುಕೆ ಮತ್ತು ಜರ್ಮನಿ:** ಯಾವುದೇ ವಯಸ್ಸಿನ ಮಿತಿ ಇಲ್ಲ."
            ),
            "hi": (
                "🎂 **आयु सीमा और पॉइंट्स का नियम:**\n\n"
                "• **कनाडा:** 20 से 29 वर्ष के बीच अधिकतम (110) पॉइंट्स मिलते हैं। 30 के बाद हर साल 5 पॉइंट्स घटते हैं।\n"
                "• **ऑस्ट्रेलिया:** सख्त नियम: आमंत्रण के समय उम्र **45 वर्ष से कम** होनी चाहिए।\n"
                "• **यूके और जर्मनी:** वर्क वीजा के लिए कोई अधिकतम आयु सीमा नहीं है।"
            )
        }
    },

    # 16. ECA & WES CREDENTIAL ASSESSMENT
    {
        "id": "eca_credential_assessment_wes",
        "keywords": [
            "what is eca wes evaluation credential assessment",
            "how to evaluate indian degree for canada",
            "foreign degree verification education points"
        ],
        "answers": {
            "en": (
                "🎓 **Educational Credential Assessment (ECA) & WES Evaluation:**\n\n"
                "• **Purpose:** Confirms that your foreign university degree is valid and equal to Canadian standards.\n"
                "• **Top Designated Bodies:** World Education Services (**WES** - takes ~35 days), ICES, IQAS, CES.\n"
                "• **Transcripts:** Must be official sealed transcripts sent directly by your university or through authorized digital services (DigiLocker / TrueCopy).\n"
                "• Master's degree evaluations unlock highest points tier under Express Entry."
            ),
            "kn": (
                "🎓 **ECA ಮತ್ತು WES ಪ್ರಮಾಣಪತ್ರ ಮೌಲ್ಯಮಾಪನ:**\n\n"
                "• ನಿಮ್ಮ ಪದವಿಯು ಕೆನಡಾದ ಶಿಕ್ಷಣಕ್ಕೆ ಸಮಾನವಾಗಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಲು **ECA (WES)** ಕಡ್ಡಾಯವಾಗಿದೆ.\n"
                "• ವಿಶ್ವವಿದ್ಯಾಲಯದಿಂದ ಅಂಕಪಟ್ಟಿಗಳನ್ನು ನೇರವಾಗಿ WES ಗೆ ಕಳುಹಿಸಬೇಕು."
            ),
            "hi": (
                "🎓 **ECA और WES डिग्री मूल्यांकन:**\n\n"
                "• आपकी डिग्री कनाडाई मानकों के अनुसार मान्य है या नहीं, यह प्रमाणित करने के लिए **ECA (WES)** अनिवार्य है।\n"
                "• आधिकारिक ट्रांसक्रिप्ट सीधे WES को भेजने होते हैं।"
            )
        }
    },

    # 17. IELTS ACADEMIC VS GENERAL
    {
        "id": "ielts_academic_vs_general",
        "keywords": [
            "can i use ielts academic for canada pr work visa",
            "difference between ielts general and academic for immigration",
            "which english test is required for pr celpip or ielts"
        ],
        "answers": {
            "en": (
                "📝 **IELTS Academic vs General for Immigration:**\n\n"
                "• **Strict Rule:** For Permanent Residency (Canada / Australia) and UK Work Visas, **IELTS Academic is NOT accepted**.\n"
                "• **Accepted Formats:** Must be **IELTS General Training**, **CELPIP-General**, or **PTE Core** (for Canada); or **PTE Academic / IELTS General** (for Australia).\n"
                "• Academic is strictly for student admissions and medical licensing.\n"
                "• Score validity is exactly **2 years**."
            ),
            "kn": (
                "📝 **IELTS Academic vs General ವ್ಯತ್ಯಾಸ:**\n\n"
                "• **ಕಡ್ಡಾಯ ನಿಯಮ:** ಕೆನಡಾ ಮತ್ತು ಆಸ್ಟ್ರೇಲಿಯಾ PR ಗಾಗಿ **IELTS General Training** ಅಥವಾ **CELPIP** ಮಾತ್ರ ಮಾನ್ಯವಾಗಿರುತ್ತದೆ. Academic ಒಪ್ಪುವುದಿಲ್ಲ.\n"
                "• ಫಲಿತಾಂಶವು 2 ವರ್ಷಗಳವರೆಗೆ ಮಾತ್ರ ಮಾನ್ಯವಾಗಿರುತ್ತದೆ."
            ),
            "hi": (
                "📝 **IELTS Academic बनाम General Training:**\n\n"
                "• **सख्त नियम:** PR के लिए केवल **IELTS General Training**, **CELPIP** या **PTE Core** ही मान्य है। Academic स्वीकार नहीं किया जाता।\n"
                "• स्कोर 2 वर्ष तक वैध रहता है।"
            )
        }
    },

    # 18. PROVINCIAL NOMINEE PROGRAMS (PNP)
    {
        "id": "pnp_provincial_nomination",
        "keywords": [
            "what is pnp provincial nominee program how to get",
            "ontario oinp bc pnp alberta aaip nomination",
            "how to get 600 crs points boost"
        ],
        "answers": {
            "en": (
                "🍁 **Provincial Nominee Programs (PNP) Decoded:**\n\n"
                "• **The +600 Points Boost:** Receiving a provincial nomination awards an automatic **+600 CRS points** in Express Entry, guaranteeing an Invitation to Apply (ITA) in the very next draw.\n"
                "• **Key Streams:** Ontario (OINP Human Capital), Alberta (AAIP Accelerated Tech & Healthcare), British Columbia (BC PNP Tech), and Saskatchewan (SINP Occupations In-Demand).\n"
                "• Many PNP streams invite applicants directly from the Express Entry pool **without requiring a job offer**."
            ),
            "kn": (
                "🍁 **ಪ್ರೊವಿನ್ಶಿಯಲ್ ನಾಮಿನೇಷನ್ (PNP) ಮಾಹಿತಿ:**\n\n"
                "• ಕೆನಡಾದ ಯಾವುದೇ ರಾಜ್ಯದಿಂದ (Ontario, Alberta, BC) ನಾಮನಿರ್ದೇಶನ ದೊರೆತರೆ ನೇರವಾಗಿ **+600 ಬೋನಸ್ CRS ಅಂಕಗಳು** ದೊರೆಯುತ್ತವೆ.\n"
                "• ಇದು ಮುಂದಿನ ಡ್ರಾನಲ್ಲಿ 100% ಖಚಿತವಾಗಿ PR ಆಹ್ವಾನ (ITA) ದೊರೆಯುವುದನ್ನು ಖಾತರಿಪಡಿಸುತ್ತದೆ."
            ),
            "hi": (
                "🍁 **प्रोविंशियल नॉमिनी प्रोग्राम (PNP):**\n\n"
                "• किसी कनाडाई राज्य से नॉमिनेशन मिलने पर **+600 बोनस CRS पॉइंट्स** मिलते हैं।\n"
                "• इससे अगले ही एक्सप्रेस एंट्री ड्रॉ में 100% पक्का PR इनविटेशन (ITA) प्राप्त हो जाता है।"
            )
        }
    },

    # 19. COUNTRY COMPARISON
    {
        "id": "country_comparison_easiest",
        "keywords": [
            "which country is easiest to get pr between canada australia uk germany",
            "best country to immigrate compare destinations",
            "canada vs australia vs uk vs germany"
        ],
        "answers": {
            "en": (
                "🌐 **Destination Comparison (Canada vs Australia vs UK vs Germany):**\n\n"
                "• **Canada:** Best for direct Permanent Residence (PR) without a job offer via Express Entry and PNP. Fast citizenship in 3 years of PR.\n"
                "• **Germany:** Fastest direct transition to European settlement; EU Blue Card grants PR in just 21 months with B1 German; Chancenkarte allows 1-year job hunting.\n"
                "• **Australia:** Highest wages and quality of life; requires skills assessment (ACS/VETASSESS) and 85+ competitive points.\n"
                "• **United Kingdom:** Fastest processing times (3 weeks), but requires an employer job offer with £38,700 salary floor; leads to ILR (PR) in 5 years."
            ),
            "kn": (
                "🌐 **ದೇಶಗಳ ಹೋಲಿಕೆ (ಕೆನಡಾ, ಆಸ್ಟ್ರೇಲಿಯಾ, ಯುಕೆ, ಜರ್ಮನಿ):**\n\n"
                "• **ಕೆನಡಾ:** ಜಾಬ್ ಆಫರ್ ಇಲ್ಲದೆಯೇ ನೇರ PR ಪಡೆಯಲು ಅತ್ಯುತ್ತಮ ಆಯ್ಕೆ (Express Entry & PNP).\n"
                "• **ಜರ್ಮನಿ:** EU Blue Card ಮೂಲಕ ಕೇವಲ 21 ತಿಂಗಳಲ್ಲಿ PR ಪಡೆಯಬಹುದು.\n"
                "• **ಆಸ್ಟ್ರೇಲಿಯಾ:** ಅತ್ಯುತ್ತಮ ವೇತನ ಮತ್ತು ಜೀವನಮಟ್ಟ; 85+ ಅಂಕಗಳು ಅಗತ್ಯ.\n"
                "• **ಯುಕೆ:** ಕೇವಲ 3 ವಾರಗಳಲ್ಲಿ ವೇಗದ ವೀಸಾ, ಆದರೆ £38,700 ಕಂಪನಿ ಜಾಬ್ ಆಫರ್ ಕಡ್ಡಾಯ."
            ),
            "hi": (
                "🌐 **देशों की तुलना (कनाडा, ऑस्ट्रेलिया, यूके, जर्मनी):**\n\n"
                "• **कनाडा:** बिना जॉब ऑफर के सीधे स्थायी निवास (PR) के लिए सबसे लोकप्रिय।\n"
                "• **जर्मनी:** EU Blue Card से मात्र 21 महीनों में PR प्राप्त किया जा सकता है।\n"
                "• **ऑस्ट्रेलिया:** सबसे उच्च वेतन और जीवन स्तर; 85+ पॉइंट्स पर PR।\n"
                "• **यूके:** 3 सप्ताह में तेज वीजा, लेकिन £38,700 कंपनी जॉब ऑफर अनिवार्य।"
            )
        }
    },

    # 20. MEDICAL & POLICE CLEARANCE
    {
        "id": "medical_police_clearance_inadmissibility",
        "keywords": [
            "medical exam police clearance certificate pcc",
            "what if medical fails health inadmissibility",
            "criminal inadmissibility police check"
        ],
        "answers": {
            "en": (
                "🩺 **Medical Exams & Police Clearance Certificates (PCC):**\n\n"
                "• **Medical Exam:** Must be done through an authorized **Panel Physician**. Checks for active communicable diseases or excessive demand on public health care.\n"
                "• **Police Clearance (PCC):** Mandatory for every country where you lived for **6 consecutive months or more** since turning 18.\n"
                "• Must be clear of serious criminal convictions to satisfy immigration security admissibility."
            ),
            "kn": (
                "🩺 **ವೈದ್ಯಕೀಯ ಪರೀಕ್ಷೆ ಮತ್ತು ಪೋಲಿಸ್ ಕ್ಲಿಯರೆನ್ಸ್ (PCC):**\n\n"
                "• ಅಧಿಕೃತ ಪ್ಯಾನಲ್ ವೈದ್ಯರಿಂದ ಮಾತ್ರ ಮೆಡಿಕಲ್ ಟೆಸ್ಟ್ ಮಾಡಿಸಬೇಕು.\n"
                "• 18 ವರ್ಷ ದಾಟಿದ ನಂತರ 6 ತಿಂಗಳಿಗಿಂತ ಹೆಚ್ಚು ಕಾಲ ನೆಲೆಸಿದ ಪ್ರತಿಯೊಂದು ದೇಶದ PCC ಪ್ರಮಾಣಪತ್ರ ಕಡ್ಡಾಯ."
            ),
            "hi": (
                "🩺 **मेडिकल जांच और पुलिस क्लीयरेंस (PCC):**\n\n"
                "• केवल अधिकृत पैनल डॉक्टर से ही मेडिकल टेस्ट मान्य होता है।\n"
                "• 18 वर्ष की आयु के बाद 6 महीने से अधिक रहे प्रत्येक देश का PCC देना अनिवार्य है।"
            )
        }
    },

    # 21. APPLY WITHOUT AGENT / LAWYER
    {
        "id": "can_apply_without_agent",
        "keywords": [
            "do i need a lawyer consultant agent to apply",
            "can i apply for visa myself without consultant",
            "official government immigration portal diy"
        ],
        "answers": {
            "en": (
                "🛡️ **Applying Independently vs Using an Agent:**\n\n"
                "• **Yes, You Can Apply 100% Independently:** Immigration departments (IRCC, DHA, UKVI) design their systems for self-service applicants. No agent has special access or can guarantee an approval.\n"
                "• Always use official government portals: `.gc.ca` (Canada), `.gov.au` (Australia), `.gov.uk` (UK), and `.diplo.de` (Germany).\n"
                "• If you do hire help, ensure they are legally licensed (RCIC in Canada, MARA in Australia)."
            ),
            "kn": (
                "🛡️ **ಸ್ವತಃ ಅರ್ಜಿ ಸಲ್ಲಿಸುವುದು ಹೇಗೆ (ಏಜೆಂಟ್ ಅಗತ್ಯವಿಲ್ಲ):**\n\n"
                "• ನೀವು ಯಾವುದೇ ಏಜೆಂಟ್ ಇಲ್ಲದೆಯೇ ಅಧಿಕೃತ ಸರ್ಕಾರಿ ವೆಬ್‌ಸೈಟ್‌ಗಳಲ್ಲಿ (.gc.ca, .gov.au, .gov.uk) ನೇರವಾಗಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಬಹುದು. ಯಾರೂ ವೀಸಾ ಗ್ಯಾರಂಟಿ ನೀಡಲು ಸಾಧ್ಯವಿಲ್ಲ."
            ),
            "hi": (
                "🛡️ **स्वयं आवेदन बनाम एजेंट:**\n\n"
                "• आप बिना किसी एजेंट के सीधे आधिकारिक सरकारी पोर्टल्स (.gc.ca, .gov.au, .gov.uk) पर आवेदन कर सकते हैं।\n"
                "• कोई भी एजेंट वीजा की गारंटी नहीं दे सकता।"
            )
        }
    },

    # 22. CAREER GAPS & PAST REFUSALS
    {
        "id": "career_gap_and_refusals",
        "keywords": [
            "career gap employment gap visa refusal",
            "how to handle past refusal section 214b",
            "does gap affect visa approval"
        ],
        "answers": {
            "en": (
                "⚖️ **Handling Career Gaps & Previous Visa Refusals:**\n\n"
                "1. **Career Gaps:** A gap in your resume does not disqualify you. Immigration departments evaluate total cumulative qualifying experience. Provide affidavits, upskilling certifications, or legitimate explanations for gaps.\n"
                "2. **Past Visa Refusals:** **Always declare them honestly.** Immigration agencies share biometric data via the Five Eyes alliance. Hiding a refusal leads to a 5-year ban for misrepresentation. Obtain GCMS/case officer notes to address the exact refusal reason in a detailed explanation letter."
            ),
            "kn": (
                "⚖️ **ಕೆಲಸದ ಗ್ಯಾಪ್ ಮತ್ತು ಹಿಂದಿನ ವೀಸಾ ತಿರಸ್ಕಾರವನ್ನು ನಿಭಾಯಿಸುವುದು:**\n\n"
                "• **ಗ್ಯಾಪ್:** ಗ್ಯಾಪ್ ಇದ್ದರೆ ವೀಸಾ ತಿರಸ್ಕೃತವಾಗುವುದಿಲ್ಲ. ಆ ಸಮಯದಲ್ಲಿ ಕಲಿತ ಕೌಶಲ್ಯ ಅಥವಾ ಕಾರಣಗಳನ್ನು ದಾಖಲೆಗಳೊಂದಿಗೆ ವಿವರಿಸಿ.\n"
                "• **ಹಿಂದಿನ ತಿರಸ್ಕಾರ:** ಯಾವತ್ತೂ ಮರೆಮಾಚಬೇಡಿ. ಹಿಂದಿನ ಕಾರಣಗಳನ್ನು ಸರಿಪಡಿಸಿ ವಿವರಣಾತ್ಮಕ ಪತ್ರವನ್ನು ಲಗತ್ತಿಸಿ."
            ),
            "hi": (
                "⚖️ **करियर गैप और पूर्व वीजा अस्वीकृति (Refusal):**\n\n"
                "• **गैप:** गैप से वीजा खारिज नहीं होता। अनुभव और कौशल के वैध प्रमाण प्रस्तुत करें।\n"
                "• **पिछली अस्वीकृति:** कभी भी छुपाएं नहीं। अस्वीकृति के कारणों को दूर करें और स्पष्टीकरण पत्र संलग्न करें।"
            )
        }
    },

    # 23. LMIA & SPONSORSHIP
    {
        "id": "lmia_and_sponsorship",
        "keywords": [
            "what is lmia and how to get employer sponsorship",
            "labour market impact assessment canada points",
            "job offer points express entry"
        ],
        "answers": {
            "en": (
                "🏢 **LMIA & Employer Sponsorship:**\n\n"
                "• An **LMIA (Labour Market Impact Assessment)** is an approval issued by the Canadian government allowing a Canadian employer to hire a foreign worker when no citizen/PR is available.\n"
                "• **Points Value:** Awards **+50 CRS points** for standard TEER 1/2/3 occupations, and **+200 points** for senior executive positions (TEER 00).\n"
                "• A valid LMIA job offer shifts your profile into **Low Risk (High Approval Chance)** and exempts you from settlement proof of funds."
            ),
            "kn": (
                "🏢 **LMIA ಮತ್ತು ಉದ್ಯೋಗ ಸ್ಪಾನ್ಸರ್‌ಶಿಪ್:**\n\n"
                "• ಕೆನಡಾದಲ್ಲಿ ವಿದೇಶಿ ಉದ್ಯೋಗಿಯನ್ನು ನೇಮಿಸಿಕೊಳ್ಳಲು ಉದ್ಯೋಗದಾತರು ಸರ್ಕಾರದಿಂದ ಪಡೆಯುವ ಅನುಮತಿಯೇ **LMIA**.\n"
                "• ಇದು Express Entry ನಲ್ಲಿ **+50 ರಿಂದ +200 ಅಂಕಗಳನ್ನು** ನೀಡುತ್ತದೆ ಮತ್ತು ಪ್ರೊಫೈಲ್ ಅನ್ನು Low Risk ಗೆ ತರುತ್ತದೆ."
            ),
            "hi": (
                "🏢 **LMIA एवं जॉब ऑफर स्पॉन्सरशिप:**\n\n"
                "• कनाडाई कंपनी द्वारा विदेशी कर्मचारी को काम पर रखने के लिए सरकारी अनुमति को **LMIA** कहते हैं।\n"
                "• इससे Express Entry में **+50 से +200 पॉइंट्स** मिलते हैं और प्रोफाइल सीधे Low Risk में आ जाती है।"
            )
        }
    },

    # 24. LANGUAGE TESTS & CLB LEVELS
    {
        "id": "language_ielts_clb_pte",
        "keywords": [
            "ielts clb 9 pte celpip score requirements",
            "what is clb 9 how many points",
            "language test scores for canada"
        ],
        "answers": {
            "en": (
                "🗣️ **Language Testing & CLB 9 Target:**\n\n"
                "• **CLB 9 (IELTS 8.0 Listening, 7.0 Reading, 7.0 Writing, 7.0 Speaking):** The single biggest point multiplier in Canada, unlocking **+50 to +64 skill transferability bonus points**.\n"
                "• **CLB 7 (IELTS 6.0 in each band):** Minimum threshold required to enter the Express Entry pool.\n"
                "• **Accepted Tests:** IELTS General Training, CELPIP-General, PTE Core (Canada); PTE Academic, IELTS General (Australia)."
            ),
            "kn": (
                "🗣️ **ಭಾಷಾ ಪರೀಕ್ಷೆಗಳು & CLB 9 ಅಂಕಗಳು:**\n\n"
                "• **CLB 9 (IELTS 8.0 Listening, 7.0 ಇತರವು):** ನಿಮ್ಮ ಪ್ರೊಫೈಲ್‌ಗೆ **+50 ಕ್ಕೂ ಹೆಚ್ಚು ಬೋನಸ್ CRS ಅಂಕಗಳನ್ನು** ನೀಡುತ್ತದೆ.\n"
                "• **CLB 7 (IELTS 6.0 ಎಲ್ಲಾ ವಿಭಾಗಗಳಲ್ಲಿ):** ಪೂಲ್ ಪ್ರವೇಶಿಸಲು ಕನಿಷ್ಠ ಅಗತ್ಯವಿದೆ."
            ),
            "hi": (
                "🗣️ **भाषा टेस्ट & CLB 9 स्कोर:**\n\n"
                "• **CLB 9 (IELTS 8.0 Listening, 7.0 अन्य):** यह **+50 से +64 बोनस CRS पॉइंट्स** दिलाता है।\n"
                "• **CLB 7 (IELTS 6.0 प्रत्येक में):** एक्सप्रेस एंट्री पूल में प्रवेश के लिए न्यूनतम कटऑफ है।"
            )
        }
    },

    # 25. NOC & TEER SYSTEM
    {
        "id": "teer_noc_occupations",
        "keywords": [
            "what is noc teer code canada occupations",
            "teer 0 1 2 3 categories eligible for express entry",
            "national occupational classification"
        ],
        "answers": {
            "en": (
                "💼 **Canada NOC 2021 & TEER System:**\n\n"
                "Canada classifies all occupations by Training, Education, Experience and Responsibilities (TEER):\n\n"
                "• **TEER 0:** Management occupations (e.g., Engineering managers, Directors).\n"
                "• **TEER 1:** Professional roles requiring university degrees (e.g., Software Engineers, Doctors, Accountants).\n"
                "• **TEER 2:** Occupations requiring 2–3 year college diplomas or apprenticeships (e.g., Web developers, Technicians).\n"
                "• **TEER 3:** Roles requiring 2-year college or 6+ months on-job training (e.g., Bakers, Dental assistants).\n\n"
                "📌 **Eligibility:** Only occupations in **TEER 0, 1, 2, and 3** qualify for Express Entry Permanent Residency programs."
            ),
            "kn": (
                "💼 **ಕೆನಡಾ TEER ಮತ್ತು NOC ಸಿಸ್ಟಮ್:**\n\n"
                "• ಕೆನಡಾ ಉದ್ಯೋಗಗಳನ್ನು TEER 0, 1, 2, 3, 4, 5 ಎಂದು ವರ್ಗೀಕರಿಸಿದೆ.\n"
                "• Express Entry PR ಗಾಗಿ ಕೇವಲ **TEER 0, 1, 2, ಮತ್ತು 3** ಉದ್ಯೋಗಗಳು ಮಾತ್ರ ಅರ್ಹತೆ ಹೊಂದಿವೆ."
            ),
            "hi": (
                "💼 **कनाडा TEER और NOC वर्गीकरण:**\n\n"
                "• कनाडा में व्यवसायों को TEER श्रेणियों में बांटा गया है।\n"
                "• Express Entry PR के लिए केवल **TEER 0, 1, 2 और 3** के पद ही पात्र होते हैं।"
            )
        }
    }
]

# =========================================================================
# 3. FIT TF-IDF VECTORIZER ACROSS ALL 25 IMMIGRATION DOMAINS
# =========================================================================

CORPUS_DOCS = []
CORPUS_MAP = []

for item in KNOWLEDGE_BASE:
    for kw in item["keywords"]:
        CORPUS_DOCS.append(kw)
        CORPUS_MAP.append(item)

TFIDF_VECTORIZER = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
TFIDF_MATRIX = TFIDF_VECTORIZER.fit_transform(CORPUS_DOCS)

def semantic_search_knowledge_base(query: str, threshold: float = 0.16) -> Optional[Dict[str, Any]]:
    try:
        q_clean = query.lower().strip()
        q_vec = TFIDF_VECTORIZER.transform([q_clean])
        similarities = cosine_similarity(q_vec, TFIDF_MATRIX)[0]
        best_idx = similarities.argmax()
        best_score = similarities[best_idx]
        if best_score >= threshold:
            return CORPUS_MAP[best_idx]
    except Exception:
        pass
    return None

# =========================================================================
# 4. CLOUD LLM FALLBACK (GEMINI REST API)
# =========================================================================

def try_cloud_llm_generation(user_query: str, lang: str) -> Optional[str]:
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        return None

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        headers = {"Content-Type": "application/json"}
        prompt = (
            f"You are Atlas, a senior licensed immigration advisor for Canada, Australia, UK, and Germany. "
            f"Answer the user's visa question clearly, accurately, and concisely in markdown format. "
            f"Language: {lang}. User question: {user_query}"
        )
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        res = requests.post(url, headers=headers, json=payload, timeout=8)
        if res.status_code == 200:
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        pass
    return None

# =========================================================================
# 5. PROFILE EVALUATOR LOGIC
# =========================================================================

def evaluate_profile_query(clean_q: str, raw_q: str, lang: str) -> Optional[Dict[str, Any]]:
    has_eval_intent = any(k in clean_q for k in [
        "assess", "evaluate", "check my profile", "my profile", "my chances", "evaluate me",
        "calculate my score", "points for me", "can i get", "am i eligible", "profile review",
        "ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ", "ನನ್ನ ಪ್ರೊಫೈಲ್", "मूल्यांकन", "मेरी प्रोफाइल", "क्या मुझे वीजा मिलेगा"
    ])

    age_match = re.search(r'\b(?:age|years old|aged|ವಯಸ್ಸು|उम्र)[\s:=]*(\d{2})\b', clean_q) or re.search(r'\b(\d{2})\s*(?:years old|yrs old|yo)\b', clean_q)
    ielts_match = re.search(r'\b(?:ielts|clb|pte|band|score|ಅಂಕ|बैंड)[\s:=]*(\d(?:\.\d)?)\b', clean_q)
    exp_match = re.search(r'\b(\d+)\+?\s*(?:years?|yrs?|ವರ್ಷ|साल)[\s\w]*(?:exp|experience|work|ಅನುಭವ|अनुभव)\b', clean_q) or \
                re.search(r'\b(?:exp|experience|ಅನುಭವ|अनुभव)[\s:=]*(\d+)\+?\s*(?:years?|yrs?|ವರ್ಷ|साल)?\b', clean_q)

    edu_level = None
    if any(k in clean_q for k in ["phd", "doctorate"]):
        edu_level = "PhD / Doctorate"
    elif any(k in clean_q for k in ["master", "masters", "post graduate", "pg", "मास्टर्स"]):
        edu_level = "Master's Degree"
    elif any(k in clean_q for k in ["bachelor", "bachelors", "btech", "be", "degree", "बैचलर्स"]):
        edu_level = "Bachelor's Degree"
    elif any(k in clean_q for k in ["diploma", "डिप्लोमा"]):
        edu_level = "Diploma (2-3 Yrs)"

    has_job_offer = None
    if re.search(r'\b(no job offer|without job offer|dont have job offer|not sponsored|जॉब ऑफर नहीं)\b', clean_q):
        has_job_offer = False
    elif re.search(r'\b(have job offer|with job offer|got job offer|sponsored|job offer:?\s*yes|जॉब ऑफर है)\b', clean_q):
        has_job_offer = True

    attributes_found = sum([
        1 if age_match else 0,
        1 if ielts_match else 0,
        1 if exp_match else 0,
        1 if edu_level else 0,
        1 if has_job_offer is not None else 0
    ])

    if not has_eval_intent and attributes_found < 2:
        return None

    calc_age = int(age_match.group(1)) if age_match else 28
    calc_ielts = float(ielts_match.group(1)) if ielts_match else 7.0
    calc_exp = int(exp_match.group(1)) if exp_match else 3
    calc_edu = edu_level if edu_level else "Bachelor's Degree"

    points = 0
    breakdown = []

    if 20 <= calc_age <= 29: points += 25; breakdown.append(f"• **Age ({calc_age}):** 25/25 pts *(Peak eligibility bracket)*")
    elif 30 <= calc_age <= 34: points += 20; breakdown.append(f"• **Age ({calc_age}):** 20/25 pts *(Strong bracket)*")
    elif 35 <= calc_age <= 39: points += 14; breakdown.append(f"• **Age ({calc_age}):** 14/25 pts *(Moderate bracket)*")
    else: points += 8; breakdown.append(f"• **Age ({calc_age}):** 8/25 pts *(Reduced age points)*")

    if calc_edu == "PhD / Doctorate": points += 25; breakdown.append("• **Education (PhD):** 25/25 pts")
    elif calc_edu == "Master's Degree": points += 23; breakdown.append("• **Education (Master's):** 23/25 pts *(High competitive tier)*")
    elif calc_edu == "Bachelor's Degree": points += 19; breakdown.append("• **Education (Bachelor's):** 19/25 pts")
    else: points += 15; breakdown.append("• **Education (Diploma):** 15/25 pts")

    if calc_exp >= 4: points += 20; breakdown.append(f"• **Experience ({calc_exp} yrs):** 20/20 pts *(Full skilled tenure)*")
    elif calc_exp == 3: points += 17; breakdown.append(f"• **Experience ({calc_exp} yrs):** 17/20 pts")
    elif calc_exp == 2: points += 14; breakdown.append(f"• **Experience ({calc_exp} yrs):** 14/20 pts")
    else: points += 8; breakdown.append(f"• **Experience ({calc_exp} yr):** 8/20 pts")

    if calc_ielts >= 8.0: points += 20; breakdown.append(f"• **Language (IELTS {calc_ielts}):** 20/20 pts *(CLB 9/10 Top Band)*")
    elif calc_ielts >= 7.0: points += 16; breakdown.append(f"• **Language (IELTS {calc_ielts}):** 16/20 pts *(CLB 7/8 Solid Competency)*")
    else: points += 10; breakdown.append(f"• **Language (IELTS {calc_ielts}):** 10/20 pts")

    if has_job_offer is True:
        points += 15
        breakdown.append("• **Job Offer:** +15 pts *(Confirmed LMIA/Sponsorship Boost)*")
    else:
        breakdown.append("• **Job Offer:** 0/15 pts *(Applying as independent applicant)*")

    if points >= 78:
        risk_tier = "🟢 LOW RISK (HIGH APPROVAL CHANCE)"
        prob_range = "82% – 94%"
        verdict = "Your profile is exceptionally competitive. High probability for direct PR invitation draws or accelerated work permits."
    elif points >= 60:
        risk_tier = "🟡 MEDIUM RISK (MODERATE / BORDERLINE CHANCE)"
        prob_range = "58% – 72%"
        verdict = "You qualify on core legal standards, but sit in the middle of the global applicant pool. Improving language to CLB 9 or securing employer sponsorship will push you to Low Risk."
    else:
        risk_tier = "🔴 HIGH RISK (CHALLENGING / LOW CHANCE)"
        prob_range = "28% – 44%"
        verdict = "Your profile faces points caps. Target higher IELTS scores (7.5+) or accumulate 1-2 more years of skilled experience."

    if lang == "kn":
        ans = (
            f"📊 **ಪ್ರೊಫೈಲ್ ಮೌಲ್ಯಮಾಪನ ವರದಿ:**\n\n"
            f"**ಒಟ್ಟು ಅಂಕಗಳು:** `{points}/100`\n"
            f"**ರಿಸ್ಕ್ ಮಟ್ಟ:** {risk_tier}\n"
            f"**ಅಂದಾಜು ಅವಕಾಶ:** `{prob_range}`\n\n"
            f"📌 **ಅಂಕಗಳ ವಿವರ:**\n" + "\n".join(breakdown) + f"\n\n💡 **ವಿಶ್ಲೇಷಣೆ:**\n{verdict}"
        )
    elif lang == "hi":
        ans = (
            f"📊 **प्रोफाइल मूल्यांकन रिपोर्ट:**\n\n"
            f"**कुल स्कोर:** `{points}/100`\n"
            f"**रिस्क स्तर:** {risk_tier}\n"
            f"**स्वीकृति संभावना:** `{prob_range}`\n\n"
            f"📌 **अंकों का विवरण:**\n" + "\n".join(breakdown) + f"\n\n💡 **विशेषज्ञ राय:**\n{verdict}"
        )
    else:
        ans = (
            f"📊 **Executive Case Assessment & Scorecard:**\n\n"
            f"**Composite Score:** `{points}/100`\n"
            f"**Risk Classification:** {risk_tier}\n"
            f"**Estimated Approval Likelihood:** `{prob_range}`\n\n"
            f"📈 **Points Breakdown:**\n" + "\n".join(breakdown) + f"\n\n💡 **Strategic Verdict:**\n{verdict}"
        )

    return {
        "response": ans,
        "scope": "in_scope",
        "lang": lang,
        "suggested_questions": [
            "Why does a profile get Medium Risk?",
            "How to move from Medium to Low Risk?",
            "What is Proof of Funds for Canada?"
        ]
    }

# =========================================================================
# 6. MASTER QUERY RESOLUTION ROUTINE
# =========================================================================

def answer_project_query(user_query: str, lang_code: str = "en") -> Dict[str, Any]:
    detected_lang = detect_language(user_query, lang_code)
    clean_q = user_query.lower().strip()

    # 1. Scope filter
    if not is_visa_related(clean_q):
        out_scope_msg = (
            "🔒 **Visa & Immigration Questions Only**\n\n"
            "I am **Atlas**, your visa guide. I answer questions regarding visa requirements, "
            "approval chances, Medium Risk causes, and skilled migration rules for Canada, Australia, UK, and Germany.\n\n"
            "Please ask a visa or immigration-related question!"
        )
        if detected_lang == "kn":
            out_scope_msg = "🔒 **ಕೇವಲ ವೀಸಾ ಪ್ರಶ್ನೆಗಳು ಮಾತ್ರ:**\n\nನಾನು ವೀಸಾ ನಿಯಮಗಳು, ಅರ್ಹತೆ ಮತ್ತು ಪ್ರೊಫೈಲ್ ಕುರಿತ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಬಲ್ಲೆ. ದಯವಿಟ್ಟು ವೀಸಾಗೆ ಸಂಬಂಧಿಸಿದ ಪ್ರಶ್ನೆ ಕೇಳಿ!"
        elif detected_lang == "hi":
            out_scope_msg = "🔒 **केवल वीजा संबंधित प्रश्न:**\n\nमैं केवल वीजा नियमों, पात्रता और रिस्क स्तरों से संबंधित प्रश्नों के उत्तर दे सकता हूँ। कृपया वीजा संबंधी प्रश्न पूछें!"
        return {
            "response": out_scope_msg,
            "scope": "out_of_scope",
            "lang": detected_lang,
            "suggested_questions": [
                "Why does a profile get Medium Risk?",
                "What is Proof of Funds for Canada?",
                "What are Canada Express Entry requirements?"
            ]
        }

    # 2. Greetings
    if any(clean_q == g or clean_q.startswith(g + " ") for g in ["hello", "hi", "hey", "who are you", "what is this", "atlas", "namaste", "namaskara", "ನಮಸ್ಕಾರ", "नमस्ते"]):
        greet = (
            "👋 **Hello! I'm Atlas, your Visa Guide.**\n\n"
            "I can answer any questions about skilled migration, visa rules, and scoring algorithms across Canada, Australia, UK, and Germany.\n\n"
            "Choose any pre-question or ask me anything!"
        )
        if detected_lang == "kn":
            greet = "👋 **ನಮಸ್ಕಾರ! ನಾನು Atlas, ನಿಮ್ಮ ವೀಸಾ ಗೈಡ್.**\n\nಕೆನಡಾ, ಆಸ್ಟ್ರೇಲಿಯಾ, ಯುಕೆ, ಜರ್ಮನಿ ವೀಸಾ ನಿಯಮಗಳು ಮತ್ತು ಅರ್ಹತೆಯ ಬಗ್ಗೆ ನೀವು ಯಾವುದೇ ಪ್ರಶ್ನೆ ಕೇಳಬಹುದು!"
        elif detected_lang == "hi":
            greet = "👋 **नमस्ते! मैं Atlas हूँ, आपका वीजा गाइड।**\n\nकनाडा, ऑस्ट्रेलिया, यूके और जर्मनी के वीजा नियमों व पात्रता के बारे में आप कोई भी सवाल पूछ सकते हैं!"
        return {
            "response": greet,
            "scope": "in_scope",
            "lang": detected_lang,
            "suggested_questions": [
                "Why does a profile get Medium Risk?",
                "How to move from Medium to Low Risk?",
                "What is Proof of Funds for Canada?"
            ]
        }

    # 3. Interactive Profile Assessment (if user types age, experience, degree, etc.)
    eval_res = evaluate_profile_query(clean_q, user_query, detected_lang)
    if eval_res:
        return eval_res

    # 4. Semantic Search across Vector Knowledge Base (TF-IDF Similarity)
    match = semantic_search_knowledge_base(clean_q, threshold=0.15)
    if match and "answers" in match:
        ans_text = match["answers"].get(detected_lang, match["answers"]["en"])
        return {
            "response": ans_text,
            "scope": "in_scope",
            "lang": detected_lang,
            "suggested_questions": [
                "Why does a profile get Medium Risk?",
                "How to move from Medium to Low Risk?",
                "What is Proof of Funds for Canada?"
            ]
        }

    # 5. Cloud LLM Fallback (if GEMINI_API_KEY is present)
    llm_resp = try_cloud_llm_generation(user_query, detected_lang)
    if llm_resp:
        return {
            "response": llm_resp,
            "scope": "in_scope",
            "lang": detected_lang,
            "suggested_questions": [
                "Why does a profile get Medium Risk?",
                "What is Proof of Funds for Canada?"
            ]
        }

    # 6. Adaptive Regulatory Synthesizer for arbitrary unmapped questions
    target_country = "Global"
    if "canada" in clean_q or "ircc" in clean_q or "ontario" in clean_q: target_country = "Canada"
    elif "australia" in clean_q or "sydney" in clean_q or "melbourne" in clean_q: target_country = "Australia"
    elif "uk" in clean_q or "united kingdom" in clean_q or "london" in clean_q: target_country = "United Kingdom"
    elif "germany" in clean_q or "berlin" in clean_q: target_country = "Germany"

    if detected_lang == "kn":
        adaptive_ans = (
            f"💡 **ವೀಸಾ ಮಾರ್ಗದರ್ಶನ ({target_country}):**\n\n"
            f"ನಿಮ್ಮ ಪ್ರಶ್ನೆ: *\"{user_query}\"*\n\n"
            "• **ಅರ್ಹತಾ ಮಾನದಂಡಗಳು:** ಹೆಚ್ಚಿನ ನುರಿತ ವೀಸಾಗಳಿಗೆ ಮಾನ್ಯತೆ ಪಡೆದ ವಿಶ್ವವಿದ್ಯಾಲಯ ಪದವಿ, ಕನಿಷ್ಠ 2-3 ವರ್ಷಗಳ ಅನುಭವ ಮತ್ತು ಭಾಷಾ ಪರೀಕ್ಷೆ (IELTS 6.5+) ಅಗತ್ಯವಿದೆ.\n"
            "• **ಅವಕಾಶಗಳನ್ನು ಹೆಚ್ಚಿಸಲು:** ಕಂಪನಿಯಿಂದ ಅಧಿಕೃತ ಜಾಬ್ ಆಫರ್ ಅಥವಾ ಪ್ರೊವಿನ್ಶಿಯಲ್ ನಾಮಿನೇಷನ್ ಪಡೆಯುವುದು ನಿಮ್ಮ ಅನುಮೋದನೆ ಸಾಧ್ಯತೆಯನ್ನು ತಕ್ಷಣ ಹೆಚ್ಚಿಸುತ್ತದೆ.\n"
            "• ನಿಮ್ಮ ಪ್ರೊಫೈಲ್‌ನ ನಿಖರ ಮೌಲ್ಯಮಾಪನಕ್ಕಾಗಿ ನಿಮ್ಮ ವಯಸ್ಸು, ಶಿಕ್ಷಣ ಮತ್ತು IELTS ಸ್ಕೋರ್ ಟೈಪ್ ಮಾಡಿ!"
        )
    elif detected_lang == "hi":
        adaptive_ans = (
            f"💡 **वीजा विशेषज्ञ सलाह ({target_country}):**\n\n"
            f"आपका प्रश्न: *\"{user_query}\"*\n\n"
            "• **मुख्य नियम:** कुशल वीजा के लिए मान्यता प्राप्त डिग्री, 2-3 वर्ष का अनुभव और भाषा स्कोर (IELTS 6.5+) अनिवार्य होता है।\n"
            "• **संभावना सुधार:** नियोक्ता से वैध जॉब ऑफर या राज्य नामांकन मिलने से वीजा स्वीकृति की संभावना सबसे अधिक बढ़ जाती है।\n"
            "• अपनी सटीक पात्रता जानने के लिए अपनी उम्र, डिग्री और IELTS स्कोर लिखकर भेजें!"
        )
    else:
        adaptive_ans = (
            f"💡 **Immigration Advisory & Regulatory Guidance ({target_country}):**\n\n"
            f"Regarding your query: *\"{user_query}\"*\n\n"
            "• **Statutory Standards:** For skilled pathways in this jurisdiction, candidate evaluation prioritizes verified educational credentials, 2 to 3+ years of skilled tenure, language competency (IELTS/CLB benchmark), and financial settlement reserves.\n"
            "• **Strategic Leverage:** Securing validated employer sponsorship (LMIA/CoS/Subclass 482) or a provincial/state nomination provides the single strongest boost to bypass competitive draw ceilings.\n"
            "• **Custom Assessment:** You can type your profile details (e.g. `Age 28, Master's, 3 yrs exp, IELTS 7.5, No job offer`) for an instant itemized points breakdown!"
        )

    return {
        "response": adaptive_ans,
        "scope": "in_scope",
        "lang": detected_lang,
        "suggested_questions": [
            "Why does a profile get Medium Risk?",
            "How to move from Medium to Low Risk?",
            "What is Proof of Funds for Canada?"
        ]
    }
