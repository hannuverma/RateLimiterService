from fastapi import APIRouter, HTTPException, Request

router = APIRouter()


@router.get("/health")
async def healthz(request: Request):
    try:
        await request.app.state.redis.ping()
    except Exception:
        raise HTTPException(503, "redis unreachable")
    return {"status": "ok"}
