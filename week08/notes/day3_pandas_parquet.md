# Week 8 Day 3 - Data Engineering with Python

## Why Columnar Formats Matter

Athena charges per terabyte of data scanned. The format determines query cost.

| Characteristic | CSV | Parquet |
|----------------|-----|---------|
| Storage layout | Row-based | Column-based |
| Athena scan for one column | Full table | One column only |
| Compression ratio | 1x | 5-10x |
| Schema embedded | No | Yes |
| Null handling | Empty string | Typed null |

**Key insight:** Parquet can reduce Athena costs by 10x or more.

## Installing Dependencies

```bash
pip install pandas pyarrow boto3 s3fs
