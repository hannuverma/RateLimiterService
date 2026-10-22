from fastapi import Request

from ..core.service import RateLimitService


def get_service(request: Request) -> RateLimitService:
    return request.app.state.service
