"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    return {"status": "ok", "service": "axiom-lens", "version": "1.0.0"}
