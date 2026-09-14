# /
#
# ---
# Last Modified:	Tuesday, 15th September 2026 5:22:09 am
# Created Date:	Tuesday, 15th Sep 2026 5:22:09 am
# Copyright (c) 2026 Mimi (https://github.com/whoamimi)

from pyspark.sql import SparkSession
spark = SparkSession.builder().master("local[1]")
    .appName("SparkByExamples.com")
    .getOrCreate()

df = spark.read.csv("{insert-file-path}")

df.printSchema()

a = ProfileReport(df)
a.to_file("spark_profile.html")


from data_profiling import ProfileReport
