import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "visa_system.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            applicant_summary TEXT NOT NULL,
            prediction TEXT NOT NULL,
            approval_probability REAL NOT NULL,
            denial_probability REAL NOT NULL,
            risk_level TEXT NOT NULL,
            positive_factors TEXT,
            negative_factors TEXT,
            recommendations TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_application_record(summary: dict, prediction: str, approval_prob: float,
                            denial_prob: float, risk_level: str,
                            positive_factors: list, negative_factors: list, recommendations: list) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applications (
            applicant_summary, prediction, approval_probability, denial_probability,
            risk_level, positive_factors, negative_factors, recommendations
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        json.dumps(summary),
        prediction,
        approval_prob,
        denial_prob,
        risk_level,
        json.dumps(positive_factors),
        json.dumps(negative_factors),
        json.dumps(recommendations)
    ))
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def fetch_application_history(limit=20) -> list:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, created_at, applicant_summary, prediction, approval_probability,
               denial_probability, risk_level, positive_factors, negative_factors, recommendations
        FROM applications
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    history = []
    for r in rows:
        history.append({
            "id": r["id"],
            "created_at": r["created_at"],
            "applicant_summary": json.loads(r["applicant_summary"]) if r["applicant_summary"] else {},
            "prediction": r["prediction"],
            "approval_probability": r["approval_probability"],
            "denial_probability": r["denial_probability"],
            "risk_level": r["risk_level"],
            "positive_factors": json.loads(r["positive_factors"]) if r["positive_factors"] else [],
            "negative_factors": json.loads(r["negative_factors"]) if r["negative_factors"] else [],
            "recommendations": json.loads(r["recommendations"]) if r["recommendations"] else []
        })
    conn.close()
    return history

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
