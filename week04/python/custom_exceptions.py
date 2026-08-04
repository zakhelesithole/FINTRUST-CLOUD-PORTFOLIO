# ============================================
# custom_exceptions.py
# FinTrust Bank - Custom Exception Examples
# Week 4 Day 1 - Cloud to Solutions Accelerator
# ============================================

print("=" * 70)
print("CUSTOM EXCEPTIONS - REFERENCE")
print("=" * 70)
print()

# ============================================
# 1. Basic Custom Exception
# ============================================
print("1. Basic Custom Exception")
print("-" * 40)


class BankingError(Exception):
    """Root class for all FinTrust errors."""
    pass


class InsufficientFundsError(BankingError):
    """Raised when balance is insufficient."""
    pass


# Example
try:
    raise InsufficientFundsError("Insufficient balance")
except InsufficientFundsError as e:
    print(f"  ✓ Caught: {e}")
print()

# ============================================
# 2. Exception with Custom Attributes
# ============================================
print("2. Exception with Custom Attributes")
print("-" * 40)


class InsufficientFundsErrorWithAttrs(BankingError):
    """Raised when balance is insufficient with full context."""

    def __init__(self, account_id, requested, available):
        self.account_id = account_id
        self.requested = requested
        self.available = available
        self.shortfall = requested - available
        message = (
            f"Account {account_id}: requested R{requested:.2f}, "
            f"available R{available:.2f} (shortfall: R{self.shortfall:.2f})"
        )
        super().__init__(message)


# Example
try:
    raise InsufficientFundsErrorWithAttrs("FT-123456", 5000.00, 3200.50)
except InsufficientFundsErrorWithAttrs as e:
    print(f"  ✓ Caught: {e}")
    print(f"    account_id: {e.account_id}")
    print(f"    requested: R{e.requested:.2f}")
    print(f"    available: R{e.available:.2f}")
    print(f"    shortfall: R{e.shortfall:.2f}")
print()

# ============================================
# 3. Exception Hierarchy
# ============================================
print("3. Exception Hierarchy")
print("-" * 40)


class TransactionError(BankingError):
    """Base for transaction errors."""
    def __init__(self, txn_id, message):
        self.txn_id = txn_id
        super().__init__(f"[TXN:{txn_id}] {message}")


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


# Example
try:
    raise DailyLimitExceededError("TXN999", "FT-999", 10000.00, 8500.00, 2000.00)
except DailyLimitExceededError as e:
    print(f"  ✓ Caught: {e}")
    print(f"    txn_id: {e.txn_id}")
    print(f"    account_id: {e.account_id}")
    print(f"    remaining: R{e.remaining:.2f}")
except TransactionError as e:
    print(f"  ✓ Caught as TransactionError: {e}")
except BankingError as e:
    print(f"  ✓ Caught as BankingError: {e}")
print()

# ============================================
# 4. Error Chaining (raise ... from)
# ============================================
print("4. Error Chaining (raise ... from)")
print("-" * 40)


class ValidationError(BankingError):
    """Raised when data validation fails."""
    pass


def validate_amount(value):
    """Convert to float, preserving error context."""
    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(f"Invalid amount: {value}") from e


# Example
try:
    amount = validate_amount("not_a_number")
except ValidationError as e:
    print(f"  ✓ Caught: {e}")
    print(f"    Cause: {e.__cause__}")
    print(f"    Type: {type(e.__cause__).__name__}")
print()

# ============================================
# 5. Re-raising Exceptions
# ============================================
print("5. Re-raising Exceptions")
print("-" * 40)


def process_payment(amount):
    try:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return amount * 1.05  # Add 5% fee
    except ValueError as e:
        print(f"  Logging error: {e}")
        raise  # Re-raise the original exception


# Example
try:
    result = process_payment(-100)
except ValueError as e:
    print(f"  ✓ Caught re-raised: {e}")
print()

print("=" * 70)
print("REFERENCE COMPLETED!")
print("=" * 70)