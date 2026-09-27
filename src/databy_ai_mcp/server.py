# src/databy_ai_mcp/server.py

from fastmcp import FastMCP

from .logging_config import get_logger
from .ui.schema import DatabySessionApp

logger = get_logger(__name__)

mcp = FastMCP("Databy AI MCP")
# mcp.add_provider(*databy_file_inputs, namespace="input_file")
# mcp.add_provider(*databy_forms, namespace="input_metadata")
mcp.add_tool(tool=DatabySessionApp)

logger.debug("registered tool %r on %s", DatabySessionApp.name, mcp.name)

if __name__ == "__main__":
    # Running this module directly is an application entry point too, so it
    # owns logging setup exactly like main.main() does.
    from .logging_config import configure_logging

    configure_logging()
    logger.info("starting %s", mcp.name)
    mcp.run()
