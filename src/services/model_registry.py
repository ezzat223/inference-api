from typing import Dict, List, Optional
import httpx
from src.core.logging import get_logger

logger = get_logger(__name__)

STATIC_MODELS: List[Dict] = [
    {
        "id": "llama3-8b-ft-v2",
        "backend_url": "http://llama3-backend:8080",
        "max_tokens": 4096,
        "avg_latency_ms": 120,
    },
    {
        "id": "mistral-7b-ft-v1",
        "backend_url": "http://mistral-backend:8080",
        "max_tokens": 8192,
        "avg_latency_ms": 180,
    },
    {
        "id": "gpt2-custom-v3",
        "backend_url": "http://gpt2-backend:8080",
        "max_tokens": 2048,
        "avg_latency_ms": 45,
    },
]


class ModelNotFoundError(Exception):
    pass


class ModelRegistryClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._client: Optional[httpx.AsyncClient] = None
        self._cache: Dict[str, Dict] = {}

    async def connect(self) -> None:
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=5.0)
        await self._refresh_cache()

    async def disconnect(self) -> None:
        if self._client:
            await self._client.aclose()

    async def _refresh_cache(self) -> None:
        try:
            resp = await self._client.get("/models")
            resp.raise_for_status()
            models = resp.json()
            self._cache = {m["id"]: m for m in models}
            logger.info(f"Model registry cache refreshed: {list(self._cache.keys())}")
        except Exception as exc:
            logger.warning(f"Registry unreachable, falling back to static catalogue: {exc}")
            self._cache = {m["id"]: m for m in STATIC_MODELS}

    def list_models(self) -> List[Dict]:
        return list(self._cache.values())

    def get_model(self, model_id: str) -> Dict:
        if model_id not in self._cache:
            raise ModelNotFoundError(f"Model '{model_id}' not found in registry")
        return self._cache[model_id]
