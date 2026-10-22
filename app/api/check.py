import math

from fastapi import APIRouter, Depends, HTTPException, Response
from redis.exceptions import RedisError

from ..core.models import CheckRequest, CheckResponse
from ..core.service import InvalidCost, RateLimitService, RuleNotFound
from .deps import get_service

router = APIRouter()


@router.post("/check", response_model=CheckResponse)
async def check(body: CheckRequest, response: Response, service: RateLimitService = Depends(get_service)):
    """Always 200 when the check itself worked: `allowed` says yes/no.
    Returning 429 to the END USER is the calling backend's job, not ours."""
    try:
        result = await service.check(body.rule, body.identifier, body.cost)
    except RuleNotFound:
        raise HTTPException(404, f"unknown rule: {body.rule}")
    except InvalidCost as e:
        raise HTTPException(422, str(e))
    except RedisError:
        raise HTTPException(503, "rate limit store unavailable")  # M4: fail-open/closed per rule

    d, rule = result.decision, result.rule
    response.headers["X-RateLimit-Limit"] = str(rule.limit)
    response.headers["X-RateLimit-Remaining"] = str(d.remaining)
    if not d.allowed:
        response.headers["Retry-After"] = str(math.ceil(d.retry_after_ms / 1000))
    return CheckResponse(
        allowed=d.allowed,
        remaining=d.remaining,
        retry_after_ms=d.retry_after_ms,
        limit=rule.limit,
        rule=rule.name,
    )