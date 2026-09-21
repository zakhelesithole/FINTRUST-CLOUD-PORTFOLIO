# Week 6 Day 4 - Python Security Automation

## IAM MFA Audit

### Purpose
- Verify all IAM console users have MFA enabled
- POPIA compliance requirement
- Identifies service accounts vs human users

### Key Methods
- iam.list_users() - Get all users
- iam.get_login_profile() - Check if user has console access
- iam.list_mfa_devices() - Check if MFA is configured

### Output
- Users without MFA are flagged as violations
- Each violation includes username, creation date, last activity

## Security Group Open Port Audit

### Purpose
- Detect security groups allowing internet access on restricted ports
- Restricted ports: SSH(22), RDP(3389), Database(5432,3306,1521)

### Key Methods
- ec2.describe_security_groups() - Get all security groups
- Check IpRanges for 0.0.0.0/0
- Check FromPort and ToPort

### Severity Levels
- CRITICAL: All traffic (0-65535)
- HIGH: Restricted ports exposed

## Stale Access Key Audit

### Purpose
- Identify access keys older than 90 days
- Security best practice: rotate keys regularly

### Key Methods
- iam.list_access_keys() - Get all access keys for a user
- Compare CreateDate with current date
- Calculate days old

## Automation Options

### Option 1: AWS Lambda + EventBridge (Recommended)
- Lambda runs the audit script
- EventBridge triggers every Monday at 7am
- Most resilient, serverless, no infrastructure

### Option 2: EC2 + Cron
- EC2 instance with scheduled cron job
- Less resilient (EC2 can fail)
- Requires instance management

### Why Lambda is More Resilient
- Serverless, automatically managed
- Built-in retry and monitoring
- No single point of failure
- Scales automatically

## Scripts Created

| File | Purpose |
|------|---------|
| iam_mfa_audit.py | Check users without MFA |
| sg_open_port_audit.py | Check security group exposure |
| stale_access_keys_audit.py | Check keys older than 90 days |

## Key Learning Points

### Paginators
- Always use paginators for list/describe calls
- Prevents missing resources

### Exception Handling
- Handle NoSuchEntityException for missing profiles
- Graceful failure for missing resources

### DateTime Serialization
- Convert datetime to ISO format: .isoformat()
- Use default=str for JSON serialization

### Security Best Practices
- Never hardcode credentials
- Use IAM roles where possible
- Encrypt sensitive data at rest
