import pytest
from src.services.model_registry import ModelRegistryClient, ModelNotFoundError, STATIC_MODELS


@pytest.fixture
def registry():
    client = ModelRegistryClient(base_url="http://mock-registry")
    client._cache = {m["id"]: m for m in STATIC_MODELS}
    return client


class TestModelRegistryClient:
    def test_list_models_returns_all(self, registry):
        models = registry.list_models()
        assert len(models) == len(STATIC_MODELS)

    def test_get_known_model(self, registry):
        model = registry.get_model("llama3-8b-ft-v2")
        assert model["id"] == "llama3-8b-ft-v2"

    def test_get_unknown_model_raises(self, registry):
        with pytest.raises(ModelNotFoundError):
            registry.get_model("nonexistent-model")

    @pytest.mark.asyncio
    async def test_refresh_falls_back_to_static_on_error(self):
        from unittest.mock import AsyncMock
        registry = ModelRegistryClient(base_url="http://unreachable")
        mock_client = AsyncMock()
        mock_client.get.side_effect = Exception("Connection refused")
        registry._client = mock_client
        await registry._refresh_cache()
        assert len(registry._cache) == len(STATIC_MODELS)
