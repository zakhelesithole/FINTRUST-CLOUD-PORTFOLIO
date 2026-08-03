# ============================================
# test_utils.py
# Test suite for fintrust_utils.py
# Week 3 Day 1 - Cloud to Solutions Accelerator
# ============================================

from fintrust_utils import (
    format_rand,
    mask_id_number,
    validate_id_number,
    validate_account_type,
    calculate_simple_interest,
    calculate_monthly_fee,
    categorise_transaction,
    summarise_transactions,
    generate_report_header
)

# ============================================
# RUN TESTS
# ============================================

print("=" * 50)
print("FINTRIST UTILITIES - TEST SUITE")
print("=" * 50)
print()

# Test 1: Formatting
print("TEST 1: Formatting")
print("-" * 30)
print(f"format_rand(45230.75)          → {format_rand(45230.75)}")
print(f"mask_id_number('8501015009084')→ {mask_id_number('8501015009084')}")
print()

# Test 2: Validation
print("TEST 2: Validation")
print("-" * 30)
print(f"validate_id_number('8501015009084') → {validate_id_number('8501015009084')}")
print(f"validate_id_number('123')           → {validate_id_number('123')}")
print(f"validate_account_type('savings')    → {validate_account_type('savings')}")
print(f"validate_account_type('invalid')    → {validate_account_type('invalid')}")
print()

# Test 3: Calculations
print("TEST 3: Calculations")
print("-" * 30)
print(f"calculate_simple_interest(10000, 0.065, 12) → R {calculate_simple_interest(10000, 0.065, 12):,.2f}")
print(f"calculate_monthly_fee('savings')            → R {calculate_monthly_fee('savings'):,.2f}")
print(f"calculate_monthly_fee('credit')             → R {calculate_monthly_fee('credit'):,.2f}")
print(f"categorise_transaction(250)                 → {categorise_transaction(250)}")
print(f"categorise_transaction(2500)                → {categorise_transaction(2500)}")
print(f"categorise_transaction(25000)               → {categorise_transaction(25000)}")
print()

# Test 4: Transaction Summary
print("TEST 4: Transaction Summary")
print("-" * 30)
amounts = [5000, -250, 1200, -800, 3500, -1500]
deposits, withdrawals, net = summarise_transactions(amounts)
print(f"Transactions: {amounts}")
print(f"Total Deposits:  {format_rand(deposits)}")
print(f"Total Withdrawals: {format_rand(abs(withdrawals))}")
print(f"Net: {format_rand(net)}")
print()

# Test 5: Report Header
print("TEST 5: Report Header")
print("-" * 30)
print(generate_report_header("Thabo Nkosi", "ACC-10042"))
print()

print("=" * 50)
print("ALL TESTS COMPLETED!")
print("=" * 50)