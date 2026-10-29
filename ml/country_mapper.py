"""
Multi-Country Profile Mapper & Evaluation Engine for:
- Canada (IRCC NOC 2021 TFWP / Express Entry)
- Australia (Home Affairs Subclass 189/482 ANZSCO)
- United Kingdom (Home Office Skilled Worker SOC 2020 / RQF)
- Germany (BAMF EU Blue Card / Academic & Shortage)
"""

COUNTRY_METADATA = {
    "canada": {
        "code": "canada",
        "name": "Canada",
        "flag": "🍁",
        "currency": "CAD",
        "currency_symbol": "$",
        "visa_stream": "Canada Work Visa (TFWP / LMIA / Express Entry)",
        "framework": "Canada NOC 2021 TEER Categories",
        "min_funds_desc": "IRCC LICO Single Threshold ≈ $14,690 CAD",
        "skill_label": "Occupation Skill / TEER Category",
        "skill_options": [
            {"val": "TEER 0", "label": "TEER 0 (Management Occupations)"},
            {"val": "TEER 1", "label": "TEER 1 (Professional - IT, Eng, Health)"},
            {"val": "TEER 2", "label": "TEER 2 (Technical & Supervisory)"},
            {"val": "TEER 3", "label": "TEER 3 (Intermediate Skilled)"},
            {"val": "TEER 4/5", "label": "TEER 4/5 (Trades & General Labor)"}
        ],
        "sponsor_label": "LMIA / Sponsorship Support *",
        "sponsor_desc": "Yes (Positive LMIA or LMIA-Exempt)",
        "salary_label": "Offered Canadian Salary (Annual CAD) *"
    },
    "australia": {
        "code": "australia",
        "name": "Australia",
        "flag": "🇦🇺",
        "currency": "AUD",
        "currency_symbol": "A$",
        "visa_stream": "Australia Skilled Independent (Subclass 189 / 482)",
        "framework": "Australian ANZSCO Skill Levels 1–5",
        "min_funds_desc": "Home Affairs Settlement Margin ≈ $20,000 AUD",
        "skill_label": "ANZSCO Occupation Skill Level *",
        "skill_options": [
            {"val": "ANZSCO Skill Level 1", "label": "ANZSCO Level 1 (Managers & Degree Professionals)"},
            {"val": "ANZSCO Skill Level 2", "label": "ANZSCO Level 2 (Technicians & Associate Professionals)"}
        ],
        "sponsor_label": "Australian State / Employer Sponsorship *",
        "sponsor_desc": "Yes (State Nomination / SBS Sponsor)",
        "salary_label": "Offered Australian Salary (Annual AUD) *"
    },
    "uk": {
        "code": "uk",
        "name": "United Kingdom",
        "flag": "🇬🇧",
        "currency": "GBP",
        "currency_symbol": "£",
        "visa_stream": "UK Skilled Worker Visa (Points-Based System)",
        "framework": "UK Regulated Qualifications Framework (RQF 3–8)",
        "min_funds_desc": "Home Office Maintenance Funds ≈ £1,270 GBP",
        "skill_label": "UK Job RQF Skill Level *",
        "skill_options": [
            {"val": "RQF Level 6", "label": "RQF Level 6 (Degree Level / Professional)"},
            {"val": "RQF Level 7", "label": "RQF Level 7 (Master's Level / Chartered Specialist)"},
            {"val": "RQF Level 8", "label": "RQF Level 8 (Doctoral Level / Research)"},
            {"val": "RQF Level 4", "label": "RQF Level 4 (Higher National / Associate)"},
            {"val": "RQF Level 3", "label": "RQF Level 3 (A-Level Equivalent / Skilled Trade)"}
        ],
        "sponsor_label": "Certificate of Sponsorship (CoS) *",
        "sponsor_desc": "Yes (Licensed Home Office A-Rating Sponsor)",
        "salary_label": "Offered UK Salary (Annual GBP £) *"
    },
    "germany": {
        "code": "germany",
        "name": "Germany",
        "flag": "🇩🇪",
        "currency": "EUR",
        "currency_symbol": "€",
        "visa_stream": "Germany EU Blue Card (Blaue Karte EU)",
        "framework": "German Recognized Academic / Shortage Occupation",
        "min_funds_desc": "German Blocked Account / Living Fund ≈ €11,904 EUR",
        "skill_label": "German Profession Classification *",
        "skill_options": [
            {"val": "Standard Academic Profession", "label": "Standard Academic Profession (Degree Required)"},
            {"val": "MINT Shortage Occupation", "label": "MINT Shortage Occupation (Math, IT, Engineering, Medicine)"}
        ],
        "sponsor_label": "German Employment Contract / ZAV Approval *",
        "sponsor_desc": "Yes (Binding Employment Contract in Germany)",
        "salary_label": "Offered German Salary (Annual EUR €) *"
    }
}

