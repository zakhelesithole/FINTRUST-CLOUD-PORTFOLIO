import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import StringIO
import os

# Simulate incoming CSV from Kinesis Firehose delivery
csv_data = """transaction_id,account_id,amount,currency,timestamp,status
txn-001,ACC-0001,1500.00,ZAR,2024-06-01 09:15:33,COMPLETED
txn-002,ACC-0002,87000.00,ZAR,2024-06-01 09:22:11,COMPLETED
txn-003,ACC-0001,250.00,ZAR,2024-06-02 14:05:02,COMPLETED
txn-004,ACC-0003,12500.00,USD,2024-06-02 16:44:55,PENDING"""

df = pd.read_csv(StringIO(csv_data))

# Transform: parse timestamp, extract date parts for partitioning
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['year'] = df['timestamp'].dt.year.astype(str)
df['month'] = df['timestamp'].dt.month.astype(str).str.zfill(2)
df['is_high_value'] = df['amount'] > 50000

print("=" * 60)
print("FINTRIST BANK - CSV TO PARQUET ETL")
print("=" * 60)
print()
print("DataFrame Info:")
print(df.dtypes)
print()
print(df.head())
print()

# Write to Parquet grouped by year and month
print("Writing Parquet files:")
for (year, month), group in df.groupby(['year', 'month']):
    path = f'fintrust_processed/year={year}/month={month}/transactions.parquet'
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Drop partition columns before writing (they're in the path)
    output_df = group.drop(columns=['year', 'month'])
    output_df.to_parquet(path, engine='pyarrow', index=False)
    print(f'  Written: {path} ({len(group)} rows)')

print()
print("ETL complete.")