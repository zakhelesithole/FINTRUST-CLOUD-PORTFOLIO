# ============================================
# transaction_flowchart.py
# FinTrust Bank — Automated Transaction Decision Engine
# Week 2 Day 4 — Cloud to Solutions Accelerator
# ============================================

BLOCKED_COUNTRIES = ["KP", "IR", "CU", "SY", "SD"]
DAILY_LIMIT = 50000
ATM_LIMIT = 5000
LARGE_THRESHOLD = 10000
REVIEW_THRESHOLD = 5000

def assess_transaction(tx_id, customer, amount, destination, is_trusted_device):
    """
    Evaluate a FinTrust Bank transaction and return a decision.

    Args:
        tx_id (str): Unique transaction reference
        customer (str): Customer full name
        amount (float): Transaction amount in ZAR
        destination (str): ISO 3166-1 alpha-2 country code
        is_trusted_device (bool): True if device is registered

    Returns:
        dict: {
            "tx_id": str,
            "customer": str,
            "status": "APPROVED" | "PENDING" | "REVIEW" | "BLOCKED",
            "reason": str
        }
    """
    # 1. Check destination against BLOCKED_COUNTRIES
    if destination.upper() in BLOCKED_COUNTRIES:
        return {
            "tx_id": tx_id,
            "customer": customer,
            "status": "BLOCKED",
            "reason": f"Transfer to {destination} is not permitted"
        }
    
    # 2. Check amount > DAILY_LIMIT
    if amount > DAILY_LIMIT:
        return {
            "tx_id": tx_id,
            "customer": customer,
            "status": "BLOCKED",
            "reason": f"Amount exceeds daily limit of R{DAILY_LIMIT:,.0f}"
        }
    
    # 3. Check amount <= 0
    if amount <= 0:
        return {
            "tx_id": tx_id,
            "customer": customer,
            "status": "BLOCKED",
            "reason": "Invalid amount"
        }
    
    # 4. Check for large transactions
    if amount > LARGE_THRESHOLD:
        if is_trusted_device:
            return {
                "tx_id": tx_id,
                "customer": customer,
                "status": "PENDING",
                "reason": "Large transfer — OTP verification required"
            }
        else:
            return {
                "tx_id": tx_id,
                "customer": customer,
                "status": "REVIEW",
                "reason": "Large transfer from unrecognised device"
            }
    
    # 5. Check for moderate amount from untrusted device
    if amount > REVIEW_THRESHOLD and not is_trusted_device:
        return {
            "tx_id": tx_id,
            "customer": customer,
            "status": "REVIEW",
            "reason": "Moderate amount from unrecognised device"
        }
    
    # 6. Default: APPROVED
    return {
        "tx_id": tx_id,
        "customer": customer,
        "status": "APPROVED",
        "reason": "All checks passed"
    }


# ============================================
# TEST CASES
# ============================================

test_cases = [
    # (tx_id, customer, amount, destination, is_trusted_device)
    ("TX001", "Thabo Nkosi",    500.00, "ZA", True),
    ("TX002", "Amahle Dlamini", 15000.00, "ZA", True),
    ("TX003", "Sipho Mokoena",  8000.00, "ZA", False),
    ("TX004", "Lerato Sithole", 200.00, "IR", True),
    ("TX005", "Nomvula Dube",   75000.00, "ZA", True),
]

if __name__ == "__main__":
    print("=" * 70)
    print("FINTRIST BANK - TRANSACTION DECISION ENGINE")
    print("=" * 70)
    print(f"{'TX ID':<8} {'Customer':<20} {'Status':<10} Reason")
    print("=" * 70)

    for tc in test_cases:
        result = assess_transaction(*tc)
        print(f"{result['tx_id']:<8} {result['customer']:<20} {result['status']:<10} {result['reason']}")

    print("=" * 70)