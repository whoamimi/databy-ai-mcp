# /
#
# ---
# Last Modified:	Tuesday, 15th September 2026 5:22:09 am
# Created Date:	Tuesday, 15th Sep 2026 5:22:09 am
# Copyright (c) 2026 Mimi (https://github.com/whoamimi)

import io
from pathlib import Path

import pandas as pd
from data_profiling import ProfileReport

from ..logging_config import get_logger

logger = get_logger(__name__)

_READERS = {
    ".csv": pd.read_csv,
    ".xlsx": pd.read_excel,
    ".xls": pd.read_excel,
    ".parquet": pd.read_parquet,
    ".html": lambda buf: pd.read_html(buf)[0],
}


def load_dataframe(filename: str, raw: bytes) -> pd.DataFrame:
    """Parse an uploaded file's raw bytes into a pandas DataFrame.

    Args:
        filename: Original filename, used to pick a reader by extension.
        raw: Raw file bytes (already base64-decoded).

    Returns:
        The parsed DataFrame.

    Raises:
        ValueError: If the file extension isn't one of the supported types.
    """

    suffix = Path(filename).suffix.lower()
    reader = _READERS.get(suffix)
    if reader is None:
        raise ValueError(
            f"Unsupported file type {suffix!r} for profiling. "
            f"Supported extensions: {sorted(_READERS)}"
        )
    return reader(io.BytesIO(raw))


def profile_dataset(filename: str, raw: bytes) -> str:
    """
    profile_dataset.

    Uses the data-profiling library to generate a detailed schema profile
    report in HTML format for a dropped file. Use this at the initial stage
    of a cleaning session.

    Args:
        filename: Original filename of the uploaded dataset (drives format
            detection — csv, xlsx, xls, parquet, html).
        raw: Raw file bytes, as read from the file upload store.

    Reference
        https://github.com/Data-Centric-AI-Community/fg-data-profiling
    """

    logger.info("profiling uploaded file %r", filename)

    df = load_dataframe(filename, raw)
    report = ProfileReport(df, title=filename)

    logger.debug("rendering profile report for %r to HTML", filename)

    # alternatively, report.to_json()
    return report.to_html()
