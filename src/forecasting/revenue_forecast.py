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

# Load income transactions
query = """
SELECT transaction_date, amount
FROM transactions
WHERE transaction_type = 'Income'
"""

df = pd.read_sql(query, connection)

# Close connection
connection.close()

# Convert date column
df["transaction_date"] = pd.to_datetime(df["transaction_date"])

print("Forecasting data loaded successfully!")
print("Dataset Shape:", df.shape)
# Prepare monthly revenue data

monthly_revenue = (
    df.groupby(
        df["transaction_date"].dt.to_period("M")
    )["amount"]
    .sum()
    .reset_index()
)

monthly_revenue.columns = ["month", "revenue"]

print("\n--- Monthly Revenue Data ---")
print(monthly_revenue)
# Create numeric month index

monthly_revenue["month_number"] = range(1, len(monthly_revenue) + 1)

print("\n--- Forecasting Dataset ---")
print(monthly_revenue)
from sklearn.linear_model import LinearRegression
# Create Linear Regression model

X = monthly_revenue[["month_number"]]
y = monthly_revenue["revenue"]

model = LinearRegression()

print("Linear Regression model created successfully!")
# Train Linear Regression model

model.fit(X, y)

print("\nLinear Regression model trained successfully!")
# Create future month numbers

future_month_numbers = pd.DataFrame({
    "month_number": range(
        len(monthly_revenue) + 1,
        len(monthly_revenue) + 7
    )
})

print("\n--- Future Month Numbers ---")
print(future_month_numbers)# Predict future revenue

future_revenue = model.predict(
    future_month_numbers[["month_number"]]
)

future_month_numbers["forecasted_revenue"] = future_revenue

print("\n--- Future Revenue Forecast ---")
print(future_month_numbers)
# Create actual future month names

future_months = pd.date_range(
    start="2026-07-01",
    periods=6,
    freq="MS"
)

future_month_numbers["month"] = future_months.strftime("%Y-%m")

print("\n--- Final Revenue Forecast ---")
print(
    future_month_numbers[
        ["month", "forecasted_revenue"]
    ]
)
from pathlib import Path

# Save revenue forecast
output_path = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
    / "revenue_forecast.csv"
)

future_month_numbers[
    ["month", "forecasted_revenue"]
].to_csv(output_path, index=False)

print("\nRevenue forecast saved successfully!")
print("File:", output_path)