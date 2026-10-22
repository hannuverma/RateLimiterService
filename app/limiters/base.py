from abc import ABC, abstractmethod
from redis.asyncio import Redis
from pathlib import Path


LUA_DIR = Path(__file__).parent/"lua"

class Decision:
    allowed: bool
    remaining:int
    retry_after:int

class RateLimiter(ABC):
    
    @abstractmethod
    async def allow(self, key:str, cost:int = 1) -> Decision: ...

class LuaLimiter(RateLimiter):
    script_name: str

    def __init__(self, r: Redis):
        source = (LUA_DIR / f"{self.script_name}.lua").read_text()
        self._script = r.register_script(source)

    def _args(self, cost : int) -> list:
        raise NotImplementedError

    async def allow(self, key:str, cost:int = 1) -> Decision:
        allowed, remaining, retry_after = await self._script(
            keys=[key], 
            args=self._args(cost)
        )
        return Decision(bool(allowed), int(remaining), int(retry_after))

    
