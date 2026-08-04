# ============================================
# FinTrust Bank — Broken Transaction Processor
# Week 4 Day 2 PM Lab — Find and fix the 5 bugs
# ============================================

ACCOUNTS = {
    "FT-001": {"balance": 10000.0, "daily_limit": 5000.0, "daily_used": 0.0, "frozen": False},
    "FT-002": {"balance": 500.0,   "daily_limit": 2000.0, "daily_used": 0.0, "frozen": False},
    "FT-003": {"balance": 25000.0, "daily_limit": 10000.0, "daily_used": 0.0, "frozen": True},
}


def calculate_fee(amount):
    """Calculate transaction fee: 0.5% of amount, minimum R5.00."""
    fee = amount * 0.05              # BUG 1: should be 0.005 (0.5%), not 0.05 (5%)
    return max(fee, 5.0)


def check_daily_limit(account, amount):
    """Return True if transaction is within daily limit."""
    remaining = account["daily_limit"] - account["daily_used"]
    return amount <= remaining


def process_payment(sender_id, receiver_id, amount):
    if sender_id not in ACCOUNTS:
        raise ValueError(f"Sender {sender_id} not found")

    if receiver_id not in ACCOUNTS:
        raise ValueError(f"Receiver {receiver_id} not found")

    sender = ACCOUNTS[sender_id]
    receiver = ACCOUNTS[receiver_id]

    if sender["frozen"]:
        raise RuntimeError(f"Sender account {sender_id} is frozen")

    if not check_daily_limit(sender, amount):
        raise RuntimeError(f"Daily limit exceeded for {sender_id}")

    fee = calculate_fee(amount)
    total_deducted = amount + fee

    if total_deducted > sender["balance"]:
        raise RuntimeError(f"Insufficient funds in {sender_id}")

    # Process
    sender["balanse"] -= total_deducted    # BUG 2: typo — 'balanse' not 'balance'
    sender["daily_used"] += amount
    receiver["balance"] += amount          # receiver gets amount (not amount+fee)

    return {
        "sender": sender_id,
        "receiver": receiver_id,
        "amount": amount,
        "fee": fee,
        "sender_new_balance": sender["balance"],
    }


payments = [
    ("FT-001", "FT-002", 200.0),
    ("FT-001", "FT-002", 300.0),
    ("FT-002", "FT-001", 100.0),
    ("FT-003", "FT-001", 500.0),   # frozen sender — should raise
]

results = []
for sender, receiver, amt in payments:
    try:
        result = process_payment(sender, receiver, amt)
        results.append(result)
        print(f"✓ {sender} → {receiver}: R{amt:.2f} (fee: R{result['fee']:.2f})")
    except RuntimeError as e:
        print(f"✗ {sender} → {receiver}: {e}")

# BUG 3: wrong key name
print(f"\nFT-001 final balance: R{ACCOUNTS['FT-001']['balanse']:.2f}")

# BUG 4: sum should only count successful amounts, not fee
total_sent = sum(r["amount"] + r["fee"] for r in results)  # counts fee twice
print(f"Total processed (excl. failed): R{total_sent:.2f}")

# BUG 5: should print number of FAILED payments, not total payments
failed_count = len(payments)    # should be len(payments) - len(results)
print(f"Failed payments: {failed_count}")