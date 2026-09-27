'''
Filename: /Users/mimiphan/mimeus-app/databy-ai/databy-ai-mcp/src/databy_ai_mcp/logging_config.py
Path: /Users/mimiphan/mimeus-app/databy-ai/databy-ai-mcp/src/databy_ai_mcp
Created Date: Monday, September 28th 2026, 12:10:36 am
Author: Mimi Phan

Copyright (c) 2026 Mimeus AI
'''

"""src/databy_ai_mcp/logging_config.py

Single logging entry point for the Databy AI MCP server.

Two rules keep this predictable:

1. **Library modules never configure logging.** They only ask for their own
   module-scoped logger::

       from ..logging_config import get_logger

       logger = get_logger(__name__)

   Importing any part of this package must not mutate global logging state
   beyond attaching a ``NullHandler`` (see below), so embedding this server in
   another application can't have its logging hijacked.

2. **The application entry point configures logging exactly once.** That is
   ``databy_ai_mcp.main.main()`` (and the ``__main__`` guard in
   ``server.py``). :func:`configure_logging` is idempotent and thread-safe, so
   a second call is a no-op rather than a duplicated handler.

Handlers are borrowed from FastMCP's own ``configure_logging`` so the
``databy_ai_mcp.*`` and ``fastmcp.*`` namespaces emit through identically
formatted handlers at a shared level — one visual stream, one threshold.

Everything goes to **stderr**, never stdout: under the MCP stdio transport
stdout is the JSON-RPC channel, and a stray log line there corrupts the
protocol stream.

Level resolution, highest precedence first:
    1. the explicit ``level=`` argument
    2. ``$DATABY_MCP_LOG_LEVEL``
    3. ``fastmcp.settings.log_level`` (i.e. ``$FASTMCP_LOG_LEVEL``, default INFO)

Setting ``FASTMCP_LOG_ENABLED=false`` silences both namespaces.
"""

from __future__ import annotations

import logging
import os
import threading
from typing import Final

import fastmcp
from fastmcp.utilities.logging import configure_logging as _fastmcp_configure_logging

__all__ = ["PACKAGE_LOGGER_NAME", "configure_logging", "get_logger", "is_configured"]

#: Root of this package's logger hierarchy; every module logger hangs off it,
#: so one level/handler change here covers the whole server.
PACKAGE_LOGGER_NAME: Final[str] = "databy_ai_mcp"

#: Logger namespace FastMCP configures for itself on import.
_FASTMCP_LOGGER_NAME: Final[str] = "fastmcp"

LOG_LEVEL_ENV_VAR: Final[str] = "DATABY_MCP_LOG_LEVEL"

_configure_lock = threading.Lock()
_configured = False

# Library-safe default: the package logger has a no-op handler from import time,
# so records raised before configure_logging() neither warn about missing
# handlers nor leak anywhere. configure_logging() replaces it with a real one.
logging.getLogger(PACKAGE_LOGGER_NAME).addHandler(logging.NullHandler())


def get_logger(name: str) -> logging.Logger:
    """Return the module-scoped logger for ``name``, nested under this package.

    Call it as ``get_logger(__name__)``. Passing a dotted module path inside
    this package returns that exact logger; any other name is nested under
    :data:`PACKAGE_LOGGER_NAME` so nothing escapes the package hierarchy.
    """

    if name == PACKAGE_LOGGER_NAME or name.startswith(f"{PACKAGE_LOGGER_NAME}."):
        return logging.getLogger(name)

    return logging.getLogger(f"{PACKAGE_LOGGER_NAME}.{name}")


def _resolve_level(level: str | int | None) -> str | int:
    """Resolve the effective log level; see this module's docstring for order."""

    if level is not None:
        return level

    env_level = os.environ.get(LOG_LEVEL_ENV_VAR)
    if env_level and env_level.strip():
        return env_level.strip().upper()

    return fastmcp.settings.log_level


def configure_logging(
    level: str | int | None = None,
    *,
    include_fastmcp: bool = True,
    force: bool = False,
) -> logging.Logger:
    """Install this package's logging handlers. Safe to call more than once.

    Intended to be called once, from the application entry point. Subsequent
    calls return immediately unless ``force=True`` (useful for tests, which can
    reconfigure without stacking handlers).

    Args:
        level: Explicit level; omit to resolve from the environment/FastMCP.
        include_fastmcp: Also pin the ``fastmcp`` logger to the resolved level,
            so server-framework and application logs share one threshold.
            FastMCP configures that logger itself on import from
            ``FASTMCP_LOG_LEVEL``; this re-aligns it with ours.
        force: Reconfigure even if already configured.

    Returns:
        The package root logger (``databy_ai_mcp``).
    """

    global _configured

    logger = logging.getLogger(PACKAGE_LOGGER_NAME)

    with _configure_lock:
        if _configured and not force:
            return logger

        resolved = _resolve_level(level)

        if not fastmcp.settings.log_enabled:
            # Logging is switched off globally. FastMCP's configure_logging
            # would no-op here and leave the logger at NOTSET, which lets
            # records propagate to whatever the root logger has attached
            # (possibly stdout). Pin it shut ourselves instead.
            logger.propagate = False
            logger.setLevel(resolved)
            _configured = True
            return logger

        # Reuse FastMCP's handler construction so both namespaces get the same
        # stderr handler, formatter and rich-traceback behaviour. It clears
        # existing handlers first, so this replaces our NullHandler and cannot
        # duplicate output on a forced reconfigure.
        _fastmcp_configure_logging(level=resolved, logger=logger)

        if include_fastmcp:
            _fastmcp_configure_logging(
                level=resolved,
                logger=logging.getLogger(_FASTMCP_LOGGER_NAME),
            )

        _configured = True

    logger.debug("logging configured (level=%s, fastmcp=%s)", resolved, include_fastmcp)
    return logger


def is_configured() -> bool:
    """Whether :func:`configure_logging` has already run."""

    return _configured
