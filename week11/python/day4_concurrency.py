import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

# =========================================================
# 1. ThreadPoolExecutor (Best for I/O-bound like boto3 API calls)
# =========================================================
def query_dynamodb_table(table_name):
    """Simulates a 200ms DynamoDB query."""
    time.sleep(0.2) 
    return f"Data from {table_name}"

def run_sequential(tables):
    print("Running Sequentially...")
    start = time.perf_counter()
    results = []
    for table in tables:
        results.append(query_dynamodb_table(table))
    elapsed = time.perf_counter() - start
    print(f"Sequential completed in {elapsed:.2f}s")
    return elapsed

def run_threaded(tables):
    print("\nRunning with ThreadPoolExecutor...")
    start = time.perf_counter()
    results = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        # Submit all tasks
        future_to_table = {executor.submit(query_dynamodb_table, t): t for t in tables}
        
        # Process as they complete
        for future in as_completed(future_to_table):
            results.append(future.result())
            
    elapsed = time.perf_counter() - start
    print(f"Threaded completed in {elapsed:.2f}s")
    return elapsed

# =========================================================
# 2. asyncio (Best for high-concurrency web requests)
# =========================================================
async def fetch_api_async(endpoint):
    """Simulates a 200ms async HTTP request."""
    await asyncio.sleep(0.2)
    return f"Data from {endpoint}"

async def run_async(endpoints):
    print("\nRunning with asyncio...")
    start = time.perf_counter()
    
    # Create tasks
    tasks = [fetch_api_async(e) for e in endpoints]
    
    # Run concurrently
    results = await asyncio.gather(*tasks)
    
    elapsed = time.perf_counter() - start
    print(f"Async completed in {elapsed:.2f}s")
    return elapsed

# =========================================================
# Main Execution
# =========================================================
if __name__ == "__main__":
    print("=" * 60)
    print("FINTRIST BANK - CONCURRENCY BENCHMARK")
    print("=" * 60)
    
    # 40 tables at 200ms each = 8 seconds sequentially
    tables = [f"Table_{i}" for i in range(1, 41)]
    
    seq_time = run_sequential(tables)
    thread_time = run_threaded(tables)
    
    print(f"\nSpeedup (Sequential vs Threading): {seq_time / thread_time:.1f}x faster")
    
    # Async test
    endpoints = [f"/api/account/{i}" for i in range(1, 101)] # 100 requests
    async_time = asyncio.run(run_async(endpoints))
