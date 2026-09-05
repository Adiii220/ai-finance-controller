from pathlib import Path
import pandas as pd
import numpy as np


# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "financial_transactions_cleaned.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "processed"
)


# Load financial transactions
df = pd.read_csv(INPUT_FILE)

df["transaction_date"] = pd.to_datetime(
    df["transaction_date"]
)


# Use 100 records as reconciliation batch
source_a = df.head(100).copy()


# Create second payment source
source_b = source_a[
    [
        "transaction_id",
        "transaction_date",
        "amount"
    ]
].copy()

source_b = source_b.rename(
    columns={
        "transaction_id": "reference_id",
        "transaction_date": "payment_date",
        "amount": "paid_amount"
    }
)


# Create 10 realistic amount mismatches
np.random.seed(42)

for i in range(0, 100, 10):

    source_b.loc[
        source_b.index[i],
        "paid_amount"
    ] = (
        source_b.loc[
            source_b.index[i],
            "paid_amount"
        ] * 1.05
    )


# Reconciliation
results = []

for _, transaction in source_a.iterrows():

    reference_id = transaction["transaction_id"]

    match = source_b[
        source_b["reference_id"] == reference_id
    ]

    if len(match) == 0:

        results.append({
            "transaction_id": reference_id,
            "status": "Exception",
            "reason": "No matching payment record"
        })

        continue


    payment = match.iloc[0]

    amount_difference = abs(
        transaction["amount"]
        - payment["paid_amount"]
    )


    if amount_difference <= 0.01:

        status = "Matched"
        reason = "Amount and reference matched"

    else:

        status = "Exception"
        reason = "Amount mismatch"


    results.append({
        "transaction_id": reference_id,
        "transaction_amount": transaction["amount"],
        "paid_amount": payment["paid_amount"],
        "difference": amount_difference,
        "status": status,
        "reason": reason
    })


# Create reconciliation result
reconciliation_df = pd.DataFrame(results)


# Calculate metrics
total_records = len(reconciliation_df)

matched_records = (
    reconciliation_df["status"] == "Matched"
).sum()

exception_records = (
    reconciliation_df["status"] == "Exception"
).sum()

match_rate = (
    matched_records / total_records
) * 100


# Save detailed results
reconciliation_df.to_csv(
    OUTPUT_DIR / "reconciliation_results.csv",
    index=False
)


# Save summary
summary = pd.DataFrame([
    {
        "total_records": total_records,
        "matched_records": matched_records,
        "exception_records": exception_records,
        "match_rate": round(match_rate, 2)
    }
])

summary.to_csv(
    OUTPUT_DIR / "reconciliation_summary.csv",
    index=False
)


# Display results
print("Reconciliation Agent completed successfully!")
print("Total Records:", total_records)
print("Matched Records:", matched_records)
print("Exceptions:", exception_records)
print("Match Rate:", round(match_rate, 2), "%")