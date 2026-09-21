# Week 7 Day 4 - Event-Driven Transaction Scoring Pipeline

## Pipeline Architecture

## Components Created

| Component | Name | Purpose |
|-----------|------|---------|
| SQS Queue | fintrust-payment-events.fifo | Receives payment events from API |
| SNS Topic | fintrust-transaction-alerts | Sends alerts to subscribers |
| Lambda Function | fintrust-fraud-scorer | Scores transactions, alerts on high risk |

## SQS FIFO Queue

- Name must end in `.fifo`
- `MessageGroupId` ensures ordering per account
- `MessageDeduplicationId` prevents duplicates
- `ContentBasedDeduplication` can auto-generate dedup IDs

## Fraud Scoring Logic

| Factor | Condition | Score Added |
|--------|-----------|-------------|
| Amount > 50,000 | Large transaction | +40 |
| Amount > 10,000 | Medium transaction | +20 |
| Amount > 1,000 | Small transaction | +5 |
| Non-ZAR currency | Cross-border | +20 |
| Risk keywords | crypto, wire, urgent, casino | +15 |
| Maximum score | | 100 |

## Risk Threshold

- Default: 75
- Configurable via environment variable
- Alerts published when score >= threshold

## Client vs Resource

| Interface | Use For |
|-----------|---------|
| Client | SQS, SNS, EventBridge (low-level API) |
| Resource | S3, DynamoDB, EC2 (higher-level OO) |

## Key Learnings

### FIFO Queue
- Ensures order per MessageGroupId
- Deduplication prevents duplicate processing
- Required for financial transactions

### Lambda Event Source Mapping
- Pulls messages from SQS automatically
- Configurable batch size
- Returns partial failures for retry

### SNS Publishing
- Topic ARN from environment variable
- Message attributes for filtering
- Email subscription for alerts

## Day 4 Checklist
- [x] SQS FIFO queue created
- [x] SNS topic created and subscribed
- [x] Fraud scorer Lambda created
- [x] Event source mapping configured
- [x] Test message sent
- [x] CloudWatch logs verified
- [x] Email alert received
- [x] Uploaded to GitHub
