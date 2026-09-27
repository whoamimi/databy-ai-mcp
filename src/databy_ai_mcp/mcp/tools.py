# src/databy_ai_mcp/mcp/tools.py

import base64
import tempfile
from pathlib import Path

from fastmcp import Context, FastMCP
from fastmcp.apps.file_upload import FileUpload

from ..core.profiler import build_report, load_dataframe, summarize_dataframe
from ..logging_config import get_logger

logger = get_logger(__name__)

#: Full HTML reports run to hundreds of KB — too large to inline as a tool
#: result — so they're written here and only the path is returned.
_REPORTS_DIR = Path(tempfile.gettempdir()) / "databy-ai-mcp" / "profiles"


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
    def databy_profile_dataset(name: str, ctx: Context) -> dict:
        """Profile a previously uploaded file and summarize its schema.

        Upload the file first through the file upload UI (list_files /
        read_file confirm it landed), then call this with the uploaded
        filename. Returns row/column counts, per-column dtypes, and
        missing-value counts, plus the path to a full HTML profiling
        report — the full report itself is far too large (hundreds of KB)
        to return as a tool result, so only its path comes back here.
        """

        logger.info("profiling uploaded file %r", name)
        raw = _read_uploaded_bytes(file_upload, name, ctx)
        df = load_dataframe(name, raw)

        report = build_report(df, title=name)
        _REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        report_path = _REPORTS_DIR / f"{Path(name).stem}.html"
        report_path.write_text(report.to_html())

        summary = summarize_dataframe(df)
        summary["report_path"] = str(report_path)
        return summary
