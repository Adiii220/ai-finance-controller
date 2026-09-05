import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to MySQL
connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Load transaction data
query = "SELECT * FROM transactions"
df = pd.read_sql(query, connection)

# Close connection
connection.close()

print("Anomaly detection data loaded successfully!")
print("Dataset Shape:", df.shape)
# Prepare transaction amount for anomaly detection

X = df[["amount"]].copy()

print("\nAmount data prepared for anomaly detection!")
print("Shape:", X.shape)
from sklearn.ensemble import IsolationForest
# Create Isolation Forest model

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

print("Isolation Forest model created successfully!")
# Train the Isolation Forest model

model.fit(X)

print("\nAnomaly detection model trained successfully!")
# Predict anomalies

df["anomaly_score"] = model.predict(X)

df["anomaly"] = df["anomaly_score"].map({
    1: "Normal",
    -1: "Anomaly"
})

print("\nAnomaly classification completed!")
print(df["anomaly"].value_counts())
# Extract anomalous transactions

anomalies = df[df["anomaly"] == "Anomaly"].copy()

print("\n--- Anomalous Transactions ---")
print("Total anomalies:", len(anomalies))

print("\nTop 10 anomalous transactions:")
print(
    anomalies[
        [
            "transaction_id",
            "transaction_date",
            "transaction_type",
            "category",
            "amount",
            "department",
            "region",
            "anomaly"
        ]
    ]
    .sort_values("amount", ascending=False)
    .head(10)
)
# Save anomaly results

from pathlib import Path

output_path = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
    / "anomaly_transactions.csv"
)

anomalies.to_csv(output_path, index=False)

print("\nAnomaly results saved successfully!")
# Anomaly Summary by Category

anomaly_summary = (
    anomalies
    .groupby("category")
    .agg(
        anomaly_count=("transaction_id", "count"),
        total_amount=("amount", "sum")
    )
    .sort_values("anomaly_count", ascending=False)
)

print("\n--- Anomaly Summary by Category ---")
print(anomaly_summary)
# Save anomaly summary

summary_path = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
    / "anomaly_summary.csv"
)

anomaly_summary.to_csv(summary_path)

print("\nAnomaly summary saved successfully!")