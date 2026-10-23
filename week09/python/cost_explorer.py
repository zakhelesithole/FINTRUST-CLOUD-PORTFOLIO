import boto3

ce = boto3.client('ce', region_name='us-east-1')

def get_monthly_spend_by_service(year, month):
    start = f'{year}-{month:02d}-01'
    end = f'{year + 1}-01-01' if month == 12 else f'{year}-{month + 1:02d}-01'

    try:
        response = ce.get_cost_and_usage(
            TimePeriod={'Start': start, 'End': end},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
    except Exception as e:
        print(f"Error fetching Cost Explorer data: {e}")
        print("Note: You may need billing permissions, and this API costs $0.01 per call.")
        return {}

    results = {}
    for group in response['ResultsByTime'][0]['Groups']:
        service = group['Keys'][0]
        cost = float(group['Metrics']['UnblendedCost']['Amount'])
        if cost > 0.01:
            results[service] = round(cost, 2)

    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

if __name__ == "__main__":
    print("=" * 60)
    print("FINTRIST BANK - MONTHLY SPEND BY SERVICE")
    print("=" * 60)
    
    # Query current month (adjust as needed)
    spend = get_monthly_spend_by_service(2026, 9)
    if not spend:
        print("No data available.")
    else:
        for service, cost in list(spend.items())[:10]:
            print(f"  {service:<45} ${cost:>10,.2f}")
