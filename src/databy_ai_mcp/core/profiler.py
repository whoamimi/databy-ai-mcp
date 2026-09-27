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


def build_report(df: pd.DataFrame, title: str) -> ProfileReport:
    """Build a data-profiling report for ``df``.

    Reference
        https://github.com/Data-Centric-AI-Community/fg-data-profiling
    """

    return ProfileReport(df, title=title)


def summarize_dataframe(df: pd.DataFrame) -> dict:
    """Return a small, tool-result-sized summary of ``df``.

    The full profiling report can run into hundreds of KB of HTML, which
    exceeds an agent's tool-result token budget. This is what
    ``databy_profile_dataset`` returns instead of the raw report.
    """

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": {col: int(n) for col, n in df.isna().sum().items()},
    }
