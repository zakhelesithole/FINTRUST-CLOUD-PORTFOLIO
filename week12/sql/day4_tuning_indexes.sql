-- =========================================================
-- Week 12 Day 4 - SQL Performance Tuning & Indexes
-- =========================================================

-- 1. Original slow query (before index)
-- EXPLAIN ANALYZE
-- SELECT
--     t.transaction_id,
--     t.amount,
--     c.customer_name,
--     a.account_type
-- FROM transactions t
-- JOIN customers c ON t.customer_id = c.customer_id
-- JOIN accounts a ON t.account_id = a.account_id
-- WHERE t.transaction_date >= '2024-01-01'
--   AND t.status = 'PENDING'
-- ORDER BY t.amount DESC
-- LIMIT 100;

-- 2. Create a targeted partial index to eliminate the Seq Scan
-- CONCURRENTLY allows index creation without locking the table.
-- The WHERE clause makes it a partial index, meaning it only indexes
-- the rows we actually query, reducing index size and write overhead.
CREATE INDEX CONCURRENTLY idx_transactions_status_date
    ON transactions (status, transaction_date DESC)
    WHERE status IN ('PENDING', 'PROCESSING');

-- 3. Verify the index is being used
-- EXPLAIN ANALYZE
-- SELECT * FROM transactions
-- WHERE status = 'PENDING' AND transaction_date >= '2024-01-01';


-- =========================================================
-- Compliance Controls Reference (AWS CLI)
-- =========================================================
-- 
-- 1. Enable audit logging via a custom parameter group:
-- aws rds modify-db-parameter-group \
--   --db-parameter-group-name fintrust-pg-audit \
--   --parameters "ParameterName=shared_preload_libraries,ParameterValue=pgaudit,ApplyMethod=pending-reboot"
--
-- 2. Verify storage encryption and customer-managed KMS key:
-- aws rds describe-db-instances \
--   --db-instance-identifier fintrust-transactions-db \
--   --query 'DBInstances[0].[StorageEncrypted,KmsKeyId]'
