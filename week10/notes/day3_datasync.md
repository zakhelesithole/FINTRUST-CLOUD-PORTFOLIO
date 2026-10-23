# Week 10 Day 3 - DataSync Automation & BI Views

## DataSync Automation
- Added `s3/sync_helpers.py` to the package.
- `start_task_execution()`: Starts the job and returns an `ExecutionArn` (unique per run).
- `set_task_throttle()`: Converts Mbps to bytes/sec and updates task limits.
- `wait_for_execution()`: Polls until `SUCCESS` or `ERROR`.

## Dynamic Throttling (FinTrust)
- **Daytime (07:00 - 22:00 SAST):** 500 Mbps. Limits bandwidth to protect production traffic.
- **Overnight (22:00 - 07:00 SAST):** 9000 Mbps. Maximizes throughput.
- Automating this prevents manual intervention using EventBridge Scheduler + Lambda.

## BI Dashboard Views
- **v_daily_transfer_volume**: Groups by date for line charts.
- **v_volume_migration_progress**: Calculates percentages. Uses `NULLIF()` to prevent division by zero if total size is 0.
- **v_transfer_audit**: Joins execution data with compliance requirements for auditability.

## Reflection: Automation vs Human Judgement
**Question:** What signals should be on a human-readable dashboard to help a migration engineer decide when to cutover?

**Answer:**
A cutover dashboard should display live, visual indicators of system health and sync status:
1. **Source Lag (seconds):** A line chart showing `CDCLatencySource` from DMS. It must be near zero and flat.
2. **Transfer Throughput:** A gauge showing current DataSync GB transferred vs. total GB remaining.
3. **Error Rate:** A red/yellow/green status indicator for recent validation errors (`ValidationErrored` counts).
4. **Time Remaining (ETA):** Calculated from the current transfer rate and remaining data size.

**Surface the SQL Audit alongside Python:**
The Python script can push metrics to CloudWatch (for alarms) or write to a DynamoDB table. QuickSight can read from that DynamoDB table or the SQL view simultaneously. The dashboard should combine Python's real-time API polling (for the "heartbeat") with the SQL view's historical audit data.
