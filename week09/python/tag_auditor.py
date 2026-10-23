import boto3
from collections import defaultdict

tagging = boto3.client('resourcegroupstaggingapi', region_name='af-south-1')
REQUIRED_TAGS = ['CostCentre', 'Team', 'Environment']

def audit_tag_compliance():
    """Scan all tagged resources and identify those missing required tags."""
    non_compliant = {}
    try:
        paginator = tagging.get_paginator('get_resources')
        for page in paginator.paginate():
            for resource in page['ResourceTagMappingList']:
                arn = resource['ResourceARN']
                existing_keys = {t['Key'] for t in resource.get('Tags', [])}
                missing = [tag for tag in REQUIRED_TAGS if tag not in existing_keys]
                if missing:
                    non_compliant[arn] = missing
    except Exception as e:
        print(f"Error accessing Tagging API: {e}")
        
    return non_compliant

if __name__ == "__main__":
    print("=" * 60)
    print("FINTRIST BANK - TAG COMPLIANCE AUDIT")
    print("=" * 60)
    
    violations = audit_tag_compliance()
    print(f"Non-compliant resources found: {len(violations)}\n")

    by_type = defaultdict(list)
    for arn, missing in violations.items():
        parts = arn.split(':')
        service = parts[2] if len(parts) > 2 else 'unknown'
        by_type[service].append((arn, missing))

    for service, items in sorted(by_type.items()):
        print(f"  {service.upper()} ({len(items)} violations):")
        for arn, missing in items[:3]:
            short_arn = '...' + arn[-40:]
            print(f"    {short_arn} missing: {', '.join(missing)}")
