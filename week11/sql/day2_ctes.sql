-- =========================================================
-- Week 11 Day 2 - SQL Common Table Expressions (CTEs)
-- =========================================================

-- =========================================================
-- Exercise 1: Month-over-month growth rate using chained CTEs
-- =========================================================
WITH MonthlyTotals AS (
    -- Step 1: Calculate monthly totals per account
    SELECT
        account_id,
        DATE_TRUNC('month', transaction_date) AS txn_month,
        SUM(amount) AS total_amount
    FROM transactions
    GROUP BY account_id, DATE_TRUNC('month', transaction_date)
),
WithPreviousMonth AS (
    -- Step 2: Use LAG to get the previous month's total
    SELECT
        account_id,
        txn_month,
        total_amount,
        LAG(total_amount) OVER (
            PARTITION BY account_id 
            ORDER BY txn_month
        ) AS prev_month_total
    FROM MonthlyTotals
)
-- Step 3: Calculate percentage change and flag > 100% growth
SELECT
    account_id,
    txn_month,
    total_amount,
    prev_month_total,
    ROUND(
        ((total_amount - prev_month_total) / NULLIF(prev_month_total, 0)) * 100, 2
    ) AS pct_growth
FROM WithPreviousMonth
WHERE prev_month_total IS NOT NULL
  AND ((total_amount - prev_month_total) / NULLIF(prev_month_total, 0)) > 1.0
ORDER BY account_id, txn_month;


-- =========================================================
-- Exercise 2: Select the top 10% of accounts by transaction value
-- =========================================================
WITH AccountTotals AS (
    -- Step 1: Aggregate total transaction value per account
    SELECT
        account_id,
        SUM(amount) AS total_volume
    FROM transactions
    GROUP BY account_id
),
RankedAccounts AS (
    -- Step 2: Use DENSE_RANK to rank accounts
    SELECT
        account_id,
        total_volume,
        DENSE_RANK() OVER (ORDER BY total_volume DESC) AS rnk,
        -- Alternatively, PERCENT_RANK() is cleaner for percentiles
        PERCENT_RANK() OVER (ORDER BY total_volume DESC) AS pct_rank
    FROM AccountTotals
)
-- Step 3: Filter for top 10% (pct_rank <= 0.10 means top 10%)
SELECT
    account_id,
    total_volume,
    rnk
FROM RankedAccounts
WHERE pct_rank <= 0.10
ORDER BY total_volume DESC;


-- =========================================================
-- Example: Recursive CTE (Account Hierarchy)
-- =========================================================
WITH RECURSIVE account_hierarchy AS (
    -- Anchor member: start with root accounts (no parent)
    SELECT
        account_id,
        parent_account_id,
        account_name,
        0 AS depth
    FROM accounts
    WHERE parent_account_id IS NULL

    UNION ALL

    -- Recursive member: find children of already-found accounts
    SELECT
        a.account_id,
        a.parent_account_id,
        a.account_name,
        h.depth + 1
    FROM accounts a
    JOIN account_hierarchy h ON a.parent_account_id = h.account_id
    WHERE h.depth < 10 -- Guard against infinite loops
)
SELECT account_id, account_name, depth
FROM account_hierarchy
ORDER BY depth, account_name;
