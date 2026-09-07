import time
from functools import wraps

def rate_limit(max_calls, period):
    def decorator(func):
        storage_name = f"__rate_limit_{func.__name__}"

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            now = time.time()

            calls = getattr(self, storage_name, [])
            calls = [t for t in calls if now - t < period]

            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")

            calls.append(now)
            setattr(self, storage_name, calls)

            return func(self, *args, **kwargs)

        return wrapper
    return decorator

# Bug 1- Because calls is assigned within the function, Python treats it as a local variable throughout wrapper. Then, on the right-hand side of that same line, you're trying to read the local variable before it has been assigned, which results in the UnboundLocalError.

# Bug 2- Modify the state tracking by storing timestamps on the instance (self) instead of in a shared closure. The wrapper can use the first argument (self) as the key for rate-limit state.
