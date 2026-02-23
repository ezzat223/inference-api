from fastapi import APIRouter, Request
from src.models.schemas import ModelCard, ModelList

router = APIRouter()


@router.get("/models", response_model=ModelList)
async def list_models(request: Request):
    registry = request.app.state.model_registry
    models = registry.list_models()
    return ModelList(data=[ModelCard(id=m["id"]) for m in models])
