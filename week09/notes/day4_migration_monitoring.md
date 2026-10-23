# Week 9 Day 4 - Migration Monitoring with Python

## DMS (Database Migration Service)
- Service name in boto3 is `database-migration-service`, not `dms`.
- **Task Statuses:** `creating`, `ready`, `starting`, `running`, `stopped`, `failed`, `deleting`.
- Terminal states: `stopped`, `failed`, `deleting`. Stop polling when reached.
- For CDC (Change Data Capture) tracking, check `describe_table_statistics()` for `ValidationErrored` and `FullLoadErrorRows`.

## AWS Snow Family
| Device | Usable Capacity | Purpose |
|--------|-----------------|---------|
| Snowcone HDD | 8 TB | Edge/disconnected |
| Snowcone SSD | 14 TB | Edge with faster storage |
| Snowball Edge Storage | 80 TB | Large storage migrations |
| Snowball Edge Compute | 28 TB | Edge compute (EC2) |
| Snowmobile | 100,000 TB | Exabyte scale (10PB+) |

**FinTrust Scenario:** 3,000 TB archive takes 38 Snowball Edge Storage devices. Over a 1 Gbps internet link, it would take 277 days. Snow takes ~2-3 weeks.

## FIS (Fault Injection Simulator)
- Used to test resilience.
- `list_experiments()`, `get_experiment()`.
- Stop conditions halt the experiment automatically if things go wrong.

## Reflection: FIS Stop Condition for ASG
**Question:** What CloudWatch metric triggers the stop condition for an ASG experiment?
**Answer:** The best metric is `GroupInServiceInstances`. If a random instance is terminated, the ASG should replace it. If the replacement instance fails to pass its health check, `GroupInServiceInstances` will drop below the expected minimum threshold (e.g., < 2 for a Multi-AZ setup). 
The CloudWatch Alarm expression would be:
`IF(GroupInServiceInstances < 2, 1, 0)` evaluated over a period of 5 minutes.
