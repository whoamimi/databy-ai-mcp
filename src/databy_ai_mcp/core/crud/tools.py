"""src/databy_ai_mcp/core/crud/tools.py


Spark-based dataset loading helpers."""

from io import StringIO
from pathlib import Path
from typing import Any, Literal

import pandas as pd
from pyspark.sql import DataFrame, SparkSession

SparkFormat = Literal["csv", "json", "parquet", "orc", "text"]


def load_dataset(
    spark: SparkSession,
    file_url_path: str,
    data_format: SparkFormat,
    **options: Any,
) -> DataFrame:
    """Load a Spark-supported dataset format."""
    return spark.read.format(data_format).options(**options).load(file_url_path)


def load_excel(
    spark: SparkSession,
    file_url_path: str,
    **kwargs: Any,
) -> DataFrame:
    """Load a local Excel file through pandas."""
    pandas_df = pd.read_excel(Path(file_url_path), **kwargs)
    return spark.createDataFrame(pandas_df)


def load_markdown_table(
    spark: SparkSession,
    file_url_path: str,
) -> DataFrame:
    """Load the first Markdown table from a local file."""
    markdown = open(file_url_path, encoding="utf-8").read()
    pandas_df = pd.read_csv(
        StringIO(markdown),
        sep="|",
        skipinitialspace=True,
    )

    pandas_df = pandas_df.dropna(axis=1, how="all")
    pandas_df.columns = [str(column).strip() for column in pandas_df.columns]

    return spark.createDataFrame(pandas_df)


def load_html_table(
    spark: SparkSession,
    file_url_path: str,
    **kwargs,
) -> DataFrame:
    """Load the first HTML table from a local file."""
    tables = pd.read_html(file_url_path, **kwargs)

    if not tables:
        raise ValueError(f"No HTML tables found in {file_url_path!r}")

    return spark.createDataFrame(tables[0])
