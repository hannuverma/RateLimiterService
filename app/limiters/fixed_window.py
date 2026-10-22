from redis.asyncio import Redis
from .base import LuaLimiter

class FixedWindow(LuaLimiter):
    script_name = "fixed_window"
    
    def __init__(self, r: Redis, limit: int, window_ms: int):
        super().__init__(r)
        self.limit, self.window_ms = limit, window_ms
    
    def _args(self, cost):
        return [self.limit, self.window_ms, cost]