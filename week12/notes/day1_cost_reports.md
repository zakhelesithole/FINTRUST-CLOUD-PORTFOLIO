# Week 12 Day 1 - Automated Cost Reports

## Cost Explorer API
- **Region:** Always `us-east-1`.
- **Granularity:** `MONTHLY` or `DAILY`.
- **Filtering:** You can filter by `Tags` (e.g., `CostCentre`), but the tags must be activated in the Billing Console first.
- **Multi-Account:** Grouping by `LINKED_ACCOUNT` and `SERVICE` returns consolidated billing data across all member accounts in an AWS Organization.

## Python Data Generation
- **CSV:** Using the `csv.DictWriter` is the safest way to generate comma-separated files, as it automatically handles escaping quotes.
- **HTML:** Python f-strings make it easy to generate a simple HTML table for emailing or hosting on S3.

## Extension: Per-Account Spend
Used `boto3.client('organizations').list_accounts()` to map Account IDs to human-readable Account Names, then joined that mapping with the Cost Explorer output.

## Reflection
The Cost Explorer API is a **billing** API, so if the sandbox account has $0 spend, the list will be empty. The script structure is correct and will output data once the account has active resources. Tag activation takes 24 hours, which is a critical delay to account for before end-of-month reporting deadlines.
