# src/databy_ai_mcp/mcp/tools.py

import base64

from fastmcp import Context, FastMCP
from fastmcp.apps.file_upload import FileUpload

from ..core.profiler import profile_dataset
from ..logging_config import get_logger

logger = get_logger(__name__)


def _read_uploaded_bytes(file_upload: FileUpload, name: str, ctx: Context) -> bytes:
    """Fetch the full raw bytes of a file uploaded through ``file_upload``.

    FileUpload.on_read() truncates binary files to a short base64 preview
    for the model-facing read_file tool, which isn't enough to profile a
    dataset. Read straight from the provider's session-scoped store instead.

    NOTE: ``_get_scope_key``/``_store`` are private FileUpload internals —
    there is no public API for a full, untruncated read as of this SDK
    version. If FileUpload ever grows one, switch to it instead of this.
    """

    scope = file_upload._get_scope_key(ctx)
    entry = file_upload._store.get(scope, {}).get(name)
    if entry is None:
        available = list(file_upload._store.get(scope, {}))
        raise ValueError(f"File {name!r} not found. Uploaded files: {available}")
    return base64.b64decode(entry["data"])


def register_tools(mcp: FastMCP, file_upload: FileUpload) -> None:
    """Register Databy AI's model-facing tools on ``mcp``."""

    @mcp.tool()
    def databy_profile_dataset(name: str, ctx: Context) -> str:
        """Generate an HTML data-profile report for a previously uploaded file.

        Upload the file first through the file upload UI (list_files /
        read_file confirm it landed), then call this with the uploaded
        filename to get a full profiling report rendered as HTML.
        """

        logger.info("profiling uploaded file %r", name)
        raw = _read_uploaded_bytes(file_upload, name, ctx)
        return profile_dataset(name, raw)
