import boto3
import time
from datetime import datetime

# Note: service name is 'database-migration-service', not 'dms'
dms = boto3.client('database-migration-service', region_name='af-south-1')

def get_task_progress(task_arn):
    """Returns a summary of a DMS replication task's current progress."""
    try:
        response = dms.describe_replication_tasks(
            Filters=[{'Name': 'replication-task-arn', 'Values': [task_arn]}]
        )
    except Exception as e:
        return {"error": str(e)}

    if not response.get('ReplicationTasks'):
        return None

    task = response['ReplicationTasks'][0]
    stats = task.get('ReplicationTaskStats', {})

    return {
        'task_id': task['ReplicationTaskIdentifier'],
        'status': task['Status'],
        'tables_loaded': stats.get('TablesLoaded', 0),
        'tables_loading': stats.get('TablesLoading', 0),
        'tables_errored': stats.get('TablesErrored', 0),
        'tables_queued': stats.get('TablesQueued', 0),
        'full_load_pct': stats.get('FullLoadProgressPercent', 0),
        'elapsed_seconds': stats.get('ElapsedTimeMillis', 0) // 1000,
        'start_time': task.get('ReplicationTaskStartDate', 'not started'),
    }

def monitor_task(task_arn, poll_interval=30, max_polls=3):
    """Poll a DMS task until it reaches a terminal state or max_polls is hit."""
    terminal = {'stopped', 'failed', 'deleting'}
    for i in range(max_polls):
        progress = get_task_progress(task_arn)
        
        if not progress:
            print('Task not found.')
            break
        if "error" in progress:
            print(f"Error checking task: {progress['error']}")
            break
            
        ts = datetime.now().strftime('%H:%M:%S')
        print(f'[{ts}] Status: {progress["status"]} | '
              f'Full load: {progress["full_load_pct"]}% | '
              f'Loaded: {progress["tables_loaded"]} | '
              f'Errored: {progress["tables_errored"]}')
              
        if progress['status'] in terminal:
            print(f'Task reached terminal state: {progress["status"]}')
            break
        
        if i < max_polls - 1:
            time.sleep(poll_interval)

if __name__ == "__main__":
    print("=" * 60)
    print("FINTRIST BANK - DMS MONITOR")
    print("=" * 60)
    print("DMS monitor function ready.")
    print("To test, replace the ARN below with a real task ARN:")
    # Replace with a real task ARN to test
    # monitor_task('arn:aws:dms:af-south-1:123456789012:task:ABCDEFGHIJ12345')
