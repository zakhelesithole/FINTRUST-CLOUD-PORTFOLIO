import boto3
import pathlib

s3 = boto3.client('s3', region_name='af-south-1')
BUCKET = 'fintrust-processed'


def upload_parquet_partition(local_path, s3_key):
    """Upload a single Parquet file to S3."""
    s3.upload_file(local_path, BUCKET, s3_key)
    print(f'  Uploaded s3://{BUCKET}/{s3_key}')


def verify_upload():
    """List objects in the transactions prefix to confirm structure."""
    print()
    print("S3 Objects:")
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=BUCKET, Prefix='transactions/'):
        for obj in page.get('Contents', []):
            size_kb = obj['Size'] // 1024
            print(f'  {obj["Key"]} ({size_kb} KB)')


def main():
    print("=" * 60)
    print("FINTRIST BANK - UPLOAD PARQUET TO S3")
    print("=" * 60)
    print()

    # Upload all .parquet files maintaining the partition structure
    for f in pathlib.Path('.').glob('fintrust_processed/**/*.parquet'):
        # Strip the local prefix and use the partition path as the S3 key
        s3_key = 'transactions/' + str(f).replace('fintrust_processed/', '').replace('\\', '/')
        upload_parquet_partition(str(f), s3_key)

    # Verify
    verify_upload()

    print()
    print("Upload complete.")


if __name__ == "__main__":
    main()