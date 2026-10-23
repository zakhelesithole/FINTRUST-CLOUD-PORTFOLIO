from ..utils.sessions import get_client

VALID_STRATEGIES = {'rehost', 'replatform', 'refactor', 'retire', 'retain', 'repurchase'}

def _get_tag(tags, key):
    for t in (tags or []):
        if t['Key'] == key:
            return t['Value']
    return None

def classify_instances(tag_prefix='migration'):
    ec2 = get_client('ec2')
    paginator = ec2.get_paginator('describe_instances')

    portfolio = {s: [] for s in VALID_STRATEGIES}
    untagged = []

    try:
        for page in paginator.paginate():
            for reservation in page['Reservations']:
                for inst in reservation['Instances']:
                    tags = inst.get('Tags', [])
                    strategy = _get_tag(tags, f'{tag_prefix}:strategy')
                    name     = _get_tag(tags, 'Name') or inst['InstanceId']
                    wave     = _get_tag(tags, f'{tag_prefix}:wave') or 'unassigned'

                    entry = {
                        'id': inst['InstanceId'],
                        'name': name,
                        'type': inst['InstanceType'],
                        'state': inst['State']['Name'],
                        'wave': wave,
                        'strategy': strategy
                    }

                    if strategy in VALID_STRATEGIES:
                        portfolio[strategy].append(entry)
                    else:
                        untagged.append(entry)
    except Exception as e:
        print(f"Error fetching EC2 instances: {e}")

    return portfolio, untagged

def get_migration_wave(wave_number):
    portfolio, _ = classify_instances()
    return [
        inst
        for instances in portfolio.values()
        for inst in instances
        if inst['wave'] == str(wave_number)
    ]
