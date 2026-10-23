import boto3

s3 = boto3.client('s3', region_name='af-south-1')
lam = boto3.client('lambda', region_name='af-south-1')
BUCKET = 'fintrust-ingest-dev'
FN_NAME = 'fintrust-ingest'

def main():
    print(f"Configuring S3 trigger for {FN_NAME} on {BUCKET}...")
    
    try:
        ACCOUNT = boto3.client('sts').get_caller_identity()['Account']
    except Exception as e:
        print(f"Could not retrieve Account ID: {e}")
        return

    # 1. Grant S3 permission to invoke Lambda
    try:
        lam.add_permission(
            FunctionName=FN_NAME,
            StatementId='s3-ingest-invoke',
            Action='lambda:InvokeFunction',
            Principal='s3.amazonaws.com',
            SourceArn=f'arn:aws:s3:::{BUCKET}',
            SourceAccount=ACCOUNT
        )
        print("Added Lambda invoke permission.")
    except lam.exceptions.ResourceConflictException:
        print("Lambda permission already exists.")
    except Exception as e:
        print(f"Error adding Lambda permission (does the function exist?): {e}")
        return

    # 2. Configure bucket notification
    try:
        FN_ARN = lam.get_function(FunctionName=FN_NAME)['Configuration']['FunctionArn']
        s3.put_bucket_notification_configuration(
            Bucket=BUCKET,
            NotificationConfiguration={'LambdaFunctionConfigurations': [{
                'LambdaFunctionArn': FN_ARN,
                'Events': ['s3:ObjectCreated:Put'],
                'Filter': {'Key': {'FilterRules': [
                    {'Name': 'prefix', 'Value': 'raw/'},
                    {'Name': 'suffix', 'Value': '.csv'}
                ]}}
            }]}
        )
        print("S3 event trigger configured.")
    except Exception as e:
        print(f"Error configuring bucket notification: {e}")

if __name__ == "__main__":
    main()
