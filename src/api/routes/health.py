from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"


@router.get("/healthz", response_model=HealthResponse)
async def liveness():
    return HealthResponse(status="ok")


@router.get("/readyz", response_model=HealthResponse)
async def readiness(request: Request):
    registry = request.app.state.model_registry
    models = registry.list_models()
    if not models:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="No models available")
    return HealthResponse(status="ready")
