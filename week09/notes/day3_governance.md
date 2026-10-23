# Week 9 Day 3 - Cost Governance Automation

## Resource Groups Tagging API
- **Region-scoped**, but **service-agnostic**.
- One call gets resources from EC2, S3, RDS, Lambda, etc.
- Key operations: `get_resources()`, `tag_resources()`, `untag_resources()`.
- Always use paginators to ensure you don't miss resources.

## FinTrust Required Tags
| Tag Key | Allowed Values |
|---------|----------------|
| CostCentre | CoreBanking, Analytics, Security, DevOps, Migration |
| Team | Platform, DataEngineering, AppSec, SRE, DataMigration |
| Environment | Production, Staging, Dev, Sandbox |

## AWS Service Catalog
- End users provision products from a catalog (backed by CloudFormation).
- Enforces tagging **at creation time** by requiring ProvisioningParameters.
- `list_portfolios()`, `list_accepted_portfolio_shares()`, `search_products_as_admin()`.

## Detect vs Enforce Reflection
The Tagging API detects violations *after* creation. Service Catalog prevents them *at* creation. 

**The Gap:** A resource created outside the Service Catalog (e.g., via direct EC2 Console access) that *does* have all the required tags, but with *incorrect values* (e.g., Environment="Prod" instead of "Production").

**The Fix:** AWS Config. You can create a Config Rule (`required-tags` or a custom Lambda rule) to continuously monitor and remediate tag values, not just the presence of tags.

## Scripts Created
| File | Purpose |
|------|---------|
| tag_auditor.py | Audit resources for missing tags |
| service_catalog.py | List Service Catalog portfolios/products |
| governance_report.py | Combine audit, auto-remediation, and S3 upload |
