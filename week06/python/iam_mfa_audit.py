import boto3
from datetime import datetime

iam = boto3.client('iam')


def get_users_without_mfa():
    """Return list of IAM users who have console access but no MFA device."""
    violations = []
    paginator = iam.get_paginator('list_users')

    for page in paginator.paginate():
        for user in page['Users']:
            username = user['UserName']

            # Check if user has a console password (not service account)
            try:
                iam.get_login_profile(UserName=username)
                has_console_access = True
            except iam.exceptions.NoSuchEntityException:
                has_console_access = False

            if not has_console_access:
                continue  # Service accounts don't need MFA

            # Check MFA devices for this user
            mfa_response = iam.list_mfa_devices(UserName=username)
            has_mfa = len(mfa_response['MFADevices']) > 0

            if not has_mfa:
                violations.append({
                    'username': username,
                    'created': user['CreateDate'].isoformat(),
                    'last_activity': user.get('PasswordLastUsed', 'never')
                })

    return violations


def main():
    print("=" * 60)
    print("FINTRIST BANK - IAM MFA AUDIT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    violations = get_users_without_mfa()
    print(f"Users without MFA: {len(violations)}")

    if violations:
        print("\nViolations found:")
        for v in violations:
            print(f"  - {v['username']} (created {v['created']})")
    else:
        print("All users with console access have MFA enabled.")

    print()
    print("=" * 60)
    print("AUDIT COMPLETE")


if __name__ == "__main__":
    main()