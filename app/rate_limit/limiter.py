import time
from collections import defaultdict

# Simple in-memory sliding window limiter
class RateLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self.requests = defaultdict(list)

    def allow(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.window
        timestamps = self.requests[key]
        self.requests[key] = [t for t in timestamps if t > window_start]

        if len(self.requests[key]) >= self.limit:
            return False

        self.requests[key].append(now)
        return True