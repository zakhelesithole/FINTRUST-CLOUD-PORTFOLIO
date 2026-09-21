import json
import os
import logging
import boto3

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# SQS client (if needed)
sqs = boto3.client('sqs')
QUEUE_URL = os.environ.get('PAYMENT_QUEUE_URL', '')


def lambda_handler(event, context):
    """
    Lambda handler for FinTrust transaction processing.
    
    Args:
        event: dict containing the trigger payload
        context: object with runtime metadata
    
    Returns:
        dict: API Gateway response format
    """
    # Log the event for debugging
    logger.info('Event: %s', json.dumps(event))
    
    # Log context information
    logger.info('Function name: %s', context.function_name)
    logger.info('Function version: %s', context.function_version)
    logger.info('Memory limit: %s MB', context.memory_limit_in_mb)
    logger.info('Remaining time (ms): %s', context.get_remaining_time_in_millis())
    logger.info('AWS Request ID: %s', context.aws_request_id)
    logger.info('Log group: %s', context.log_group_name)

    # Check for API Gateway event
    if 'httpMethod' in event:
        return handle_api_gateway(event, context)
    
    # Check for SQS event
    if 'Records' in event and event.get('Records', [{}])[0].get('eventSource') == 'aws:sqs':
        return handle_sqs(event, context)
    
    # Check for S3 event
    if 'Records' in event and event.get('Records', [{}])[0].get('eventSource') == 'aws:s3':
        return handle_s3(event, context)
    
    # Default response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Hello from FinTrust Lambda!',
            'event': event
        })
    }


def handle_api_gateway(event, context):
    """Handle API Gateway proxy event."""
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    params = event.get('queryStringParameters') or {}
    body_str = event.get('body') or '{}'
    
    try:
        body = json.loads(body_str)
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON body'})
        }
    
    # Validate required fields for POST /transactions
    if method == 'POST' and path == '/transactions':
        account_id = body.get('account_id')
        amount = body.get('amount')
        
        if not account_id or not amount:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'account_id and amount are required'
                })
            }
        
        logger.info('Processing transaction for account %s, amount %s', account_id, amount)
        
        return {
            'statusCode': 201,
            'body': json.dumps({
                'status': 'accepted',
                'account_id': account_id,
                'amount': amount,
                'message': 'Transaction accepted for processing'
            })
        }
    
    # GET /transactions
    if method == 'GET' and path == '/transactions':
        account_id = params.get('account_id')
        if account_id:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'account_id': account_id,
                    'transactions': []
                })
            }
        return {
            'statusCode': 200,
            'body': json.dumps({'transactions': []})
        }
    
    # Health check
    if path == '/health':
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'ok'})
        }
    
    return {
        'statusCode': 404,
        'body': json.dumps({'error': f'Route {method} {path} not found'})
    }


def handle_sqs(event, context):
    """Handle SQS event."""
    logger.info('Processing SQS event with %d records', len(event['Records']))
    
    for record in event['Records']:
        body = json.loads(record['body'])
        queue_arn = record.get('eventSourceARN', 'unknown')
        message_id = record.get('messageId', 'unknown')
        
        logger.info('Processing message %s from %s', message_id, queue_arn)
        logger.info('Message body: %s', body)
    
    # Return nothing: Lambda reports success


def handle_s3(event, context):
    """Handle S3 event."""
    logger.info('Processing S3 event with %d records', len(event['Records']))
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        size = record['s3']['object'].get('size', 0)
        event_name = record.get('eventName', 'unknown')
        
        logger.info('Event: %s - s3://%s/%s (%d bytes)', event_name, bucket, key, size)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'S3 event processed'})
    }


if __name__ == "__main__":
    # For local testing
    test_event = {
        'httpMethod': 'POST',
        'path': '/transactions',
        'body': '{"account_id": "ACC-001", "amount": 500.00}'
    }
    
    # Mock context
    class MockContext:
        function_name = 'local-test'
        function_version = '$LATEST'
        memory_limit_in_mb = 128
        aws_request_id = 'local-123'
        log_group_name = '/aws/lambda/local'
        
        def get_remaining_time_in_millis(self):
            return 60000
    
    result = lambda_handler(test_event, MockContext())
    print(json.dumps(result, indent=2))