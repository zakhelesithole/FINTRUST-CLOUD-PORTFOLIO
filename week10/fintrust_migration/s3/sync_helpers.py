import time
import os
from ..utils.sessions import get_client

def start_task_execution(task_arn):
    """Starts a DataSync task execution."""
    ds = get_client('datasync')
    try:
        resp = ds.start_task_execution(TaskArn=task_arn)
        return resp['TaskExecutionArn']
    except Exception as e:
        print(f"Error starting task {task_arn}: {e}")
        return None

def get_execution_status(execution_arn):
    """Gets the status of a DataSync task execution."""
    ds = get_client('datasync')
    try:
        resp = ds.describe_task_execution(TaskExecutionArn=execution_arn)
        return {
            'status':          resp['Status'],
            'files_prepared':  resp.get('Result', {}).get('PrepareDuration'),
            'files_transferred': resp.get('FilesTransferred', 0),
            'bytes_transferred': resp.get('BytesTransferred', 0),
            'files_verified':  resp.get('FilesVerified', 0),
            'result':          resp.get('Result', {})
        }
    except Exception as e:
        return {'status': 'ERROR', 'error': str(e), 'bytes_transferred': 0, 'files_transferred': 0}

def wait_for_execution(execution_arn, poll_seconds=60):
    """Polls execution until it finishes."""
    terminal = {'SUCCESS', 'ERROR'}
    while True:
        info = get_execution_status(execution_arn)
        status = info['status']
        transferred_gb = info.get('bytes_transferred', 0) / (1024**3)
        print(f'[{time.strftime("%H:%M:%S")}] {status} | '
              f'{info.get("files_transferred", 0)} files | {transferred_gb:.2f} GB')
        if status in terminal:
            return info
        time.sleep(poll_seconds)

MBPS_TO_BYTES = 1_000_000 / 8

def set_task_throttle(task_arn, bandwidth_mbps):
    """Updates DataSync task bandwidth throttle."""
    ds = get_client('datasync')
    if bandwidth_mbps == 0:
        throttle = 0          # 0 = unlimited
    else:
        throttle = int(bandwidth_mbps * MBPS_TO_BYTES)

    try:
        ds.update_task(
            TaskArn=task_arn,
            Options={'BytesPerSecond': throttle}
        )
        label = f'{bandwidth_mbps} Mbps' if throttle else 'unlimited'
        print(f'Task throttle updated to {label} ({throttle} bytes/sec)')
    except Exception as e:
        print(f"Error updating throttle: {e}")

def lambda_handler(event, context):
    """EventBridge Scheduler handler for dynamic throttling."""
    task_arn = os.getenv('DATASYNC_TASK_ARN', 'arn:aws:datasync:af-south-1:123456789012:task/task-123')
    mode     = event.get('mode', 'daytime')

    throttle_map = {
        'daytime':  500,   # 07:00-22:00 SAST
        'overnight': 9000, # 22:00-07:00 SAST
    }
    bandwidth = throttle_map.get(mode, 500)
    set_task_throttle(task_arn, bandwidth)
    return {'statusCode': 200, 'bandwidth_mbps': bandwidth, 'mode': mode}
