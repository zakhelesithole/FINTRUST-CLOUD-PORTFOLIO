# ============================================
# parse_aws_billing.py
# Demo: Read an AWS Cost Explorer CSV export
# and summarise costs by service.
# Week 3 Day 3 - Cloud to Solutions Accelerator
# ============================================

import csv
from collections import defaultdict
from pathlib import Path

BILLING_CSV = Path("data/aws_billing_export.csv")


def create_sample_billing_data():
    """Create sample AWS billing CSV for testing."""
    sample_data = """Service,Cost,Region,Usage
Amazon S3,45.23,af-south-1,Storage
Amazon EC2,234.50,af-south-1,Compute
AWS Lambda,12.75,af-south-1,Serverless
Amazon RDS,156.80,af-south-1,Database
Amazon S3,23.45,us-east-1,Storage
Amazon EC2,89.90,us-east-1,Compute
AWS CloudTrail,8.50,af-south-1,Management
Amazon VPC,34.20,af-south-1,Networking"""

    BILLING_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(BILLING_CSV, "w", newline="", encoding="utf-8") as f:
        f.write(sample_data)
    print(f"Created sample billing file: {BILLING_CSV}")


def summarise_by_service(filepath):
    """Return dict of {service_name: total_cost} from AWS billing CSV."""
    service_costs = defaultdict(float)

    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service = row.get("Service", "Unknown")
            try:
                cost = float(row.get("Cost", 0))
                service_costs[service] += cost
            except ValueError:
                pass  # Skip rows with non-numeric cost

    # Sort by cost descending
    return dict(sorted(service_costs.items(), key=lambda x: x[1], reverse=True))


def print_cost_report(service_costs, currency="USD"):
    """Print a formatted cost breakdown."""
    total = sum(service_costs.values())
    print(f"\nAWS Cost Breakdown — Total: {currency} {total:,.2f}")
    print("-" * 55)
    for service, cost in service_costs.items():
        pct = (cost / total * 100) if total > 0 else 0
        bar = "█" * int(pct / 2)
        print(f"  {service:<35} {currency} {cost:>8.2f}  {pct:4.1f}% {bar}")


def main():
    if not BILLING_CSV.exists():
        print(f"File not found: {BILLING_CSV}")
        create_sample_billing_data()
        print("\nRun the script again to process the data.")
        return

    costs = summarise_by_service(BILLING_CSV)
    print_cost_report(costs)


if __name__ == "__main__":
    main()