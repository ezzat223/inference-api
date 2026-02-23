import time
import uuid
from typing import AsyncGenerator, Dict

import httpx

from src.core.config import settings
from src.core.logging import get_logger
from src.models.schemas import (
    Choice, ChoiceMessage, CompletionChunk, CompletionRequest,
    CompletionResponse, DeltaMessage, StreamChoice, Usage,
)
from src.services.model_registry import ModelRegistryClient, ModelNotFoundError

logger = get_logger(__name__)


def _count_tokens(text: str) -> int:
    return max(1, len(text.split()))


class InferenceService:
    def __init__(self, model_registry: ModelRegistryClient):
        self.registry = model_registry

    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        model = self.registry.get_model(request.model)
        max_tokens = min(
            request.max_tokens or settings.DEFAULT_MAX_TOKENS,
            settings.MAX_TOKENS_LIMIT,
        )
        payload = {
            "messages": [m.model_dump() for m in request.messages],
            "max_tokens": max_tokens,
            "temperature": request.temperature or settings.DEFAULT_TEMPERATURE,
            "top_p": request.top_p or 1.0,
            "stop": request.stop,
            "n": request.n,
        }
        start = time.monotonic()
        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT_SECONDS) as client:
            resp = await client.post(f"{model['backend_url']}/generate", json=payload)
            resp.raise_for_status()

        elapsed_ms = (time.monotonic() - start) * 1000
        logger.info(f"model={request.model} latency_ms={elapsed_ms:.0f}")

        raw = resp.json()
        prompt_tokens = sum(_count_tokens(m.content) for m in request.messages)
        choices = []
        completion_tokens = 0

        for i, choice in enumerate(raw.get("choices", [])):
            content = choice.get("text", "")
            completion_tokens += _count_tokens(content)
            choices.append(Choice(
                index=i,
                message=ChoiceMessage(content=content),
                finish_reason=choice.get("finish_reason", "stop"),
            ))

        return CompletionResponse(
            id=f"chatcmpl-{uuid.uuid4().hex[:12]}",
            model=request.model,
            choices=choices,
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
            ),
        )

    async def stream(self, request: CompletionRequest) -> AsyncGenerator[str, None]:
        model = self.registry.get_model(request.model)
        completion_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
        payload = {
            "messages": [m.model_dump() for m in request.messages],
            "max_tokens": request.max_tokens or settings.DEFAULT_MAX_TOKENS,
            "temperature": request.temperature or settings.DEFAULT_TEMPERATURE,
            "stream": True,
        }
        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT_SECONDS) as client:
            async with client.stream("POST", f"{model['backend_url']}/generate", json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line or line == "data: [DONE]":
                        continue
                    token = line.removeprefix("data: ")
                    chunk = CompletionChunk(
                        id=completion_id,
                        model=request.model,
                        choices=[StreamChoice(index=0, delta=DeltaMessage(content=token))],
                    )
                    yield f"data: {chunk.model_dump_json()}\n\n"
        yield "data: [DONE]\n\n"
