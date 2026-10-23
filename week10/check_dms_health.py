import boto3
from fintrust_migration.utils.sessions import get_client

def check_all_tasks_health():
    dms = get_client('dms')
    print("=" * 80)
    print("FINTRIST BANK - DMS HEALTH CHECK SUMMARY")
    print("=" * 80)
    
    try:
        paginator = dms.get_paginator('describe_replication_tasks')
        pages = paginator.paginate()
    except Exception as e:
        print(f"Error connecting to DMS: {e}")
        return

    found_any = False
    print(f"{'Identifier':<25} {'Status':<12} {'Source Lag':<12} {'Cutover Ready?':<15}")
    print("-" * 80)

    for page in pages:
        for task in page.get('ReplicationTasks', []):
            found_any = True
            identifier = task['ReplicationTaskIdentifier']
            status = task['Status']
            task_arn = task['ReplicationTaskArn']
            
            # Get the instance ID from the task ARN or definition (simplified for this example)
            # In a real environment, you'd fetch this from the task details
            instance_id = task.get('ReplicationInstanceArn', '').split(':')[-1]
            
            source_lag = "N/A"
            cutover_ready = "No"
            
            if status == 'running' and instance_id:
                from fintrust_migration.rds.dms_helpers import get_cdc_latency
                latency = get_cdc_latency(instance_id, identifier)
                if latency['cdc_latency_source_sec'] is not None:
                    source_lag = f"{latency['cdc_latency_source_sec']}s"
                    cutover_ready = "Yes" if latency['cutover_safe'] else "No (Lag High)"

            print(f"{identifier:<25} {status:<12} {source_lag:<12} {cutover_ready:<15}")

    if not found_any:
        print("No DMS tasks found in this region.")

if __name__ == "__main__":
    check_all_tasks_health()
