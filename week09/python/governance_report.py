import boto3
import json
from datetime import datetime
from collections import defaultdict
from tag_auditor import audit_tag_compliance

s3 = boto3.client('s3')
tagging = boto3.client('resourcegroupstaggingapi', region_name='af-south-1')
BUCKET = 'fintrust-governance'

def generate_governance_report():
    print("1. Running initial audit...")
    initial_violations = audit_tag_compliance()
    initial_count = len(initial_violations)
    
    total_scanned = initial_count
    try:
        paginator = tagging.get_paginator('get_resources')
        total_scanned = sum(len(page['ResourceTagMappingList']) for page in paginator.paginate())
    except Exception:
        pass

    print(f"   Scanned: {total_scanned} | Violations: {initial_count}")

    print("2. Auto-remediating (applying Environment=Production)...")
    remediated = 0
    for arn in initial_violations.keys():
        try:
            tagging.tag_resources(
                ResourceARNList=[arn],
                Tags={'Environment': 'Production'}
            )
            remediated += 1
        except Exception:
            pass

    print(f"   Successfully remediated: {remediated}")

    print("3. Re-checking violations...")
    remaining = audit_tag_compliance()
    remaining_count = len(remaining)

    by_service = defaultdict(int)
    for arn in remaining.keys():
        parts = arn.split(':')
        service = parts[2] if len(parts) > 2 else 'unknown'
        by_service[service] += 1

    report = {
        'report_date': datetime.utcnow().isoformat(),
        'total_scanned': total_scanned,
        'initial_violations': initial_count,
        'auto_remediated': remediated,
        'remaining_violations': remaining_count,
        'violations_by_service': dict(by_service)
    }

    today = datetime.utcnow().strftime('%Y-%m-%d')
    key = f"tag-audit/{today}.json"
    
    try:
        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=json.dumps(report, indent=2),
            ContentType='application/json'
        )
        print(f"4. Report uploaded to s3://{BUCKET}/{key}")
    except Exception as e:
        print(f"4. Could not upload to S3: {e}")
        print("   Local Report:")
        print(json.dumps(report, indent=2))

if __name__ == "__main__":
    print("=" * 60)
    print("FINTRIST BANK - GOVERNANCE REPORT")
    print("=" * 60)
    generate_governance_report()
