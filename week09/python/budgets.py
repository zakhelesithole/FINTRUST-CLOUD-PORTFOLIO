import boto3

# Budgets API is always us-east-1
budgets = boto3.client('budgets', region_name='us-east-1')
sts = boto3.client('sts')

try:
    ACCOUNT_ID = sts.get_caller_identity()['Account']
except Exception as e:
    print(f"Could not get Account ID: {e}")
    ACCOUNT_ID = "123456789012"

def create_monthly_budget(budget_name, limit_usd, alert_pct, email):
    """Create a monthly cost budget with a single percentage-threshold alert."""
    try:
        budgets.create_budget(
            AccountId=ACCOUNT_ID,
            Budget={
                'BudgetName': budget_name,
                'BudgetLimit': {'Amount': str(limit_usd), 'Unit': 'USD'},
                'TimeUnit': 'MONTHLY',
                'BudgetType': 'COST',
            },
            NotificationsWithSubscribers=[{
                'Notification': {
                    'NotificationType': 'ACTUAL',
                    'ComparisonOperator': 'GREATER_THAN',
                    'Threshold': alert_pct,
                    'ThresholdType': 'PERCENTAGE',
                },
                'Subscribers': [{'SubscriptionType': 'EMAIL', 'Address': email}]
            }]
        )
        print(f'Budget "{budget_name}" created successfully.')
    except Exception as e:
        print(f"Failed to create budget (might need permissions): {e}")

def list_budgets():
    try:
        response = budgets.describe_budgets(AccountId=ACCOUNT_ID)
        for b in response['Budgets']:
            limit = float(b['BudgetLimit']['Amount'])
            actual = float(b.get('CalculatedSpend', {}).get('ActualSpend', {}).get('Amount', 0))
            pct = (actual / limit * 100) if limit > 0 else 0
            print(f'  {b["BudgetName"]}: ${actual:.2f} / ${limit:.2f} ({pct:.1f}%)')
    except Exception as e:
        print(f"Failed to list budgets: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("FINTRIST BANK - BUDGETS API")
    print("=" * 60)
    
    create_monthly_budget('FinTrust-Analytics-Monthly', 15000, 80.0, 'test@example.com')
    print("\nExisting Budgets:")
    list_budgets()
