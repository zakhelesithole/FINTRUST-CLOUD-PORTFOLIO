import boto3
from datetime import date
from fintrust_migration import (
    get_monthly_spend_by_service,
    write_csv_report,
    write_html_report,
    get_per_account_spend
)

def main():
    print("=" * 60)
    print("FINTRIST BANK - COST REPORT GENERATOR")
    print("=" * 60)

    today = date.today()
    folder = f"reports/{today.year}/{today.month:02d}"

    print("\n1. Fetching monthly spend by service...")
    data = get_monthly_spend_by_service(months_back=1)
    
    if data:
        csv_path = f"{folder}/cost_report.csv"
        html_path = f"{folder}/cost_report.html"
        
        write_csv_report(data, csv_path)
        write_html_report(data, html_path)
        print(f"Created {csv_path} and {html_path}")
        
        print("\n2. Uploading to S3...")
        s3 = boto3.client('s3')
        bucket = 'fintrust-audit-bucket'
        s3_key = f"cost-reports/{today.year}/{today.month:02d}/cost_report.csv"
        
        try:
            s3.upload_file(csv_path, bucket, s3_key)
            print(f"Uploaded to s3://{bucket}/{s3_key}")
        except Exception as e:
            print(f"S3 Upload failed (expected if bucket doesn't exist): {e}")
    else:
        print("No cost data found or missing permissions.")

    print("\n3. Fetching per-account spend...")
    acct_data = get_per_account_spend(months_back=1)
    if acct_data:
        acct_csv = f"{folder}/per_account_cost_report.csv"
        import csv
        with open(acct_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['period', 'account_id', 'account_name', 'service', 'cost_usd'])
            writer.writeheader()
            writer.writerows(acct_data)
        print(f"Created {acct_csv}")

if __name__ == "__main__":
    main()
