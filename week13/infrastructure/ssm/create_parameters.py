import boto3

ssm = boto3.client('ssm', region_name='af-south-1')

def main():
    print("Storing SSM parameters...")
    
    params = {
        '/fintrust/dev/db_host':     'your-rds-endpoint.af-south-1.rds.amazonaws.com',
        '/fintrust/dev/db_name':     'fintrust',
        '/fintrust/dev/db_user':     'fintrust_app',
        '/fintrust/dev/db_password': 'CHANGE_ME_BEFORE_COMMITTING',
    }

    for name, value in params.items():
        ptype = 'SecureString' if 'password' in name else 'String'
        try:
            ssm.put_parameter(Name=name, Value=value, Type=ptype, Overwrite=True)
            print(f"Stored: {name} ({ptype})")
        except Exception as e:
            print(f"Error storing {name}: {e}")

if __name__ == "__main__":
    main()
