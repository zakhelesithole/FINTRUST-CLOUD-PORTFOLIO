
# Week 8 Day 1 - Querying AWS Athena and Glue with Python

## Athena Overview

Athena is a serverless query service that analyzes data in S3 using standard SQL. It uses the Glue Data Catalog for schema information.

### The Async Execution Model

Athena does not return results synchronously. The workflow is:

| Step | API Call | Purpose |
|------|----------|---------|
| 1 | `start_query_execution` | Submit SQL, get QueryExecutionId |
| 2 | `get_query_execution` | Poll for status (QUEUED/RUNNING/SUCCEEDED/FAILED) |
| 3 | `get_query_results` | Retrieve rows after SUCCEEDED |
| 4 | `stop_query_execution` | Cancel a running query |

### Why Async?

- Queries may scan terabytes of data
- Prevents HTTP timeouts
- Allows other work while waiting
- Poll with 1-2 second sleep to avoid throttling

## Result Structure

Athena returns results as a list of Row objects:
- `rows[0]` is always the header row
- `rows[1:]` are data rows
- Each row has a `Data` list
- Each element has a `VarCharValue` key
- All values are returned as strings

```python
for row in rows[1:]:
    values = [c.get('VarCharValue', '') for c in row['Data']]
    print(values)
