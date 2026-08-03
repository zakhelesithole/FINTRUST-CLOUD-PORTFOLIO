# ============================================
# test_standard_lib.py
# Test script for Python Standard Library
# Week 3 Day 2 - Cloud to Solutions Accelerator
# ============================================

import sys
import os
from pathlib import Path
from datetime import date, datetime
import math

print("=" * 50)
print("PYTHON STANDARD LIBRARY - DEMO")
print("=" * 50)
print()

# ============================================
# 1. pathlib - Modern File Path Handling
# ============================================
print("1. pathlib - File Path Handling")
print("-" * 30)

# Current directory
cwd = Path.cwd()
print(f"Current Directory: {cwd}")

# Home directory
home = Path.home()
print(f"Home Directory: {home}")

# Build paths
data_dir = Path("data") / "fintrust" / "transactions" / "2026"
print(f"Data Directory: {data_dir}")

# Create directories
data_dir.mkdir(parents=True, exist_ok=True)
print(f"Created: {data_dir}")

# Check existence
print(f"Exists? {data_dir.exists()}")
print(f"Is directory? {data_dir.is_dir()}")
print()

# Create a test file
test_file = Path("test.txt")
test_file.write_text("FinTrust Bank - Test File")
print(f"Created test file: {test_file}")

# Read the file
content = test_file.read_text()
print(f"Content: {content}")

# File info
print(f"File name: {test_file.name}")
print(f"File stem: {test_file.stem}")
print(f"File suffix: {test_file.suffix}")

# Clean up
test_file.unlink()
print(f"Removed test file")
print()

# ============================================
# 2. os - Operating System Interface
# ============================================
print("2. os - Operating System Interface")
print("-" * 30)

# Current working directory
print(f"os.getcwd(): {os.getcwd()}")

# List directory contents
print("Files in current directory:")
for item in os.listdir(".")[:10]:  # Show first 10
    print(f"  {item}")

# Environment variables
print(f"\nFINTRUST_DATA_DIR: {os.environ.get('FINTRUST_DATA_DIR', 'Not set')}")
print(f"AWS_DEFAULT_REGION: {os.environ.get('AWS_DEFAULT_REGION', 'Not set')}")

# Set an environment variable
os.environ["TEST_VAR"] = "FinTrust Test"
print(f"TEST_VAR: {os.environ.get('TEST_VAR')}")
print()

# ============================================
# 3. sys - Python Interpreter Interface
# ============================================
print("3. sys - Python Interpreter Interface")
print("-" * 30)

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Platform: {sys.platform}")
print(f"Script arguments: {sys.argv}")
print()

# ============================================
# 4. datetime - Date and Time
# ============================================
print("4. datetime - Date and Time")
print("-" * 30)

today = date.today()
print(f"Today: {today}")
print(f"Today formatted: {today.strftime('%d %B %Y')}")
print(f"Year: {today.year}")
print(f"Month: {today.month}")
print(f"Day: {today.day}")

now = datetime.now()
print(f"\nCurrent time: {now}")
print(f"Time formatted: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print()

# ============================================
# 5. math - Mathematical Functions
# ============================================
print("5. math - Mathematical Functions")
print("-" * 30)

print(f"math.pi: {math.pi}")
print(f"math.e: {math.e}")
print(f"math.sqrt(16): {math.sqrt(16)}")
print(f"math.pow(2, 10): {math.pow(2, 10)}")
print(f"math.floor(3.7): {math.floor(3.7)}")
print(f"math.ceil(3.2): {math.ceil(3.2)}")
print()

print("=" * 50)
print("DEMO COMPLETED SUCCESSFULLY!")
print("=" * 50)