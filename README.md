# AI Finance Controller

An AI-powered financial data analytics and reconciliation system built for financial operations, data analysis, anomaly detection, forecasting, and automated reconciliation.

## 🎯 Project Overview

AI Finance Controller is an end-to-end finance analytics system that helps organizations analyze financial transactions, identify unusual transactions, forecast revenue, and automate a finance-operations reconciliation workflow.

The project combines:

- Python
- Pandas & NumPy
- MySQL
- SQL Analytics
- Machine Learning
- Power BI
- Flask
- Automated Reconciliation

The system works on synthetic financial transaction data and provides both analytical insights and an automated reconciliation workflow.

---

# 🚀 Buildathon Track 04

This project addresses the requirement:

> Build an agent that closes one finance-ops loop across a 50+ record batch of synthetic data, reporting its match rate and the exceptions it could not resolve.

### Finance Reconciliation Agent

The project includes a reconciliation agent that processes a batch of **100 synthetic financial records**.

The agent:

1. Reads financial transaction records.
2. Creates a second payment-source dataset.
3. Matches transactions using transaction/reference IDs.
4. Compares transaction amounts.
5. Identifies successfully matched records.
6. Detects unresolved exceptions.
7. Calculates the overall match rate.
8. Generates detailed reconciliation results.
9. Displays the results through the Flask dashboard.

### Reconciliation Results

| Metric | Result |
|---|---:|
| Total Records | 100 |
| Matched Records | 90 |
| Exceptions | 10 |
| Match Rate | 90% |

The 10 exceptions are intentionally generated as amount mismatches to simulate realistic finance-operation exceptions.

---

# 📊 Key Features

## 1. Financial Data Analytics

The system analyzes financial transactions to calculate:

- Total Revenue
- Total Expenses
- Net Profit
- Profit Margin
- Department-wise Revenue
- Department-wise Expenses
- Department-wise Profit
- Category-wise Revenue
- Category-wise Expenses
- Region-wise Analysis
- Payment Method Analysis
- Monthly Financial Performance

---

## 2. Data Cleaning

Financial transaction data is cleaned using Python and Pandas.

The cleaning process includes:

- Duplicate removal
- Invalid amount removal
- Date conversion
- Missing-value analysis
- Data validation
- Clean dataset generation

---

## 3. SQL / MySQL Analytics

Financial transactions are stored in a MySQL database.

The project performs SQL analysis for:

- Revenue
- Expenses
- Profit
- Monthly performance
- Department performance
- Category analysis
- Region analysis
- Payment methods
- Transaction summaries

---

## 4. AI-Based Anomaly Detection

The project uses **Isolation Forest** to identify unusual financial transactions.

The anomaly detection system:

- Analyzes transaction amounts
- Detects unusual transactions
- Calculates anomaly status
- Generates anomaly reports
- Provides anomaly summaries for Power BI

---

## 5. Revenue Forecasting

The system uses **Linear Regression** to forecast future revenue.

The model:

- Uses historical income transactions
- Aggregates monthly revenue
- Trains a regression model
- Forecasts revenue for the next 6 months

Forecast period:

**July 2026 – December 2026**

---

# 🤖 Finance Reconciliation Agent

The reconciliation agent is located at:

```text
src/reconciliation/reconciliation_agent.py