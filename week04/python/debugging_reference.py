# ============================================
# Debugging Reference - Stack Traces & pdb Commands
# Week 4 Day 2 - Cloud to Solutions Accelerator
# ============================================

print("=" * 70)
print("DEBUGGING REFERENCE")
print("=" * 70)
print()

# ============================================
# 1. Common Exception Types
# ============================================
print("1. Common Exception Types")
print("-" * 40)

examples = [
    ("NameError", "variable used before assignment or typo"),
    ("TypeError", "wrong type passed to function"),
    ("KeyError", "dictionary key does not exist"),
    ("IndexError", "list index out of range"),
    ("AttributeError", "object doesn't have the attribute"),
    ("ValueError", "right type, wrong value"),
    ("FileNotFoundError", "file does not exist"),
]

for exception_name, description in examples:
    print(f"  {exception_name}: {description}")
print()

# ============================================
# 2. pdb Commands
# ============================================
print("2. pdb Commands")
print("-" * 40)

commands = [
    ("l", "list", "Show current source code context"),
    ("n", "next", "Execute current line, step OVER function calls"),
    ("s", "step", "Execute current line, step INTO function calls"),
    ("c", "continue", "Resume execution until next breakpoint"),
    ("p expr", "print", "Evaluate and print an expression"),
    ("w", "where", "Show full call stack"),
    ("u/d", "up/down", "Move up/down the call stack"),
    ("q", "quit", "Exit pdb and the program"),
]

for short_name, long_name, description in commands:
    print(f"  {short_name:<5} {long_name:<8} - {description}")
print()

# ============================================
# 3. Reading Stack Traces
# ============================================
print("3. Reading Stack Traces")
print("-" * 40)

print("""
  Read bottom-up:
    1. Last line = exception type + message
    2. Line above = WHERE it happened
    3. Work upward to find YOUR code

  Example:
  Traceback (most recent call last):
    File "transactions.py", line 48, in <module>
      result = process_withdrawal(...)
    File "transactions.py", line 31, in process_withdrawal
      if amount > account["balanse"]:
  KeyError: 'balanse'

  Problem: 'balanse' is a typo, should be 'balance'
""")

# ============================================
# 4. breakpoint() Demo
# ============================================
print("4. breakpoint() Demo")
print("-" * 40)

def demo_breakpoint(value):
    """Function with breakpoint for debugging."""
    print(f"  Value: {value}")
    # breakpoint()  # Uncomment to test
    result = value * 2
    print(f"  Result: {result}")
    return result

print("  To use breakpoint():")
print("  1. Insert breakpoint() in your code")
print("  2. Run the script")
print("  3. Use pdb commands to inspect state")
print("  4. Type 'c' to continue or 'q' to quit")
print()

print("=" * 70)
print("REFERENCE COMPLETED")
print("=" * 70)