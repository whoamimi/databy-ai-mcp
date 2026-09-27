"""Databy AI MCP — FastMCP server exposing Databy AI's data-engineering tools.

``main`` is the console-script target declared in pyproject.toml
(``databy-ai-mcp = "databy_ai_mcp:main"``).
"""

from .logging_config import configure_logging, get_logger
from .main import main

__all__ = ["configure_logging", "get_logger", "main"]
