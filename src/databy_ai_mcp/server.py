# /Users/mimiphan/mimeus-app/databy-ai/databy-ai-mcp/src/databy_ai_mcp/server.py
#
# ------------------------------------------------------------------------------
# Last Modified:	Wednesday, 26th August 2026 9:58:11 pm
# Created Date:	Wednesday, 26th Aug 2026 9:58:06 pm
# Copyright (c) 2026 Mimi P. (https://github.com/whoamimi)

from fastmcp import FastMCP
from .ui.schema import databy_forms, databy_file_inputs

mcp = FastMCP("Databy AI MCP")
mcp.add_provider(*databy_file_inputs, namespace="input_file")
mcp.add_provider(*databy_forms, namespace="input_metadata")

if __name__ == "__main__":
    mcp.run()
