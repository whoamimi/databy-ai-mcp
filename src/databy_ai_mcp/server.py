# src/databy_ai_mcp/server.py

from fastmcp import FastMCP

from .ui.form import create_session
from .utils.logging import get_logger

logger = get_logger(__name__)

mcp = FastMCP("Databy AI MCP", stateless_app=True)
# mcp.add_provider(*databy_file_inputs, namespace="input_file")
# mcp.add_provider(*databy_forms, namespace="input_metadata")
mcp.add_tool(tool=create_session)
logger.info("starting %s", mcp.name)

if __name__ == "__main__":
    mcp.run()
