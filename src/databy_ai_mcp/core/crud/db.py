# src/databy_ai_mcp/core/crud/db.py
# Spark session builders & Database client connectors.

from pyspark.sql import SparkSession

DEFAULT_APP_NAME = "databy-ai-mcp"


def get_spark() -> SparkSession:
    """
    get_spark

    A shared SparkSession is appropriate for concurrent read/query requests, but avoid changing shared session state inside individual tools:
        # Avoid in request handlers:
        spark.conf.set("some.key", value)
        spark.catalog.createTempView(...)
        spark.udf.register(...)

    Returns:
        SparkSession: New spark session.
    """

    return SparkSession.builder.appName("databy-ai-mcp").getOrCreate()
