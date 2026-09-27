# src/databy_ai_mcp/server.py

from fastmcp import FastMCP
from fastmcp.apps.file_upload import FileUpload
from fastmcp.apps.form import FormInput

from .logging_config import get_logger
from .mcp.tools import register_tools
from .ui.schema import SessionForm, submit_input

logger = get_logger(__name__)

mcp = FastMCP("Databy AI MCP")

file_upload = FileUpload(
    name="Upload File",
    max_file_size=10 * 1024 * 1024,
    title="File Upload",
    description=(
        "Drop files to upload them to the server. "
        "The model can then read and analyze them "
        "without using the context window."
    ),
    drop_label="Drop files here. Acceptable filetype extensions: csv, xlsx, parquet, html.",
)

mcp.add_provider(FormInput(model=SessionForm, on_submit=submit_input))
mcp.add_provider(file_upload)
register_tools(mcp, file_upload)

logger.debug("registered providers and tools on %s", mcp.name)

if __name__ == "__main__":
    # Running this module directly is an application entry point too, so it
    # owns logging setup exactly like main.main() does.
    from .logging_config import configure_logging

    configure_logging()
    logger.info("starting %s", mcp.name)
    mcp.run()
