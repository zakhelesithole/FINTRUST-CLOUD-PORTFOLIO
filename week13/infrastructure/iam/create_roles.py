import boto3
import json

iam = boto3.client('iam')

TRUST_POLICY = json.dumps({
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "lambda.amazonaws.com"},
        "Action": "sts:AssumeRole"
    }]
})

ROLE_NAME = 'fintrust-lambda-ingest-role'

INGEST_POLICY = json.dumps({
    "Version": "2012-10-17",
    "Statement": [
        {"Effect":"Allow","Action":["s3:GetObject"],
         "Resource":"arn:aws:s3:::fintrust-ingest-dev/raw/*"},
        {"Effect":"Allow","Action":["ssm:GetParameter"],
         "Resource":"arn:aws:ssm:af-south-1:*:parameter/fintrust/dev/*"},
        {"Effect":"Allow","Action":["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"],
         "Resource":"*"}
    ]
})

def main():
    print("Creating IAM Role...")
    try:
        resp = iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=TRUST_POLICY,
            Description='Ingest Lambda: read S3, write RDS, get SSM params',
            Tags=[{'Key':'Project','Value':'FinTrust'}]
        )
        role_arn = resp['Role']['Arn']
        print(f"Role created: {role_arn}")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"Role {ROLE_NAME} already exists.")
        role_arn = iam.get_role(RoleName=ROLE_NAME)['Role']['Arn']

    print("Attaching inline policy...")
    try:
        iam.put_role_policy(
            RoleName=ROLE_NAME,
            PolicyName='IngestPermissions',
            PolicyDocument=INGEST_POLICY
        )
        print("Inline policy attached.")
    except Exception as e:
        print(f"Error attaching policy: {e}")

if __name__ == "__main__":
    main()
