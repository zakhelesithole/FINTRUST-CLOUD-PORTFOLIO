import boto3
from datetime import datetime

def list_all_buckets():
    """List all S3 buckets with their creation date and region."""
    s3 = boto3.client('s3')

    print("=" * 80)
    print("FINTRIST BANK - S3 BUCKETS LIST")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()

    response = s3.list_buckets()

    print(f"{'BUCKET NAME':<45} {'CREATED':<15} {'REGION':<15}")
    print("-" * 75)

    for bucket in response['Buckets']:
        name = bucket['Name']
        created = bucket['CreationDate'].strftime('%Y-%m-%d')

        # Get bucket location
        loc = s3.get_bucket_location(Bucket=name)
        region = loc['LocationConstraint'] or 'us-east-1'

        print(f"{name:<45} {created:<15} {region:<15}")

    print("-" * 75)
    print(f"Total buckets: {len(response['Buckets'])}")
    print("=" * 80)

if __name__ == "__main__":
    list_all_buckets()