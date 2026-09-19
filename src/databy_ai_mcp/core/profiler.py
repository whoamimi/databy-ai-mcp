# /
#
# ---
# Last Modified:	Tuesday, 15th September 2026 5:22:09 am
# Created Date:	Tuesday, 15th Sep 2026 5:22:09 am
# Copyright (c) 2026 Mimi (https://github.com/whoamimi)

from data_profiling import ProfileReport
from pyspark.sql import SparkSession


def get_data_profile(session_id: str, **kwargs):
    """
    get_data_profile.

    Reference
        https://github.com/Data-Centric-AI-Community/fg-data-profiling/blob/master/examples/integrations/databricks/ydata-profiling%20in%20Databricks.ipynb
    """

    spark = SparkSession.builder.appName("databy-ai-mcp").getOrCreate()
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

    # alternatively, report.to_json()
    return report.to_html()
