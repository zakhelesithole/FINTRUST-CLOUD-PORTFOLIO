import sqlite3
import pandas as pd
from pathlib import Path

DB_FILE = Path("data/fintrust_analytics.db")

# Load the transactions table into a DataFrame
conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query("SELECT * FROM transactions", conn)
conn.close()

print("=" * 60)
print("PANDAS ANALYSIS")
print("=" * 60)

print("\n=== DataFrame Shape ===")
print(f"Rows: {len(df)}  Columns: {len(df.columns)}")

print("\n=== Column Types ===")
print(df.dtypes)

print("\n=== First 3 Rows ===")
print(df.head(3))

# Filter: only COMPLETED transfers
completed_transfers = df[
    (df["status"] == "COMPLETED") & (df["type"] == "TRANSFER")
]
print(f"\nCompleted transfers: {len(completed_transfers)}")
print(f"Total volume: ZAR {completed_transfers['amount'].sum():,.2f}")

# Filter: large transactions (above average)
avg = df["amount"].mean()
large = df[df["amount"] > avg]
print(f"\nAbove-average transactions (>{avg:,.2f}):")
print(large[["transaction_id", "amount", "type", "status"]])

# Group by status
by_status = df.groupby("status").agg(
    count=("transaction_id", "count"),
    total_volume=("amount", "sum"),
    avg_amount=("amount", "mean")
).round(2)
print("\n=== By Status ===")
print(by_status)

# Group by type
by_type = df.groupby("type")["amount"].sum().sort_values(ascending=False)
print("\n=== Volume by Type ===")
print(by_type)

# Add columns
df["high_value"] = df["amount"] > 2000
df["txn_date"] = pd.to_datetime(df["timestamp"]).dt.date

print("\n=== DataFrame with New Columns ===")
print(df[["transaction_id", "amount", "high_value", "txn_date"]].to_string())

# Export to CSV
df.to_csv("data/transactions_enriched.csv", index=False)
print("\nExported to data/transactions_enriched.csv")
