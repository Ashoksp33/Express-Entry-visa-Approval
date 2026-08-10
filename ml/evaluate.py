import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

def evaluate_classifier(model, X_test, y_test, model_name="Model"):
    """
    Evaluates a classification model on test set and returns metric summary.
    """
    y_pred = model.predict(X_test)
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]
    else:
        y_proba = y_pred

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_proba)

    metrics = {
        "Model": model_name,
        "Accuracy": round(float(acc), 4),
        "Precision": round(float(prec), 4),
        "Recall": round(float(rec), 4),
        "F1 Score": round(float(f1), 4),
        "ROC-AUC": round(float(roc_auc), 4)
    }

    return metrics

def compare_models(model_results_list):
    """
    Generates a formatted pandas DataFrame comparing model metrics.
    """
    df_results = pd.DataFrame(model_results_list)
    df_results = df_results.sort_values(by="ROC-AUC", ascending=False).reset_index(drop=True)
    return df_results
