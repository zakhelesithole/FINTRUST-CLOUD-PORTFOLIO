import boto3
from datetime import date

# Cost Explorer is always us-east-1
ce = boto3.client('ce', region_name='us-east-1')

def get_monthly_spend_by_service(year, month):
    """Returns dict mapping service name to total spend (USD) for the given month."""
    start = f'{year}-{month:02d}-01'
    
    # Compute first day of next month
    if month == 12:
        end = f'{year + 1}-01-01'
    else:
        end = f'{year}-{month + 1:02d}-01'

    try:
        response = ce.get_cost_and_usage(
            TimePeriod={'Start': start, 'End': end},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
    except Exception as e:
        print(f"Error fetching Cost Explorer data: {e}")
        return {}

    results = {}
    for group in response['ResultsByTime'][0]['Groups']:
        service = group['Keys'][0]
        cost = float(group['Metrics']['UnblendedCost']['Amount'])
        if cost > 0.01:  # filter out near-zero services
            results[service] = round(cost, 2)

    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

if __name__ == "__main__":
    print("=" * 60)
    print("FINTRIST BANK - MONTHLY SPEND BY SERVICE")
    print("=" * 60)
    
    # Query last month's data
    spend = get_monthly_spend_by_service(2026, 8) # Example month
    if not spend:
        print("No data available or missing permissions.")
    else:
        for service, cost in list(spend.items())[:10]:
            print(f"  {service:<45} ${cost:>10,.2f}")
