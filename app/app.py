from flask import Flask, jsonify, render_template
import os
import mysql.connector
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv


# ==============================
# LOAD ENVIRONMENT VARIABLES
# ==============================

load_dotenv()


# ==============================
# FLASK APP
# ==============================

app = Flask(__name__)


# ==============================
# DATABASE CONNECTION
# ==============================

def get_db_connection():

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
def home():

    return render_template("index.html")


# ==============================
# FINANCIAL SUMMARY API
# ==============================

@app.route("/api/summary")
def summary():

    connection = get_db_connection()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            SUM(
                CASE
                    WHEN transaction_type = 'Income'
                    THEN amount
                    ELSE 0
                END
            ) AS total_revenue,

            SUM(
                CASE
                    WHEN transaction_type = 'Expense'
                    THEN amount
                    ELSE 0
                END
            ) AS total_expense

        FROM transactions
    """)

    result = cursor.fetchone()

    connection.close()

    total_revenue = float(
        result["total_revenue"] or 0
    )

    total_expense = float(
        result["total_expense"] or 0
    )

    net_profit = (
        total_revenue - total_expense
    )

    return jsonify({

        "total_revenue": total_revenue,

        "total_expense": total_expense,

        "net_profit": net_profit

    })


# ==============================
# MONTHLY FINANCIAL API
# ==============================

@app.route("/api/monthly")
def monthly():

    connection = get_db_connection()

    query = """
        SELECT
            DATE_FORMAT(
                transaction_date,
                '%Y-%m'
            ) AS month,

            SUM(
                CASE
                    WHEN transaction_type = 'Income'
                    THEN amount
                    ELSE 0
                END
            ) AS revenue,

            SUM(
                CASE
                    WHEN transaction_type = 'Expense'
                    THEN amount
                    ELSE 0
                END
            ) AS expense

        FROM transactions

        GROUP BY
            DATE_FORMAT(
                transaction_date,
                '%Y-%m'
            )

        ORDER BY month
    """

    df = pd.read_sql(
        query,
        connection
    )

    connection.close()

    df["revenue"] = df["revenue"].astype(float)

    df["expense"] = df["expense"].astype(float)

    df["profit"] = (
        df["revenue"]
        - df["expense"]
    )

    return jsonify({

        "message":
            "Monthly financial API is working",

        "data":
            df.to_dict(
                orient="records"
            )

    })


# ==============================
# ANOMALY SUMMARY API
# ==============================

@app.route("/api/anomalies")
def anomalies():

    file_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "processed"
        / "anomaly_transactions.csv"
    )

    df = pd.read_csv(file_path)

    anomaly_df = df[
        df["anomaly"] == "Anomaly"
    ]

    total_anomalies = len(
        anomaly_df
    )

    total_anomaly_amount = (
        anomaly_df["amount"].sum()
    )

    return jsonify({

        "message":
            "Anomaly detection API is working",

        "total_anomalies":
            total_anomalies,

        "total_anomaly_amount":
            float(total_anomaly_amount)

    })


# ==============================
# ANOMALY DETAILS API
# ==============================

@app.route("/api/anomaly-details")
def anomaly_details():

    file_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "processed"
        / "anomaly_transactions.csv"
    )

    df = pd.read_csv(file_path)

    anomaly_df = df[
        df["anomaly"] == "Anomaly"
    ].copy()

    anomaly_df = anomaly_df.sort_values(
        "amount",
        ascending=False
    ).head(10)

    return jsonify({

        "anomalies":
            anomaly_df[
                [
                    "transaction_id",
                    "amount",
                    "category",
                    "department",
                    "payment_method",
                    "region"
                ]
            ].to_dict(
                orient="records"
            )

    })


# ==============================
# REVENUE FORECAST API
# ==============================

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

        "message":
            "Revenue forecast API is working",

        "forecast":
            df.to_dict(
                orient="records"
            )

    })


# ==============================
# AI FINANCIAL INSIGHTS API
# ==============================

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


# ==============================
# RECONCILIATION API
# ==============================

@app.route("/api/reconciliation")
def reconciliation():

    file_path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "processed"
        / "reconciliation_results.csv"
    )

    df = pd.read_csv(file_path)


    # Total records

    total_records = len(df)


    # Matched records

    matched_records = (
        df["status"] == "Matched"
    ).sum()


    # Exception records

    exception_records = (
        df["status"] == "Exception"
    ).sum()


    # Match rate

    if total_records > 0:

        match_rate = (
            matched_records
            / total_records
        ) * 100

    else:

        match_rate = 0


    # Get unresolved exceptions

    exceptions = df[
        df["status"] == "Exception"
    ].head(10)


    return jsonify({

        "total_records":
            int(total_records),

        "matched_records":
            int(matched_records),

        "exception_records":
            int(exception_records),

        "match_rate":
            round(match_rate, 2),

        "exceptions":
            exceptions.to_dict(
                orient="records"
            )

    })


# ==============================
# API STATUS
# ==============================

@app.route("/api/status")
def status():

    return jsonify({

        "project":
            "AI Finance Controller",

        "status":
            "running",

        "api":
            "working",

        "reconciliation":
            "available"

    })


# ==============================
# RUN FLASK APPLICATION
# ==============================

if __name__ == "__main__":

    app.run(
        debug=True
    )