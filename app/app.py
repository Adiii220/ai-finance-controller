from flask import Flask, jsonify, render_template
import os
import mysql.connector
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/api/summary")
def summary():
    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            SUM(CASE WHEN transaction_type = 'Income' THEN amount ELSE 0 END) AS total_revenue,
            SUM(CASE WHEN transaction_type = 'Expense' THEN amount ELSE 0 END) AS total_expense
        FROM transactions
    """)

    result = cursor.fetchone()

    connection.close()

    total_revenue = float(result["total_revenue"] or 0)
    total_expense = float(result["total_expense"] or 0)
    net_profit = total_revenue - total_expense

    return jsonify({
        "total_revenue": total_revenue,
        "total_expense": total_expense,
        "net_profit": net_profit
    })
@app.route("/api/monthly")
def monthly():
    return jsonify({
        "message": "Monthly financial API is working",
        "data": [
            {
                "month": "2026-01",
                "revenue": 45000000,
                "expense": 40000000,
                "profit": 5000000
            },
            {
                "month": "2026-02",
                "revenue": 48000000,
                "expense": 42000000,
                "profit": 6000000
            },
            {
                "month": "2026-03",
                "revenue": 52000000,
                "expense": 44000000,
                "profit": 8000000
            }
        ]
    })
@app.route("/api/anomalies")
def anomalies():
    file_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "processed"
        / "anomaly_transactions.csv"
    )

    df = pd.read_csv(file_path)

    anomaly_df = df[df["anomaly"] == "Anomaly"]

    total_anomalies = len(anomaly_df)
    total_anomaly_amount = anomaly_df["amount"].sum()

    return jsonify({
        "message": "Anomaly detection API is working",
        "total_anomalies": total_anomalies,
        "total_anomaly_amount": float(total_anomaly_amount)
    })
@app.route("/api/forecast")
def forecast():
    file_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "processed"
        / "revenue_forecast.csv"
    )

    df = pd.read_csv(file_path)

    return jsonify({
        "message": "Revenue forecast API is working",
        "forecast": df.to_dict(orient="records")
    })
@app.route("/api/anomaly-details")
def anomaly_details():
    file_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "processed"
        / "anomaly_transactions.csv"
    )

    df = pd.read_csv(file_path)

    anomaly_df = df[df["anomaly"] == "Anomaly"].copy()

    anomaly_df = anomaly_df.sort_values(
        "amount",
        ascending=False
    ).head(10)

    return jsonify({
        "anomalies": anomaly_df[
            [
                "transaction_id",
                "amount",
                "category",
                "department",
                "payment_method",
                "region"
            ]
        ].to_dict(orient="records")
    })
@app.route("/api/status")
def status():
    return jsonify({
        "project": "AI Finance Controller",
        "status": "running",
        "api": "working"
    })
@app.route("/api/insights")
def insights():
    return jsonify({
        "insights": [
            "Revenue is higher than expenses, indicating positive financial performance.",
            "498 unusual financial transactions were detected.",
            "High-value transactions should be monitored carefully.",
            "Anomaly-prone categories should be reviewed regularly."
        ]
    })
if __name__ == "__main__":
    app.run(debug=True)