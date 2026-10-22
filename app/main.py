from contextlib import asynccontextmanager
 
from fastapi import FastAPI
from redis.asyncio import Redis
 
from . import config
from .api import check, health
from .core.rules import DEFAULT_RULES, StaticRules
from .core.service import RateLimitService

@asynccontextmanager
async def lifespan(app: FastAPI):
    r = Redis.from_url(config.REDIS_URL, decode_responses=True)
    app.state.redis = r
    app.state.service = RateLimitService(r, StaticRules(DEFAULT_RULES))
    yield
    await r.aclose()

app = FastAPI(title="Rate Limiter Service", lifespan=lifespan)
app.include_router(check.router)
app.include_router(health.router)