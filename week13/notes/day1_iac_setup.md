# Week 13 Day 1 - Infrastructure-as-Code

## S3 Bucket Setup
- **Versioning**: Enabled to protect against accidental deletion/overwrite.
- **Public Access Block**: All four settings `True` (BlockPublicAcls, IgnorePublicAcls, BlockPublicPolicy, RestrictPublicBuckets) for security.
- **Lifecycle Rules**: Move objects in `raw/` to Glacier after 90 days. Expire after 2,555 days (7 years) for compliance.

## IAM Role Creation
- **Trust Policy**: Allows `lambda.amazonaws.com` to assume the role.
- **Least Privilege**: Only allows `s3:GetObject` on `raw/*`, `ssm:GetParameter` on `/fintrust/dev/*`, and CloudWatch Logs.

## S3 Event Triggers
- Must grant Lambda invoke permission with `SourceArn` restricted to the specific bucket.
- Filter rules ensure the Lambda only fires on `.csv` files uploaded to the `raw/` folder.

## SSM Parameter Store
- Use `SecureString` for passwords (encrypted with KMS).
- Standard `String` for non-sensitive config like DB host and name.
