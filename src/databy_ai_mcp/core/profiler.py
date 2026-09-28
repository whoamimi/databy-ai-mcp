# src.databy_ai_mcp.core.profiler

from data_profiling import ProfileReport

from ..utils.logging import get_logger
from .crud.db import get_spark

logger = get_logger(__name__)


def profile_dataset(session_id: str, **kwargs):
    """
    profile_dataset.

    Uses ydata-dataset library to generate detailed schema profile report in HTML format. Use this at the initial stage of cleaning session.

    Reference
        https://github.com/Data-Centric-AI-Community/fg-data-profiling/blob/master/examples/integrations/databricks/ydata-profiling%20in%20Databricks.ipynb
    """

    logger.info("profiling dataset for session %s", session_id)

    spark = get_spark()
    df = spark.table(session_id)

    report = ProfileReport(
        df,
        title=session_id,
        # data_profiling's typeset inference (typeset.infer_type) isn't wired
        # to its Spark backend, so infer_dtypes=True raises a multimethod
        # DispatchError; False falls back to reading types off the Spark
        # schema directly, which is the supported path for Spark input.
        infer_dtypes=kwargs.get("infer_dtypes", False),
        # The Spark scatter-matrix path assumes every interacting column is
        # numeric and errors on the rest, so continuous interactions are off
        # by default here.
        interactions={"continuous": kwargs.get("interactions", False)},
        # missing_bar's Spark implementation casts every column to double to
        # check for NaNs, which fails on non-numeric columns; leave missing
        # diagrams off by default and let callers opt in for numeric-only data.
        missing_diagrams={
            "bar": kwargs.get("missing_diagrams", False),
            "matrix": kwargs.get("missing_diagrams", False),
            "heatmap": kwargs.get("missing_diagrams", False),
        },
        correlations={
            "auto": {"calculate": False},
            "pearson": {"calculate": True},
            "spearman": {"calculate": True},
        },
    )

    logger.debug("rendering profile report for session %s to HTML", session_id)

    # alternatively, report.to_json()
    return report.to_html()
