-- ============================================
-- Week 2 Day 1 - SQL JOIN Exercises
-- FinTrust Bank Database
-- Date: 10 July 2026
-- ============================================

USE fintrust_db;

-- ============================================
-- QUICK REFERENCE
-- ============================================
-- INNER JOIN: Only rows with matches in BOTH tables
-- LEFT JOIN: ALL rows from left + matches from right (NULL if no match)
-- LEFT JOIN + IS NULL: Rows from left with NO match in right
-- ============================================

-- ============================================
-- Exercise 1: Basic INNER JOIN
-- ============================================
-- Write a query that returns: customer first name, last name, 
-- account type, and current balance for all customers.
-- Sort by balance descending.

SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    a.balance
FROM customers c
INNER JOIN accounts a 
    ON c.customer_id = a.customer_id
ORDER BY a.balance DESC;


-- ============================================
-- Exercise 2: Filtered JOIN
-- ============================================
-- Find all customers from Gauteng with a balance greater than R 25,000.
-- Show: name, province, account type, balance.

SELECT
    c.first_name,
    c.last_name,
    c.province,
    a.account_type,
    a.balance
FROM customers c
INNER JOIN accounts a 
    ON c.customer_id = a.customer_id
WHERE c.province = 'Gauteng'
  AND a.balance > 25000
ORDER BY a.balance DESC;


-- ============================================
-- Exercise 3: 3-Table JOIN
-- ============================================
-- Write a query joining all three tables.
-- Show: customer name, account type, transaction amount, and transaction date.
-- Filter to only debit transactions.
-- Sort by transaction date descending.

SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    t.amount,
    t.transaction_date,
    t.transaction_type
FROM customers c
INNER JOIN accounts a 
    ON c.customer_id = a.customer_id
INNER JOIN transactions t 
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'DEBIT'
ORDER BY t.transaction_date DESC;


-- ============================================
-- Exercise 4: LEFT JOIN Anti-Pattern
-- ============================================
-- Find any customers who have never made a transaction.
-- Use a LEFT JOIN from customers → accounts → transactions
-- with an IS NULL filter.

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province,
    t.transaction_id
FROM customers c
LEFT JOIN accounts a 
    ON c.customer_id = a.customer_id
LEFT JOIN transactions t 
    ON a.account_id = t.account_id
WHERE t.transaction_id IS NULL;


-- ============================================
-- Exercise 5: Challenge Query
-- ============================================
-- Find all transactions greater than R 10,000 for customers 
-- in Western Cape or KwaZulu-Natal.
-- Show customer name, province, and transaction amount.
-- Sort by amount descending.

SELECT
    c.first_name,
    c.last_name,
    c.province,
    t.amount,
    t.transaction_date
FROM customers c
INNER JOIN accounts a 
    ON c.customer_id = a.customer_id
INNER JOIN transactions t 
    ON a.account_id = t.account_id
WHERE c.province IN ('Western Cape', 'KwaZulu-Natal')
  AND t.amount > 10000
ORDER BY t.amount DESC;


-- ============================================
-- BONUS: Additional Practice
-- ============================================

-- Bonus 1: Find all customers with their total account balances
SELECT
    c.first_name,
    c.last_name,
    COUNT(a.account_id) AS account_count,
    SUM(a.balance) AS total_balance
FROM customers c
LEFT JOIN accounts a 
    ON c.customer_id = a.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_balance DESC;

-- Bonus 2: Find the top 5 customers by transaction amount
SELECT
    c.first_name,
    c.last_name,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount) AS total_spent
FROM customers c
INNER JOIN accounts a 
    ON c.customer_id = a.customer_id
INNER JOIN transactions t 
    ON a.account_id = t.account_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC
LIMIT 5;