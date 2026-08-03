# ============================================
# test_file_io.py
# Test script for CSV and JSON file I/O
# Week 3 Day 3 - Cloud to Solutions Accelerator
# ============================================

import csv
import json
from pathlib import Path
from datetime import date

print("=" * 50)
print("FILE I/O - CSV & JSON DEMO")
print("=" * 50)
print()

# ============================================
# 1. Create Sample CSV
# ============================================
print("1. Creating Sample CSV")
print("-" * 30)

sample_csv = Path("data/sample_transactions.csv")
sample_csv.parent.mkdir(parents=True, exist_ok=True)

with open(sample_csv, "w", newline="", encoding="utf-8") as f:
    f.write("id,account,type,amount,date\n")
    f.write("1,101,deposit,5000.00,2026-07-21\n")
    f.write("2,101,withdrawal,-250.00,2026-07-21\n")
    f.write("3,102,deposit,12000.00,2026-07-21\n")

print(f"Created: {sample_csv}")
print()

# ============================================
# 2. Read CSV
# ============================================
print("2. Reading CSV")
print("-" * 30)

with open(sample_csv, "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['id']}: {row['type']} R{row['amount']}")
print()

# ============================================
# 3. Create JSON
# ============================================
print("3. Creating JSON")
print("-" * 30)

transactions = [
    {"id": 1, "account": 101, "type": "deposit", "amount": 5000.00},
    {"id": 2, "account": 101, "type": "withdrawal", "amount": -250.00},
    {"id": 3, "account": 102, "type": "deposit", "amount": 12000.00},
]

summary = {
    "date": date.today().isoformat(),
    "total_transactions": len(transactions),
    "total_deposits": 17000.00,
    "total_withdrawals": -250.00,
}

json_file = Path("data/daily_summary_demo.json")
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print(f"Created: {json_file}")
print()

# ============================================
# 4. Read JSON
# ============================================
print("4. Reading JSON")
print("-" * 30)

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"  Date: {data['date']}")
print(f"  Total: {data['total_transactions']}")
print(f"  Deposits: R{data['total_deposits']:,.2f}")
print(f"  Withdrawals: R{data['total_withdrawals']:,.2f}")
print()

# ============================================
# 5. Write to JSON String
# ============================================
print("5. JSON String (for API)")
print("-" * 30)

json_string = json.dumps(transactions[0], indent=2)
print(json_string)
print()

print("=" * 50)
print("DEMO COMPLETED SUCCESSFULLY!")
print("=" * 50)