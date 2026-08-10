# AI-Driven Canada Employment Visa Decision Support System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.2+-orange.svg)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-University%20Prototype%20Ready-brightgreen.svg)]()

> **University Final-Year Engineering Project Prototype**  
> An end-to-end Machine Learning and Explainable AI (XAI) decision-support platform for evaluating Canadian employment and work immigration application profiles.

---

## 📌 1. Project Purpose & Problem Statement
Navigating Canadian employment immigration pathways (Express Entry Federal Skilled Worker, Employer Work Permits, and Provincial Nominee Programs) involves complex multi-variable evaluations across age, educational credentials, specialized work experience, NOC TEER skill categories, language benchmarks (IELTS/CELPIP), and liquid settlement solvency.

This project delivers a **web-based AI decision-support platform** designed to provide prospective applicants and university review panels with transparent, model-derived estimates of approval likelihood, risk classification, factor attribution (XAI), and personalized profile optimization guidance.

> [!IMPORTANT]
> **Academic Disclaimer**: This tool is an academic AI decision-support prototype. Predictions are statistical estimates generated from trained machine learning models and do **NOT** represent official Canadian government immigration decisions. Final visa determinations are made exclusively by Immigration, Refugees and Citizenship Canada (IRCC) officers.

---

## 🎯 2. Main System Workflow
```
HOME / OVERVIEW (1-Click Presets)
       │
       ▼
APPLICATION FORM (Multi-Section Form)
       │
       ▼
DATA VALIDATION & PREPROCESSING (Feature Engineering)
       │
       ▼
MACHINE LEARNING MODEL (Random Forest Pipeline)
       │
       ▼
PROBABILITY & RISK EVALUATION (Approval/Denial % & LOW/MEDIUM/HIGH Risk)
       │
       ▼
EXPLAINABLE AI (XAI Positive & Risk Factors + SHAP Feature Importance)
       │
       ▼
PERSONALIZED RECOMMENDATIONS (Targeted Profile Optimization Suggestions)
       │
       ▼
SQLITE DATABASE HISTORY & VISUAL DASHBOARD
```

---

## 💻 3. Technology Stack
- **Machine Learning & Pipeline**: Scikit-Learn (`Pipeline`, `ColumnTransformer`, `RandomForestClassifier`), Pandas, NumPy, Joblib, SHAP
- **Backend API**: FastAPI, Pydantic v2, Uvicorn, SQLite3
- **Frontend Dashboard**: HTML5, CSS3 (Vanilla CSS design system), Modern JavaScript (Fetch API, Chart.js)
- **Testing**: Python `unittest`, `httpx` (FastAPI TestClient)

---

## 📊 4. Dataset & Preprocessing Strategy
- **Raw Data**: `data/raw/canada_employment_visa_raw.csv` (1,200 records)
- **Processed Data**: `data/processed/canada_employment_visa_processed.csv` (1,200 records, 34 engineered features)
- **Feature Engineering**:
  - `settlement_funds_adequate`: Evaluates available liquid reserves against mandatory IRCC LICO (Low Income Cut-Off) family size thresholds.
  - `financial_strength_score`: Composite metric (0.0 - 100.0) factoring solvency ratio, income, and debt ratio.
  - `debt_to_income_ratio`: Outstanding debt relative to annual income & salary.
  - `relevant_exp_ratio`: Ratio of NOC/TEER relevant work experience to total experience.

---

## 📈 5. Machine Learning Methodology & Model Benchmark
Four candidate classification algorithms were trained and evaluated on an independent 20% stratified test dataset (240 samples):

| Model Architecture | Accuracy | Precision | Recall | F1 Score | ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 90.42% | 93.63% | 91.87% | 0.9274 | **0.9651** | Benchmark Candidate |
| **Gradient Boosting** | 89.58% | 91.41% | 93.13% | 0.9226 | 0.9404 | Benchmark Candidate |
| 🌟 **Random Forest** | **83.33%** | **86.59%** | **88.75%** | **0.8765** | **0.9288** | **Selected Primary Pipeline** |
| **Decision Tree** | 77.50% | 85.33% | 80.00% | 0.8258 | 0.7788 | Baseline |

**Selection Rationale**: Random Forest Classifier was selected as the primary production decision engine due to its non-linear feature interaction capacity, high stability on tabular data, balanced recall/precision, and native Mean Decrease in Impurity (MDI) feature importance.

---

## 🔍 6. Explainable AI (XAI) & Risk Classification
- **Approval Probability**: $P(\text{Approved})$ estimated via `model.predict_proba()`
- **Denial Probability**: $P(\text{Denied}) = 1.0 - P(\text{Approved})$
- **Configurable Risk Rules**:
  - $P(\text{Approved}) \ge 75\% \implies$ **LOW RISK**
  - $50\% \le P(\text{Approved}) < 75\% \implies$ **MEDIUM RISK**
  - $P(\text{Approved}) < 50\% \implies$ **HIGH RISK**
- **Attribution Explanations**: Identifies specific positive factors (Master's degree, LMIA sponsorship, IELTS 8.0+) and negative factors (Low funds, previous refusal history) with quantified impact percentages.

---

## 🚀 7. Installation & Running Instructions

### Step 1: Clone Repository & Virtual Environment
```bash
git clone https://github.com/Ashoksp33/My-Portfolio.git
cd My-Portfolio
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Full Pipeline & Training Script
```bash
python ml/generate_dataset.py
python ml/preprocessing.py
python ml/eda.py
python ml/train.py
```

### Step 4: Run Automated Test Suite
```bash
python -m unittest discover tests
```

### Step 5: Launch FastAPI Web Application
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
Open your browser at: **[http://localhost:8000](http://localhost:8000)**

---

## 🌐 8. API Endpoint Documentation

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Server health and ML engine status |
| `GET` | `/presets` | Pre-configured demo profiles for 1-click panel testing |
| `POST` | `/predict` | Evaluates applicant profile and returns probabilities & risk |
| `POST` | `/explain` | Generates XAI factor breakdown and SHAP values |
| `POST` | `/analyze` | Complete analysis: Predicts + Explains + Recommends + Stores to DB |
| `GET` | `/history` | Fetches saved prediction history from SQLite |
| `GET` | `/model-info` | Returns model comparison matrix & global feature importances |

---

## 🚀 9. Future MLOps Roadmap

```
PHASE 2 (Containerization & CI/CD):
- Docker containerization & docker-compose orchestration
- GitHub Actions CI/CD automated test & build pipeline
- MLflow tracking for hyperparameter logging and model registry

PHASE 3 (Monitoring & Cloud Infrastructure):
- Evidently AI for automated data drift and concept drift detection
- Cloud PostgreSQL database integration & OAuth2 user authentication
- Prometheus & Grafana dashboard for API latency and inference monitoring

PHASE 4 (Multi-Pathways & Advanced Recommendation):
- Multi-class expansion for Student, Visitor, and Provincial Nominee Streams
- Optical Character Recognition (OCR) for automated passport & IELTS transcript parsing
```

---

## ⚖️ 10. Official Academic Disclaimer
> "This application is an academic AI-based decision-support prototype. Its predictions are statistical estimates generated from available training data and are not official Canadian immigration decisions. The system does not guarantee visa approval or denial and should not be considered legal or immigration advice. Final decisions are made exclusively by authorized Canadian immigration officials."
