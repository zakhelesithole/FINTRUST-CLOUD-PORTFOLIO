-- ============================================
-- Week 2 Day 2 - Advanced JOINs & Aggregates
-- FinTrust Bank Database
-- Date: 11 July 2026
-- ============================================

USE fintrust_db;

-- ============================================
-- QUICK REFERENCE
-- ============================================
-- Aggregate Functions: COUNT, SUM, AVG, MIN, MAX
-- WHERE: Filters individual rows (before GROUP BY)
-- HAVING: Filters groups (after GROUP BY)
-- GROUP BY: Groups rows for aggregation
-- ============================================

-- ============================================
-- Exercise 1: Count transactions per customer
-- ============================================
-- Shows each customer's name, province, total number of transactions,
-- and total transaction amount. Include only customers with at least 1 transaction.
-- Sort by total amount descending.

SELECT
    c.first_name,
    c.last_name,
    c.province,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_amount
FROM customers c
INNER JOIN accounts a 
    ON c.customer_id = a.customer_id
INNER JOIN transactions t 
    ON a.account_id = t.account_id
GROUP BY 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province
HAVING COUNT(t.transaction_id) >= 1
ORDER BY total_amount DESC;


-- ============================================
-- Exercise 2: Average balance by account type
-- ============================================
-- Show each account type (savings, cheque, etc.),
-- the number of accounts of that type, and the average balance.
-- Sort by average balance descending.

SELECT
    account_type,
    COUNT(account_id) AS account_count,
    AVG(balance) AS avg_balance,
    SUM(balance) AS total_balance
FROM accounts
GROUP BY account_type
ORDER BY avg_balance DESC;


-- ============================================
-- Exercise 3: HAVING filter
-- ============================================
-- Find all provinces where the total deposits (credit transactions) 
-- exceed R 100,000. Show: province, total deposit amount, 
-- and number of credit transactions. Use HAVING to filter.

SELECT
    c.province,
    COUNT(t.transaction_id) AS credit_transaction_count,
    SUM(t.amount) AS total_deposits
FROM customers c
INNER JOIN accounts a 
    ON c.customer_id = a.customer_id
INNER JOIN transactions t 
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'CREDIT'
GROUP BY c.province
HAVING SUM(t.amount) > 100000
ORDER BY total_deposits DESC;


-- ============================================
-- Exercise 4: Monthly summary
-- ============================================
-- Show the total transaction amount and count per month 
-- (for all transaction types). Use YEAR() and MONTH() functions.
-- Sort by year then month.

SELECT
    YEAR(transaction_date) AS year,
    MONTH(transaction_date) AS month,
    COUNT(transaction_id) AS transaction_count,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY 
    YEAR(transaction_date),
    MONTH(transaction_date)
ORDER BY year DESC, month DESC;


-- ============================================
-- Exercise 5: Challenge - Fraud signal
-- ============================================
-- Find customers who have made more than 3 debit transactions in a single day.
-- This is a fraud detection pattern. Show: customer name, transaction date, 
-- and count of debits that day.

SELECT
    c.first_name,
    c.last_name,
    DATE(t.transaction_date) AS transaction_date,
    COUNT(t.transaction_id) AS debit_count
FROM customers c
INNER JOIN accounts a 
    ON c.customer_id = a.customer_id
INNER JOIN transactions t 
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'DEBIT'
GROUP BY 
    c.customer_id,
    c.first_name,
    c.last_name,
    DATE(t.transaction_date)
HAVING COUNT(t.transaction_id) > 3
ORDER BY debit_count DESC, transaction_date;


-- ============================================
-- BONUS: Additional Analytics Queries
-- ============================================

-- Bonus 1: Top 5 customers by total transaction amount
SELECT
    c.first_name,
    c.last_name,
    c.province,
    COUNT(t.transaction_id) AS num_transactions,
    SUM(t.amount) AS total_transacted,
    AVG(t.amount) AS avg_transaction,
    MAX(t.amount) AS largest_single_transaction
FROM customers c
INNER JOIN accounts a 
    ON c.customer_id = a.customer_id
INNER JOIN transactions t 
    ON a.account_id = t.account_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province
ORDER BY total_transacted DESC
LIMIT 5;

-- Bonus 2: Monthly transaction volumes by account type
SELECT
    YEAR(t.transaction_date) AS year,
    MONTH(t.transaction_date) AS month,
    a.account_type,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount) AS monthly_volume
FROM accounts a
INNER JOIN transactions t 
    ON a.account_id = t.account_id
GROUP BY
    YEAR(t.transaction_date),
    MONTH(t.transaction_date),
    a.account_type
ORDER BY year DESC, month DESC, monthly_volume DESC;

-- Bonus 3: Customers with accounts but no transactions (anti-join)
SELECT
    c.first_name,
    c.last_name,
    c.province,
    COUNT(a.account_id) AS account_count
FROM customers c
INNER JOIN accounts a 
    ON c.customer_id = a.customer_id
LEFT JOIN transactions t 
    ON a.account_id = t.account_id
WHERE t.transaction_id IS NULL
GROUP BY 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province;