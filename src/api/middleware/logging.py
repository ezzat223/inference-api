import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from src.core.logging import get_logger

logger = get_logger("api.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start = time.monotonic()
        response = await call_next(request)
        elapsed_ms = (time.monotonic() - start) * 1000
        logger.info(
            f"request_id={request_id} method={request.method} "
            f"path={request.url.path} status={response.status_code} "
            f"duration_ms={elapsed_ms:.1f}"
        )
        response.headers["X-Request-ID"] = request_id
        return response
