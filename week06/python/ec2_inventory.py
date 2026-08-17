import boto3
from datetime import datetime

def get_ec2_inventory(region_name='af-south-1'):
    """Get inventory of all EC2 instances in a region."""
    ec2 = boto3.client('ec2', region_name=region_name)

    # Create paginator for describe_instances
    paginator = ec2.get_paginator('describe_instances')

    instances = []

    # Paginate through all reservations
    for page in paginator.paginate():
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                # Get instance details
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                instance_type = instance['InstanceType']
                vpc_id = instance.get('VpcId', 'N/A')
                subnet_id = instance.get('SubnetId', 'N/A')
                private_ip = instance.get('PrivateIpAddress', 'N/A')
                public_ip = instance.get('PublicIpAddress', 'N/A')
                launch_time = instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S')

                # Get Name tag
                name = 'No Name'
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                        name = tag['Value']

                # Get Security Groups
                sg_names = []
                for sg in instance.get('SecurityGroups', []):
                    sg_names.append(sg['GroupName'])

                instances.append({
                    'instance_id': instance_id,
                    'name': name,
                    'state': state,
                    'instance_type': instance_type,
                    'vpc_id': vpc_id,
                    'subnet_id': subnet_id,
                    'private_ip': private_ip,
                    'public_ip': public_ip,
                    'launch_time': launch_time,
                    'security_groups': ', '.join(sg_names)
                })

    return instances

def print_inventory(instances):
    """Print EC2 inventory in a formatted table."""
    print("=" * 100)
    print("FINTRIST BANK - EC2 INVENTORY REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    print()

    if not instances:
        print("No EC2 instances found.")
        return

    # Header
    print(f"{'INSTANCE ID':<20} {'NAME':<20} {'STATE':<12} {'TYPE':<14} {'PRIVATE IP':<15} {'PUBLIC IP':<15} {'VPC':<12}")
    print("-" * 108)

    # Count by state
    state_counts = {}

    for inst in instances:
        print(f"{inst['instance_id']:<20} {inst['name']:<20} {inst['state']:<12} {inst['instance_type']:<14} {inst['private_ip']:<15} {inst['public_ip']:<15} {inst['vpc_id']:<12}")
        state_counts[inst['state']] = state_counts.get(inst['state'], 0) + 1

    print("-" * 108)
    print()

    print("SUMMARY:")
    for state, count in state_counts.items():
        print(f"  {state}: {count}")

    print()
    print("=" * 100)
    print("INVENTORY COMPLETE")

def main():
    # Get instances from Cape Town region
    instances = get_ec2_inventory('af-south-1')
    print_inventory(instances)

if __name__ == "__main__":
    main()