# ============================================
# test_error_handling.py
# Test script for error handling and logging
# Week 3 Day 4 - Cloud to Solutions Accelerator
# ============================================

import logging
from pathlib import Path

# ── Logging setup ──────────────────────────────────────────────────
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_DIR / "test_log.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("fintrust.test")

print("=" * 50)
print("ERROR HANDLING & LOGGING - DEMO")
print("=" * 50)
print()

# ============================================
# 1. try/except/else/finally
# ============================================
print("1. try/except/else/finally")
print("-" * 30)


def divide_numbers(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        logger.error("Cannot divide by zero!")
        return None
    except TypeError as e:
        logger.error(f"Type error: {e}")
        return None
    else:
        logger.info(f"Division successful: {a} / {b} = {result}")
        return result
    finally:
        logger.debug("Division operation completed")


print(f"divide_numbers(10, 2) = {divide_numbers(10, 2)}")
print(f"divide_numbers(10, 0) = {divide_numbers(10, 0)}")
print()

# ============================================
# 2. Handling Multiple Exceptions
# ============================================
print("2. Handling Multiple Exceptions")
print("-" * 30)


def parse_number(value):
    try:
        result = int(value)
        logger.info(f"Parsed '{value}' to {result}")
        return result
    except ValueError:
        logger.warning(f"Could not parse '{value}' as integer")
        return None
    except TypeError:
        logger.error(f"Invalid type: {type(value)}")
        return None


print(f"parse_number('42') = {parse_number('42')}")
print(f"parse_number('abc') = {parse_number('abc')}")
print(f"parse_number(None) = {parse_number(None)}")
print()

# ============================================
# 3. File Operations with Error Handling
# ============================================
print("3. File Operations with Error Handling")
print("-" * 30)


def safe_read_file(filepath):
    path = Path(filepath)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        logger.info(f"Successfully read {filepath}")
        return content
    except FileNotFoundError:
        logger.warning(f"File not found: {filepath}")
        return None
    except PermissionError:
        logger.error(f"Permission denied: {filepath}")
        return None
    except UnicodeDecodeError as e:
        logger.error(f"Encoding error in {filepath}: {e}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error reading {filepath}: {e}")
        return None


print("Reading existing file...")
result = safe_read_file("data/sample_transactions.csv")
print(f"Content length: {len(result) if result else 0}")

print("\nReading missing file...")
result = safe_read_file("data/missing_file.csv")
print(f"Result: {result}")
print()

# ============================================
# 4. Custom Exception Classes
# ============================================
print("4. Custom Exception Classes")
print("-" * 30)


class FinTrustValidationError(ValueError):
    """Raised when FinTrust business validation rules are violated."""
    pass


def validate_account_id(account_id):
    """Raises FinTrustValidationError if account_id is invalid."""
    try:
        if not isinstance(account_id, int):
            raise FinTrustValidationError(f"Account ID must be an integer, got {type(account_id)}")
        if account_id <= 0:
            raise FinTrustValidationError(f"Account ID must be positive, got {account_id}")
        if account_id < 100 or account_id > 999:
            raise FinTrustValidationError(f"Account ID must be between 100 and 999, got {account_id}")
        logger.info(f"Account ID {account_id} is valid")
        return True
    except FinTrustValidationError as e:
        logger.warning(f"Validation failed: {e}")
        return False


print(f"validate_account_id(101) = {validate_account_id(101)}")
print(f"validate_account_id(-5) = {validate_account_id(-5)}")
print(f"validate_account_id('abc') = {validate_account_id('abc')}")
print(f"validate_account_id(1000) = {validate_account_id(1000)}")
print()

# ============================================
# 5. Logging Levels Demo
# ============================================
print("5. Logging Levels Demo")
print("-" * 30)

logger.debug("This is a DEBUG message - only shown if level=DEBUG")
logger.info("This is an INFO message")
logger.warning("This is a WARNING message")
logger.error("This is an ERROR message")
logger.critical("This is a CRITICAL message")
print()

print("=" * 50)
print("DEMO COMPLETED! Check logs/test_log.log for output")
print("=" * 50)