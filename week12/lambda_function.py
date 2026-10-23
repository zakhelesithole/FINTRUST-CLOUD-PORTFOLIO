import json
import boto3
import tempfile
from datetime import date
from fintrust_migration import (
    get_monthly_spend_by_service,
    write_csv_report,
    write_html_report,
)

S3_BUCKET = "fintrust-cost-reports"

def lambda_handler(event, context):
    today = date.today()
    prefix = f"cost-reports/{today.year}/{today.month:02d}"
    
    print("Fetching cost data...")
    data = get_monthly_spend_by_service(months_back=1)

    if not data:
        print("No data found.")
        return {'statusCode': 200, 'body': json.dumps('No data to report')}

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = write_csv_report(data, f"{tmpdir}/cost_report.csv")
        html_path = write_html_report(data, f"{tmpdir}/cost_report.html")

        s3 = boto3.client('s3')
        files_to_upload = [
            (csv_path, "cost_report.csv"), 
            (html_path, "cost_report.html")
        ]
        
        for path, key_suffix in files_to_upload:
            try:
                s3.upload_file(str(path), S3_BUCKET, f"{prefix}/{key_suffix}")
                print(f"Uploaded {key_suffix} to s3://{S3_BUCKET}/{prefix}/")
            except Exception as e:
                print(f"Failed to upload {key_suffix}: {e}")

    return {
        'statusCode': 200, 
        'body': json.dumps(f'Reports uploaded to {prefix}')
    }
