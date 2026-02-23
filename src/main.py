from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from src.api.routes import completions, health, models
from src.api.middleware.logging import LoggingMiddleware
from src.core.config import settings
from src.core.logging import setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.services.model_registry import ModelRegistryClient
    app.state.model_registry = ModelRegistryClient(base_url=settings.MODEL_REGISTRY_URL)
    await app.state.model_registry.connect()
    yield
    await app.state.model_registry.disconnect()


app = FastAPI(
    title="LLM Inference API",
    description="OpenAI-compatible inference API for fine-tuned LLMs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

app.include_router(health.router, tags=["Health"])
app.include_router(models.router, prefix="/v1", tags=["Models"])
app.include_router(completions.router, prefix="/v1", tags=["Completions"])
