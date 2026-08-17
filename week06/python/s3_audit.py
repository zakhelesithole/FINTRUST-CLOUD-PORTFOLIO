import boto3
from datetime import datetime

# Create S3 client
s3 = boto3.client('s3')

def get_bucket_region(bucket_name):
    """Get the region where the bucket is located."""
    try:
        loc = s3.get_bucket_location(Bucket=bucket_name)
        return loc['LocationConstraint'] or 'us-east-1'
    except Exception as e:
        return f"Error: {str(e)}"

def is_public_access_blocked(bucket_name):
    """Check if all public access block settings are enabled."""
    try:
        r = s3.get_public_access_block(Bucket=bucket_name)
        config = r['PublicAccessBlockConfiguration']
        return all([
            config.get('BlockPublicAcls', False),
            config.get('IgnorePublicAcls', False),
            config.get('BlockPublicPolicy', False),
            config.get('RestrictPublicBuckets', False),
        ])
    except s3.exceptions.NoSuchPublicAccessBlockConfiguration:
        return False
    except Exception as e:
        print(f"  Error checking public access for {bucket_name}: {e}")
        return False

def is_encryption_enabled(bucket_name):
    """Check if default encryption is enabled on the bucket."""
    try:
        r = s3.get_bucket_encryption(Bucket=bucket_name)
        return True
    except s3.exceptions.ServerSideEncryptionConfigurationNotFoundError:
        return False
    except Exception as e:
        print(f"  Error checking encryption for {bucket_name}: {e}")
        return False

def get_bucket_size(bucket_name):
    """Get total size of objects in the bucket."""
    try:
        paginator = s3.get_paginator('list_objects_v2')
        total_size = 0
        object_count = 0
        for page in paginator.paginate(Bucket=bucket_name):
            for obj in page.get('Contents', []):
                total_size += obj['Size']
                object_count += 1
        return total_size, object_count
    except Exception as e:
        return 0, 0

def main():
    print("=" * 80)
    print("FINTRIST BANK - S3 AUDIT REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()

    # Get all buckets
    response = s3.list_buckets()
    buckets = response['Buckets']

    print(f"Found {len(buckets)} buckets")
    print()

    # Header
    print(f"{'BUCKET NAME':<45} {'REGION':<15} {'PUBLIC':<8} {'ENCRYPTED':<12} {'SIZE (MB)':<12} {'OBJECTS':<10}")
    print("-" * 102)

    # Track statistics
    total_buckets = 0
    exposed_buckets = 0
    unencrypted_buckets = 0

    # Process each bucket
    for bucket in buckets:
        bucket_name = bucket['Name']
        total_buckets += 1

        # Get region
        region = get_bucket_region(bucket_name)

        # Check public access
        blocked = is_public_access_blocked(bucket_name)
        public_status = "SAFE" if blocked else "EXPOSED"
        if not blocked:
            exposed_buckets += 1

        # Check encryption
        encrypted = is_encryption_enabled(bucket_name)
        encryption_status = "ENCRYPTED" if encrypted else "UNENCRYPTED"
        if not encrypted:
            unencrypted_buckets += 1

        # Get size
        size_bytes, object_count = get_bucket_size(bucket_name)
        size_mb = size_bytes / 1024 / 1024

        # Print row
        print(f"{bucket_name:<45} {region:<15} {public_status:<8} {encryption_status:<12} {size_mb:>10.1f} {object_count:>10}")

    print("-" * 102)
    print()
    print("SUMMARY:")
    print(f"  Total buckets: {total_buckets}")
    print(f"  Exposed buckets (no public access block): {exposed_buckets}")
    print(f"  Unencrypted buckets: {unencrypted_buckets}")
    print()

    # Security recommendation
    if exposed_buckets > 0 or unencrypted_buckets > 0:
        print("SECURITY RECOMMENDATIONS:")
        if exposed_buckets > 0:
            print(f"  - Enable Public Access Block on {exposed_buckets} bucket(s)")
        if unencrypted_buckets > 0:
            print(f"  - Enable default encryption on {unencrypted_buckets} bucket(s)")

    print()
    print("=" * 80)
    print("AUDIT COMPLETE")

if __name__ == "__main__":
    main()