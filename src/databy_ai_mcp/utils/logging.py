# src/databy_ai_mcp/utils/logging.py
#
# For a module-level ASGI application, use LOGGING_CONFIG
# For core features, use get_logger

from __future__ import annotations

import logging
import os

PACKAGE_NAME = "databy_ai_mcp"

logging.getLogger(PACKAGE_NAME).addHandler(logging.NullHandler())

LOG_LEVEL = os.getenv("DATABY_MCP_LOG_LEVEL", "DEBUG").upper()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s %(levelprefix)s [%(name)s] %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            "use_colors": None,
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "databy_ai_mcp": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.error": {
            "level": LOG_LEVEL,
        },
        "uvicorn.access": {
            "level": LOG_LEVEL,
            "propagate": True,
        },
    },
}


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a logger under the package namespace."""
    if not name:
        return logging.getLogger(PACKAGE_NAME)

    if name == PACKAGE_NAME or name.startswith(f"{PACKAGE_NAME}."):
        return logging.getLogger(name)

    return logging.getLogger(f"{PACKAGE_NAME}.{name}")
