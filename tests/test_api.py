import os
import sys
import unittest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.main import app
from backend.database import init_db

class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")

    def test_presets_endpoint(self):
        response = self.client.get("/presets")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("strong_profile", data)
        self.assertIn("moderate_profile", data)
        self.assertIn("weak_profile", data)

    def test_predict_endpoint(self):
        sample_payload = {
            "age": 32,
            "country_citizenship": "India",
            "country_residence": "India",
            "marital_status": "Single",
            "dependents": 0,
            "education_level": "Master's",
            "field_of_study": "Computer Science",
            "eca_done": 1,
            "total_work_exp": 7,
            "relevant_work_exp": 6,
            "current_employment_status": "Employed",
            "teer_category": "TEER 1",
            "job_offer": 1,
            "employer_sponsorship": 1,
            "offered_salary_cad": 105000,
            "english_test": "IELTS",
            "language_overall_score": 8.5,
            "french_proficiency": "Basic",
            "annual_income_cad": 60000,
            "settlement_funds_cad": 50000,
            "outstanding_debt_cad": 0,
            "financial_sponsor": "Self",
            "previous_canada_visa": 0,
            "previous_visa_refusal": 0,
            "previous_immigration_violation": 0,
            "previous_canada_work": 0,
            "previous_canada_study": 0,
            "criminal_record": 0,
            "medical_flag": 0
        }
        response = self.client.post("/predict", json=sample_payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn("prediction", json_data)
        self.assertIn("approval_probability", json_data)
        self.assertIn("denial_probability", json_data)

    def test_analyze_endpoint(self):
        sample_payload = {
            "age": 29,
            "country_citizenship": "China",
            "country_residence": "China",
            "marital_status": "Single",
            "dependents": 0,
            "education_level": "Bachelor's",
            "field_of_study": "Engineering",
            "eca_done": 1,
            "total_work_exp": 4,
            "relevant_work_exp": 3,
            "current_employment_status": "Employed",
            "teer_category": "TEER 2",
            "job_offer": 1,
            "employer_sponsorship": 0,
            "offered_salary_cad": 70000,
            "english_test": "IELTS",
            "language_overall_score": 7.0,
            "french_proficiency": "No French",
            "annual_income_cad": 35000,
            "settlement_funds_cad": 25000,
            "outstanding_debt_cad": 1000,
            "financial_sponsor": "Self",
            "previous_canada_visa": 0,
            "previous_visa_refusal": 0,
            "previous_immigration_violation": 0,
            "previous_canada_work": 0,
            "previous_canada_study": 0,
            "criminal_record": 0,
            "medical_flag": 0
        }
        response = self.client.post("/analyze", json=sample_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("recommendations", data)
        self.assertIn("top_positive_factors", data)

    def test_invalid_age_validation(self):
        invalid_payload = {
            "age": 12, # Min allowed is 18
            "total_work_exp": 2,
            "relevant_work_exp": 2,
            "language_overall_score": 7.0,
            "settlement_funds_cad": 20000,
            "job_offer": 1
        }
        response = self.client.post("/predict", json=invalid_payload)
        self.assertEqual(response.status_code, 422) # Unprocessable Entity Validation Error

if __name__ == "__main__":
    unittest.main()
