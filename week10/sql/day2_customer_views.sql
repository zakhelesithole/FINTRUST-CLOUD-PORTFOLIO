-- =========================================================
-- Week 10 Day 2 - Customer and Transaction Views
-- =========================================================

-- Task 1: Customer Account Summary View
CREATE OR REPLACE VIEW v_customer_accounts AS
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name       AS full_name,
    c.segment,
    c.region,
    COUNT(a.account_id)                        AS account_count,
    SUM(a.balance)                             AS total_balance,
    SUM(CASE WHEN a.currency = 'ZAR' THEN a.balance ELSE 0 END) AS zar_balance,
    MIN(c.onboarded_date)                      AS onboarded_date
FROM   customers  c
LEFT JOIN accounts a ON c.customer_id = a.customer_id
                    AND a.status = 'active'
GROUP BY c.customer_id, c.first_name, c.last_name, c.segment, c.region;

-- Task 2: Monthly Transaction Summary View
CREATE OR REPLACE VIEW v_monthly_txn_summary AS
SELECT
    DATE_TRUNC('month', t.txn_date)    AS txn_month,
    c.segment,
    t.channel,
    t.txn_type,
    COUNT(*)                            AS txn_count,
    SUM(t.amount)                       AS total_amount,
    AVG(t.amount)                       AS avg_amount,
    MAX(t.amount)                       AS max_amount
FROM   transactions t
JOIN   accounts    a ON t.account_id = a.account_id
JOIN   customers   c ON a.customer_id = c.customer_id
GROUP BY
    DATE_TRUNC('month', t.txn_date),
    c.segment, t.channel, t.txn_type
ORDER BY txn_month DESC, total_amount DESC;

-- Extension 2: Migration Audit View
CREATE OR REPLACE VIEW v_migration_audit AS
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS full_name,
    a.account_id,
    m.source_system,
    m.validation_state,
    m.migrated_at
FROM   migration_status m
JOIN   accounts a ON m.asset_id = a.account_id
JOIN   customers c ON a.customer_id = c.customer_id;

-- =========================================================
-- Verification Queries
-- =========================================================

-- Top 5 customers by total balance
SELECT full_name, segment, account_count, total_balance
FROM v_customer_accounts
ORDER BY total_balance DESC
LIMIT 5;

-- Digital channel volume last 3 months
SELECT txn_month, txn_count, total_amount
FROM v_monthly_txn_summary
WHERE channel = 'digital'
ORDER BY txn_month DESC
LIMIT 3;
