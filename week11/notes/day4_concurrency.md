# Week 11 Day 4 - Python Concurrency

## Python Concurrency Models
Because of the Global Interpreter Lock (GIL), Python can only execute one thread of bytecode at a time. Therefore, choosing the right concurrency model depends on the type of task.

| Approach | Best For | Runs Parallel? | Complexity |
|----------|----------|----------------|------------|
| `ThreadPoolExecutor` | I/O-Bound (API calls, DB queries) | No (GIL), but overlaps wait time | Low |
| `asyncio` | High-concurrency I/O (1000s of sockets) | No (Single thread, event loop) | Medium |
| `multiprocessing` | CPU-Bound (Heavy computation) | Yes (Separate processes, bypasses GIL) | High |

## 1. ThreadPoolExecutor
- Use for `boto3` calls, `requests`, or file reads.
- **`executor.submit()`**: Schedules the task.
- **`as_completed()`**: Yields results as they finish (ideal for progress tracking and error handling).

## 2. asyncio
- Use for massive web scraping or webhooks.
- Requires `async`/`await` syntax.
- **CRITICAL:** Must use async-compatible libraries (e.g., `aiohttp` instead of `requests`, `aiobotocore` instead of `boto3`).
- `asyncio.gather(*tasks)`: Runs a list of coroutines concurrently.

## 3. multiprocessing
- Use for CPU tasks like hashing, image processing, or ML training.
- Data must be picklable to pass between processes.

## Exercise Result
The FinTrust pipeline querying 40 DynamoDB tables sequentially (8 seconds) can be rewritten using `ThreadPoolExecutor` (max_workers=40). It reduces the execution time to ~0.2 seconds, yielding a ~40x speedup.
