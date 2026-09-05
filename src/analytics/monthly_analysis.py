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

# Convert date column
df["transaction_date"] = pd.to_datetime(df["transaction_date"])

print("Monthly analysis data loaded successfully!")
print("Dataset Shape:", df.shape)# Monthly Revenue

income_df = df[df["transaction_type"] == "Income"]

monthly_revenue = (
    income_df
    .groupby(
        income_df["transaction_date"].dt.to_period("M")
    )["amount"]
    .sum()
)

print("\n--- Monthly Revenue ---")
print(monthly_revenue)
# Monthly Expense

expense_df = df[df["transaction_type"] == "Expense"]

monthly_expense = (
    expense_df
    .groupby(
        expense_df["transaction_date"].dt.to_period("M")
    )["amount"]
    .sum()
)

print("\n--- Monthly Expense ---")
print(monthly_expense)
# Monthly Revenue vs Expense

monthly_financials = pd.DataFrame({
    "Revenue": monthly_revenue,
    "Expense": monthly_expense
})

print("\n--- Monthly Revenue vs Expense ---")
print(monthly_financials)
# Monthly Profit

monthly_financials["Profit"] = (
    monthly_financials["Revenue"]
    - monthly_financials["Expense"]
)

print("\n--- Monthly Profit ---")
print(monthly_financials)
# Best and Worst Month

best_month = monthly_financials["Profit"].idxmax()
best_profit = monthly_financials["Profit"].max()

worst_month = monthly_financials["Profit"].idxmin()
worst_profit = monthly_financials["Profit"].min()

print("\n--- Best & Worst Month ---")
print("Best Month:", best_month)
print(f"Best Month Profit: ₹{best_profit:,.2f}")

print("\nWorst Month:", worst_month)
print(f"Worst Month Profit: ₹{worst_profit:,.2f}")
# Save Monthly Analysis

from pathlib import Path

output_path = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
    / "monthly_financials.csv"
)

monthly_financials.to_csv(output_path)

print("\nMonthly financial analysis saved successfully!")