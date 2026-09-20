# src/databy_ai_mcp/server.py

from fastmcp import FastMCP
from .ui.schema import databy_forms, databy_file_inputs, DatabySessionApp

mcp = FastMCP("Databy AI MCP")
# mcp.add_provider(*databy_file_inputs, namespace="input_file")
# mcp.add_provider(*databy_forms, namespace="input_metadata")
mcp.add_tool(tool=DatabySessionApp)

if __name__ == "__main__":
    mcp.run()
