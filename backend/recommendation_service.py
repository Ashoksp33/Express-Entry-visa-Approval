def generate_personalized_recommendations(profile_dict: dict, prediction_res: dict) -> list:
    """
    Generates actionable, profile-tailored guidance for enhancing applicant approval odds
    customized specifically for Canada, Australia, UK, and Germany.
    """
    country_key = profile_dict.get("target_country", "canada").lower().strip()
    recommendations = []

    job_offer = int(profile_dict.get("job_offer", 0))
    sponsorship = int(profile_dict.get("employer_sponsorship", 0))
    lang_score = float(profile_dict.get("language_overall_score", 0))
    exp = int(profile_dict.get("relevant_work_exp", 0))
    edu = profile_dict.get("education_level", "")
    funds = float(profile_dict.get("settlement_funds_cad", 0))
    refusal = int(profile_dict.get("previous_visa_refusal", 0))

    if country_key == "australia":
        # Australia Subclass 189/482 recommendations
        if lang_score < 8.0:
            recommendations.append({
                "category": "English Points (DHA)",
                "priority": "High Impact",
                "title": "Achieve Superior English (IELTS 8.0+ / PTE 79+)",
                "action": "Raising your English score to Superior grants +20 immigration points on the Australian Points Test.",
                "estimated_impact": "+20 Points Allocation",
                "disclaimer": "English test results must be valid at the time of Expression of Interest (EOI) submission."
            })
        if profile_dict.get("eca_done") == 0:
            recommendations.append({
                "category": "Skills Assessment",
                "priority": "Critical Requirement",
                "title": "Obtain Positive Skills Assessment (VETASSESS / Engineers Australia / ACS)",
                "action": "A positive migration skills assessment in your nominated ANZSCO occupation is mandatory for Australian visa grant.",
                "estimated_impact": "Mandatory Requirement",
                "disclaimer": "Verify assessment requirements with your relevant assessing authority."
            })
        if exp < 5:
            recommendations.append({
                "category": "Skilled Experience Points",
                "priority": "Medium Impact",
                "title": "Accumulate 5+ Years of Overseas Skilled Experience",
                "action": "Reaching 5-7 years of verified experience in your nominated ANZSCO role increases your points from +5 to +10.",
                "estimated_impact": "+5 Points Allocation",
                "disclaimer": "Experience must be closely related to your nominated skilled occupation."
            })

    elif country_key == "uk":
        # UK Skilled Worker Visa recommendations
        if sponsorship == 0 or job_offer == 0:
            recommendations.append({
                "category": "UK Sponsorship",
                "priority": "Critical Requirement",
                "title": "Obtain Job Offer with Home Office Licensed Sponsor (CoS)",
                "action": "UK Skilled Worker visas require a valid Certificate of Sponsorship (CoS) from a registered A-rating employer.",
                "estimated_impact": "Mandatory Approval Condition",
                "disclaimer": "Ensure the role aligns with eligible SOC codes (RQF Level 3 or higher)."
            })
        if float(profile_dict.get("offered_salary_cad", 0)) * 0.58 < 38700:
            recommendations.append({
                "category": "Salary Threshold",
                "priority": "High Impact",
                "title": "Meet General Salary Threshold (£38,700 GBP)",
                "action": "Negotiate salary to satisfy the Home Office general threshold or check for Immigration Salary List discounts.",
                "estimated_impact": "+25% Approval Probability",
                "disclaimer": "Going rates vary depending on the specific 4-digit SOC occupation code."
            })
        if lang_score < 6.0:
            recommendations.append({
                "category": "English Language",
                "priority": "High Impact",
                "title": "Pass SELT English at CEFR Level B1+",
                "action": "Take an approved Secure English Language Test (SELT) achieving at least IELTS 4.0 / B1 in all 4 components.",
                "estimated_impact": "Mandatory Approval Condition",
                "disclaimer": "Must be taken at an authorized UKVI approved test centre."
            })

    elif country_key == "germany":
        # Germany EU Blue Card recommendations
        if float(profile_dict.get("offered_salary_cad", 0)) * 0.68 < 45300:
            recommendations.append({
                "category": "German Minimum Salary",
                "priority": "High Impact",
                "title": "Satisfy EU Blue Card Salary (€45,300 or €41,041 for MINT)",
                "action": "Ensure gross annual salary meets the statutory German Federal Ministry threshold for skilled talent.",
                "estimated_impact": "+35% Approval Probability",
                "disclaimer": "Shortage occupations (IT, engineers, doctors) qualify for the lower threshold."
            })
        if profile_dict.get("eca_done") == 0:
            recommendations.append({
                "category": "Degree Recognition (ZAB)",
                "priority": "Critical Requirement",
                "title": "Verify Degree on Anabin / Central Office (ZAB)",
                "action": "Check if your foreign university and degree are classified as H+ on the German Anabin database.",
                "estimated_impact": "Mandatory Approval Condition",
                "disclaimer": "Statement of Comparability (Zeugnisbewertung) may be requested by the German embassy."
            })
        recommendations.append({
            "category": "Language Integration",
            "priority": "Medium Impact",
            "title": "Acquire German Language Proficiency (A2 / B1 CEFR)",
            "action": "German B1 certification accelerates permanent residency (Niederlassungserlaubnis) eligibility from 27 to 21 months.",
            "estimated_impact": "+10% Approval Boost & Fast-Track PR",
            "disclaimer": "Certificates must be from Goethe-Institut, telc, or TestDaF."
        })

    else:
        # Canada (Original baseline)
        if job_offer == 0:
            recommendations.append({
                "category": "Employment & Job Offer",
                "priority": "High Impact",
                "title": "Secure a Valid Canadian Job Offer or PNP Nomination",
                "action": "Seek employment opportunities with employers offering LMIA sponsorship or pursue Provincial Nominee Program (PNP) employer-driven streams.",
                "estimated_impact": "+20% to +35% Approval Boost",
                "disclaimer": "Job offers must conform to official IRCC and ESDC requirements."
            })
        elif sponsorship == 0:
            recommendations.append({
                "category": "Employment Documentation",
                "priority": "Medium Impact",
                "title": "Request LMIA Support or LMIA-Exemption Documentation",
                "action": "Coordinate with your Canadian employer to obtain a positive LMIA or verify qualification for LMIA-exempt codes under international trade agreements.",
                "estimated_impact": "+15% Approval Boost",
                "disclaimer": "Ensure job offer letter includes detailed NOC TEER role descriptions and prevailing wage alignment."
            })

        if lang_score < 7.5:
            boost = "+12.0%" if lang_score < 6.5 else "+8.0%"
            recommendations.append({
                "category": "Language Proficiency",
                "priority": "High Impact",
                "title": "Improve English Language Benchmark (IELTS / CELPIP)",
                "action": "Target an overall IELTS Band score of 8.0+ (CLB 9/10 equivalent) to maximize human capital points.",
                "estimated_impact": f"{boost} Approval Boost",
                "disclaimer": "Language test results must be less than 2 years old at time of visa application submission."
            })

        if exp < 3:
            recommendations.append({
                "category": "Work Experience",
                "priority": "Medium Impact",
                "title": "Accumulate Continuous Skilled Experience in TEER 0/1/2/3",
                "action": "Gain additional years of continuous full-time skilled work experience in your primary occupation.",
                "estimated_impact": "+10.0% Approval Boost",
                "disclaimer": "Ensure experience is supported by official employment reference letters and payroll documentation."
            })

        if edu not in ["High School"] and profile_dict.get("eca_done") == 0:
            recommendations.append({
                "category": "Academic Credentials",
                "priority": "High Impact",
                "title": "Complete Educational Credential Assessment (ECA)",
                "action": "Submit your academic transcripts to WES, ICAS, or IQAS for official Canadian equivalency verification.",
                "estimated_impact": "+8.0% Approval Boost",
                "disclaimer": "ECA report must be issued by an IRCC-designated organization."
            })

    # Universal Admissibility / Refusal Advice
    if refusal == 1:
        recommendations.append({
            "category": "Immigration Admissibility",
            "priority": "Critical Review",
            "title": "Provide Detailed Explanation for Previous Refusal",
            "action": "Submit official case notes and transparently address reasons for past refusal in your letter of explanation.",
            "estimated_impact": "Prevents Automatic Procedural Fairness Refusal",
            "disclaimer": "All historical refusals across all jurisdictions must be truthfully declared."
        })

    return recommendations
