from .fixed_window import FixedWindow
from .sliding_counter import SlidingCounter
from .sliding_log import SlidingLog
from .token_bucket import TokenBucket
from redis.asyncio import Redis
from .base import RateLimiter

ALGORITHMS = ("fixed_window", "sliding_log", "sliding_counter", "token_bucket")

def build_limiter(algorithm: str, r: Redis, limit: int, window_ms: int) -> RateLimiter:
    if algorithm == "fixed_window":
        return FixedWindow(r, limit, window_ms)
    elif algorithm == "sliding_log":
        return SlidingLog(r, limit, window_ms)
    elif algorithm == "sliding_counter":
        return SlidingCounter(r, limit, window_ms)
    elif algorithm == "token_bucket":
        return TokenBucket(r, limit, limit / (window_ms / 1000))
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")