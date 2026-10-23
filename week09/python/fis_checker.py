import boto3

fis = boto3.client('fis', region_name='af-south-1')

def summarise_fis_experiments(max_results=10):
    """Print a summary of the most recent FIS experiments."""
    print("=" * 60)
    print("FINTRIST BANK - FIS EXPERIMENTS")
    print("=" * 60)
    
    try:
        experiments = fis.list_experiments().get('experiments', [])
    except Exception as e:
        print(f"Error accessing FIS (might not have permissions or experiments): {e}")
        return

    print(f'Found {len(experiments)} experiments (showing up to {max_results}):')
    print('-' * 80)
    
    if not experiments:
        print("No FIS experiments found in this region.")
        return

    for exp in experiments[:max_results]:
        try:
            detail = fis.get_experiment(id=exp['id'])['experiment']
            short_id = exp['id'][-16:]
            state = detail['state']['status']
            template = detail.get('experimentTemplateId', 'unknown')
            start_time = detail.get('startTime', 'not started')
            stop_cond = (detail.get('stopConditions', [{}])[0].get('value', 'none'))
            
            print(f'ID: ...{short_id} | State: {state:12s} | Template: {template}')
            print(f'  Started: {start_time} | Stop condition: {stop_cond}')
        except Exception as e:
            print(f"Could not fetch details for {exp['id']}: {e}")

if __name__ == "__main__":
    summarise_fis_experiments()
