import boto3
from datetime import datetime

def get_bucket_region(s3_client, bucket_name):
    """Get the region where the bucket is located."""
    try:
        loc = s3_client.get_bucket_location(Bucket=bucket_name)
        return loc['LocationConstraint'] or 'us-east-1'
    except Exception:
        return 'Unknown'

def check_public_access_block(s3_client, bucket_name):
    """Check if public access block is fully enabled."""
    try:
        r = s3_client.get_public_access_block(Bucket=bucket_name)
        config = r['PublicAccessBlockConfiguration']
        return all([
            config.get('BlockPublicAcls', False),
            config.get('IgnorePublicAcls', False),
            config.get('BlockPublicPolicy', False),
            config.get('RestrictPublicBuckets', False),
        ])
    except s3_client.exceptions.NoSuchPublicAccessBlockConfiguration:
        return False
    except Exception:
        return False

def check_encryption_enabled(s3_client, bucket_name):
    """Check if default encryption is enabled."""
    try:
        s3_client.get_bucket_encryption(Bucket=bucket_name)
        return True
    except s3_client.exceptions.ServerSideEncryptionConfigurationNotFoundError:
        return False
    except Exception:
        return False

def main():
    s3_client = boto3.client('s3')

    print("=" * 90)
    print("FINTRIST BANK - FULL S3 AUDIT REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)
    print()

    # Get all buckets
    response = s3_client.list_buckets()
    buckets = response['Buckets']

    print(f"Found {len(buckets)} buckets")
    print()

    # Header
    print(f"{'BUCKET NAME':<40} {'REGION':<12} {'PUBLIC':<8} {'ENCRYPTED':<12}")
    print("-" * 72)

    exposed_count = 0
    unencrypted_count = 0

    for bucket in buckets:
        name = bucket['Name']

        region = get_bucket_region(s3_client, name)
        public_blocked = check_public_access_block(s3_client, name)
        encrypted = check_encryption_enabled(s3_client, name)

        public_status = "SAFE" if public_blocked else "EXPOSED"
        encryption_status = "YES" if encrypted else "NO"

        if not public_blocked:
            exposed_count += 1
        if not encrypted:
            unencrypted_count += 1

        print(f"{name:<40} {region:<12} {public_status:<8} {encryption_status:<12}")

    print("-" * 72)
    print()

    print("SUMMARY:")
    print(f"  Total buckets: {len(buckets)}")
    print(f"  Exposed buckets (no public block): {exposed_count}")
    print(f"  Unencrypted buckets: {unencrypted_count}")

    if exposed_count > 0 or unencrypted_count > 0:
        print()
        print("RECOMMENDATIONS:")
        if exposed_count > 0:
            print(f"  - Enable Public Access Block on {exposed_count} bucket(s)")
        if unencrypted_count > 0:
            print(f"  - Enable default encryption on {unencrypted_count} bucket(s)")

    print()
    print("=" * 90)
    print("AUDIT COMPLETE")

if __name__ == "__main__":
    main()
    