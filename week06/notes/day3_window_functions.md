
# Week 6 Day 3 - Python and boto3

## boto3 Concepts

### What is boto3?
Amazon's official Python SDK for AWS. Allows programmatic interaction with any AWS service.

### Two Ways to Use boto3

| Interface | Type | Description |
|-----------|------|-------------|
| Client | Low-level | Mirrors AWS API directly. Returns raw JSON. More control. |
| Resource | High-level | Object-oriented. More Pythonic. Not available for all services. |

### Authentication Order
1. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
2. ~/.aws/credentials file (aws configure)
3. IAM instance role (EC2)
4. IAM task role (ECS/Lambda)

**Best practice:** Use IAM roles, never hardcode credentials.

### Pagination
- AWS API calls return paginated results (max 1000 items)
- Use Paginators to automatically handle NextToken
- Without pagination, you will miss resources

## Scripts Created Today

### 1. list_buckets.py
- Lists all S3 buckets
- Shows creation date and region
- Uses get_bucket_location for region

### 2. s3_audit.py
- Lists all buckets with region, public access, encryption
- Calculates bucket size and object count
- Shows security recommendations

### 3. ec2_inventory.py
- Lists all EC2 instances
- Shows instance ID, name, state, type, IPs, VPC
- Uses paginator for large results

### 4. s3_full_audit.py
- Complete audit with all checks
- Shows public access block status
- Shows encryption status
- Generates recommendations

## Key boto3 Methods Used

| Service | Method | Purpose |
|---------|--------|---------|
| S3 | list_buckets() | Get all buckets |
| S3 | get_bucket_location() | Get bucket region |
| S3 | get_public_access_block() | Check public access |
| S3 | get_bucket_encryption() | Check encryption |
| S3 | list_objects_v2() | List objects in bucket |
| EC2 | describe_instances() | Get instance details |

## Exception Handling

```python
try:
    # operation
except s3.exceptions.NoSuchPublicAccessBlockConfiguration:
    # handle missing configuration
except Exception as e:
    # handle other errors
