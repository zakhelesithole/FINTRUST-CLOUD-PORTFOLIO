USE fintrust_db;

-- ============================================
-- Add More Data to FinTrust Database
-- ============================================

-- Add more customers
INSERT INTO customers (first_name, last_name, email, province) VALUES
    ('Lerato',   'Sithole',   'lerato.s@fintrust.co.za',    'Western Cape'),
    ('Nomsa',    'Zulu',      'nomsa.zulu@gmail.com',       'Eastern Cape'),
    ('Pieter',   'van Wyk',   'pieter.vw@gmail.com',        'Western Cape'),
    ('Fatima',   'Moosa',     'fatima.moosa@outlook.com',   'KwaZulu-Natal'),
    ('Lungelo',  'Ndlovu',    'lungelo.n@gmail.com',        'Mpumalanga'),
    ('Cleo',     'Petersen',  'cleo.petersen@gmail.com',    'Western Cape'),
    ('David',    'Smith',     'david.smith@yahoo.com',      'Gauteng'),
    ('Sarah',    'Johnson',   'sarah.j@gmail.com',          'Gauteng'),
    ('Michael',  'Brown',     'michael.b@fintrust.co.za',   'KwaZulu-Natal'),
    ('Lisa',     'Williams',  'lisa.w@gmail.com',           'Western Cape');

-- Add more accounts
INSERT INTO accounts (customer_id, account_type, account_number, balance) VALUES
    (6, 'CHEQUE',   'FT-CHQ-000006',  4500.00),
    (6, 'SAVINGS',  'FT-SAV-000003',  15000.50),
    (7, 'CHEQUE',   'FT-CHQ-000007',  8750.00),
    (7, 'CREDIT',   'FT-CRD-000001',  -1200.00),
    (8, 'SAVINGS',  'FT-SAV-000004',  25000.00),
    (9, 'CHEQUE',   'FT-CHQ-000008',  3200.75),
    (9, 'BUSINESS', 'FT-BUS-000002',  45000.00),
    (10, 'CHEQUE',  'FT-CHQ-000009',  12800.00),
    (10, 'SAVINGS', 'FT-SAV-000005',  500.00),
    (1, 'CREDIT',   'FT-CRD-000002',  -350.00);

-- Add more transactions
INSERT INTO transactions (account_id, transaction_type, amount, merchant_category) VALUES
    (1, 'DEBIT',   450.00,  'Groceries'),
    (1, 'DEBIT',   1200.00, 'Electronics'),
    (2, 'CREDIT',  5000.00, 'Salary'),
    (3, 'DEBIT',   320.50,  'Fuel'),
    (3, 'DEBIT',   800.00,  'Online Shopping'),
    (4, 'PAYMENT', 2500.00, 'Insurance'),
    (5, 'DEBIT',   150.00,  'Streaming'),
    (6, 'CREDIT',  85000.00, 'Business Income'),
    (7, 'DEBIT',   600.00,  'Healthcare'),
    (8, 'DEBIT',   89.99,   'Groceries'),
    (8, 'DEBIT',   2500.00, 'Retail'),
    (9, 'CREDIT',  12000.00, 'Salary'),
    (10, 'DEBIT',  450.00,  'Groceries'),
    (10, 'DEBIT',  3200.00, 'Electronics'),
    (11, 'DEBIT',  180.00,  'Fuel');
    
    SELECT COUNT(*) AS customers FROM customers;
SELECT COUNT(*) AS accounts FROM accounts;
SELECT COUNT(*) AS transactions FROM transactions;

-- ============================================
-- Day 4 - WHERE Clause Exercises
-- FinTrust Bank Database
-- Date: 9 July 2026
-- ============================================

USE fintrust_db;

-- ============================================
-- PRACTICE EXERCISES (1-6)
-- ============================================

-- Exercise 1: Basic Equality
-- Find all customers from Gauteng.
SELECT * FROM customers
WHERE province = 'Gauteng';

-- Exercise 2: Numeric Comparison
-- Find all accounts with a balance greater than R5,000.
SELECT account_id, account_number, account_type, balance
FROM accounts
WHERE balance > 5000;

-- Exercise 3: LIKE Pattern
-- Find all customers whose email address ends in '.co.za'.
SELECT first_name, last_name, email
FROM customers
WHERE email LIKE '%.co.za';

-- Exercise 4: IN Operator
-- Find all transactions of type DEBIT or PAYMENT using IN.
SELECT transaction_id, account_id, transaction_type, amount
FROM transactions
WHERE transaction_type IN ('DEBIT', 'PAYMENT');

-- Exercise 5: AND Combination
-- Find all SAVINGS accounts with a balance between R1,000 and R50,000.
SELECT account_id, account_number, balance
FROM accounts
WHERE account_type = 'SAVINGS' 
  AND balance BETWEEN 1000 AND 50000;

-- Exercise 6: IS NOT NULL
-- Find all transactions that DO have a merchant_category recorded.
SELECT transaction_id, account_id, amount, merchant_category
FROM transactions
WHERE merchant_category IS NOT NULL;

-- ============================================
-- BUSINESS INTELLIGENCE QUERIES (1-5)
-- ============================================

-- Query 1: Gauteng Customers
-- Marketing team needs a list of all customers in Gauteng.
SELECT customer_id, first_name, last_name, email
FROM customers
WHERE province = 'Gauteng'
ORDER BY last_name;

-- Query 2: High-Balance Accounts
-- Risk management needs to identify all accounts with balance above R10,000.
SELECT account_id, account_number, account_type, balance
FROM accounts
WHERE balance > 10000
ORDER BY balance DESC;

-- Query 3: SAVINGS Accounts
-- Savings product team needs to see all SAVINGS accounts.
SELECT account_id, customer_id, account_number, balance
FROM accounts
WHERE account_type = 'SAVINGS'
ORDER BY balance DESC;

-- Query 4: Large Grocery Transactions
-- Fraud team wants to review all transactions over R500 in Groceries.
SELECT transaction_id, account_id, amount, transaction_type, transaction_date
FROM transactions
WHERE merchant_category = 'Groceries'
  AND amount > 500
ORDER BY amount DESC;

-- Query 5: Gmail Customers
-- Digital team is running a campaign targeting Gmail customers.
SELECT first_name, last_name, email
FROM customers
WHERE email LIKE '%gmail%'
ORDER BY last_name;

-- ============================================
-- BONUS: My Own Query
-- ============================================

-- Find all transactions over R1000 that are CREDIT or DEBIT
SELECT transaction_id, account_id, transaction_type, amount, merchant_category
FROM transactions
WHERE amount > 1000
  AND (transaction_type = 'CREDIT' OR transaction_type = 'DEBIT')
ORDER BY amount DESC;