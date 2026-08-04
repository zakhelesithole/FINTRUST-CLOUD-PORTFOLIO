# ============================================
# FinTrust Bank — Transaction Processing Module
# Week 4, Day 1 PM Lab
# ============================================

from datetime import datetime
import logging

# ── Logging setup ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("fintrust.transactions")

# ──────────────────────────────────────────────
# 1. Exception Hierarchy
# ──────────────────────────────────────────────

class BankingError(Exception):
    """Root class for all FinTrust errors."""
    pass


class TransactionError(BankingError):
    """Base class for transaction-related errors."""
    def __init__(self, txn_id, message):
        self.txn_id = txn_id
        super().__init__(f"[TXN:{txn_id}] {message}")


class InsufficientFundsError(TransactionError):
    """Raised when balance is insufficient for a transaction."""
    def __init__(self, txn_id, account_id, requested, available):
        self.account_id = account_id
        self.requested = requested
        self.available = available
        self.shortfall = requested - available
        super().__init__(
            txn_id,
            f"Account {account_id}: requested R{requested:.2f}, "
            f"available R{available:.2f} (shortfall: R{self.shortfall:.2f})"
        )


class AccountFrozenError(TransactionError):
    """Raised when an account is frozen due to compliance hold."""
    def __init__(self, txn_id, account_id, reason):
        self.account_id = account_id
        self.reason = reason
        super().__init__(txn_id, f"Account {account_id} frozen: {reason}")


class InvalidAmountError(TransactionError):
    """Raised when transaction amount is zero or negative."""
    def __init__(self, txn_id, account_id, amount):
        self.account_id = account_id
        self.amount = amount
        super().__init__(
            txn_id,
            f"Invalid amount R{amount:.2f} on account {account_id} "
            f"(must be greater than 0)"
        )


class DailyLimitExceededError(TransactionError):
    """Raised when transaction exceeds daily limit."""
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


class AccountNotFoundError(TransactionError):
    """Raised when account ID does not exist."""
    def __init__(self, txn_id, account_id):
        self.account_id = account_id
        super().__init__(txn_id, f"Account {account_id} not found")


# ──────────────────────────────────────────────
# 2. Account Store
# ──────────────────────────────────────────────

ACCOUNTS = {
    "FT-001234": {
        "balance": 3200.50,
        "frozen": False,
        "daily_used": 0.0,
        "daily_limit": 10000.0,
        "freeze_reason": None
    },
    "FT-005678": {
        "balance": 50000.00,
        "frozen": True,
        "daily_used": 0.0,
        "daily_limit": 50000.0,
        "freeze_reason": "POPIA compliance hold"
    },
    "FT-009999": {
        "balance": 1500.00,
        "frozen": False,
        "daily_used": 8500.0,
        "daily_limit": 10000.0,
        "freeze_reason": None
    },
    "FT-008888": {
        "balance": 10000.00,
        "frozen": False,
        "daily_used": 0.0,
        "daily_limit": 10000.0,
        "freeze_reason": None
    },
}


# ──────────────────────────────────────────────
# 3. Audit Log
# ──────────────────────────────────────────────

AUDIT_LOG = []


def log_transaction_error(error: TransactionError):
    """Log a transaction error to the audit log."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "txn_id": error.txn_id,
        "error_type": error.__class__.__name__,
        "message": str(error)
    }
    AUDIT_LOG.append(entry)
    logger.error(f"[{error.txn_id}] {error.__class__.__name__}: {error}")


def log_success(txn_id, account_id, amount, new_balance):
    """Log a successful transaction."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "txn_id": txn_id,
        "account_id": account_id,
        "amount": amount,
        "new_balance": new_balance,
        "status": "SUCCESS"
    }
    AUDIT_LOG.append(entry)
    logger.info(f"[{txn_id}] SUCCESS: R{amount:.2f} from {account_id}, new balance R{new_balance:.2f}")


