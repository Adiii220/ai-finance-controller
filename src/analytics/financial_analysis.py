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

# Load transactions
query = "SELECT * FROM transactions"
df = pd.read_sql(query, connection)

# Close connection
connection.close()

print("Financial data loaded successfully!")
print("Dataset Shape:", df.shape)
# Financial KPIs

total_revenue = df.loc[
    df["transaction_type"] == "Income",
    "amount"
].sum()

total_expense = df.loc[
    df["transaction_type"] == "Expense",
    "amount"
].sum()

net_profit = total_revenue - total_expense

profit_margin = (net_profit / total_revenue) * 100

print("\n--- Financial KPIs ---")
print(f"Total Revenue : ₹{total_revenue:,.2f}")
print(f"Total Expense : ₹{total_expense:,.2f}")
print(f"Net Profit    : ₹{net_profit:,.2f}")
print(f"Profit Margin : {profit_margin:.2f}%")
# Expense by Category

expense_df = df[df["transaction_type"] == "Expense"]

expense_by_category = (
    expense_df
    .groupby("category")["amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Expense by Category ---")
print(expense_by_category)
# Expense by Department

expense_by_department = (
    expense_df
    .groupby("department")["amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Expense by Department ---")
print(expense_by_department)
# Revenue by Department

income_df = df[df["transaction_type"] == "Income"]

revenue_by_department = (
    income_df
    .groupby("department")["amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Revenue by Department ---")
print(revenue_by_department)
# Revenue by Region

revenue_by_region = (
    income_df
    .groupby("region")["amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Revenue by Region ---")
print(revenue_by_region)
# Monthly Financial Analysis

df["transaction_date"] = pd.to_datetime(df["transaction_date"])

monthly_financials = (
    df.groupby(
        df["transaction_date"].dt.to_period("M")
    )
    .apply(
        lambda x: pd.Series({
            "revenue": x.loc[
                x["transaction_type"] == "Income", "amount"
            ].sum(),
            "expense": x.loc[
                x["transaction_type"] == "Expense", "amount"
            ].sum()
        }),
        include_groups=False
    )
)

monthly_financials["profit"] = (
    monthly_financials["revenue"]
    - monthly_financials["expense"]
)

print("\n--- Monthly Financial Analysis ---")
print(monthly_financials)
# Best and Worst Performing Month

best_month = monthly_financials["profit"].idxmax()
best_profit = monthly_financials["profit"].max()

worst_month = monthly_financials["profit"].idxmin()
worst_profit = monthly_financials["profit"].min()

print("\n--- Monthly Performance ---")
print("Best Performing Month:", best_month)
print(f"Best Month Profit: ₹{best_profit:,.2f}")

print("\nWorst Performing Month:", worst_month)
print(f"Worst Month Profit: ₹{worst_profit:,.2f}")
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
# Revenue by Category

revenue_by_category = (
    income_df
    .groupby("category")["amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n--- Revenue by Category ---")
print(revenue_by_category)
# Profit by Department

department_profit = (
    df.groupby("department")
      .apply(
          lambda x: pd.Series({
              "revenue": x.loc[
                  x["transaction_type"] == "Income", "amount"
              ].sum(),
              "expense": x.loc[
                  x["transaction_type"] == "Expense", "amount"
              ].sum()
          }),
          include_groups=False
      )
)

department_profit["profit"] = (
    department_profit["revenue"]
    - department_profit["expense"]
)

department_profit = department_profit.sort_values(
    "profit",
    ascending=False
)

print("\n--- Profit by Department ---")
print(department_profit)
# Profit by Region

region_profit = (
    df.groupby("region")
      .apply(
          lambda x: pd.Series({
              "revenue": x.loc[
                  x["transaction_type"] == "Income", "amount"
              ].sum(),
              "expense": x.loc[
                  x["transaction_type"] == "Expense", "amount"
              ].sum()
          }),
          include_groups=False
      )
)

region_profit["profit"] = (
    region_profit["revenue"]
    - region_profit["expense"]
)

region_profit = region_profit.sort_values(
    "profit",
    ascending=False
)

print("\n--- Profit by Region ---")
print(region_profit)
# Save analysis results for Power BI

from pathlib import Path

output_path = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
    / "department_profit.csv"
)
department_profit.to_csv(output_path)

print("\nDepartment profit analysis saved successfully!")