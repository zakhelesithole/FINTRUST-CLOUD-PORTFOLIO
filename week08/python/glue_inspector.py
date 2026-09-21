import boto3

glue = boto3.client('glue', region_name='af-south-1')


def list_databases():
    """List all databases in the Glue Data Catalog."""
    print("=" * 60)
    print("GLUE DATA CATALOG - DATABASES")
    print("=" * 60)
    print()

    response = glue.get_databases()

    if not response['DatabaseList']:
        print("No databases found.")
        return

    for db in response['DatabaseList']:
        print(f"Database: {db['Name']}")
        if db.get('Description'):
            print(f"  Description: {db['Description']}")


def list_tables(database_name):
    """List all tables in a Glue database."""
    print()
    print("=" * 60)
    print(f"TABLES IN DATABASE: {database_name}")
    print("=" * 60)
    print()

    try:
        response = glue.get_tables(DatabaseName=database_name)
    except glue.exceptions.EntityNotFoundException:
        print(f"Database '{database_name}' not found.")
        return

    if not response['TableList']:
        print("No tables found.")
        return

    for tbl in response['TableList']:
        location = tbl.get('StorageDescriptor', {}).get('Location', 'N/A')
        print(f"Table: {tbl['Name']}")
        print(f"  Location: {location}")
        print(f"  Created: {tbl.get('CreateTime', 'N/A')}")
        print()


def get_table_schema(database_name, table_name):
    """Get the full schema of a Glue table."""
    print()
    print("=" * 60)
    print(f"SCHEMA: {database_name}.{table_name}")
    print("=" * 60)
    print()

    try:
        response = glue.get_table(
            DatabaseName=database_name,
            Name=table_name
        )
    except glue.exceptions.EntityNotFoundException:
        print(f"Table '{database_name}.{table_name}' not found.")
        return

    table = response['Table']

    # Columns
    columns = table['StorageDescriptor']['Columns']
    print("Columns:")
    print(f"  {'Name':<30} {'Type':<20}")
    print("-" * 50)
    for col in columns:
        print(f"  {col['Name']:<30} {col['Type']:<20}")

    # Partition keys
    partition_keys = table.get('PartitionKeys', [])
    if partition_keys:
        print()
        print("Partition Keys:")
        print(f"  {'Name':<30} {'Type':<20}")
        print("-" * 50)
        for pk in partition_keys:
            print(f"  {pk['Name']:<30} {pk['Type']:<20}")

    # Storage format
    sd = table.get('StorageDescriptor', {})
    print()
    print("Storage:")
    print(f"  Input Format:  {sd.get('InputFormat', 'N/A')}")
    print(f"  Output Format: {sd.get('OutputFormat', 'N/A')}")
    print(f"  SerDe:         {sd.get('SerdeInfo', {}).get('SerializationLibrary', 'N/A')}")


def main():
    # List all databases
    list_databases()

    # List tables in a specific database
    list_tables('fintrust_curated')

    # Get schema of a specific table
    get_table_schema('fintrust_curated', 'transactions')


if __name__ == "__main__":
    main()