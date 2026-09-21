import boto3
import time

athena = boto3.client('athena', region_name='af-south-1')


def run_athena_query(sql, database, output_bucket):
    """
    Run an Athena query and return the results.
    
    Args:
        sql: SQL query string
        database: Athena database name
        output_bucket: S3 bucket for query results
    
    Returns:
        List of rows from the result set
    """
    # Start the query
    response = athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={
            'OutputLocation': f's3://{output_bucket}/athena-results/'
        }
    )
    query_id = response['QueryExecutionId']
    print(f"Query started: {query_id}")

    # Poll for completion
    while True:
        status = athena.get_query_execution(QueryExecutionId=query_id)
        state = status['QueryExecution']['Status']['State']
        print(f"  Status: {state}")
        
        if state in ('SUCCEEDED', 'FAILED', 'CANCELLED'):
            break
        time.sleep(2)

    if state != 'SUCCEEDED':
        reason = status['QueryExecution']['Status'].get('StateChangeReason', 'Unknown')
        raise RuntimeError(f'Query failed: {state} - {reason}')

    # Get results
    results = athena.get_query_results(QueryExecutionId=query_id)
    return results['ResultSet']['Rows']


def main():
    print("=" * 60)
    print("FINTRIST BANK - ATHENA QUERY")
    print("=" * 60)
    print()

    # Simple test query
    sql = """
    SELECT account_id, SUM(amount) as total, COUNT(*) as tx_count
    FROM transactions
    WHERE amount > 50000
    GROUP BY account_id
    ORDER BY total DESC
    LIMIT 10
    """

    try:
        rows = run_athena_query(
            sql,
            database='fintrust_curated',
            output_bucket='fintrust-athena-results'
        )

        # Print results
        print("\nResults:")
        print("-" * 60)
        
        # First row is header
        headers = [c.get('VarCharValue', '') for c in rows[0]['Data']]
        print(f"{headers[0]:20} {headers[1]:>15} {headers[2]:>10}")
        print("-" * 60)

        for row in rows[1:]:
            vals = [c.get('VarCharValue', '') for c in row['Data']]
            print(f"{vals[0]:20} {vals[1]:>15} {vals[2]:>10}")

    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: This requires actual AWS resources (S3, Glue, Athena).")
        print("If you don't have these, the script will fail.")


if __name__ == "__main__":
    main()