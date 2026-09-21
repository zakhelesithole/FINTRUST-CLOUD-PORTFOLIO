import json
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns')
ALERT_TOPIC_ARN = os.environ.get('ALERT_TOPIC_ARN', '')
HIGH_RISK_THRESHOLD = float(os.environ.get('HIGH_RISK_THRESHOLD', '75.0'))


def calculate_risk_score(txn):
    """Calculate fraud risk score (0-100)."""
    score = 0.0

    # Amount scoring
    amount = float(txn.get('amount', 0))
    if amount > 50_000:
        score += 40
    elif amount > 10_000:
        score += 20
    elif amount > 1_000:
        score += 5

    # Currency scoring (cross-border)
    if txn.get('currency') != 'ZAR':
        score += 20

    # Description risk keywords
    desc = txn.get('description', '').lower()
    for keyword in ['crypto', 'wire', 'urgent', 'casino']:
        if keyword in desc:
            score += 15
            break

    return min(score, 100.0)


def lambda_handler(event, context):
    """Process SQS messages and publish high-risk alerts to SNS."""
    logger.info('Processing %d records', len(event.get('Records', [])))

    for record in event['Records']:
        try:
            txn = json.loads(record['body'])
            score = calculate_risk_score(txn)
            logger.info('Transaction %s risk score: %.1f', txn.get('id', 'unknown'), score)

            if score >= HIGH_RISK_THRESHOLD:
                if ALERT_TOPIC_ARN:
                    sns.publish(
                        TopicArn=ALERT_TOPIC_ARN,
                        Subject=f'HIGH RISK: Transaction {txn.get("id", "unknown")}',
                        Message=json.dumps({
                            'transaction_id': txn.get('id'),
                            'account_id': txn.get('account_id'),
                            'amount': txn.get('amount'),
                            'currency': txn.get('currency'),
                            'risk_score': score,
                            'reason': 'Score exceeds threshold'
                        }),
                        MessageAttributes={
                            'risk_level': {'DataType': 'String', 'StringValue': 'HIGH'}
                        }
                    )
                    logger.warning('Alert published for transaction %s (score: %.1f)', txn.get('id'), score)
                else:
                    logger.error('ALERT_TOPIC_ARN not set - cannot publish alert')

        except Exception as e:
            logger.error('Error processing record: %s', str(e))
            # Continue processing other records
            continue

    return {'statusCode': 200, 'body': json.dumps({'message': 'Processing complete'})}


if __name__ == "__main__":
    # Local test
    test_event = {
        'Records': [
            {
                'body': json.dumps({
                    'id': 'txn-123',
                    'account_id': 'ACC-999',
                    'amount': 75000,
                    'currency': 'USD',
                    'description': 'crypto wire transfer urgent'
                })
            }
        ]
    }

    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))