import pytest
from pydantic import ValidationError
from src.models.schemas import CompletionRequest, Message


class TestCompletionRequest:
    def test_valid_request(self):
        req = CompletionRequest(
            model="llama3-8b-ft-v2",
            messages=[Message(role="user", content="Hello")],
        )
        assert req.model == "llama3-8b-ft-v2"
        assert req.stream is False

    def test_temperature_bounds(self):
        with pytest.raises(ValidationError):
            CompletionRequest(
                model="llama3-8b-ft-v2",
                messages=[Message(role="user", content="Hi")],
                temperature=3.0,
            )

    def test_max_tokens_bounds(self):
        with pytest.raises(ValidationError):
            CompletionRequest(
                model="llama3-8b-ft-v2",
                messages=[Message(role="user", content="Hi")],
                max_tokens=99999,
            )

    def test_default_values(self):
        req = CompletionRequest(
            model="gpt2-custom-v3",
            messages=[Message(role="user", content="Test")],
        )
        assert req.n == 1
        assert req.stream is False
        assert req.stop is None
