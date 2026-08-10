import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

NUMERIC_FEATURES = [
    "age",
    "dependents",
    "total_work_exp",
    "relevant_work_exp",
    "offered_salary_cad",
    "language_overall_score",
    "annual_income_cad",
    "settlement_funds_cad",
    "outstanding_debt_cad",
    "financial_strength_score",
    "debt_to_income_ratio",
    "relevant_exp_ratio"
]

CATEGORICAL_FEATURES = [
    "education_level",
    "field_of_study",
    "current_employment_status",
    "teer_category",
    "english_test",
    "french_proficiency",
    "financial_sponsor",
    "marital_status",
    "country_citizenship",
    "country_residence"
]

BINARY_FEATURES = [
    "eca_done",
    "job_offer",
    "employer_sponsorship",
    "settlement_funds_adequate",
    "previous_canada_visa",
    "previous_visa_refusal",
    "previous_immigration_violation",
    "previous_canada_work",
    "previous_canada_study",
    "criminal_record",
    "medical_flag"
]

TARGET_COL = "visa_outcome"

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies domain feature engineering based on IRCC LICO thresholds
    and employment immigration metrics.
    """
    df = df.copy()

    # Ensure required numeric columns exist with defaults if missing
    for col, default_val in [
        ("dependents", 0),
        ("settlement_funds_cad", 0.0),
        ("annual_income_cad", 0.0),
        ("offered_salary_cad", 0.0),
        ("outstanding_debt_cad", 0.0),
        ("relevant_work_exp", 0),
        ("total_work_exp", 0)
    ]:
        if col not in df.columns:
            df[col] = default_val

    # Calculate LICO (Low Income Cut-Off) base requirement ~13,757 CAD + ~3,500 CAD per dependent
    lico_required = 13757 + (df["dependents"] * 3500)
    df["settlement_funds_adequate"] = (df["settlement_funds_cad"] >= lico_required).astype(int)

    # Debt to income ratio
    total_income = df["annual_income_cad"] + df["offered_salary_cad"] + 1.0
    df["debt_to_income_ratio"] = np.round(df["outstanding_debt_cad"] / total_income, 4)

    # Relevant experience ratio
    df["relevant_exp_ratio"] = np.round(df["relevant_work_exp"] / (df["total_work_exp"] + 1.0), 4)

    # Composite financial strength score (0 to 100)
    solvency_ratio = np.clip(df["settlement_funds_cad"] / lico_required, 0.0, 5.0)
    income_score = np.clip(df["annual_income_cad"] / 50000.0, 0.0, 3.0)
    debt_penalty = np.clip(df["debt_to_income_ratio"], 0.0, 2.0) * 15.0

    financial_score = (solvency_ratio * 30.0) + (income_score * 20.0) - debt_penalty + 25.0
    df["financial_strength_score"] = np.round(np.clip(financial_score, 0.0, 100.0), 2)

    return df

def build_preprocessor() -> ColumnTransformer:
    """
    Constructs an sklearn ColumnTransformer for numeric and categorical attributes.
    """
    numeric_transformer = Pipeline(steps=[
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
            ("bin", "passthrough", BINARY_FEATURES)
        ]
    )

    return preprocessor

def prepare_data(raw_csv_path="data/raw/canada_employment_visa_raw.csv",
                 processed_csv_path="data/processed/canada_employment_visa_processed.csv",
                 test_size=0.2, random_state=42):
    """
    Loads raw dataset, cleans data, engineers features, splits into train/test, and saves processed dataset.
    """
    if not os.path.exists(raw_csv_path):
        raise FileNotFoundError(f"Raw dataset not found at {raw_csv_path}")

    df_raw = pd.read_csv(raw_csv_path)

    # Data cleaning
    df_clean = df_raw.drop_duplicates().dropna()

    # Feature engineering
    df_processed = engineer_features(df_clean)

    # Save processed CSV
    os.makedirs(os.path.dirname(processed_csv_path), exist_ok=True)
    df_processed.to_csv(processed_csv_path, index=False)
    print(f"Processed dataset saved to: {processed_csv_path} (Shape: {df_processed.shape})")

    X = df_processed[NUMERIC_FEATURES + CATEGORICAL_FEATURES + BINARY_FEATURES]
    y = df_processed[TARGET_COL]

    # Stratified train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    return df_processed, X_train, X_test, y_train, y_test

if __name__ == "__main__":
    df_p, X_tr, X_te, y_tr, y_te = prepare_data()
    print(f"Train size: {X_tr.shape[0]}, Test size: {X_te.shape[0]}")
