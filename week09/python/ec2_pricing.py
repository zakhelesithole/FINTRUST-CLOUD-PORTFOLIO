import boto3
import json

# Pricing API is ALWAYS us-east-1
pricing = boto3.client('pricing', region_name='us-east-1')

REGION_NAMES = {
    'af-south-1': 'Africa (Cape Town)',
    'eu-west-1': 'Europe (Ireland)',
    'us-east-1': 'US East (N. Virginia)',
    'us-west-2': 'US West (Oregon)',
    'ap-southeast-1': 'Asia Pacific (Singapore)',
}

def get_ec2_ondemand_price(instance_type, region='af-south-1', os='Linux'):
    region_name = REGION_NAMES.get(region)
    if not region_name:
        return None

    response = pricing.get_products(
        ServiceCode='AmazonEC2',
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': region_name},
            {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': os},
            {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
            {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw', 'Value': 'NA'},
            {'Type': 'TERM_MATCH', 'Field': 'capacityStatus', 'Value': 'Used'},
        ],
        MaxResults=1
    )

    if not response['PriceList']:
        return None

    product = json.loads(response['PriceList'][0])
    terms = product['terms']['OnDemand']
    price_dimensions = next(iter(next(iter(terms.values()))['priceDimensions'].values()))
    return float(price_dimensions['pricePerUnit']['USD'])

def monthly_cost(hourly_price):
    return hourly_price * 730

if __name__ == "__main__":
    print("=" * 70)
    print("FINTRIST BANK - EC2 ON-DEMAND PRICE QUERY")
    print("=" * 70)
    
    instances = ['m5.xlarge', 'r5.2xlarge', 'c5.large', 't3.micro']
    for inst in instances:
        price = get_ec2_ondemand_price(inst, region='af-south-1')
        if price:
            print(f"{inst:<15} ${price:.4f}/hr  ${monthly_cost(price):,.2f}/month")
        else:
            print(f"{inst:<15} Not available in af-south-1")
