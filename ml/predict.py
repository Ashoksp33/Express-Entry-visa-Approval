import os
import sys
import joblib
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.preprocessing import engineer_features, NUMERIC_FEATURES, CATEGORICAL_FEATURES, BINARY_FEATURES

DEFAULT_PIPELINE_PATH = os.path.join("models", "visa_prediction_pipeline.pkl")

class VisaPredictor:
    def __init__(self, model_path=DEFAULT_PIPELINE_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model pipeline artifact not found at {model_path}. Run ml/train.py first.")
        
        artifact = joblib.load(model_path)
        self.pipeline = artifact["pipeline"]
        self.model_name = artifact.get("model_name", "Random Forest")
        self.comparison_metrics = artifact.get("comparison_metrics", [])

    def classify_risk(self, approval_proba: float) -> str:
        """
        Classifies risk based on approval probability thresholds:
        - Approval >= 75%: LOW RISK
        - Approval 50% - 74.9%: MEDIUM RISK
        - Approval < 50%: HIGH RISK
        """
        if approval_proba >= 0.75:
            return "LOW RISK"
        elif approval_proba >= 0.50:
            return "MEDIUM RISK"
        else:
            return "HIGH RISK"

    def predict_profile(self, raw_input_dict: dict) -> dict:
        """
        Processes raw applicant dictionary and returns decision support prediction.
        """
        df_input = pd.DataFrame([raw_input_dict])

        # Apply domain feature engineering
        df_engineered = engineer_features(df_input)

        # Ensure all expected columns exist
        expected_cols = NUMERIC_FEATURES + CATEGORICAL_FEATURES + BINARY_FEATURES
        for col in expected_cols:
            if col not in df_engineered.columns:
                df_engineered[col] = 0

        X_input = df_engineered[expected_cols]

        # Model probability estimation
        probas = self.pipeline.predict_proba(X_input)[0]
        # Class index 1 is Approved, index 0 is Denied
        approval_prob = float(np.round(probas[1], 4))
        denial_prob = float(np.round(1.0 - approval_prob, 4))

        prediction = "Likely Approved" if approval_prob >= 0.50 else "Likely Denied"
        risk_level = self.classify_risk(approval_prob)

        return {
            "prediction": prediction,
            "approval_probability": float(np.round(approval_prob * 100, 2)),
            "denial_probability": float(np.round(denial_prob * 100, 2)),
            "raw_approval_prob": approval_prob,
            "raw_denial_prob": denial_prob,
            "risk_level": risk_level,
            "model_used": self.model_name
        }

if __name__ == "__main__":
    predictor = VisaPredictor()
    sample_applicant = {
        "age": 30,
        "country_citizenship": "India",
        "country_residence": "India",
        "marital_status": "Single",
        "dependents": 0,
        "education_level": "Master's",
        "field_of_study": "Computer Science",
        "eca_done": 1,
        "total_work_exp": 6,
        "relevant_work_exp": 5,
        "current_employment_status": "Employed",
        "teer_category": "TEER 1",
        "job_offer": 1,
        "employer_sponsorship": 1,
        "offered_salary_cad": 95000,
        "english_test": "IELTS",
        "language_overall_score": 8.5,
        "french_proficiency": "Basic",
        "annual_income_cad": 55000,
        "settlement_funds_cad": 45000,
        "outstanding_debt_cad": 2000,
        "financial_sponsor": "Self",
        "previous_canada_visa": 0,
        "previous_visa_refusal": 0,
        "previous_immigration_violation": 0,
        "previous_canada_work": 0,
        "previous_canada_study": 0,
        "criminal_record": 0,
        "medical_flag": 0
    }
    res = predictor.predict_profile(sample_applicant)
    print("Sample Prediction Result:", res)
