# ============================================
# test_exceptions.py
# Test script for custom exception classes
# Week 4 Day 1 - Cloud to Solutions Accelerator
# ============================================

import logging
from datetime import datetime

# ── Logging setup ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("fintrust.test")

print("=" * 70)
print("CUSTOM EXCEPTION CLASSES - DEMO")
print("=" * 70)
print()

# ============================================
# 1. Define Exception Hierarchy
# ============================================
print("1. Exception Hierarchy")
print("-" * 40)


class BankingError(Exception):
    """Root class for all FinTrust errors."""
    pass


class TransactionError(BankingError):
    """Base class for transaction-related errors."""
    def __init__(self, txn_id, message):
        self.txn_id = txn_id
        super().__init__(f"[TXN:{txn_id}] {message}")


class InsufficientFundsError(TransactionError):
    """Raised when balance is insufficient."""
    def __init__(self, txn_id, account_id, requested, available):
        self.account_id = account_id
        self.requested = requested
        self.available = available
        self.shortfall = requested - available
        super().__init__(
            txn_id,
            f"Account {account_id}: R{requested:.2f} requested, "
            f"R{available:.2f} available (shortfall: R{self.shortfall:.2f})"
        )


class AccountFrozenError(TransactionError):
    """Raised when account is frozen."""
    def __init__(self, txn_id, account_id, reason):
        self.account_id = account_id
        self.reason = reason
        super().__init__(txn_id, f"Account {account_id} frozen: {reason}")


class InvalidAmountError(TransactionError):
    """Raised when amount is zero or negative."""
    def __init__(self, txn_id, account_id, amount):
        self.account_id = account_id
        self.amount = amount
        # Check if amount is a number before formatting
        try:
            amount_str = f"R{amount:.2f}"
        except (TypeError, ValueError):
            amount_str = f"'{amount}'"
        super().__init__(txn_id, f"Invalid amount {amount_str} (must be > 0)")


class DailyLimitExceededError(TransactionError):
    """Raised when daily limit is exceeded."""
    def __init__(self, txn_id, account_id, limit, already_used, requested):
        self.account_id = account_id
        self.limit = limit
        self.already_used = already_used
        self.requested = requested
        self.remaining = limit - already_used
        super().__init__(
            txn_id,
            f"Daily limit R{limit:.2f}: used R{already_used:.2f}, "
            f"remaining R{self.remaining:.2f}, requested R{requested:.2f}"
        )


print("  ✅ BankingError")
print("  ✅ TransactionError")
print("  ✅ InsufficientFundsError")
print("  ✅ AccountFrozenError")
print("  ✅ InvalidAmountError")
print("  ✅ DailyLimitExceededError")
print()

# ============================================
# 2. Test Each Exception
# ============================================
print("2. Testing Each Exception")
print("-" * 40)

test_cases = [
    ("TXN001", "FT-123", 100, "InsufficientFundsError"),
    ("TXN002", "FT-456", 0, "InvalidAmountError"),
]

# Test InvalidAmountError
try:
    raise InvalidAmountError("TXN001", "FT-123", -50.00)
except InvalidAmountError as e:
    print(f"  ✓ Caught: {e.__class__.__name__} — {e}")
    print(f"    account_id: {e.account_id}")
    print(f"    amount: R{e.amount:.2f}")

# Test InsufficientFundsError
try:
    raise InsufficientFundsError("TXN002", "FT-456", 5000.00, 3200.50)
except InsufficientFundsError as e:
    print(f"  ✓ Caught: {e.__class__.__name__} — {e}")
    print(f"    account_id: {e.account_id}")
    print(f"    requested: R{e.requested:.2f}")
    print(f"    available: R{e.available:.2f}")
    print(f"    shortfall: R{e.shortfall:.2f}")

# Test AccountFrozenError
try:
    raise AccountFrozenError("TXN003", "FT-789", "POPIA compliance hold")
except AccountFrozenError as e:
    print(f"  ✓ Caught: {e.__class__.__name__} — {e}")
    print(f"    account_id: {e.account_id}")
    print(f"    reason: {e.reason}")

# Test DailyLimitExceededError
try:
    raise DailyLimitExceededError("TXN004", "FT-999", 10000.00, 8500.00, 2000.00)
except DailyLimitExceededError as e:
    print(f"  ✓ Caught: {e.__class__.__name__} — {e}")
    print(f"    account_id: {e.account_id}")
    print(f"    limit: R{e.limit:.2f}")
    print(f"    already_used: R{e.already_used:.2f}")
    print(f"    remaining: R{e.remaining:.2f}")
print()

# ============================================
# 3. Exception Hierarchy Test (Catching)
# ============================================
print("3. Testing Exception Hierarchy (Catching)")
print("-" * 40)


def process_transaction(txn_id, account_id, amount):
    """Simple function that raises different exceptions."""
    if amount <= 0:
        raise InvalidAmountError(txn_id, account_id, amount)
    if account_id == "FT-FROZEN":
        raise AccountFrozenError(txn_id, account_id, "Test freeze")
    if amount > 5000:
        raise InsufficientFundsError(txn_id, account_id, amount, 3200.50)
    return {"status": "SUCCESS", "new_balance": 3200.50 - amount}


test_txns = [
    ("TXN-A", "FT-123", 100.00),      # Success
    ("TXN-B", "FT-123", -50.00),      # InvalidAmountError
    ("TXN-C", "FT-FROZEN", 100.00),   # AccountFrozenError
    ("TXN-D", "FT-123", 6000.00),     # InsufficientFundsError
]

for txn_id, account_id, amount in test_txns:
    try:
        result = process_transaction(txn_id, account_id, amount)
        print(f"  ✓ {txn_id}: SUCCESS — new balance R{result['new_balance']:.2f}")
    except InvalidAmountError as e:
        print(f"  ✗ {txn_id}: {e.__class__.__name__} — amount must be > 0")
    except AccountFrozenError as e:
        print(f"  ✗ {txn_id}: {e.__class__.__name__} — {e.reason}")
    except InsufficientFundsError as e:
        print(f"  ✗ {txn_id}: {e.__class__.__name__} — shortfall R{e.shortfall:.2f}")
    except TransactionError as e:
        print(f"  ✗ {txn_id}: TransactionError — {e}")
    except BankingError as e:
        print(f"  ✗ {txn_id}: BankingError — {e}")
print()

# ============================================
# 4. raise ... from e (Error Chaining)
# ============================================
print("4. Error Chaining (raise ... from e)")
print("-" * 40)


def parse_amount(value):
    """Convert string to float, preserving error context."""
    try:
        return float(value)
    except ValueError as e:
        raise InvalidAmountError("TXN-X", "FT-123", value) from e


try:
    amount = parse_amount("not_a_number")
except InvalidAmountError as e:
    print(f"  ✓ Caught: {e}")
    print(f"    Cause: {e.__cause__}")
print()

print("=" * 70)
print("DEMO COMPLETED SUCCESSFULLY!")
print("=" * 70)