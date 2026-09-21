import boto3
import time
import csv
import os


class FinTrustComplianceReporter:
    """Automated compliance reporting using Athena and S3."""

    def __init__(self, database, output_bucket, region='af-south-1'):
        """
        Initialise the reporter.
        
        Args:
            database: Athena/Glue database name
            output_bucket: S3 bucket for Athena query results
            region: AWS region
        """
        self.database = database
        self.output_bucket = output_bucket
        self.region = region
        self.athena = boto3.client('athena', region_name=region)
        self.s3 = boto3.client('s3', region_name=region)

    def run_report(self, report_name, sql):
        """
        Execute SQL, poll for completion, write results to CSV.
        
        Args:
            report_name: Name of the report (used for CSV filename)
            sql: SQL query string
        
        Returns:
            Number of data rows written (excluding header)
        """
        print(f"Running report: {report_name}")
        print(f"  Database: {self.database}")
        print(f"  SQL: {sql[:100]}...")

        # Start query
        response = self.athena.start_query_execution(
            QueryString=sql,
            QueryExecutionContext={'Database': self.database},
            ResultConfiguration={
                'OutputLocation': f's3://{self.output_bucket}/athena-results/'
            }
        )
        query_id = response['QueryExecutionId']
        print(f"  Query ID: {query_id}")

        # Poll for completion
        while True:
            status = self.athena.get_query_execution(QueryExecutionId=query_id)
            state = status['QueryExecution']['Status']['State']
            print(f"  Status: {state}")

            if state in ('SUCCEEDED', 'FAILED', 'CANCELLED'):
                break
            time.sleep(2)

        if state != 'SUCCEEDED':
            reason = status['QueryExecution']['Status'].get('StateChangeReason', 'Unknown')
            raise RuntimeError(f'Query failed: {state} - {reason}')

        # Get results
        results = self.athena.get_query_results(QueryExecutionId=query_id)
        rows = results['ResultSet']['Rows']

        # Write to CSV
        csv_filename = f"{report_name}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            for row in rows:
                values = [c.get('VarCharValue', '') for c in row['Data']]
                writer.writerow(values)

        data_rows = len(rows) - 1  # Exclude header
        print(f"Report '{report_name}' complete: {data_rows} rows written to {csv_filename}")
        return data_rows

    def save_to_s3(self, bucket, key, local_path):
        """
        Upload a local file to S3.
        
        Args:
            bucket: S3 bucket name
            key: S3 object key (path in bucket)
            local_path: Local file path
        
        Returns:
            S3 URL of uploaded file
        """
        self.s3.upload_file(local_path, bucket, key)
        s3_url = f"s3://{bucket}/{key}"
        print(f"Uploaded {local_path} to {s3_url}")
        return s3_url


def main():
    print("=" * 60)
    print("FINTRIST BANK - COMPLIANCE REPORTER")
    print("=" * 60)
    print()

    reporter = FinTrustComplianceReporter(
        database='fintrust_curated',
        output_bucket='fintrust-athena-results'
    )

    # Report 1: High-value transactions
    sql1 = """
    SELECT account_id, SUM(amount) as total, COUNT(*) as tx_count
    FROM transactions
    WHERE amount > 50000
    GROUP BY account_id
    ORDER BY total DESC
    LIMIT 100
    """

    try:
        rows_written = reporter.run_report('high_value_transactions', sql1)
        print()

        # Upload to S3
        reporter.save_to_s3(
            bucket='fintrust-compliance-reports',
            key='reports/high_value_transactions.csv',
            local_path='high_value_transactions.csv'
        )
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: This requires actual AWS resources.")
        print("If you don't have S3, Glue, and Athena set up, this will fail.")


if __name__ == "__main__":
    main()