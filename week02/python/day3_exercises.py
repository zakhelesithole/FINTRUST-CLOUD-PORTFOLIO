# ============================================
# Week 2 Day 3 - Python Fundamentals Exercises
# FinTrust Bank
# Date: 12 July 2026
# ============================================

from decimal import Decimal
import math

# ============================================
# Exercise 1: Account Formatter
# ============================================

def format_account_summary(customer_name, account_type, balance):
    """
    Formats an account summary string.
    
    Args:
        customer_name: str - Full name of customer
        account_type: str - Type of account (e.g., SAVINGS, CHEQUE)
        balance: float or Decimal - Account balance
    
    Returns:
        str: Formatted account summary
    """
    d_balance = Decimal(str(balance))
    return (
        f"Customer: {customer_name.title()}\n"
        f"Account:  {account_type.upper()}\n"
        f"Balance:  R {d_balance:,.2f}\n"
        f"Status:   ACTIVE"
    )


# ============================================
# Exercise 2: Compound Interest Calculator
# ============================================

def calculate_compound_interest(principal, annual_rate, years, n=12):
    """
    Calculates compound interest.
    
    Formula: A = P(1 + r/n)^(nt)
    
    Args:
        principal: Decimal - Initial amount
        annual_rate: float - Annual interest rate (e.g., 0.085 for 8.5%)
        years: int - Number of years
        n: int - Compounding periods per year (default 12 = monthly)
    
    Returns:
        tuple: (final_amount, interest_earned) as Decimals
    """
    p = float(principal)
    amount = p * (1 + annual_rate / n) ** (n * years)
    interest_earned = amount - p
    return Decimal(str(round(amount, 2))), Decimal(str(round(interest_earned, 2)))


# ============================================
# Exercise 3: List Operations - Transaction Analysis
# ============================================

def analyze_transactions(transactions):
    """
    Analyzes a list of transaction amounts.
    
    Args:
        transactions: list of Decimal - Transaction amounts
    
    Returns:
        dict: Contains total, average, max, min, count_above_5000
    """
    if not transactions:
        return None
    
    total = sum(transactions)
    average = total / len(transactions)
    max_amount = max(transactions)
    min_amount = min(transactions)
    count_above_5000 = sum(1 for t in transactions if t > Decimal("5000.00"))
    
    return {
        "total": total,
        "average": average,
        "max": max_amount,
        "min": min_amount,
        "count_above_5000": count_above_5000
    }


# ============================================
# TEST ALL EXERCISES
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("WEEK 2 DAY 3 - PYTHON EXERCISES")
    print("=" * 50)
    print()

    # Test Exercise 1
    print("=" * 40)
    print("EXERCISE 1: Account Formatter")
    print("=" * 40)
    print(format_account_summary("thabo nkosi", "savings", 52750.00))
    print()
    print(format_account_summary("amahle dlamini", "cheque", 8900.50))
    print()

    # Test Exercise 2
    print("=" * 40)
    print("EXERCISE 2: Compound Interest")
    print("=" * 40)
    
    principal = Decimal("50000.00")
    amount, interest = calculate_compound_interest(principal, 0.085, 3)
    print(f"Principal: R {principal:,.2f}")
    print(f"Rate: 8.5% p.a.")
    print(f"Years: 3")
    print(f"Final Amount: R {amount:,.2f}")
    print(f"Interest Earned: R {interest:,.2f}")
    print()

    # Test Exercise 3
    print("=" * 40)
    print("EXERCISE 3: Transaction Analysis")
    print("=" * 40)
    
    transactions = [
        Decimal("250.00"), Decimal("12500.00"), Decimal("750.50"),
        Decimal("88000.00"), Decimal("1200.00"), Decimal("3450.00"),
        Decimal("55000.00"), Decimal("125.00"), Decimal("9800.00")
    ]
    
    print("Transactions:")
    for i, t in enumerate(transactions, 1):
        print(f"  {i}. R {t:,.2f}")
    print()
    
    result = analyze_transactions(transactions)
    
    print("Analysis Results:")
    print(f"  Total:              R {result['total']:,.2f}")
    print(f"  Average:            R {result['average']:,.2f}")
    print(f"  Largest:            R {result['max']:,.2f}")
    print(f"  Smallest:           R {result['min']:,.2f}")
    print(f"  Transactions > R5k: {result['count_above_5000']}")