from redis.asyncio import Redis
from .base import LuaLimiter
 
 
class TokenBucket(LuaLimiter):
    script_name = "token_bucket"
 
    def __init__(self, r: Redis, capacity: int, refill_per_sec: float):
        super().__init__(r)
        self.capacity, self.rate = capacity, refill_per_sec
 
    def _args(self, cost):
        return [self.capacity, self.rate, cost]