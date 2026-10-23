# Week 12 Day 1 - Automated Cost Reports

## Cost Explorer API
- Always `us-east-1`.
- Grouping by `LINKED_ACCOUNT` returns account IDs, not names.
- Account names must be fetched via Organizations API and joined.
- Tags must be activated in Billing Console first.

## Report Generation
- `csv.DictWriter` handles formatting and escaping automatically.
- HTML generation uses Python f-strings.
- `pathlib.Path` handles cross-platform file paths and creates directories automatically.
