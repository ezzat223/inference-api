import logging
import sys
from src.core.config import settings


def setup_logging() -> None:
    log_format = (
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        if settings.APP_ENV == "development"
        else '{"time": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
    )
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format=log_format,
        stream=sys.stdout,
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
