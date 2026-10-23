# Week 10 Day 2 - Python DMS Automation & SQL Views

## DMS Automation
- Added `rds/dms_helpers.py` to the package.
- `start_task(arn, 'start-replication')`: Drops target data and starts fresh (DANGEROUS in CDC phase).
- `start_task(arn, 'resume-processing')`: Resumes from last checkpoint (SAFE).
- `get_cdc_latency()`: Queries CloudWatch for `CDCLatencySource` and `CDCLatencyTarget`.

## CDC Cutover Readiness
- FinTrust threshold: `CDCLatencySource` must be < 30 seconds to initiate cutover.
- The `cutover_safe` boolean encapsulates this logic.

## SQL Views
- **v_customer_accounts**: Uses `LEFT JOIN` to ensure customers without accounts are still listed.
- **v_monthly_txn_summary**: Uses `DATE_TRUNC` to group transactions by month, joined across 3 tables.
- **v_migration_audit**: Joins `migration_status` to `accounts` and `customers` to show business-level migration state.

## Reflection: Automation and Audit
**Question:** How to decide between Python script vs SQL view vs QuickSight dashboard?

**Answer:**
1. **Python Script (Operational):** Best for tasks requiring action or direct interaction with infrastructure (e.g., triggering DMS start/stop, polling live AWS APIs, sending alerts).
2. **SQL View (Encapsulation):** Best for abstracting complex joins and business logic for other systems. It acts as a stable API for developers and BI tools to query without knowing the raw table structure.
3. **QuickSight Dashboard (Presentation):** Best for business stakeholders (analysts, management). It provides visual trends, drill-downs, and self-service analytics without needing to write code or SQL.

**Decision Rule:**
- Need to *do* something? -> Python.
- Need to *standardize data logic*? -> SQL View.
- Need to *visualize and share insights*? -> QuickSight.
