from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from src.models.schemas import CompletionRequest, CompletionResponse
from src.services.inference import InferenceService
from src.services.model_registry import ModelNotFoundError

router = APIRouter()


def get_inference_service(request: Request) -> InferenceService:
    return InferenceService(model_registry=request.app.state.model_registry)


@router.post("/chat/completions", response_model=CompletionResponse)
async def chat_completions(
    body: CompletionRequest,
    service: InferenceService = Depends(get_inference_service),
):
    try:
        if body.stream:
            return StreamingResponse(
                service.stream(body),
                media_type="text/event-stream",
                headers={"X-Accel-Buffering": "no"},
            )
        return await service.complete(body)
    except ModelNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Backend error: {exc}")
