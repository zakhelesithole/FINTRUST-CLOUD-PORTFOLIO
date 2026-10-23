import math

DEVICE_SPECS = {
    'Snowcone-HDD':              {'usable_tb': 8,       'description': 'Smallest, edge/disconnected'},
    'Snowcone-SSD':              {'usable_tb': 14,      'description': 'Snowcone with SSD'},
    'Snowball-Edge-Storage-Opt': {'usable_tb': 80,      'description': 'High-capacity storage migration'},
    'Snowball-Edge-Compute-Opt': {'usable_tb': 28,      'description': 'Edge compute and EC2-compatible'},
    'Snowmobile':                {'usable_tb': 100_000, 'description': 'Exabyte-scale, AWS truck required'},
}

SNOWMOBILE_THRESHOLD_TB = 10_000

def plan_snow_transfer(data_size_tb, purpose='archive'):
    """Recommend a Snow device and quantity for a given data volume."""
    if data_size_tb >= SNOWMOBILE_THRESHOLD_TB:
        device = 'Snowmobile'
        count = math.ceil(data_size_tb / DEVICE_SPECS['Snowmobile']['usable_tb'])
        return {
            'device': device, 
            'count': count,
            'total_capacity_tb': count * DEVICE_SPECS['Snowmobile']['usable_tb']
        }

    device = 'Snowball-Edge-Storage-Opt' if purpose == 'archive' else 'Snowball-Edge-Compute-Opt'
    usable = DEVICE_SPECS[device]['usable_tb']
    count = math.ceil(data_size_tb / usable)

    return {
        'device': device,
        'count': count,
        'total_capacity_tb': count * usable,
        'overhead_tb': round(count * usable - data_size_tb, 1),
        'description': DEVICE_SPECS[device]['description'],
    }

if __name__ == "__main__":
    print("=" * 60)
    print("FINTRIST BANK - SNOW TRANSFER PLANNER")
    print("=" * 60)
    
    # FinTrust: 3PB regulatory archive
    data_tb = 3000
    plan = plan_snow_transfer(data_tb, purpose='archive')
    
    print(f"Data size: {data_tb:,} TB")
    print(f"Device: {plan['device']}")
    print(f"Count: {plan['count']} devices")
    print(f"Total capacity: {plan['total_capacity_tb']:,} TB")
    print(f"Overhead: {plan.get('overhead_tb', 0):,} TB unused")
    
    # Internet alternative
    gbps = 1.0
    transfer_days = (data_tb * 1024) / (gbps * 3600 * 24 / 8)
    print(f"\nAlternative: internet transfer at {gbps} Gbps = {transfer_days:.0f} days")
    print("Snow transfer: ~2 weeks (ship + ingest + return)")
