import boto3
import json

s3 = boto3.client('s3', region_name='af-south-1')
BUCKET = 'fintrust-ingest-dev'

def main():
    print(f"Setting up bucket: {BUCKET}")
    
    # 1. Create bucket
    try:
        s3.create_bucket(
            Bucket=BUCKET,
            CreateBucketConfiguration={'LocationConstraint': 'af-south-1'}
        )
        print("Bucket created.")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print("Bucket already exists and is owned by you.")
    except Exception as e:
        print(f"Error creating bucket: {e}")
        return

    # 2. Enable versioning
    try:
        s3.put_bucket_versioning(
            Bucket=BUCKET,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        print("Versioning enabled.")
    except Exception as e:
        print(f"Error enabling versioning: {e}")

    # 3. Block ALL public access
    try:
        s3.put_public_access_block(
            Bucket=BUCKET,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True, 'IgnorePublicAcls': True,
                'BlockPublicPolicy': True, 'RestrictPublicBuckets': True
            }
        )
        print("Public access blocked.")
    except Exception as e:
        print(f"Error blocking public access: {e}")

    # 4. Lifecycle rule
    try:
        s3.put_bucket_lifecycle_configuration(
            Bucket=BUCKET,
            LifecycleConfiguration={'Rules': [{
                'ID': 'archive-and-expire', 'Status': 'Enabled',
                'Filter': {'Prefix': 'raw/'},
                'Transitions': [{'Days': 90, 'StorageClass': 'GLACIER'}],
                'Expiration': {'Days': 2555}    # 7 years
            }]}
        )
        print("Lifecycle configuration applied.")
    except Exception as e:
        print(f"Error applying lifecycle configuration: {e}")

if __name__ == "__main__":
    main()
