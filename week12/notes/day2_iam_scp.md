# Week 12 Day 2 - IAM & SCP Troubleshooting

## Scheduling with EventBridge
EventBridge cron expressions run in **UTC**.
SAST (South Africa Standard Time) is UTC+2.
To run a report at 08:00 SAST (06:00 UTC) on the first Monday of every month:
`cron(0 6 ? * 2#1 *)`

## IAM and SCP Conflict Scenarios

### Scenario 1: Explicit Deny in SCP
- **Symptom:** "Access Denied with an explicit deny".
- **Cause:** An SCP (Service Control Policy) at the Organization/OU level is blocking the action (e.g., restricting regions to `af-south-1`).
- **Fix:** Modify the SCP to allow the new region, or inform the developer it's out of compliance.

### Scenario 2: Cross-Account S3 Access
- **Symptom:** Lambda in Account A gets AccessDenied writing to S3 in Account B.
- **Cause:** Cross-account access requires **both** the identity policy (Account A) AND the resource policy (Account B) to allow it.
- **Fix:** Add a bucket policy in Account B allowing the Lambda execution role ARN from Account A.

## Lab Scenarios Writeup

### SCP-001: Cannot disable GuardDuty
**Cause:** An SCP is explicitly denying the `guardduty:DeleteDetector` or `guardduty:DisassociateFromMasterAccount` action to protect the account.
**Layer:** Service Control Policy (SCP).
**Fix:** Check the Organizations console for the exact SCP. You must temporarily detach the SCP or use the management account to override it.

### IAM-002: Can read S3 but cannot delete
**Cause:** Even though the IAM policy allows `s3:DeleteObject`, an S3 Bucket Policy attached to the bucket contains an explicit `Deny` for deletes.
**Layer:** Resource Policy (S3 Bucket Policy).
**Fix:** Review the S3 bucket policy. If the environment is non-prod and the delete is legitimate, modify the bucket policy to remove the Deny statement.

### PB-003: Admin cannot create IAM roles
**Cause:** A Permissions Boundary is attached to the Administrator role. If the boundary doesn't explicitly allow `iam:CreateRole`, the action is blocked.
**Layer:** Permissions Boundary.
**Fix:** Update the Permissions Boundary policy to include `iam:CreateRole` and `iam:PutRolePolicy`.

## Reflection
Access Denied evaluation order:
1. Explicit Deny (SCP or Resource Policy)
2. SCPs
3. Resource Policies (Bucket/Queue)
4. Permission Boundaries
5. Identity Policies (IAM Roles/Users)
