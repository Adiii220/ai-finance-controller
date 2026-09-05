import pandas as pd
import numpy as np
from pathlib import Path

# Reproducible results
np.random.seed(42)

# Number of transactions
NUM_TRANSACTIONS = 10000

# Date range
dates = pd.date_range(
    start="2025-01-01",
    end="2026-06-30",
    periods=NUM_TRANSACTIONS
)

transaction_types = [
    "Income",
    "Expense"
]

categories = [
    "Sales",
    "Marketing",
    "Salary",
    "Rent",
    "Technology",
    "Travel",
    "Utilities",
    "Office Supplies",
    "Inventory",
    "Consulting"
]

departments = [
    "Sales",
    "Marketing",
    "HR",
    "IT",
    "Finance",
    "Operations"
]

payment_methods = [
    "Bank Transfer",
    "Credit Card",
    "Debit Card",
    "UPI",
    "Cash"
]

regions = [
    "North",
    "South",
    "East",
    "West",
    "Central"
]

# Generate transaction types
transaction_type = np.random.choice(
    transaction_types,
    size=NUM_TRANSACTIONS,
    p=[0.35, 0.65]
)

# Generate categories
category = np.random.choice(
    categories,
    size=NUM_TRANSACTIONS
)

# Generate departments
department = np.random.choice(
    departments,
    size=NUM_TRANSACTIONS
)

# Generate amounts
amount = np.random.uniform(
    1000,
    250000,
    size=NUM_TRANSACTIONS
).round(2)

# Make income generally larger
income_mask = transaction_type == "Income"
amount[income_mask] = np.random.uniform(
    10000,
    500000,
    size=income_mask.sum()
).round(2)

# Create DataFrame
df = pd.DataFrame({
    "transaction_id": [
        f"TXN{i:05d}" for i in range(1, NUM_TRANSACTIONS + 1)
    ],
    "transaction_date": dates,
    "transaction_type": transaction_type,
    "category": category,
    "department": department,
    "amount": amount,
    "payment_method": np.random.choice(
        payment_methods,
        size=NUM_TRANSACTIONS
    ),
    "customer_id": [
        f"CUST{i:04d}" for i in np.random.randint(
            1, 1001, size=NUM_TRANSACTIONS
        )
    ],
    "region": np.random.choice(
        regions,
        size=NUM_TRANSACTIONS
    ),
    "description": [
        f"{cat} transaction"
        for cat in category
    ]
})

# Convert date format
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"]
).dt.date

# Create output directory
output_path = Path("data/raw")
output_path.mkdir(parents=True, exist_ok=True)

# Save CSV
file_path = output_path / "financial_transactions.csv"

df.to_csv(file_path, index=False)

print("Dataset generated successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {file_path}")