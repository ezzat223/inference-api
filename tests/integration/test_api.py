import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.main import app
from src.services.model_registry import STATIC_MODELS


@pytest.fixture
def client():
    mock_registry = MagicMock()
    mock_registry.list_models.return_value = STATIC_MODELS
    mock_registry.get_model.return_value = STATIC_MODELS[0]
    app.state.model_registry = mock_registry
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


class TestHealthEndpoints:
    def test_liveness(self, client):
        resp = client.get("/healthz")
        assert resp.status_code == 200

    def test_readiness_with_models(self, client):
        resp = client.get("/readyz")
        assert resp.status_code == 200

    def test_readiness_no_models(self, client):
        app.state.model_registry.list_models.return_value = []
        resp = client.get("/readyz")
        assert resp.status_code == 503


class TestModelsEndpoint:
    def test_list_models(self, client):
        resp = client.get("/v1/models")
        assert resp.status_code == 200
        assert resp.json()["object"] == "list"


class TestCompletionsEndpoint:
    def test_model_not_found(self, client):
        from src.services.model_registry import ModelNotFoundError
        app.state.model_registry.get_model.side_effect = ModelNotFoundError("not found")
        resp = client.post(
            "/v1/chat/completions",
            json={"model": "nonexistent", "messages": [{"role": "user", "content": "hi"}]},
        )
        assert resp.status_code == 404
