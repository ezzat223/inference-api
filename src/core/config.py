from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    ALLOWED_ORIGINS: List[str] = ["*"]

    MODEL_REGISTRY_URL: str = "http://model-registry:8000"

    MAX_TOKENS_LIMIT: int = 8192
    DEFAULT_MAX_TOKENS: int = 512
    DEFAULT_TEMPERATURE: float = 0.7
    REQUEST_TIMEOUT_SECONDS: int = 120

    ENABLE_STREAMING: bool = True
    ENABLE_BATCH: bool = True


settings = Settings()
