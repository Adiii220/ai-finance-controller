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

print("Payment analysis data loaded successfully!")
print("Dataset Shape:", df.shape)
# Payment Method Analysis

payment_analysis = (
    df.groupby("payment_method")
      .agg(
          transaction_count=("transaction_id", "count"),
          total_amount=("amount", "sum"),
          average_amount=("amount", "mean")
      )
      .sort_values("transaction_count", ascending=False)
)

print("\n--- Payment Method Analysis ---")
print(payment_analysis)
# Save Payment Analysis

from pathlib import Path

output_path = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
    / "payment_analysis.csv"
)

payment_analysis.to_csv(output_path)

print("\nPayment analysis saved successfully!")