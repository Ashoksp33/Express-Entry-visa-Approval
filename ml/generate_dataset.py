import os
import numpy as np
import pandas as pd

def generate_canada_visa_dataset(num_samples=1200, random_state=42):
    np.random.seed(random_state)

    ages = np.random.randint(18, 62, size=num_samples)
    citizenships = np.random.choice(
        ["India", "Philippines", "Nigeria", "China", "Brazil", "UK", "USA", "Pakistan", "France", "Vietnam"],
        size=num_samples,
        p=[0.25, 0.15, 0.12, 0.10, 0.08, 0.07, 0.08, 0.06, 0.05, 0.04]
    )
    residences = np.random.choice(
        ["India", "Philippines", "Nigeria", "China", "Brazil", "UK", "USA", "Canada", "UAE", "Germany"],
        size=num_samples
    )
    marital_statuses = np.random.choice(["Single", "Married", "Common-Law", "Divorced"], size=num_samples, p=[0.45, 0.42, 0.08, 0.05])
    dependents = np.random.choice([0, 1, 2, 3, 4], size=num_samples, p=[0.50, 0.22, 0.18, 0.07, 0.03])

    education_levels = np.random.choice(
        ["High School", "Diploma", "Bachelor's", "Master's", "PhD"],
        size=num_samples,
        p=[0.10, 0.20, 0.45, 0.20, 0.05]
    )
    fields_of_study = np.random.choice(
        ["Computer Science", "Information Technology", "Engineering", "Healthcare", "Business", "Finance", "Other"],
        size=num_samples,
        p=[0.22, 0.18, 0.20, 0.12, 0.15, 0.08, 0.05]
    )
    eca_done = np.where(np.isin(education_levels, ["High School"]), np.random.choice([0, 1], size=num_samples, p=[0.7, 0.3]),
                        np.random.choice([0, 1], size=num_samples, p=[0.15, 0.85]))

    # Work experience
    total_exp = np.array([max(0, min(a - 20, np.random.poisson(lam=5))) for a in ages])
    relevant_exp = np.array([min(t, np.random.randint(0, t + 1)) if t > 0 else 0 for t in total_exp])

    employment_status = np.random.choice(["Employed", "Self-employed", "Unemployed"], size=num_samples, p=[0.78, 0.15, 0.07])
    teer_category = np.random.choice(["TEER 0", "TEER 1", "TEER 2", "TEER 3", "TEER 4/5"], size=num_samples, p=[0.25, 0.35, 0.22, 0.12, 0.06])

    job_offer = np.random.choice([1, 0], size=num_samples, p=[0.55, 0.45])
    employer_sponsorship = np.where(job_offer == 1, np.random.choice([1, 0], size=num_samples, p=[0.75, 0.25]), 0)

    offered_salary = np.where(job_offer == 1,
                              np.random.normal(loc=78000, scale=22000, size=num_samples).astype(int),
                              0)
    offered_salary = np.maximum(offered_salary, 0)

    english_test = np.random.choice(["IELTS", "CELPIP", "Other", "No Test"], size=num_samples, p=[0.60, 0.25, 0.08, 0.07])
    # Language score (equivalent CLB scale 4.0 to 10.0)
    language_score = np.where(english_test == "No Test", np.random.uniform(4.0, 5.5, size=num_samples),
                              np.random.uniform(5.5, 9.5, size=num_samples))
    language_score = np.round(language_score, 1)

    french_proficiency = np.random.choice(["No French", "Basic", "Intermediate", "Advanced"], size=num_samples, p=[0.70, 0.18, 0.08, 0.04])

    annual_income = np.random.normal(loc=45000, scale=20000, size=num_samples).astype(int)
    annual_income = np.maximum(annual_income, 8000)

    settlement_funds = np.random.exponential(scale=25000, size=num_samples).astype(int) + 3000
    outstanding_debt = np.random.exponential(scale=8000, size=num_samples).astype(int)

    financial_sponsor = np.random.choice(["Self", "Family", "Employer", "Other"], size=num_samples, p=[0.60, 0.20, 0.15, 0.05])

    # Immigration history
    prev_ca_visa = np.random.choice([1, 0], size=num_samples, p=[0.30, 0.70])
    prev_refusal = np.random.choice([1, 0], size=num_samples, p=[0.18, 0.82])
    prev_violation = np.random.choice([1, 0], size=num_samples, p=[0.05, 0.95])
    prev_ca_work = np.random.choice([1, 0], size=num_samples, p=[0.22, 0.78])
    prev_ca_study = np.random.choice([1, 0], size=num_samples, p=[0.18, 0.82])

    criminal_record = np.random.choice([1, 0], size=num_samples, p=[0.04, 0.96])
    medical_flag = np.random.choice([1, 0], size=num_samples, p=[0.03, 0.97])

    # Calculate realistic outcome logit based on domain logic
    # Base probability calculation:
    score = np.zeros(num_samples)

    # Job offer & LMIA are critical for Canadian employment visa
    score += job_offer * 2.2
    score += employer_sponsorship * 1.8

    # Work experience
    score += np.minimum(relevant_exp, 8) * 0.35

    # Education & ECA
    edu_score_map = {"High School": 0.0, "Diploma": 0.5, "Bachelor's": 1.2, "Master's": 1.8, "PhD": 2.2}
    score += np.array([edu_score_map[e] for e in education_levels])
    score += eca_done * 0.8

    # Language score (CLB / IELTS equivalent)
    score += (language_score - 5.0) * 0.55
    french_map = {"No French": 0.0, "Basic": 0.3, "Intermediate": 0.7, "Advanced": 1.2}
    score += np.array([french_map[f] for f in french_proficiency])

    # Financial solvency (LICO threshold ~13,757 CAD baseline + dependents)
    required_lico = 13757 + dependents * 3500
    funds_ratio = settlement_funds / required_lico
    score += np.clip(funds_ratio - 1.0, -2.0, 2.0) * 0.6

    # Canadian experience advantage
    score += prev_ca_work * 1.2
    score += prev_ca_study * 0.8
    score += prev_ca_visa * 0.5

    # Age points (optimal 20-35)
    age_penalty = np.where(ages > 35, (ages - 35) * 0.08, 0.0)
    score -= age_penalty

    # Negative flags
    score -= prev_refusal * 2.0
    score -= prev_violation * 3.5
    score -= criminal_record * 4.5
    score -= medical_flag * 3.0

    # Add random variation
    logits = score - 3.8 + np.random.normal(0, 0.8, size=num_samples)
    probs = 1 / (1 + np.exp(-logits))
    visa_outcome = (probs >= 0.50).astype(int)

    df = pd.DataFrame({
        "age": ages,
        "country_citizenship": citizenships,
        "country_residence": residences,
        "marital_status": marital_statuses,
        "dependents": dependents,
        "education_level": education_levels,
        "field_of_study": fields_of_study,
        "eca_done": eca_done,
        "total_work_exp": total_exp,
        "relevant_work_exp": relevant_exp,
        "current_employment_status": employment_status,
        "teer_category": teer_category,
        "job_offer": job_offer,
        "employer_sponsorship": employer_sponsorship,
        "offered_salary_cad": offered_salary,
        "english_test": english_test,
        "language_overall_score": language_score,
        "french_proficiency": french_proficiency,
        "annual_income_cad": annual_income,
        "settlement_funds_cad": settlement_funds,
        "outstanding_debt_cad": outstanding_debt,
        "financial_sponsor": financial_sponsor,
        "previous_canada_visa": prev_ca_visa,
        "previous_visa_refusal": prev_refusal,
        "previous_immigration_violation": prev_violation,
        "previous_canada_work": prev_ca_work,
        "previous_canada_study": prev_ca_study,
        "criminal_record": criminal_record,
        "medical_flag": medical_flag,
        "visa_outcome": visa_outcome
    })

    return df

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    df_raw = generate_canada_visa_dataset(1200, random_state=42)
    raw_path = "data/raw/canada_employment_visa_raw.csv"
    df_raw.to_csv(raw_path, index=False)
    print(f"Generated raw dataset: {raw_path} with shape {df_raw.shape}")
    print(f"Approval Target Distribution:\n{df_raw['visa_outcome'].value_counts(normalize=True)}")
