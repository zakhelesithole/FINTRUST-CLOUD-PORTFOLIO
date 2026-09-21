import base64
import json


def lambda_handler(event, context):
    """Lambda handler that decodes Kinesis records (base64 encoded)."""
    for record in event['Records']:
        # Decode from base64, then parse JSON
        raw = base64.b64decode(record['kinesis']['data'])
        transaction = json.loads(raw.decode('utf-8'))

        print(f'Received: {transaction["transaction_id"]} | '
              f'Account: {transaction["account_id"]} | '
              f'Amount: {transaction["amount"]} {transaction["currency"]}')

        # Optional: index into OpenSearch here
        # index_transaction(transaction)


def main():
    print("=" * 60)
    print("FINTRIST BANK - KINESIS CONSUMER (LOCAL TEST)")
    print("=" * 60)
    print()

    # Simulate a KDS event payload (what Lambda actually receives)
    simulated_event = {
        'Records': [
            {
                'kinesis': {
                    'data': base64.b64encode(json.dumps({
                        'transaction_id': 'txn-test-001',
                        'account_id': 'ACC-0001',
                        'amount': 15000.00,
                        'currency': 'ZAR',
                        'type': 'PAYMENT'
                    }).encode()).decode()
                }
            }
        ]
    }

    lambda_handler(simulated_event, None)


if __name__ == "__main__":
    main()