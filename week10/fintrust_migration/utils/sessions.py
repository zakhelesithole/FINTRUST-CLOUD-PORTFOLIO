import boto3
import os

_session = None

def get_session():
    global _session
    if _session is None:
        # Fallback to None profile if fintrust-migration profile doesn't exist
        profile = os.getenv('AWS_PROFILE', 'fintrust-migration')
        try:
            _session = boto3.Session(
                region_name=os.getenv('AWS_REGION', 'af-south-1'),
                profile_name=profile
            )
        except Exception:
            # If profile fails, use default credentials
            _session = boto3.Session(region_name=os.getenv('AWS_REGION', 'af-south-1'))
    return _session

def get_client(service):
    return get_session().client(service)

def get_resource(service):
    return get_session().resource(service)
