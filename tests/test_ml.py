import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.predict import VisaPredictor
from ml.explain import VisaExplainer
from backend.recommendation_service import generate_personalized_recommendations

class TestMLPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.predictor = VisaPredictor()
        cls.explainer = VisaExplainer()

    def test_valid_applicant_prediction(self):
        sample = {
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
        result = self.predictor.predict_profile(sample)
        
        self.assertIn("prediction", result)
        self.assertIn(result["prediction"], ["Likely Approved", "Likely Denied"])
        
        # Test probability sum condition (approx 100%)
        prob_sum = result["approval_probability"] + result["denial_probability"]
        self.assertAlmostEqual(prob_sum, 100.0, places=1)
        self.assertIn(result["risk_level"], ["LOW RISK", "MEDIUM RISK", "HIGH RISK"])

    def test_explainability_generation(self):
        sample = {
            "age": 25,
            "education_level": "Diploma",
            "field_of_study": "Business",
            "eca_done": 0,
            "total_work_exp": 1,
            "relevant_work_exp": 1,
            "current_employment_status": "Unemployed",
            "teer_category": "TEER 4/5",
            "job_offer": 0,
            "employer_sponsorship": 0,
            "offered_salary_cad": 0,
            "english_test": "IELTS",
            "language_overall_score": 5.5,
            "french_proficiency": "No French",
            "annual_income_cad": 10000,
            "settlement_funds_cad": 5000,
            "outstanding_debt_cad": 5000,
            "financial_sponsor": "Family",
            "previous_canada_visa": 0,
            "previous_visa_refusal": 1,
            "previous_immigration_violation": 0,
            "previous_canada_work": 0,
            "previous_canada_study": 0,
            "criminal_record": 0,
            "medical_flag": 0
        }
        explanation = self.explainer.explain_individual_profile(sample)
        self.assertTrue(len(explanation["top_negative_factors"]) > 0)

    def test_recommendation_logic(self):
        sample = {
            "age": 28,
            "education_level": "Bachelor's",
            "eca_done": 0,
            "relevant_work_exp": 1,
            "job_offer": 0,
            "employer_sponsorship": 0,
            "language_overall_score": 6.0,
            "settlement_funds_cad": 8000,
            "dependents": 0,
            "previous_visa_refusal": 1
        }
        recs = generate_personalized_recommendations(sample, {"approval_probability": 35.0})
        self.assertTrue(len(recs) >= 3)
        categories = [r["category"] for r in recs]
        self.assertIn("Employment & Job Offer", categories)
        self.assertIn("Language Proficiency", categories)

if __name__ == "__main__":
    unittest.main()
