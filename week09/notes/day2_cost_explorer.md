# Week 9 Day 2 - Automating Cost Reporting

## Cost Explorer API
- Global endpoint: `us-east-1`
- `get_cost_and_usage()` returns billing data across all regions.
- `UnblendedCost` is the actual cost paid (including SP/RI discounts).
- `BlendedCost` spreads SP/RI discounts across linked accounts.
- **Cost:** $0.01 per API request.

## AWS Budgets API
- Requires `AccountId` in every call. Get it via `sts.get_caller_identity()`.
- Can set `ACTUAL` or `FORECASTED` alerts.
- Budget Actions can automatically apply SCPs or IAM policies if a budget is breached (requires an IAM role).

## S3 Uploads
- `put_object()` is best for small strings.
- `upload_file()` is best for existing large files on disk.

## Python vs QuickSight for Cost Reporting
- **Python:** Best for scheduled automated distribution, joining with non-AWS data, and custom formatting.
- **QuickSight:** Best for ad-hoc interactive drill-downs, visual charts, and sharing dashboards across teams.
