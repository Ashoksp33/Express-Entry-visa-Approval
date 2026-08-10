import os
import sys
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.preprocessing import prepare_data, build_preprocessor
from ml.evaluate import evaluate_classifier, compare_models

def train_and_evaluate_models(models_dir="models"):
    os.makedirs(models_dir, exist_ok=True)

    # Prepare dataset
    df_proc, X_train, X_test, y_train, y_test = prepare_data()

    # Preprocessor
    preprocessor = build_preprocessor()

    # Define candidate models with balanced class weights where applicable
    candidate_models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=6, class_weight="balanced", random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=250, max_depth=12, class_weight="balanced", random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=150, max_depth=5, learning_rate=0.08, random_state=42)
    }

    eval_results = []
    trained_pipelines = {}

    print("--- TRAINING & EVALUATING MODELS ---")
    for name, clf in candidate_models.items():
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])

        pipeline.fit(X_train, y_train)
        metrics = evaluate_classifier(pipeline, X_test, y_test, model_name=name)
        eval_results.append(metrics)
        trained_pipelines[name] = pipeline
        print(f"[{name}] -> Accuracy: {metrics['Accuracy']}, F1: {metrics['F1 Score']}, ROC-AUC: {metrics['ROC-AUC']}")

    comparison_df = compare_models(eval_results)
    print("\n--- MODEL COMPARISON TABLE ---")
    print(comparison_df.to_string(index=False))

    # Select Random Forest as primary production pipeline
    best_model_name = "Random Forest"
    best_pipeline = trained_pipelines[best_model_name]

    pipeline_save_path = os.path.join(models_dir, "visa_prediction_pipeline.pkl")
    joblib.dump({
        "pipeline": best_pipeline,
        "model_name": best_model_name,
        "comparison_metrics": comparison_df.to_dict(orient="records")
    }, pipeline_save_path)

    print(f"\nSaved primary ML pipeline ({best_model_name}) to: {pipeline_save_path}")

    return best_pipeline, comparison_df

if __name__ == "__main__":
    train_and_evaluate_models()
