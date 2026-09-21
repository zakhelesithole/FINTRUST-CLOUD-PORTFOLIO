import boto3
from datetime import datetime

ec2 = boto3.client('ec2', region_name='af-south-1')

RESTRICTED_PORTS = {22, 3389, 5432, 3306, 1521}
OPEN_CIDR = '0.0.0.0/0'


def check_sg_exposure(sg):
    """Return list of exposed port findings for a Security Group."""
    findings = []
    sg_id = sg['GroupId']
    sg_name = sg.get('GroupName', sg_id)

    for rule in sg.get('IpPermissions', []):
        from_port = rule.get('FromPort', 0)
        to_port = rule.get('ToPort', 65535)

        # Check IPv4 CIDR ranges
        for ip_range in rule.get('IpRanges', []):
            if ip_range['CidrIp'] == OPEN_CIDR:
                exposed_ports = [
                    p for p in RESTRICTED_PORTS
                    if from_port <= p <= to_port
                ]
                if exposed_ports or (from_port == 0 and to_port == 65535):
                    findings.append({
                        'sg_id': sg_id,
                        'sg_name': sg_name,
                        'port_range': f"{from_port}-{to_port}",
                        'cidr': OPEN_CIDR,
                        'severity': 'CRITICAL' if from_port == 0 else 'HIGH'
                    })
    return findings


def main():
    print("=" * 60)
    print("FINTRIST BANK - SECURITY GROUP OPEN PORT AUDIT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    paginator = ec2.get_paginator('describe_security_groups')
    all_findings = []

    for page in paginator.paginate():
        for sg in page['SecurityGroups']:
            all_findings.extend(check_sg_exposure(sg))

    print(f"Security Groups with open restricted ports: {len(all_findings)}")

    if all_findings:
        print("\nFindings:")
        for f in all_findings:
            print(f"  [{f['severity']}] {f['sg_name']} ({f['sg_id']}) port {f['port_range']} open to {f['cidr']}")
    else:
        print("No open restricted ports found.")

    print()
    print("=" * 60)
    print("AUDIT COMPLETE")


if __name__ == "__main__":
    main()