import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_eda(csv_path="data/processed/canada_employment_visa_processed.csv", output_dir="reports/figures"):
    os.makedirs(output_dir, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    df = pd.read_csv(csv_path)
    print("--- DATASET OVERVIEW ---")
    print(f"Shape: {df.shape}")
    print(f"Missing Values:\n{df.isnull().sum().sum()}")
    print(f"\nTarget Class Distribution:\n{df['visa_outcome'].value_counts(normalize=True)}")

    # 1. Target Distribution
    fig, ax = plt.subplots(figsize=(6, 5))
    counts = df["visa_outcome"].value_counts()
    labels = ["Approved (1)", "Denied (0)"]
    colors = ["#10b981", "#ef4444"]
    ax.pie(counts, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90, explode=(0.05, 0))
    ax.set_title("Visa Outcome Distribution (Target Variable)", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "approval_vs_denial.png"), dpi=300)
    plt.close()

    # 2. Education vs Outcome
    fig, ax = plt.subplots(figsize=(8, 5))
    edu_df = df.groupby(["education_level", "visa_outcome"]).size().unstack(fill_value=0)
    edu_df.plot(kind="bar", stacked=True, color=["#ef4444", "#10b981"], ax=ax)
    ax.set_title("Visa Outcome by Education Level", fontsize=13, fontweight="bold")
    ax.set_xlabel("Education Level")
    ax.set_ylabel("Applicant Count")
    ax.legend(["Denied", "Approved"])
    plt.xticks(rotation=15)
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "education_vs_outcome.png"), dpi=300)
    plt.close()

    # 3. Work Experience & Salary vs Outcome
    fig, ax = plt.subplots(figsize=(8, 5))
    scatter = ax.scatter(
        df["total_work_exp"],
        df["offered_salary_cad"] / 1000,
        c=df["visa_outcome"],
        cmap="coolwarm",
        alpha=0.7,
        edgecolors="none",
        s=40
    )
    ax.set_title("Work Experience vs Offered Salary (k CAD)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Total Work Experience (Years)")
    ax.set_ylabel("Offered Salary (in $1,000 CAD)")
    cbar = plt.colorbar(scatter)
    cbar.set_label("Outcome (0=Denied, 1=Approved)")
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "experience_salary_outcome.png"), dpi=300)
    plt.close()

    # 4. Language Score vs Outcome
    fig, ax = plt.subplots(figsize=(7, 5))
    df.boxplot(column="language_overall_score", by="visa_outcome", ax=ax, grid=True)
    ax.set_title("Language Proficiency Score by Visa Outcome", fontsize=13, fontweight="bold")
    fig.suptitle("")
    ax.set_xlabel("Visa Outcome (0 = Denied, 1 = Approved)")
    ax.set_ylabel("Language Overall Score (CLB Scale)")
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "language_vs_outcome.png"), dpi=300)
    plt.close()

    # 5. Job Offer & Employer Sponsorship vs Outcome
    fig, ax = plt.subplots(figsize=(7, 5))
    job_df = df.groupby(["job_offer", "visa_outcome"]).size().unstack(fill_value=0)
    job_df.plot(kind="bar", color=["#ef4444", "#10b981"], ax=ax)
    ax.set_title("Visa Outcome by Canadian Job Offer", fontsize=13, fontweight="bold")
    ax.set_xticklabels(["No Job Offer", "Has Job Offer"], rotation=0)
    ax.set_ylabel("Applicant Count")
    ax.legend(["Denied", "Approved"])
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "job_offer_vs_outcome.png"), dpi=300)
    plt.close()

    # 6. Numeric Feature Correlation Heatmap
    numeric_cols = [
        "age", "total_work_exp", "relevant_work_exp", "offered_salary_cad",
        "language_overall_score", "settlement_funds_cad", "financial_strength_score", "visa_outcome"
    ]
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(9, 7))
    cax = ax.matshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0, len(numeric_cols), 1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(numeric_cols, rotation=45, ha="left", fontsize=9)
    ax.set_yticklabels(numeric_cols, fontsize=9)
    ax.set_title("Key Numerical Features Correlation Matrix", fontsize=12, fontweight="bold", pad=40)
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "feature_correlation_heatmap.png"), dpi=300)
    plt.close()

    print(f"EDA visual reports generated and saved to: {output_dir}")

if __name__ == "__main__":
    run_eda()