def print_audit_log():
    """Print the full audit log."""
    print("\n" + "=" * 70)
    print("AUDIT LOG")
    print("=" * 70)
    for entry in AUDIT_LOG:
        if entry.get("status") == "SUCCESS":
            print(f"✓ [{entry['txn_id']}] SUCCESS: R{entry['amount']:.2f} from {entry['account_id']} "
                  f"→ balance R{entry['new_balance']:.2f}")
        else:
            print(f"✗ [{entry['txn_id']}] {entry['error_type']}: {entry['message']}")
    print("=" * 70)
    print(f"Total entries: {len(AUDIT_LOG)}")


# ──────────────────────────────────────────────
# 4. Transaction Processor
# ──────────────────────────────────────────────

def process_withdrawal(txn_id: str, account_id: str, amount: float) -> dict:
    """
    Process a withdrawal with full error handling.

    Returns a result dict on success.
    Raises TransactionError subclasses on failure.
    """
    # Validate amount
    if amount <= 0:
        raise InvalidAmountError(txn_id, account_id, amount)

    # Check if account exists
    if account_id not in ACCOUNTS:
        raise AccountNotFoundError(txn_id, account_id)

    account = ACCOUNTS[account_id]

    # Check if account is frozen
    if account["frozen"]:
        raise AccountFrozenError(txn_id, account_id, account["freeze_reason"])

    # Check daily limit
    remaining = account["daily_limit"] - account["daily_used"]
    if amount > remaining:
        raise DailyLimitExceededError(
            txn_id,
            account_id,
            account["daily_limit"],
            account["daily_used"],
            amount
        )

    # Check balance
    if amount > account["balance"]:
        raise InsufficientFundsError(txn_id, account_id, amount, account["balance"])

    # Process transaction
    account["balance"] -= amount
    account["daily_used"] += amount

    result = {
        "txn_id": txn_id,
        "account_id": account_id,
        "amount": amount,
        "new_balance": account["balance"],
        "timestamp": datetime.now().isoformat(),
        "status": "SUCCESS"
    }

    log_success(txn_id, account_id, amount, account["balance"])
    return result


# ──────────────────────────────────────────────
# 5. Main — test all scenarios
# ──────────────────────────────────────────────

def main():
    print("=" * 70)
    print("FINTRIST BANK - TRANSACTION PROCESSING")
    print("=" * 70)
    print()

    test_cases = [
        ("TXN001", "FT-001234", 100.00),       # ✅ should succeed
        ("TXN002", "FT-001234", 5000.00),      # ❌ insufficient funds
        ("TXN003", "FT-005678", 500.00),       # ❌ account frozen
        ("TXN004", "FT-009999", 2000.00),      # ❌ daily limit exceeded
        ("TXN005", "FT-001234", -50.00),       # ❌ invalid amount
        ("TXN006", "FT-999999", 100.00),       # ❌ account not found
        ("TXN007", "FT-008888", 5000.00),      # ✅ should succeed (daily limit not reached)
    ]

    for txn_id, account_id, amount in test_cases:
        try:
            result = process_withdrawal(txn_id, account_id, amount)
            print(f"✓ {txn_id}: SUCCESS — new balance R{result['new_balance']:.2f}")
        except InsufficientFundsError as e:
            print(f"✗ {txn_id}: INSUFFICIENT FUNDS — shortfall: R{e.shortfall:.2f}")
            log_transaction_error(e)
        except AccountFrozenError as e:
            print(f"✗ {txn_id}: ACCOUNT FROZEN — {e.reason}")
            log_transaction_error(e)
        except DailyLimitExceededError as e:
            print(f"✗ {txn_id}: DAILY LIMIT — remaining R{e.remaining:.2f}")
            log_transaction_error(e)
        except InvalidAmountError as e:
            print(f"✗ {txn_id}: INVALID AMOUNT — R{e.amount:.2f}")
            log_transaction_error(e)
        except AccountNotFoundError as e:
            print(f"✗ {txn_id}: ACCOUNT NOT FOUND — {e.account_id}")
            log_transaction_error(e)
        except TransactionError as e:
            print(f"✗ {txn_id}: TRANSACTION ERROR — {e}")
            log_transaction_error(e)
        except BankingError as e:
            print(f"✗ {txn_id}: BANKING ERROR — {e}")
            log_transaction_error(e)

    # Print audit log
    print_audit_log()


if __name__ == "__main__":
    main()