def map_profile_to_country(raw_profile: dict, country_key: str, expected_cols: list) -> dict:
    """
    Transforms the standardized applicant profile input into the exact feature columns
    expected by the country's dedicated ML pipeline.
    """
    country_key = country_key.lower().strip()
    profile = raw_profile.copy()
    
    age = int(profile.get("age", 30))
    exp_tot = int(profile.get("total_work_exp", 5))
    exp_rel = int(profile.get("relevant_work_exp", 4))
    lang_score = float(profile.get("language_overall_score", 7.5))
    salary = float(profile.get("offered_salary_cad", 75000.0))
    annual_inc = float(profile.get("annual_income_cad", 45000.0))
    settle_funds = float(profile.get("settlement_funds_cad", 35000.0))
    debt = float(profile.get("outstanding_debt_cad", 2000.0))
    edu = profile.get("education_level", "Bachelor's")
    job_offer = int(profile.get("job_offer", 1))
    sponsorship = int(profile.get("employer_sponsorship", 1))
    
    mapped = {}

    if country_key == "australia":
        # Points Test simulation
        # Age points (18-24: 25, 25-32: 30, 33-39: 25, 40-44: 15, 45+: 0)
        if 25 <= age <= 32:
            pts_age = 30
        elif (18 <= age <= 24) or (33 <= age <= 39):
            pts_age = 25
        elif 40 <= age <= 44:
            pts_age = 15
        else:
            pts_age = 0

        # English points (Competent: 0, Proficient >=7.0: 10, Superior >=8.0: 20)
        if lang_score >= 8.0:
            pts_eng = 20
            eng_lvl = "Superior"
        elif lang_score >= 7.0:
            pts_eng = 10
            eng_lvl = "Proficient"
        elif lang_score >= 6.0:
            pts_eng = 0
            eng_lvl = "Competent"
        else:
            pts_eng = 0
            eng_lvl = "Below Competent"

        # Overseas work experience (3-4: 5, 5-7: 10, 8+: 15)
        if exp_rel >= 8:
            pts_exp_overseas = 15
        elif exp_rel >= 5:
            pts_exp_overseas = 10
        elif exp_rel >= 3:
            pts_exp_overseas = 5
        else:
            pts_exp_overseas = 0

        # Australian work experience
        prev_au_work = int(profile.get("previous_canada_work", 0))
        pts_exp_au = 5 if prev_au_work == 1 else 0

        # Education points (PhD: 20, Bachelor/Master: 15, Diploma: 10)
        if edu == "PhD":
            pts_edu = 20
        elif edu in ["Bachelor's", "Master's"]:
            pts_edu = 15
        elif edu == "Diploma":
            pts_edu = 10
        else:
            pts_edu = 0

        prev_au_study = int(profile.get("previous_canada_study", 0))
        pts_study = 5 if prev_au_study == 1 else 0

        skills_assess = int(profile.get("eca_done", 1))
        pts_skills = 0 # Baseline

        total_pts = pts_age + pts_eng + pts_exp_overseas + pts_exp_au + pts_edu + pts_study

        # Build feature dict
        mapped = {
            "age": age,
            "country_citizenship": profile.get("country_citizenship", "India"),
            "country_residence": profile.get("country_residence", "India"),
            "marital_status": profile.get("marital_status", "Single"),
            "dependents": int(profile.get("dependents", 0)),
            "education_level": edu,
            "field_of_study": profile.get("field_of_study", "Computer Science"),
            "total_work_exp": exp_tot,
            "relevant_work_exp": exp_rel,
            "current_employment_status": profile.get("current_employment_status", "Employed"),
            "english_test": profile.get("english_test", "IELTS"),
            "language_overall_score": lang_score,
            "annual_income": annual_inc,
            "settlement_funds": settle_funds,
            "outstanding_debt": debt,
            "debt_to_income_ratio": round(debt / (annual_inc + salary + 1.0), 4),
            "relevant_exp_ratio": round(exp_rel / (exp_tot + 1.0), 4),
            "financial_sponsor": profile.get("financial_sponsor", "Self"),
            "previous_visa": int(profile.get("previous_canada_visa", 0)),
            "previous_visa_refusal": int(profile.get("previous_visa_refusal", 0)),
            "previous_immigration_violation": int(profile.get("previous_immigration_violation", 0)),
            "previous_work": prev_au_work,
            "previous_study": prev_au_study,
            "criminal_record": int(profile.get("criminal_record", 0)),
            "medical_flag": int(profile.get("medical_flag", 0)),
            "job_offer": job_offer,
            "employer_sponsorship": sponsorship,
            "occupation_skill_level": profile.get("occupation_skill_level", "ANZSCO Skill Level 1"),
            "points_age": pts_age,
            "english_level": eng_lvl,
            "points_english": pts_eng,
            "points_skilled_employment_overseas": pts_exp_overseas,
            "points_skilled_employment_australia": pts_exp_au,
            "points_education": pts_edu,
            "australian_study": prev_au_study,
            "points_australian_study": pts_study,
            "community_language_credential": 0,
            "points_community_language": 0,
            "skills_assessment": skills_assess,
            "points_skills_assessment": pts_skills,
            "total_points": total_pts
        }

    elif country_key == "uk":
        threshold_gbp = 38700
        salary_gbp = salary * 0.58  # approximate CAD to GBP conversion
        meets_threshold = 1 if (salary_gbp >= threshold_gbp and job_offer == 1) else 0
        b1_plus = 1 if lang_score >= 6.0 else 0
        
        raw_skill = profile.get("occupation_skill_level") or profile.get("teer_category") or "RQF Level 6"
        rqf_str = str(raw_skill)
        rqf_num = 6
        if "3" in rqf_str: rqf_num = 3
        elif "4" in rqf_str: rqf_num = 4
        elif "7" in rqf_str: rqf_num = 7
        elif "8" in rqf_str: rqf_num = 8
        if "RQF" not in rqf_str: rqf_str = f"RQF Level {rqf_num}"

        mapped = {
            "age": age,
            "country_citizenship": profile.get("country_citizenship", "India"),
            "country_residence": profile.get("country_residence", "India"),
            "marital_status": profile.get("marital_status", "Single"),
            "dependents": int(profile.get("dependents", 0)),
            "education_level": edu,
            "field_of_study": profile.get("field_of_study", "Computer Science"),
            "total_work_exp": exp_tot,
            "relevant_work_exp": exp_rel,
            "current_employment_status": profile.get("current_employment_status", "Employed"),
            "english_test": profile.get("english_test", "IELTS"),
            "language_overall_score": lang_score,
            "annual_income": annual_inc * 0.58,
            "settlement_funds": settle_funds * 0.58,
            "outstanding_debt": debt * 0.58,
            "debt_to_income_ratio": round(debt / (annual_inc + salary + 1.0), 4),
            "relevant_exp_ratio": round(exp_rel / (exp_tot + 1.0), 4),
            "financial_sponsor": profile.get("financial_sponsor", "Self"),
            "previous_visa": int(profile.get("previous_canada_visa", 0)),
            "previous_visa_refusal": int(profile.get("previous_visa_refusal", 0)),
            "previous_immigration_violation": int(profile.get("previous_immigration_violation", 0)),
            "previous_work": int(profile.get("previous_canada_work", 0)),
            "previous_study": int(profile.get("previous_canada_study", 0)),
            "criminal_record": int(profile.get("criminal_record", 0)),
            "medical_flag": int(profile.get("medical_flag", 0)),
            "job_offer": job_offer,
            "sponsor_licensed": sponsorship,
            "employer_sponsorship": sponsorship,
            "rqf_level": rqf_num,
            "occupation_skill_level": rqf_str,
            "threshold_applicable_gbp": threshold_gbp,
            "salary_gbp": round(salary_gbp, 2),
            "salary_meets_threshold": meets_threshold,
            "english_b1_plus": b1_plus
        }

    elif country_key == "germany":
        # Germany EU Blue Card threshold ~45,300 EUR (MINT shortage: ~41,041 EUR)
        is_shortage = 1 if "Shortage" in str(profile.get("occupation_skill_level", "")) or profile.get("field_of_study") in ["Computer Science", "Information Technology", "Engineering", "Healthcare"] else 0
        thresh_eur = 41041.0 if is_shortage == 1 else 45300.0
        salary_eur = salary * 0.68  # approximate CAD to EUR
        meets_eur = 1 if (salary_eur >= thresh_eur and job_offer == 1) else 0

        mapped = {
            "age": age,
            "country_citizenship": profile.get("country_citizenship", "India"),
            "country_residence": profile.get("country_residence", "India"),
            "marital_status": profile.get("marital_status", "Single"),
            "dependents": int(profile.get("dependents", 0)),
            "education_level": edu,
            "field_of_study": profile.get("field_of_study", "Computer Science"),
            "total_work_exp": exp_tot,
            "relevant_work_exp": exp_rel,
            "current_employment_status": profile.get("current_employment_status", "Employed"),
            "english_test": profile.get("english_test", "IELTS"),
            "language_overall_score": lang_score,
            "annual_income": annual_inc * 0.68,
            "settlement_funds": settle_funds * 0.68,
            "outstanding_debt": debt * 0.68,
            "debt_to_income_ratio": round(debt / (annual_inc + salary + 1.0), 4),
            "relevant_exp_ratio": round(exp_rel / (exp_tot + 1.0), 4),
            "financial_sponsor": profile.get("financial_sponsor", "Self"),
            "previous_visa": int(profile.get("previous_canada_visa", 0)),
            "previous_visa_refusal": int(profile.get("previous_visa_refusal", 0)),
            "previous_immigration_violation": int(profile.get("previous_immigration_violation", 0)),
            "previous_work": int(profile.get("previous_canada_work", 0)),
            "previous_study": int(profile.get("previous_canada_study", 0)),
            "criminal_record": int(profile.get("criminal_record", 0)),
            "medical_flag": int(profile.get("medical_flag", 0)),
            "job_offer": job_offer,
            "employer_sponsorship": sponsorship,
            "is_shortage_occupation": is_shortage,
            "occupation_skill_level": "MINT Shortage Occupation" if is_shortage == 1 else "Standard Academic Profession",
            "salary_threshold_eur": thresh_eur,
            "offered_salary_eur": round(salary_eur, 2),
            "salary_meets_threshold": meets_eur,
            "degree_recognition": "Recognized" if profile.get("eca_done", 1) == 1 else "In Progress",
            "health_insurance": "Public",
            "german_language_level": "B1" if profile.get("french_proficiency") in ["Intermediate", "Advanced"] else "A2"
        }

    # Ensure all expected columns are filled
    final_dict = {}
    for col in expected_cols:
        final_dict[col] = mapped.get(col, 0)
        
    return final_dict
