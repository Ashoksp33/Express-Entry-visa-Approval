import os
import sys
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "countries")
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODELS_DIR, exist_ok=True)

COUNTRY_CONFIGS = {
    "australia": {
        "file": os.path.join(DATA_DIR, "australia_raw.xlsx"),
        "target": "visa_outcome",
        "drop_cols": ["country", "visa_outcome"],
        "name": "Australia (Subclass 189 Skilled Independent)",
        "currency": "AUD",
        "model_file": os.path.join(MODELS_DIR, "australia_model_pipeline.pkl")
    },
    "uk": {
        "file": os.path.join(DATA_DIR, "uk_raw.xlsx"),
        "target": "visa_outcome",
        "drop_cols": ["country", "visa_outcome"],
        "name": "United Kingdom (Skilled Worker Visa)",
        "currency": "GBP",
        "model_file": os.path.join(MODELS_DIR, "uk_model_pipeline.pkl")
    },
    "germany": {
        "file": os.path.join(DATA_DIR, "germany_raw.xlsx"),
        "target": "visa_outcome",
        "drop_cols": ["country", "visa_outcome"],
        "name": "Germany (EU Blue Card)",
        "currency": "EUR",
        "model_file": os.path.join(MODELS_DIR, "germany_model_pipeline.pkl")
    }
}

def train_country_model(country_key: str):
    cfg = COUNTRY_CONFIGS[country_key]
    print(f"\n========================================================")
    print(f"--- Training Dedicated Model for {cfg['name']} ---")
    print(f"========================================================")
    
    df = pd.read_excel(cfg["file"])
    target = cfg["target"]
    X = df.drop(columns=cfg["drop_cols"])
    y = df[target]

    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()

    preprocessor = ColumnTransformer(transformers=[
        ('num', Pipeline([
            ('imp', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), num_cols),
        ('cat', Pipeline([
            ('imp', SimpleImputer(strategy='most_frequent')),
            ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ]), cat_cols)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train Logistic Regression as primary transparent model
    clf = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', clf)
    ])

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    probas = pipeline.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, zero_division=0)
    rec = recall_score(y_test, preds, zero_division=0)
    f1 = f1_score(y_test, preds, zero_division=0)
    roc = roc_auc_score(y_test, probas)

    print(f"[{cfg['name']}] Test Evaluation:")
    print(f"  • Accuracy: {acc*100:.2f}%")
    print(f"  • Precision: {prec*100:.2f}%")
    print(f"  • Recall: {rec*100:.2f}%")
    print(f"  • F1 Score: {f1:.4f}")
    print(f"  • ROC-AUC: {roc:.4f}")

    # Save artifact
    artifact = {
        "pipeline": pipeline,
        "country": country_key,
        "country_name": cfg["name"],
        "currency": cfg["currency"],
        "expected_columns": list(X.columns),
        "num_cols": num_cols,
        "cat_cols": cat_cols,
        "metrics": {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "roc_auc": round(roc, 4)
        }
    }
    joblib.dump(artifact, cfg["model_file"])
    print(f"Saved artifact to: {cfg['model_file']}")
    return artifact

def train_all_countries():
    results = {}
    for country in COUNTRY_CONFIGS:
        results[country] = train_country_model(country)
    return results

if __name__ == "__main__":
    train_all_countries()
