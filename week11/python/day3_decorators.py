import time
import logging
from functools import wraps

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# =========================================================
# 1. Timer Decorator
# =========================================================
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} completed in {elapsed:.4f}s")
        return result
    return wrapper

# =========================================================
# 2. Retry Decorator (with arguments)
# =========================================================
def retry(max_attempts=3, delay_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    wait = delay_seconds * (2 ** attempt)
                    logging.warning(f"Attempt {attempt+1}/{max_attempts} failed: {e}. Retrying in {wait}s")
                    time.sleep(wait)
            raise last_error
        return wrapper
    return decorator

# =========================================================
# 3. Log Call Decorator
# =========================================================
def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned: {result}")
        return result
    return wrapper

# =========================================================
# 4. Memoize (Cache) Decorator
# =========================================================
def memoize(func):
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"Returning cached result for {args}")
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

# =========================================================
# 5. Validate Types Decorator
# =========================================================
def validate_types(**expected_types):
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            for param, expected in expected_types.items():
                if param in kwargs and not isinstance(kwargs[param], expected):
                    raise TypeError(f"'{param}' must be {expected.__name__}, got {type(kwargs[param]).__name__}")
            return func(**kwargs)
        return wrapper
    return decorator


# =========================================================
# TESTING
# =========================================================
@timer
@retry(max_attempts=2, delay_seconds=1)
def fetch_api_data(endpoint):
    print(f"Fetching {endpoint}...")
    raise Exception("Transient Network Error")

@memoize
@log_call
def slow_db_query(account_id):
    time.sleep(1)
    return {"account_id": account_id, "balance": 5000}

@validate_types(account_id=int, amount=float)
def process_transaction(account_id, amount):
    return f"Processed R{amount} for account {account_id}"

if __name__ == "__main__":
    print("=== Testing Retry + Timer (Stacked) ===")
    try:
        fetch_api_data("/api/v1/transactions")
    except Exception as e:
        print(f"Final failure: {e}")
        
    print("\n=== Testing Memoize + Log ===")
    slow_db_query(account_id=101)
    slow_db_query(account_id=101) # Should hit cache
    
    print("\n=== Testing Type Validation ===")
    print(process_transaction(account_id=101, amount=500.00))
    try:
        process_transaction(account_id="101", amount=500.00)
    except TypeError as e:
        print(f"Validation caught: {e}")
