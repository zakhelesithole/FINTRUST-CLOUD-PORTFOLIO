# ============================================
# exception_types.py
# Common exception types and how to handle them
# Week 3 Day 4 - Cloud to Solutions Accelerator
# ============================================

import csv
import json
from pathlib import Path

print("=" * 50)
print("COMMON EXCEPTION TYPES - REFERENCE")
print("=" * 50)
print()


# ============================================
# 1. FileNotFoundError
# ============================================
print("1. FileNotFoundError")
print("-" * 30)


def safe_load_csv(filepath):
    """Load CSV safely, return empty list on error."""
    path = Path(filepath)
    if not path.exists():
        print(f"  Warning: {filepath} not found — returning empty list")
        return []
    try:
        with open(path, "r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except (csv.Error, UnicodeDecodeError) as e:
        print(f"  Error reading {filepath}: {e}")
        return []


print("  Trying to load missing file...")
result = safe_load_csv("data/missing.csv")
print(f"  Result: {len(result)} rows")
print()


# ============================================
# 2. KeyError - Use .get() or check
# ============================================
print("2. KeyError")
print("-" * 30)

customer = {"id": 1001, "name": "Thabo"}

# Safe way 1: Use .get()
email = customer.get("email", "No email provided")
print(f"  .get() result: {email}")

# Safe way 2: Check first
if "email" in customer:
    print(f"  Email: {customer['email']}")
else:
    print("  No email key in customer dict")

# Unsafe way (causes KeyError)
try:
    print(f"  Attempting unsafe access: {customer['email']}")
except KeyError:
    print("  KeyError caught!")
print()


# ============================================
# 3. ValueError - Invalid conversion
# ============================================
print("3. ValueError")
print("-" * 30)


def safe_float(value):
    """Convert to float safely, return None on error."""
    try:
        return float(value)
    except ValueError:
        print(f"  Cannot convert '{value}' to float")
        return None


print(f"  safe_float('42.5') = {safe_float('42.5')}")
print(f"  safe_float('abc') = {safe_float('abc')}")
print()


# ============================================
# 4. TypeError - Wrong type
# ============================================
print("4. TypeError")
print("-" * 30)


def add_numbers(a, b):
    """Add two numbers safely."""
    try:
        return a + b
    except TypeError as e:
        print(f"  TypeError: {e}")
        return None


print(f"  add_numbers(5, 3) = {add_numbers(5, 3)}")
print(f"  add_numbers('5', 3) = {add_numbers('5', 3)}")
print()


# ============================================
# 5. JSONDecodeError - Invalid JSON
# ============================================
print("5. JSONDecodeError")
print("-" * 30)


def safe_load_json(filepath):
    """Load JSON safely, return None on error."""
    path = Path(filepath)
    if not path.exists():
        print(f"  File not found: {filepath}")
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"  Invalid JSON in {filepath}: {e}")
        return None
    except Exception as e:
        print(f"  Unexpected error: {e}")
        return None


# Create a valid and invalid JSON file
Path("data/valid.json").write_text('{"name": "Thabo", "balance": 52750}')
Path("data/invalid.json").write_text('{"name": "Thabo", "balance": 52750')  # Missing }

print("  Loading valid JSON...")
result = safe_load_json("data/valid.json")
print(f"    Result: {result}")

print("  Loading invalid JSON...")
result = safe_load_json("data/invalid.json")
print(f"    Result: {result}")
print()


# ============================================
# 6. IndexError - Out of bounds
# ============================================
print("6. IndexError")
print("-" * 30)


def safe_list_get(lst, index, default=None):
    """Safe list access with default value."""
    try:
        return lst[index]
    except IndexError:
        print(f"  Index {index} out of range (length: {len(lst)})")
        return default


transactions = [1001, 1002, 1003]
print(f"  safe_list_get(transactions, 1) = {safe_list_get(transactions, 1)}")
print(f"  safe_list_get(transactions, 5) = {safe_list_get(transactions, 5)}")
print()

print("=" * 50)
print("REFERENCE COMPLETED!")
print("=" * 50)