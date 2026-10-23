# Week 12 Portfolio Audit Checklist

Use this checklist to verify your GitHub repository before Portfolio Check-In #12 on Friday.

| Deliverable | Expected Location | Status |
|-------------|-------------------|--------|
| fintrust_migration package | `fintrust_migration/__init__.py` with all module imports | [ ] |
| Migration classifier module | `fintrust_migration/ec2/classifier.py` with `classify_instances()` | [ ] |
| DMS task module | `fintrust_migration/rds/dms_helpers.py` with start/stop/status functions | [ ] |
| Data sync module | `fintrust_migration/s3/sync_helpers.py` | [ ] |
| Cost reporting module | `fintrust_migration/cost_reporting.py` | [ ] |
| SQL views file | `week11/sql/` (window functions & CTEs) and `week10/sql/` | [ ] |
| requirements.txt | Repo root; includes `boto3`, `pandas`, `pyarrow`, `fastapi`, `flask` | [ ] |
| Lab notes | `/notes/` directories across all weeks | [ ] |

## Security Check
- [ ] No hardcoded AWS Access Keys in any file.
- [ ] No hardcoded database passwords.
- [ ] `venv/` and `__pycache__/` are included in `.gitignore`.

**If credentials are found:** Immediately rotate the key in AWS IAM and use `git filter-repo` or BFG Repo Cleaner to purge it from history.
