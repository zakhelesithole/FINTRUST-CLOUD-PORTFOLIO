import pandas as pd

print("=" * 60)
print("READ PARQUET FROM S3")
print("=" * 60)
print()

try:
    df = pd.read_parquet(
        's3://fintrust-processed/transactions/year=2024/month=06/transactions.parquet',
        engine='pyarrow'
        # storage_options not needed if using IAM credentials
    )

    print("Data loaded from S3:")
    print(df)
    print()

    # Query 1: Filter for high-value transactions
    high_value = df[df['is_high_value'] == True]
    print(f"High-value transactions: {len(high_value)}")
    if len(high_value) > 0:
        print(high_value[['account_id', 'amount', 'currency']])

    print()

    # Query 2: Total amount by currency
    by_currency = df.groupby('currency')['amount'].sum().reset_index()
    by_currency.columns = ['currency', 'total_amount']
    print("Total by currency:")
    print(by_currency)

except Exception as e:
    print(f"Error: {e}")
    print()
    print("Note: This requires an S3 bucket with Parquet files.")
    print("Run csv_to_parquet.py and upload_to_s3.py first.")