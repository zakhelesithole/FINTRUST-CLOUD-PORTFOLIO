USE fintrust;

-- ============================================
-- Day 2 - Basic SELECT Exercises
-- FinTrust Bank Database
-- Date: 7 July 2026
-- ============================================

-- First, select the database
USE fintrust;

-- ============================================
-- Exercise 1: List customers by province
-- ============================================
SELECT first_name, last_name, province
FROM customers
ORDER BY province;

-- ============================================
-- Exercise 2: Savings accounts only (first 20)
-- ============================================
SELECT account_number, account_type, balance
FROM accounts
WHERE account_type = 'SAVINGS'
LIMIT 20;

-- ============================================
-- Exercise 3: Unique provinces
-- ============================================
SELECT DISTINCT province
FROM customers
ORDER BY province;

-- ============================================
-- Exercise 4: Projected balance (with 10% interest)
-- ============================================
SELECT 
    account_number,
    account_type,
    balance,
    balance * 1.10 AS projected_balance
FROM accounts;

-- ============================================
-- Exercise 5: Count total accounts (Stretch)
-- ============================================
SELECT COUNT(*) AS total_accounts
FROM accounts;