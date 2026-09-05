import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

# Load database settings
load_dotenv()

# Connect to MySQL
connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# SQL query
query = "SELECT * FROM transactions"

# Load MySQL data into Pandas
df = pd.read_sql(query, connection)

# Close connection
connection.close()

# Display results
print("Data loaded successfully!")
print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nDataset Information:")
print(df.info())

print("\nTransaction Type:")
print(df["transaction_type"].value_counts())

print("\nTotal Revenue:")
print(df.loc[df["transaction_type"] == "Income", "amount"].sum())

print("\nTotal Expense:")
print(df.loc[df["transaction_type"] == "Expense", "amount"].sum())