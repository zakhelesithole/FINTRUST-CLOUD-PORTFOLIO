import json
import boto3
import os
from datetime import datetime
from fintrust_migration import (
    classify_instances, get_migration_wave,
    start_task, is_cutover_ready,
    start_task_execution, wait_for_execution,
    get_client
)

def lambda_handler(event, context):
    action = event.get('action')
    wave   = event.get('wave', 1)

    if action == 'classify_and_start':
        return _classify_and_start_dms(wave)
    elif action == 'check_cutover':
        return _check_cutover(event)
    elif action == 'final_sync':
        return _run_final_datasync(event)
    else:
        raise ValueError(f'Unknown action: {action}')

def _classify_and_start_dms(wave):
    print(f"Classifying Wave {wave} Rehost instances...")
    portfolio, untagged = classify_instances()
    rehost_instances = portfolio.get('rehost', [])
    wave_instances = [i for i in rehost_instances if i['wave'] == str(wave)]
    
    if not wave_instances:
        return {"status": "skipped", "message": "No instances found for this wave"}

    print(f"Tagging {len(wave_instances)} instances as in-progress...")
    ec2 = get_client('ec2')
    for inst in wave_instances:
        try:
            ec2.create_tags(
                Resources=[inst['id']],
                Tags=[{'Key': 'migration:status', 'Value': 'in-progress'}]
            )
        except Exception as e:
            print(f"Failed to tag {inst['id']}: {e}")
            
    print("Starting DMS task...")
    task_arn = os.getenv('DMS_TASK_ARN', 'arn:aws:dms:af-south-1:123456789012:task:EXAMPLE')
    try:
        start_task(task_arn, 'resume-processing')
    except Exception as e:
        print(f"DMS start failed: {e}")
        return {"status": "error", "message": str(e)}
        
    return {"status": "started", "instances_tagged": len(wave_instances)}

def _check_cutover(event):
    print("Checking cutover readiness...")
    task_arn = os.getenv('DMS_TASK_ARN', 'arn:aws:dms:af-south-1:123456789012:task:EXAMPLE')
    instance_id = os.getenv('DMS_INSTANCE_ID', 'dms-instance-1')
    
    ready = is_cutover_ready(task_arn, instance_id)
    return {"ready": ready}

def _run_final_datasync(event):
    print("Starting final DataSync run...")
    task_arn = os.getenv('DATASYNC_TASK_ARN', 'arn:aws:datasync:af-south-1:123456789012:task/task-EXAMPLE')
    
    exec_arn = start_task_execution(task_arn)
    if not exec_arn:
        return {"status": "FAILED", "reason": "Could not start execution"}
        
    info = wait_for_execution(exec_arn, poll_seconds=10)
    
    summary = {
        "cutover_timestamp": datetime.utcnow().isoformat(),
        "final_status": info.get('status', 'UNKNOWN'),
        "bytes_transferred": info.get('bytes_transferred', 0),
        "files_transferred": info.get('files_transferred', 0)
    }
    
    print("Writing summary to S3...")
    s3 = get_client('s3')
    try:
        s3.put_object(
            Bucket='fintrust-migration-audit',
            Key=f'cutover/summary-{exec_arn.split("/")[-1]}.json',
            Body=json.dumps(summary, indent=2)
        )
    except Exception as e:
        print(f"S3 write failed: {e}")
        
    return summary

if __name__ == "__main__":
    # Local test block
    print("=" * 60)
    print("MIGRATION ORCHESTRATOR (LOCAL TEST)")
    print("=" * 60)
    test_event = {"action": "check_cutover"}
    try:
        result = lambda_handler(test_event, None)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
