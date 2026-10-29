import os
import sys
import joblib
import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.predict import VisaPredictor
from ml.country_mapper import map_profile_to_country, COUNTRY_METADATA

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

class MultiCountryPredictor:
    def __init__(self):
        # Canada model (primary default)
        self.canada_predictor = VisaPredictor()
        
        # Load dedicated country models
        self.country_models = {}
        for country in ["australia", "uk", "germany"]:
            pkl_path = os.path.join(MODELS_DIR, f"{country}_model_pipeline.pkl")
            if os.path.exists(pkl_path):
                self.country_models[country] = joblib.load(pkl_path)
            else:
                print(f"[Warning] Model file not found for {country}: {pkl_path}")

    def predict_profile(self, profile_dict: dict) -> dict:
        country_key = profile_dict.get("target_country", "canada").lower().strip()
        
        # If Canada or unsupported, use original Canada predictor
        if country_key not in self.country_models:
            res = self.canada_predictor.predict_profile(profile_dict)
            res["target_country"] = "canada"
            res["country_name"] = "Canada"
            res["country_flag"] = "🍁"
            res["currency"] = "CAD"
            res["model_used"] = "Standard Eligibility Assessment (Canada)"
            return res

        # Predict using dedicated country model
        artifact = self.country_models[country_key]
        pipeline = artifact["pipeline"]
        expected_cols = artifact["expected_columns"]
        country_name = artifact.get("country_name", country_key.title())
        currency = artifact.get("currency", "USD")
        meta = COUNTRY_METADATA.get(country_key, {})

        # Map applicant input to country-specific features
        mapped_dict = map_profile_to_country(profile_dict, country_key, expected_cols)
        df_input = pd.DataFrame([mapped_dict])[expected_cols]

        probas = pipeline.predict_proba(df_input)[0]
        approval_prob = float(np.round(probas[1], 4))
        denial_prob = float(np.round(1.0 - approval_prob, 4))

        prediction = "Likely Approved" if approval_prob >= 0.50 else "Likely Denied"
        
        if approval_prob >= 0.75:
            risk_level = "LOW RISK"
        elif approval_prob >= 0.50:
            risk_level = "MEDIUM RISK"
        else:
            risk_level = "HIGH RISK"

        return {
            "prediction": prediction,
            "approval_probability": round(approval_prob * 100, 2),
            "denial_probability": round(denial_prob * 100, 2),
            "risk_level": risk_level,
            "model_used": f"Standard Eligibility Assessment ({country_name})",
            "target_country": country_key,
            "country_name": country_name,
            "country_flag": meta.get("flag", "🌐"),
            "currency": currency,
            "applicant_summary": {
                "age": profile_dict.get("age", 30),
                "education_level": profile_dict.get("education_level", "Bachelor's"),
                "field_of_study": profile_dict.get("field_of_study", "Computer Science"),
                "relevant_work_exp": profile_dict.get("relevant_work_exp", 4),
                "offered_salary": profile_dict.get("offered_salary_cad", 75000),
                "language_score": profile_dict.get("language_overall_score", 7.5),
                "job_offer": profile_dict.get("job_offer", 1),
                "settlement_funds": profile_dict.get("settlement_funds_cad", 30000)
            }
        }

_multi_predictor = None

def get_model_service():
    global _multi_predictor
    if _multi_predictor is None:
        _multi_predictor = MultiCountryPredictor()
    return _multi_predictor
