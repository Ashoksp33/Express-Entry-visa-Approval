# Canada Employment Visa Decision Support Dataset

## Overview
This directory contains the dataset used for training, validating, and evaluating the **AI-Driven Canada Employment Visa Decision Support System**.

## Data Structure
- `raw/canada_employment_visa_raw.csv`: Raw synthetic applicant profile records (1,200 samples) generated for Canadian Employment/Work Immigration pathways.
- `processed/canada_employment_visa_processed.csv`: Cleaned, validated, engineered, and encoded dataset ready for machine learning model training.

## Conceptual Features
- `age`: Applicant age (18 - 70 years)
- `country_citizenship`: Country of citizenship
- `education_level`: Highest academic qualification (High School, Diploma, Bachelor's, Master's, PhD)
- `field_of_study`: Major field of study (Computer Science, Information Technology, Engineering, Healthcare, Business, Finance, Other)
- `eca_done`: Educational Credential Assessment status (1 = Yes, 0 = No)
- `total_work_exp`: Total years of work experience
- `relevant_work_exp`: Years of relevant work experience in NOC/TEER category
- `current_employment_status`: Current status (Employed, Self-employed, Unemployed)
- `teer_category`: NOC TEER Category (TEER 0, TEER 1, TEER 2, TEER 3, TEER 4/5)
- `job_offer`: Valid Canadian employment offer (1 = Yes, 0 = No)
- `employer_sponsorship`: LMIA / Employer sponsorship support (1 = Yes, 0 = No)
- `offered_salary_cad`: Annual offered salary in CAD
- `english_test`: Language test taken (IELTS, CELPIP, Other, None)
- `language_overall_score`: Standardized English language proficiency score (equivalent CLB 4-10 scale)
- `french_proficiency`: French language proficiency level (None, Basic, Intermediate, Advanced)
- `annual_income_cad`: Current annual income in CAD
- `settlement_funds_cad`: Available liquid proof of funds in CAD
- `outstanding_debt_cad`: Outstanding debt liabilities in CAD
- `financial_sponsor`: Financial backing source (Self, Family, Employer, Other)
- `financial_strength_score`: Derived financial strength metric (0.0 to 100.0)
- `settlement_funds_adequate`: Binary indicator if settlement funds meet minimum IRCC LICO threshold (~13,757 CAD baseline for single applicant)
- `previous_canada_visa`: History of prior Canadian visa approval (1 = Yes, 0 = No)
- `previous_visa_refusal`: Record of previous visa refusal from Canada or Five Eyes (1 = Yes, 0 = No)
- `previous_immigration_violation`: Overstay or violation history (1 = Yes, 0 = No)
- `previous_canada_work`: Prior work experience inside Canada (1 = Yes, 0 = No)
- `previous_canada_study`: Prior study experience inside Canada (1 = Yes, 0 = No)
- `criminal_record`: Criminal inadmissibility flag (1 = Yes, 0 = No)
- `medical_flag`: Medical inadmissibility flag (1 = Yes, 0 = No)
- `visa_outcome`: Binary Target variable (1 = Likely Approved, 0 = Likely Denied)

## Data Provenance & Academic Disclaimer
> [!IMPORTANT]
> **Academic Project Disclaimer**: This dataset is a high-fidelity synthetic prototype dataset engineered specifically for university project demonstration and software pipeline verification. It models realistic Canadian Express Entry (Federal Skilled Worker) and Employer-driven Work Permit assessment patterns, but does **NOT** represent actual confidential IRCC (Immigration, Refugees and Citizenship Canada) applicant records. Predictions derived from this dataset are for decision-support evaluation only.
