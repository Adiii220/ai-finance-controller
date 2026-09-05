# AI Finance Controller

## AI-Powered Financial Data Analytics and Forecasting System

AI Finance Controller is a data analytics project designed to analyze
financial transactions, revenue, expenses, budgets and financial performance.

## Objectives

- Analyze financial transactions
- Clean and preprocess financial data
- Perform SQL-based financial analysis
- Create interactive Power BI dashboards
- Detect unusual financial transactions
- Forecast future revenue and expenses
- Generate financial insights

## Key Features

- Financial transaction analysis
- Revenue and expense analysis
- Department-wise and region-wise performance analysis
- Monthly financial performance tracking
- Budget and actual financial comparison
- AI-based anomaly detection
- Revenue forecasting for upcoming months
- Interactive Power BI dashboard
- Flask-based financial analytics web dashboard

## Project Architecture

```text
Financial Data
      ↓
Data Cleaning & Preprocessing
      ↓
MySQL Database
      ↓
SQL Analysis
      ↓
Python Analytics
      ↓
Anomaly Detection + Forecasting
      ↓
Power BI Dashboard
      ↓
Flask Web Dashboard
      ↓
Financial Insights


## Project Structure

```text
ai-finance-controller/
│
├── app/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── 01_data_cleaning.ipynb
│
├── src/
│   ├── analytics/
│   ├── anomaly_detection/
│   ├── data/
│   ├── forecasting/
│   ├── mysql_connection.py
│   └── load_data_from_mysql.py
│
├── sql/
├── tests/
├── README.md
└── requirements.txt

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Adiii220/ai-finance-controller.git
cd ai-finance-controller

## MySQL Database Setup

### 1. Create the database

```sql
CREATE DATABASE ai_finance_controller;


## Project Workflow

1. Financial transaction data is generated and collected.
2. Data is cleaned and preprocessed using Python and Pandas.
3. Cleaned data is stored and analyzed using MySQL.
4. Python is used for financial analysis and KPI calculation.
5. Machine Learning is used for anomaly detection.
6. Revenue forecasting is performed using Linear Regression.
7. Power BI is used to create interactive financial dashboards.
8. Flask is used to provide a web-based financial analytics dashboard.
9. Financial insights are presented through dashboards and reports.

## Dashboard

The project includes three main dashboard sections:

### Executive Dashboard
- Total Revenue
- Total Expense
- Net Profit
- Monthly Revenue vs Expense
- Department-wise Profit
- Payment Method Analysis
- Anomaly Analysis
- Revenue Forecast

### Financial Analysis
- Expense by Category
- Department-wise Expense
- Revenue by Department
- Revenue by Region
- Expense by Region
- Revenue by Category
- Payment Method Analysis
- Anomaly Transaction Details

### AI Financial Insights
- Total Anomalies
- Total Anomaly Amount
- Financial Performance Insights
- High-value Transaction Monitoring
- Anomaly-prone Category Monitoring

## Project Results

The system successfully provides:

- Financial performance analysis
- Revenue and expense tracking
- Department and region-wise analysis
- Monthly financial performance
- Automated anomaly detection
- Six-month revenue forecasting
- Interactive Power BI dashboards
- Flask-based web analytics dashboard
- AI-generated financial insights

## Repository

GitHub: https://github.com/Adiii220/ai-finance-controller

## Technology Stack

- Python
- Pandas
- NumPy
- SQL
- MySQL
- Power BI
- Excel
- Scikit-learn
- Flask

## Project Workflow

Financial Data
→ Data Cleaning
→ SQL Analysis
→ Exploratory Data Analysis
→ Power BI Dashboard
→ Machine Learning
→ Financial Insights