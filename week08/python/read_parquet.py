import pandas as pd

print("=" * 60)
print("READ PARQUET FILE")
print("=" * 60)
print()

df_check = pd.read_parquet(
    'fintrust_processed/year=2024/month=06/transactions.parquet',
    engine='pyarrow'
)

print("Column types:")
print(df_check.dtypes)
print()
print("Data:")
print(df_check)
print()
print(f"Rows: {len(df_check)}, Columns: {len(df_check.columns)}")