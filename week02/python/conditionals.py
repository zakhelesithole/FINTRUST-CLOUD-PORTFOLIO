# ============================================
# Week 2 Day 4 - Python IF/ELSE Exercises
# FinTrust Bank
# Date: 13 July 2026
# ============================================

# ============================================
# Exercise 1: Transaction Classifier
# ============================================

def classify_transaction(amount):
    """
    Classifies a transaction amount into a category.
    
    Args:
        amount: float - Transaction amount
    
    Returns:
        str: Category name
    """
    if amount <= 0:
        return "INVALID"
    elif amount <= 100:
        return "MICRO"
    elif amount <= 1000:
        return "SMALL"
    elif amount <= 10000:
        return "STANDARD"
    else:
        return "LARGE"


# ============================================
# Exercise 2: Interest Rate Calculator
# ============================================

def get_interest_rate(credit_score):
    """
    Returns the interest rate based on credit score.
    
    Args:
        credit_score: int - Customer's credit score
    
    Returns:
        float: Interest rate percentage
    """
    if credit_score >= 750:
        return 7.5
    elif credit_score >= 700:
        return 9.5
    elif credit_score >= 650:
        return 12.0
    else:
        return 18.5


# ============================================
# Exercise 3: ATM Withdrawal Logic
# ============================================

def atm_withdraw(balance, amount):
    """
    Processes an ATM withdrawal.
    
    Args:
        balance: float - Current account balance
        amount: float - Amount to withdraw
    
    Returns:
        tuple: (success: bool, message: str)
    """
    ATM_LIMIT = 5000
    
    if amount <= 0:
        return (False, "Invalid amount")
    elif amount > ATM_LIMIT:
        return (False, "ATM daily limit is R5 000")
    elif amount > balance:
        return (False, "Insufficient funds")
    else:
        return (True, f"Dispensing R{amount:.2f}")


# ============================================
# Exercise 4: Transaction Tagger
# ============================================

def tag_transaction(tx_type, merchant_category, amount):
    """
    Tags a transaction based on type, category, and amount.
    
    Args:
        tx_type: str - Transaction type (e.g., DEBIT, REFUND)
        merchant_category: str - Merchant category
        amount: float - Transaction amount
    
    Returns:
        str: Transaction tag
    """
    if tx_type == "REFUND":
        return "REFUND"
    elif merchant_category == "GAMBLING":
        return "HIGH_RISK"
    elif merchant_category == "GROCERY" and amount < 500:
        return "ROUTINE"
    elif amount > 10000:
        return "LARGE_PURCHASE"
    else:
        return "STANDARD"


# ============================================
# TEST ALL EXERCISES
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("WEEK 2 DAY 4 - PYTHON CONDITIONALS")
    print("=" * 50)
    print()

    # Test Exercise 1
    print("=" * 40)
    print("EXERCISE 1: Transaction Classifier")
    print("=" * 40)
    print(f"classify_transaction(50)     → {classify_transaction(50)}")      # MICRO
    print(f"classify_transaction(9999)   → {classify_transaction(9999)}")    # STANDARD
    print(f"classify_transaction(-5)     → {classify_transaction(-5)}")      # INVALID
    print(f"classify_transaction(150)    → {classify_transaction(150)}")     # SMALL
    print(f"classify_transaction(50000)  → {classify_transaction(50000)}")   # LARGE
    print()

    # Test Exercise 2
    print("=" * 40)
    print("EXERCISE 2: Interest Rate Calculator")
    print("=" * 40)
    print(f"get_interest_rate(720)  → {get_interest_rate(720)}%")   # 9.5
    print(f"get_interest_rate(800)  → {get_interest_rate(800)}%")   # 7.5
    print(f"get_interest_rate(680)  → {get_interest_rate(680)}%")   # 12.0
    print(f"get_interest_rate(600)  → {get_interest_rate(600)}%")   # 18.5
    print(f"get_interest_rate(750)  → {get_interest_rate(750)}%")   # 7.5
    print()

    # Test Exercise 3
    print("=" * 40)
    print("EXERCISE 3: ATM Withdrawal Logic")
    print("=" * 40)
    print(f"atm_withdraw(3000, 1500)  → {atm_withdraw(3000, 1500)}")  # (True, "Dispensing R1500.00")
    print(f"atm_withdraw(500, 600)    → {atm_withdraw(500, 600)}")    # (False, "Insufficient funds")
    print(f"atm_withdraw(10000, 6000) → {atm_withdraw(10000, 6000)}") # (False, "ATM daily limit is R5 000")
    print(f"atm_withdraw(1000, -100)  → {atm_withdraw(1000, -100)}")  # (False, "Invalid amount")
    print(f"atm_withdraw(5000, 2000)  → {atm_withdraw(5000, 2000)}")  # (True, "Dispensing R2000.00")
    print()

    # Test Exercise 4
    print("=" * 40)
    print("EXERCISE 4: Transaction Tagger")
    print("=" * 40)
    print(f"tag_transaction('DEBIT', 'GROCERY', 200)    → {tag_transaction('DEBIT', 'GROCERY', 200)}")    # ROUTINE
    print(f"tag_transaction('DEBIT', 'GROCERY', 600)    → {tag_transaction('DEBIT', 'GROCERY', 600)}")    # STANDARD
    print(f"tag_transaction('DEBIT', 'GAMBLING', 1000)  → {tag_transaction('DEBIT', 'GAMBLING', 1000)}")  # HIGH_RISK
    print(f"tag_transaction('REFUND', 'RETAIL', 500)    → {tag_transaction('REFUND', 'RETAIL', 500)}")    # REFUND
    print(f"tag_transaction('DEBIT', 'RETAIL', 15000)   → {tag_transaction('DEBIT', 'RETAIL', 15000)}")   # LARGE_PURCHASE
    print()