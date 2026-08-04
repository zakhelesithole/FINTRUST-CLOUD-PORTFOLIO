# ============================================
# Bug Snippets - Spot and Fix
# Week 4 Day 2 - Cloud to Solutions Accelerator
# ============================================

print("=" * 70)
print("BUG SNIPPETS - SPOT AND FIX")
print("=" * 70)
print()

# ============================================
# BUG 1: Variable name typo
# ============================================
print("1. BUG 1 - Variable name typo")
print("-" * 40)

def calculate_interest(principal, rate, years):
    total = principal * (1 + rate) ** years
    return total

accounts = [
    {"id": "FT-001", "balance": 10000, "rate": 0.055},
    {"id": "FT-002", "balance": 25000, "rate": 0.062},
]

for acc in accounts:
    future_value = calculate_interest(acc["balance"], acc["rate"], 5)
    print(f"  {acc['id']}: R{future_value:.2f}")

# FIX: bonus_account exists, bonus_account["balance"] used
bonus_account = {"id": "FT-003", "balance": 5000, "rate": 0.07}
future_value = calculate_interest(bonus_account["balance"], bonus_account["rate"], 5)
print(f"  Bonus (FT-003): R{future_value:.2f}")
print()

# ============================================
# BUG 2: Off-by-one error in loop
# ============================================
print("2. BUG 2 - Off-by-one error")
print("-" * 40)

transactions = [
    {"id": "TXN001", "amount": 500.0, "type": "debit"},
    {"id": "TXN002", "amount": 1200.0, "type": "credit"},
    {"id": "TXN003", "amount": 75.50, "type": "debit"},
]

# FIX: range(len(transactions)) not len(transactions) + 1
total_debits = 0
for i in range(len(transactions)):
    txn = transactions[i]
    if txn["type"] == "debit":
        total_debits += txn["amount"]

print(f"  Total debits: R{total_debits:.2f}")
print()

# ============================================
# BUG 3: Type error - string instead of number
# ============================================
print("3. BUG 3 - Type error")
print("-" * 40)

def get_account_tier(balance):
    if balance >= 100000:
        return "Platinum"
    elif balance >= 50000:
        return "Gold"
    elif balance >= 10000:
        return "Silver"
    else:
        return "Standard"

# FIX: convert input to float
balance_str = input("  Enter account balance: ")
balance = float(balance_str)
tier = get_account_tier(balance)
print(f"  Account tier: {tier}")
print()

print("=" * 70)
print("ALL BUGS FIXED!")
print("=" * 70)