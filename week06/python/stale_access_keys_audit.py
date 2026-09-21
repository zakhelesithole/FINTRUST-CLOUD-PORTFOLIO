import boto3
from datetime import datetime, timezone

iam = boto3.client('iam')


def get_stale_access_keys(days_threshold=90):
    """Return list of IAM users with access keys older than threshold."""
    violations = []
    paginator = iam.get_paginator('list_users')

    now = datetime.now(timezone.utc)

    for page in paginator.paginate():
        for user in page['Users']:
            username = user['UserName']

            try:
                keys_response = iam.list_access_keys(UserName=username)
            except Exception:
                continue

            for key in keys_response.get('AccessKeyMetadata', []):
                create_date = key['CreateDate']
                if create_date.tzinfo is None:
                    create_date = create_date.replace(tzinfo=timezone.utc)

                days_old = (now - create_date).days

                if days_old > days_threshold:
                    violations.append({
                        'username': username,
                        'access_key_id': key['AccessKeyId'],
                        'created': create_date.isoformat(),
                        'days_old': days_old,
                        'status': key['Status']
                    })

    return violations


def main():
    print("=" * 60)
    print("FINTRIST BANK - STALE ACCESS KEY AUDIT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    violations = get_stale_access_keys(90)
    print(f"Stale access keys (>90 days old): {len(violations)}")

    if violations:
        print("\nViolations found:")
        for v in violations:
            print(f"  - {v['username']}: {v['access_key_id']} ({v['days_old']} days old)")
    else:
        print("No stale access keys found.")

    print()
    print("=" * 60)
    print("AUDIT COMPLETE")


if __name__ == "__main__":
    main()