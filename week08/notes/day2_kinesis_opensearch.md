# Week 8 Day 2 - Real-time Data Pipelines with Kinesis and OpenSearch

## Kinesis Data Streams

### Key Producer Operations

| Operation | Use Case | Limit |
|-----------|----------|-------|
| `put_record` | Single record | 1 MB per record |
| `put_records` | Batch up to 500 records | 500 records or 5 MB |

### The PartitionKey Decision

The PartitionKey determines which shard receives the record:

- **Ordering**: Same partition key always goes to the same shard
- **Hot shards**: If one key dominates, one shard gets all load

For FinTrust, use `account_id` as the partition key to guarantee ordering per account.

### Shard Capacity

| Capacity | Per Shard |
|----------|-----------|
| Write | 1 MB/s (1000 records/s) |
| Read | 2 MB/s |

8 shards = 8 MB/s write, 16 MB/s read.

## OpenSearch

### Connecting to OpenSearch

```python
from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{'host': 'search-...es.amazonaws.com', 'port': 443}],
    http_auth=('admin', 'password'),
    use_ssl=True,
    verify_certs=True
)
