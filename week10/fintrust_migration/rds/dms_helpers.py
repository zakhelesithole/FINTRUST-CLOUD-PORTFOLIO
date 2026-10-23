import boto3
import time
from datetime import datetime, timezone, timedelta
from ..utils.sessions import get_client

def get_task_status(task_arn):
    dms = get_client('dms')
    try:
        resp = dms.describe_replication_tasks(
            Filters=[{'Name': 'replication-task-arn', 'Values': [task_arn]}]
        )
    except Exception as e:
        return {"error": str(e)}
        
    tasks = resp.get('ReplicationTasks', [])
    if not tasks:
        raise ValueError(f'Task not found: {task_arn}')
        
    task = tasks[0]
    return {
        'arn': task['ReplicationTaskArn'],
        'identifier': task['ReplicationTaskIdentifier'],
        'status': task['Status'],
        'stats': task.get('ReplicationTaskStats', {}),
        'stop_reason': task.get('StopReason'),
    }

def wait_for_status(task_arn, target_status, timeout_seconds=1800):
    start = time.time()
    while True:
        info = get_task_status(task_arn)
        if "error" in info:
            print(f"Error: {info['error']}")
            return None
            
        current = info['status']
        print(f'[{time.strftime("%H:%M:%S")}] Status: {current}')
        if current == target_status:
            return info
        if current in {'failed', 'error'}:
            raise RuntimeError(f'Task failed. Stop reason: {info["stop_reason"]}')
        if time.time() - start > timeout_seconds:
            raise TimeoutError(f'Timeout after {timeout_seconds}s waiting for {target_status}')
        time.sleep(30)

def start_task(task_arn, start_type='resume-processing'):
    dms = get_client('dms')
    dms.start_replication_task(
        ReplicationTaskArn=task_arn,
        StartReplicationTaskType=start_type
    )
    return wait_for_status(task_arn, 'running')

def get_cdc_latency(replication_instance_id, task_identifier, lookback_minutes=5):
    cw = get_client('cloudwatch')
    now = datetime.now(timezone.utc)

    def _get_metric(metric_name):
        try:
            resp = cw.get_metric_statistics(
                Namespace='AWS/DMS',
                MetricName=metric_name,
                Dimensions=[
                    {'Name': 'ReplicationInstanceIdentifier', 'Value': replication_instance_id},
                    {'Name': 'ReplicationTaskIdentifier', 'Value': task_identifier},
                ],
                StartTime=now - timedelta(minutes=lookback_minutes),
                EndTime=now,
                Period=60,
                Statistics=['Maximum']
            )
            points = resp.get('Datapoints', [])
            if not points:
                return None
            latest = sorted(points, key=lambda x: x['Timestamp'])[-1]
            return latest['Maximum']
        except Exception:
            return None

    source_lag = _get_metric('CDCLatencySource')
    target_lag = _get_metric('CDCLatencyTarget')

    return {
        'cdc_latency_source_sec': source_lag,
        'cdc_latency_target_sec': target_lag,
        'cutover_safe': (source_lag is not None) and (source_lag < 30),
        'checked_at': now.isoformat()
    }

def is_cutover_ready(task_arn, replication_instance_id):
    """Checks if task is running and source latency is < 30s."""
    status = get_task_status(task_arn)
    if "error" in status:
        return False
    latency = get_cdc_latency(replication_instance_id, status['identifier'])
    return (
        status['status'] == 'running' and
        latency['cutover_safe']
    )
