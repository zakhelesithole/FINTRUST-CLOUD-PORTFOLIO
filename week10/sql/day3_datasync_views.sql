-- =========================================================
-- Week 10 Day 3 - BI Dashboard Views
-- =========================================================

-- View 1: Daily Transfer Volume (for line chart)
CREATE OR REPLACE VIEW v_daily_transfer_volume AS
SELECT
    DATE(started_at)                          AS transfer_date,
    source_volume,
    COUNT(*)                                  AS execution_count,
    SUM(files_transferred)                    AS total_files,
    ROUND(SUM(bytes_transferred) / 1073741824.0, 2) AS total_gb,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS successful_runs,
    SUM(CASE WHEN status = 'ERROR'   THEN 1 ELSE 0 END) AS failed_runs
FROM datasync_executions
GROUP BY DATE(started_at), source_volume
ORDER BY transfer_date DESC;

-- View 2: Migration Progress by Volume (for bar chart)
CREATE OR REPLACE VIEW v_volume_migration_progress AS
SELECT
    v.volume_name,
    v.source_system,
    v.total_size_gb,
    COALESCE(SUM(e.bytes_transferred) / 1073741824.0, 0) AS transferred_gb,
    ROUND(
        100.0 * COALESCE(SUM(e.bytes_transferred) / 1073741824.0, 0)
        / NULLIF(v.total_size_gb, 0), 1
    ) AS pct_complete,
    MAX(e.completed_at) AS last_transfer
FROM transfer_volumes v
LEFT JOIN datasync_executions e ON v.volume_id = e.task_id
                               AND e.status = 'SUCCESS'
GROUP BY v.volume_id, v.volume_name, v.source_system, v.total_size_gb
ORDER BY pct_complete DESC;

-- Extension Task 1: Transfer Audit View
CREATE OR REPLACE VIEW v_transfer_audit AS
SELECT
    v.volume_name,
    c.regulation,
    c.encryption_required,
    e.status AS execution_status,
    e.bytes_transferred,
    e.completed_at
FROM datasync_executions e
JOIN transfer_volumes v ON e.task_id = v.volume_id
JOIN compliance_requirements c ON v.volume_id = c.volume_id;
