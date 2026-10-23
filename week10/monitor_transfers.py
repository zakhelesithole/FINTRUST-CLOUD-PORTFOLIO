import time
from fintrust_migration.s3.sync_helpers import start_task_execution, get_execution_status

def monitor_nightly_transfers(task_arns):
    """
    Starts and monitors multiple DataSync tasks simultaneously.
    """
    print("Starting all DataSync tasks...")
    executions = {}
    for arn in task_arns:
        exec_arn = start_task_execution(arn)
        if exec_arn:
            executions[exec_arn] = {"task_arn": arn, "status": "STARTING"}
        else:
            executions[f"FAILED_{arn}"] = {"task_arn": arn, "status": "FAILED"}

    if not executions:
        print("No tasks were started successfully.")
        return {}

    print("\nPolling executions (this will take a few seconds in test mode)...")
    
    # In a real environment, this would be a `while True` loop until all finish.
    # For testing, we will just poll 3 times.
    max_polls = 3
    poll_count = 0
    
    while poll_count < max_polls:
        all_done = True
        print(f"\n--- Poll {poll_count + 1} ---")
        print(f"{'Execution ARN (short)':<25} {'Status':<12} {'GB Transferred':<15}")
        print("-" * 55)
        
        for exec_arn, info in executions.items():
            if info['status'] in ['SUCCESS', 'ERROR']:
                continue
                
            all_done = False
            status_info = get_execution_status(exec_arn)
            
            executions[exec_arn]['status'] = status_info['status']
            gb = status_info.get('bytes_transferred', 0) / (1024**3)
            short_exec = exec_arn[-20:] if len(exec_arn) > 20 else exec_arn
            
            print(f"...{short_exec:<22} {status_info['status']:<12} {gb:.2f} GB")
            
            if status_info['status'] in ['SUCCESS', 'ERROR']:
                executions[exec_arn]['status'] = status_info['status']
                
        if all_done:
            print("\nAll tasks completed!")
            break
            
        poll_count += 1
        if poll_count < max_polls:
            time.sleep(2) # Short sleep for testing

    return executions

if __name__ == "__main__":
    print("=" * 60)
    print("FINTRIST BANK - DATASYNC TRANSFER MONITOR")
    print("=" * 60)
    
    # Use dummy ARNs for testing since you likely don't have active tasks
    test_arns = [
        "arn:aws:datasync:af-south-1:123456789012:task/task-11111111",
        "arn:aws:datasync:af-south-1:123456789012:task/task-22222222"
    ]
    
    monitor_nightly_transfers(test_arns)
