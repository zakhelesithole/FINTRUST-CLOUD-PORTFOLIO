-- =========================================================
-- Week 11 Day 1 - SQL Window Functions
-- =========================================================

-- Note: The schema is assumed to be:
-- transactions(customer_id, account_id, transaction_date, amount)

-- =========================================================
-- Exercise 1: Top 3 transactions by amount for each customer
-- =========================================================
WITH RankedTransactions AS (
    SELECT
        customer_id,
        transaction_date,
        amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY amount DESC
        ) AS rank_in_history
    FROM transactions
)
SELECT
    customer_id,
    transaction_date,
    amount,
    rank_in_history
FROM RankedTransactions
WHERE rank_in_history <= 3
ORDER BY customer_id, rank_in_history;


-- =========================================================
-- Exercise 2: Month-over-month change in total transaction value
-- =========================================================
WITH MonthlyTotals AS (
    SELECT
        account_id,
        DATE_TRUNC('month', transaction_date) AS txn_month,
        SUM(amount) AS monthly_total
    FROM transactions
    GROUP BY account_id, DATE_TRUNC('month', transaction_date)
),
WithPreviousMonth AS (
    SELECT
        account_id,
        txn_month,
        monthly_total,
        LAG(monthly_total) OVER (
            PARTITION BY account_id 
            ORDER BY txn_month
        ) AS prev_month_total
    FROM MonthlyTotals
)
SELECT
    account_id,
    txn_month,
    monthly_total,
    prev_month_total,
    ROUND(
        ((monthly_total - prev_month_total) / NULLIF(prev_month_total, 0)) * 100, 2
    ) AS pct_change,
    CASE 
        WHEN ((monthly_total - prev_month_total) / NULLIF(prev_month_total, 0)) > 0.50 THEN 'FLAG: >50% Increase'
        WHEN ((monthly_total - prev_month_total) / NULLIF(prev_month_total, 0)) < -0.50 THEN 'FLAG: >50% Decrease'
        ELSE 'Normal'
    END AS alert_flag
FROM WithPreviousMonth
WHERE prev_month_total IS NOT NULL
ORDER BY account_id, txn_month;


-- =========================================================
-- Exercise 3: Divide accounts into 4 quartiles based on volume
-- =========================================================
WITH AccountTotals AS (
    SELECT
        account_id,
        SUM(amount) AS total_volume
    FROM transactions
    -- Assuming current year filter: WHERE transaction_date >= DATE_TRUNC('year', CURRENT_DATE)
    GROUP BY account_id
),
Quartiles AS (
    SELECT
        account_id,
        total_volume,
        NTILE(4) OVER (ORDER BY total_volume DESC) AS quartile
    FROM AccountTotals
)
SELECT
    quartile,
    COUNT(*) AS account_count,
    MIN(total_volume) AS min_volume,
    MAX(total_volume) AS max_volume,
    ROUND(AVG(total_volume), 2) AS avg_volume
FROM Quartiles
GROUP BY quartile
ORDER BY quartile ASC;

-- Note: Top 10% of accounts by volume will always fall into Quartile 1 (highest volume).
