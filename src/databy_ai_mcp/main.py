# src/databy_ai_mcp/main.py

from .logging_config import configure_logging, get_logger

logger = get_logger(__name__)


def main() -> None:
    """App's entry point.

    The one place logging is initialised — do it before importing the server so
    that registration-time logs from the MCP layer are captured too.
    """

    configure_logging()

    from .server import mcp

    logger.info("starting %s", mcp.name)

    return mcp.run()
