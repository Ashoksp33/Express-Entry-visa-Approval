from flask import Flask, render_template, request, jsonify
from ml_engine import VisaIntelligenceEngine

app = Flask(__name__)

# Initialize the trained machine learning & XAI engine
engine = VisaIntelligenceEngine("visa_dataset.csv")

# Define preset profiles for rapid prototype testing
PRESETS = {
    "strong_tech": {
        "title": "Strong Tech Professional (Canada)",
        "data": {
            "age": 32,
            "salary": 135000,
            "experience": 8,
            "ielts_score": 8.5,
            "bank_balance": 85000,
            "education": "Masters",
            "job_role": "Data Scientist",
            "sponsorship": "Yes",
            "international_experience": "Yes",
            "criminal_record": "No",
            "employment_type": "Full-Time",
            "country": "Canada"
        }
    },
    "high_risk": {
        "title": "High Risk Tourist (Low Funds & Criminal Flag)",
        "data": {
            "age": 24,
            "salary": 35000,
            "experience": 1,
            "ielts_score": 5.8,
            "bank_balance": 18000,
            "education": "Diploma",
            "job_role": "Software Engineer",
            "sponsorship": "No",
            "international_experience": "No",
            "criminal_record": "Yes",
            "employment_type": "Contract",
            "country": "Australia"
        }
    },
    "borderline": {
        "title": "Borderline Applicant (USA)",
        "data": {
            "age": 29,
            "salary": 65000,
            "experience": 3,
            "ielts_score": 6.5,
            "bank_balance": 32000,
            "education": "Bachelors",
            "job_role": "Cloud Engineer",
            "sponsorship": "No",
            "international_experience": "Yes",
            "criminal_record": "No",
            "employment_type": "Contract",
            "country": "USA"
        }
    },
    "phd_researcher": {
        "title": "PhD AI Researcher (Germany)",
        "data": {
            "age": 30,
            "salary": 110000,
            "experience": 7,
            "ielts_score": 8.0,
            "bank_balance": 62000,
            "education": "PhD",
            "job_role": "AI Engineer",
            "sponsorship": "Yes",
            "international_experience": "Yes",
            "criminal_record": "No",
            "employment_type": "Full-Time",
            "country": "Germany"
        }
    }
}

@app.route("/", methods=["GET", "POST"])
def home():
    result_data = None
    input_data = PRESETS["strong_tech"]["data"] # Default template values

    if request.method == "POST":
        input_data = {
            "age": int(request.form.get("age", 30)),
            "salary": int(request.form.get("salary", 75000)),
            "experience": int(request.form.get("experience", 3)),
            "ielts_score": float(request.form.get("ielts_score", 7.0)),
            "bank_balance": int(request.form.get("bank_balance", 40000)),
            "education": request.form.get("education", "Bachelors"),
            "job_role": request.form.get("job_role", "Software Engineer"),
            "sponsorship": request.form.get("sponsorship", "No"),
            "international_experience": request.form.get("international_experience", "No"),
            "criminal_record": request.form.get("criminal_record", "No"),
            "employment_type": request.form.get("employment_type", "Full-Time"),
            "country": request.form.get("country", "USA")
        }

        # Run Prediction & XAI Analysis
        result_data = engine.predict(input_data)

    return render_template("index.html", 
                           result=result_data, 
                           input_data=input_data, 
                           presets=PRESETS)

@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid payload"}), 400
    
    result_data = engine.predict(data)
    return jsonify(result_data)

@app.route("/api/presets", methods=["GET"])
def api_presets():
    return jsonify(PRESETS)

if __name__ == "__main__":
    print("Starting AI Driven Immigration Decision Support System on 0.0.0.0:5000...")
    app.run(host="0.0.0.0", port=5000, debug=False)
