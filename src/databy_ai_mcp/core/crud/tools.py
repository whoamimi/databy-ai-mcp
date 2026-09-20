"""src/databy_ai_mcp/core/crud/tools.py

Contains CRUD methods.
"""

_DEFAULT_HEADER = False
_DEFAULT_INFERSCHEMA = True
_DEFAULT_TXT_SEP = _DEFAULT_HTML_SEP = _DEFAULT_MD_SEP = "|"


def load_dataset(
    file_url_path: str,
    spark_read_extension: Literal["csv", "xlsx", "html", "txt", "markdown"],
    **kwargs,
):
    """
        load_dataset

        Loads dataset with Spark context client.
        Usage example:
            ```(
                spark.read.format("com.databricks.spark.csv")
                .options(header="False", inferschema="true", sep="|")
                .load("s3://ui-spark-social-science-public/data/Performance_2015Q1.txt")
            )
            ```
        Args:
            file_url_path (str): File dump path URL location in datalake.
            spark_read_extension (Literal[&quot;csv&quot;, &quot;xlsx&quot;, &quot;html&quot;, &quot;txt&quot;, &quot;markdown&quot;]): Defines table reader type.

        Returns:
            (pyspark.sql.dataframe.DataFrame
    ): Loaded parsed table.
    """

    return spark.read.format(file_url_path).options(
        header=kwargs.get("header", _DEFAULT_HEADER),
        inferschema=kwargs.get("inferschema", _DEFAULT_INFERSCHEMA),
        sep=kwargs.get("sep", _DEFAULT_TXT_SEP).load(file_url_path),
    )
