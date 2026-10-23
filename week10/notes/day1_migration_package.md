# Week 10 Day 1 - Python Migration Scripts

## Python Package Structure
We created a package `fintrust_migration` to organize code:
- `utils/sessions.py`: Centralized boto3 client creation.
- `ec2/classifier.py`: 6Rs classification based on AWS tags.
- `__init__.py`: Exposes the public API.

## The 6Rs Migration Strategies
1. **Rehost**: Lift and shift (EC2 to EC2).
2. **Replatform**: Lift, tinker, and shift (e.g., move to RDS).
3. **Refactor**: Re-architect (e.g., monolith to microservices).
4. **Repurchase**: Drop and shop (move to SaaS).
5. **Retain**: Revisit (keep on-prem for now).
6. **Retire**: Decommission (no longer needed).

## SQL Views
Views encapsulate complex JOINs and provide a stable API for BI tools (like QuickSight). They run the underlying query on-demand.

### Reflection
**Question:** What would you call the function in the package that writes classifier results back to the database?
**Answer:** `sync_classification_to_db()` or `save_portfolio_to_rds()`. It would use `boto3` or a library like `psycopg2` (if connecting directly to RDS PostgreSQL) to execute `INSERT` or `UPDATE` statements, syncing the real-time AWS state with the migration tracking database.
