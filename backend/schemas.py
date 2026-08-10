from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ApplicantProfileSchema(BaseModel):
    # Section A: Personal Details
    age: int = Field(default=30, ge=18, le=70, description="Applicant age between 18 and 70")
    country_citizenship: str = Field(default="India")
    country_residence: str = Field(default="India")
    marital_status: str = Field(default="Single")
    dependents: int = Field(default=0, ge=0, le=10)

    # Section B: Education Details
    education_level: str = Field(default="Bachelor's")
    field_of_study: str = Field(default="Computer Science")
    eca_done: int = Field(default=1, ge=0, le=1)

    # Section C: Employment Details
    total_work_exp: int = Field(default=5, ge=0, le=50)
    relevant_work_exp: int = Field(default=4, ge=0, le=50)
    current_employment_status: str = Field(default="Employed")
    teer_category: str = Field(default="TEER 1")
    job_offer: int = Field(default=1, ge=0, le=1)
    employer_sponsorship: int = Field(default=0, ge=0, le=1)
    offered_salary_cad: float = Field(default=75000.0, ge=0.0)

    # Section D: Language Details
    english_test: str = Field(default="IELTS")
    language_overall_score: float = Field(default=7.5, ge=0.0, le=10.0)
    french_proficiency: str = Field(default="No French")

    # Section E: Financial Details
    annual_income_cad: float = Field(default=35000.0, ge=0.0)
    settlement_funds_cad: float = Field(default=30000.0, ge=0.0)
    outstanding_debt_cad: float = Field(default=0.0, ge=0.0)
    financial_sponsor: str = Field(default="Self")

    # Section F: Immigration History
    previous_canada_visa: int = Field(default=0, ge=0, le=1)
    previous_visa_refusal: int = Field(default=0, ge=0, le=1)
    previous_immigration_violation: int = Field(default=0, ge=0, le=1)
    previous_canada_work: int = Field(default=0, ge=0, le=1)
    previous_canada_study: int = Field(default=0, ge=0, le=1)

    # Section G: Background
    criminal_record: int = Field(default=0, ge=0, le=1)
    medical_flag: int = Field(default=0, ge=0, le=1)

class AnalysisResponseSchema(BaseModel):
    id: Optional[int] = None
    prediction: str
    approval_probability: float
    denial_probability: float
    risk_level: str
    model_used: str
    top_positive_factors: List[Dict[str, Any]]
    top_negative_factors: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    global_feature_importances: List[Dict[str, Any]]
    shap_available: bool
    applicant_summary: Dict[str, Any]
