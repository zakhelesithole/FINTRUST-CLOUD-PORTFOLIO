import csv
import boto3
from datetime import date, timedelta
from pathlib import Path

def get_monthly_spend_by_service(months_back=1):
    """Return list of (service, cost_usd) tuples for the past N months."""
    ce = boto3.client('ce', region_name='us-east-1')
    today = date.today()
    start = (today.replace(day=1) - timedelta(days=months_back * 31)).strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')

    try:
        resp = ce.get_cost_and_usage(
            TimePeriod={'Start': start, 'End': end},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
    except Exception as e:
        print(f"Error fetching Cost Explorer data: {e}")
        return []

    results = []
    for period in resp['ResultsByTime']:
        period_start = period['TimePeriod']['Start']
        for group in period['Groups']:
            service = group['Keys'][0]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])
            results.append({'period': period_start, 'service': service, 'cost_usd': cost})
    return results

def write_csv_report(data, output_path='cost_report.csv'):
    """Write cost data to CSV. Returns path to written file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['period', 'service', 'cost_usd'])
        writer.writeheader()
        writer.writerows(data)
    return path

def write_html_report(data, output_path='cost_report.html'):
    """Write a simple HTML cost report. Returns path to written file."""
    rows = ''.join(
        f"<tr><td>{r['period']}</td><td>{r['service']}</td><td>${r['cost_usd']:.2f}</td></tr>\n"
        for r in sorted(data, key=lambda x: x['cost_usd'], reverse=True)
        if r['cost_usd'] > 0
    )
    html = f"""<!DOCTYPE html>
<html><head><title>FinTrust Cost Report</title></head>
<body><h1>Monthly Cost Report</h1>
<table border="1"><tr><th>Period</th><th>Service</th><th>Cost (USD)</th></tr>
{rows}</table></body></html>"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html)
    return path

def get_per_account_spend(months_back=1):
    """Extension: Get spend grouped by linked account and service."""
    ce = boto3.client('ce', region_name='us-east-1')
    org = boto3.client('organizations', region_name='us-east-1')
    
    # 1. Fetch account names
    account_map = {}
    try:
        paginator = org.get_paginator('list_accounts')
        for page in paginator.paginate():
            for acct in page['Accounts']:
                account_map[acct['Id']] = acct['Name']
    except Exception as e:
        print(f"Could not fetch Organizations data (ignoring names): {e}")

    today = date.today()
    start = (today.replace(day=1) - timedelta(days=months_back * 31)).strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')

    try:
        resp = ce.get_cost_and_usage(
            TimePeriod={'Start': start, 'End': end},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                {'Type': 'DIMENSION', 'Key': 'SERVICE'}
            ]
        )
    except Exception as e:
        print(f"Error fetching multi-account data: {e}")
        return []

    results = []
    for period in resp['ResultsByTime']:
        period_start = period['TimePeriod']['Start']
        for group in period['Groups']:
            account_id, service = group['Keys']
            cost = float(group['Metrics']['UnblendedCost']['Amount'])
            results.append({
                'period': period_start,
                'account_id': account_id,
                'account_name': account_map.get(account_id, 'Unknown'),
                'service': service,
                'cost_usd': cost
            })
    return results
