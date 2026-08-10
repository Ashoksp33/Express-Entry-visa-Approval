def generate_personalized_recommendations(profile_dict: dict, prediction_res: dict) -> list:
    """
    Generates actionable, profile-tailored guidance for enhancing applicant approval odds.
    """
    recommendations = []

    # 1. Job Offer & Sponsorship
    if profile_dict.get("job_offer") == 0:
        recommendations.append({
            "category": "Employment & Job Offer",
            "priority": "High Impact",
            "title": "Secure a Valid Canadian Job Offer or PNP Nomination",
            "action": "Seek employment opportunities with employers offering LMIA sponsorship or pursue Provincial Nominee Program (PNP) employer-driven streams.",
            "estimated_impact": "+20% to +35% Approval Boost",
            "disclaimer": "Job offers must conform to official IRCC and Employment and Social Development Canada (ESDC) requirements."
        })
    elif profile_dict.get("employer_sponsorship") == 0:
        recommendations.append({
            "category": "Employment Documentation",
            "priority": "Medium Impact",
            "title": "Request LMIA Support or LMIA-Exemption Documentation",
            "action": "Coordinate with your Canadian employer to obtain a positive LMIA or verify qualification for LMIA-exempt codes under international trade agreements.",
            "estimated_impact": "+15% Approval Boost",
            "disclaimer": "Ensure job offer letter includes detailed NOC TEER role descriptions and prevailing wage alignment."
        })

    # 2. Language Proficiency
    lang_score = float(profile_dict.get("language_overall_score", 0))
    if lang_score < 7.5:
        boost = "+12.0%" if lang_score < 6.5 else "+8.0%"
        recommendations.append({
            "category": "Language Proficiency",
            "priority": "High Impact",
            "title": "Improve English Language Benchmark (IELTS / CELPIP)",
            "action": f"Target an overall IELTS Band score of 8.0+ (CLB 9/10 equivalent) to maximize human capital points.",
            "estimated_impact": f"{boost} Approval Boost",
            "disclaimer": "Language test results must be less than 2 years old at time of visa application submission."
        })

    # 3. Work Experience
    exp = int(profile_dict.get("relevant_work_exp", 0))
    if exp < 3:
        recommendations.append({
            "category": "Work Experience",
            "priority": "Medium Impact",
            "title": "Accumulate Continuous Skilled Experience in TEER 0/1/2/3",
            "action": f"Gain additional years of continuous full-time skilled work experience in your primary occupation.",
            "estimated_impact": "+10.0% Approval Boost",
            "disclaimer": "Ensure experience is supported by official employment reference letters and payroll documentation."
        })

    # 4. Educational Credential Assessment (ECA)
    edu = profile_dict.get("education_level", "")
    if edu not in ["High School"] and profile_dict.get("eca_done") == 0:
        recommendations.append({
            "category": "Academic Credentials",
            "priority": "High Impact",
            "title": "Complete Educational Credential Assessment (ECA)",
            "action": "Submit your academic transcripts to WES (World Education Services), ICAS, or IQAS for official Canadian equivalency verification.",
            "estimated_impact": "+8.0% Approval Boost",
            "disclaimer": "ECA verification is required for foreign educational qualification recognition."
        })

    # 5. Settlement Funds
    funds = float(profile_dict.get("settlement_funds_cad", 0))
    dependents = int(profile_dict.get("dependents", 0))
    min_required = 13757 + (dependents * 3500)

    if funds < min_required * 1.2:
        recommended_target = int(min_required * 1.3)
        recommendations.append({
            "category": "Financial Solvency",
            "priority": "High Impact",
            "title": "Strengthen Proof of Unencumbered Settlement Funds",
            "action": f"Increase available liquid bank balances to at least ${recommended_target:,.0f} CAD and maintain unencumbered funds for 6+ months.",
            "estimated_impact": "+14.0% Approval Boost",
            "disclaimer": "Borrowed funds or real estate valuation cannot be counted as liquid settlement proof."
        })

    # 6. Previous Refusal
    if profile_dict.get("previous_visa_refusal") == 1:
        recommendations.append({
            "category": "Immigration History",
            "priority": "Critical Impact",
            "title": "Address Previous Refusal Grounds via GCMS Officer Notes",
            "action": "Obtain official IRCC GCMS case notes to analyze exact refusal rationale and submit a detailed submission letter with updated supporting evidence.",
            "estimated_impact": "Removes Key Negative Scrutiny Penalty",
            "disclaimer": "Failure to address prior refusal reasons will likely result in recurring application rejection."
        })

    # Default general recommendation if profile is already very strong
    if not recommendations:
        recommendations.append({
            "category": "Profile Optimization",
            "priority": "General Guidance",
            "title": "Maintain Document Integrity & Ensure Complete Application Submission",
            "action": "Your profile demonstrates strong alignment with Canadian employment immigration criteria. Ensure all supporting certificates, employment contracts, and police clearances are current.",
            "estimated_impact": "Profile Readiness Optimized",
            "disclaimer": "All predictions are model-derived estimates and do not guarantee official IRCC approval."
        })

    return recommendations
