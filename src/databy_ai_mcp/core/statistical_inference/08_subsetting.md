---
source_repo: https://github.com/whoamimi/pyspark-statistical-inference.git
source_commit: db970f3bc3dec59147f327b066e07f43d61d09da
source_branch: master
source_path: 08_subsetting.ipynb
source_url: https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/08_subsetting.ipynb
generated_at: 2026-09-20T03:46:55+00:00
generated_by: scripts/notebooks_to_md.py
---

> Converted from [`08_subsetting.ipynb`](https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/08_subsetting.ipynb) in [https://github.com/whoamimi/pyspark-statistical-inference.git](https://github.com/whoamimi/pyspark-statistical-inference.git) at commit `db970f3bc3de`. Edit the notebook in the submodule, not this file — re-run `scripts/notebooks_to_md.py` to refresh it.

**_pySpark Basics: Subsetting Data_**

_by Jeff Levy (jlevy@urban.org)_

_Last Updated: 31 Jul 2017, Spark v2.1_

_Abstract: This guide will go over filtering your data based on a specified criteria in order to get a subset_

_Main operations used: `dtypes`, `take`, `show`, `select`, `drop`, `filter/where`, `sample`_

***

We begin by loading some real data from an S3 bucket (the same data used in the *basics* tutorial), allowing pySpark to auto determine the schema, then take a look at its contents:

```python
df = spark.read.csv('s3://ui-spark-social-science-public/data/Performance_2015Q1.txt', header=False, inferSchema=True, sep='|')
```

```python
df.dtypes
```




    [('_c0', 'bigint'),
     ('_c1', 'string'),
     ('_c2', 'string'),
     ('_c3', 'double'),
     ('_c4', 'double'),
     ('_c5', 'int'),
     ('_c6', 'int'),
     ('_c7', 'int'),
     ('_c8', 'string'),
     ('_c9', 'int'),
     ('_c10', 'string'),
     ('_c11', 'string'),
     ('_c12', 'int'),
     ('_c13', 'string'),
     ('_c14', 'string'),
     ('_c15', 'string'),
     ('_c16', 'string'),
     ('_c17', 'string'),
     ('_c18', 'string'),
     ('_c19', 'string'),
     ('_c20', 'string'),
     ('_c21', 'string'),
     ('_c22', 'string'),
     ('_c23', 'string'),
     ('_c24', 'string'),
     ('_c25', 'string'),
     ('_c26', 'int'),
     ('_c27', 'string')]



```python
df.take(5)
```




    [Row(_c0=100002091588, _c1=u'01/01/2015', _c2=u'OTHER', _c3=4.125, _c4=None, _c5=0, _c6=360, _c7=360, _c8=u'01/2045', _c9=16740, _c10=u'0', _c11=u'N', _c12=None, _c13=None, _c14=None, _c15=None, _c16=None, _c17=None, _c18=None, _c19=None, _c20=None, _c21=None, _c22=None, _c23=None, _c24=None, _c25=None, _c26=None, _c27=None),
     Row(_c0=100002091588, _c1=u'02/01/2015', _c2=None, _c3=4.125, _c4=None, _c5=1, _c6=359, _c7=359, _c8=u'01/2045', _c9=16740, _c10=u'0', _c11=u'N', _c12=None, _c13=None, _c14=None, _c15=None, _c16=None, _c17=None, _c18=None, _c19=None, _c20=None, _c21=None, _c22=None, _c23=None, _c24=None, _c25=None, _c26=None, _c27=None),
     Row(_c0=100002091588, _c1=u'03/01/2015', _c2=None, _c3=4.125, _c4=None, _c5=2, _c6=358, _c7=358, _c8=u'01/2045', _c9=16740, _c10=u'0', _c11=u'N', _c12=None, _c13=None, _c14=None, _c15=None, _c16=None, _c17=None, _c18=None, _c19=None, _c20=None, _c21=None, _c22=None, _c23=None, _c24=None, _c25=None, _c26=None, _c27=None),
     Row(_c0=100002091588, _c1=u'04/01/2015', _c2=None, _c3=4.125, _c4=None, _c5=3, _c6=357, _c7=357, _c8=u'01/2045', _c9=16740, _c10=u'0', _c11=u'N', _c12=None, _c13=None, _c14=None, _c15=None, _c16=None, _c17=None, _c18=None, _c19=None, _c20=None, _c21=None, _c22=None, _c23=None, _c24=None, _c25=None, _c26=None, _c27=None),
     Row(_c0=100002091588, _c1=u'05/01/2015', _c2=None, _c3=4.125, _c4=None, _c5=4, _c6=356, _c7=356, _c8=u'01/2045', _c9=16740, _c10=u'0', _c11=u'N', _c12=None, _c13=None, _c14=None, _c15=None, _c16=None, _c17=None, _c18=None, _c19=None, _c20=None, _c21=None, _c22=None, _c23=None, _c24=None, _c25=None, _c26=None, _c27=None)]



Note that this output looks messy because `take` doesn't format the results, it just shows you the row object with the format *column=value* for each column across a row.  It can be formatted nicely with `show()`, but due to the width of this data it will still look messy.  See below for `show()` in action.

# Subsetting by Columns

One of the simplest subsettings is done by selecting just a few of the columns:

```python
from pyspark.sql.functions import col

df_select = df.select(col('_c0'), col('_c1'), col('_c3'), col('_c9'))
df_select.show(5)
```

    +------------+----------+-----+-----+
    |         _c0|       _c1|  _c3|  _c9|
    +------------+----------+-----+-----+
    |100002091588|01/01/2015|4.125|16740|
    |100002091588|02/01/2015|4.125|16740|
    |100002091588|03/01/2015|4.125|16740|
    |100002091588|04/01/2015|4.125|16740|
    |100002091588|05/01/2015|4.125|16740|
    +------------+----------+-----+-----+
    only showing top 5 rows
    


Note that `show` defaults to showing the first 20 rows, but here we've specified only 5.  There is also a shortcut for this notation that does the same thing but is a little easier to read.  We show both because they both show up frequently in Spark resources:

```python
df_select = df[['_c0', '_c1', '_c3', '_c9']]
df_select.show(5)
```

    +------------+----------+-----+-----+
    |         _c0|       _c1|  _c3|  _c9|
    +------------+----------+-----+-----+
    |100002091588|01/01/2015|4.125|16740|
    |100002091588|02/01/2015|4.125|16740|
    |100002091588|03/01/2015|4.125|16740|
    |100002091588|04/01/2015|4.125|16740|
    |100002091588|05/01/2015|4.125|16740|
    +------------+----------+-----+-----+
    only showing top 5 rows
    


Or we can do the same thing by dropping, which is convenient if we want to keep more columns than we want to drop:

```python
df_drop = df_select.drop(col('_c3'))
```

```python
df_drop.show(5)
```

    +------------+----------+-----+
    |         _c0|       _c1|  _c9|
    +------------+----------+-----+
    |100002091588|01/01/2015|16740|
    |100002091588|02/01/2015|16740|
    |100002091588|03/01/2015|16740|
    |100002091588|04/01/2015|16740|
    |100002091588|05/01/2015|16740|
    +------------+----------+-----+
    only showing top 5 rows
    


# Subsetting by Rows

We often want to subset by rows also, for example by specifying a conditional.  Note that we have to use `.show()` at the end of `.describe()`, because **.describe() returns a new dataframe** with the information.  In many other programs, such as Stata, `describe` returns a formatted table; here, both `summary` and `C6` are actually column names.

```python
df.describe('_c6').show()
```

    +-------+-----------------+
    |summary|              _c6|
    +-------+-----------------+
    |  count|          3526154|
    |   mean|354.7084951479714|
    | stddev| 4.01181251079202|
    |    min|              292|
    |    max|              480|
    +-------+-----------------+
    


```python
df_sub = df.where(df['_c6'] < 358)
```

```python
df_sub.describe('_c6').show()
```

    +-------+------------------+
    |summary|               _c6|
    +-------+------------------+
    |  count|           2598037|
    |   mean|353.15604897081914|
    | stddev|3.5170213056883983|
    |    min|               292|
    |    max|               357|
    +-------+------------------+
    


You can see from the `max` entry for `_c6` that we've cut it off at below 358 now.  Also note that **`where` is an alias for `filter`**; you can use them interchangeably in pySpark.

We can repeat the same proceedure for multiple conditions and columns using standard logical operators:

```python
df_filter = df.where((df['_c6'] > 340) & (df['_c5'] < 4))
```

```python
df_filter.describe('_c6', '_c5').show()
```

    +-------+------------------+------------------+
    |summary|               _c6|               _c5|
    +-------+------------------+------------------+
    |  count|           1254131|           1254131|
    |   mean|358.48713810598736| 1.474693632483369|
    | stddev| 1.378961910349754|1.2067831502138422|
    |    min|               341|                -1|
    |    max|               361|                 3|
    +-------+------------------+------------------+
    


# Random Sampling

And finally, you might want to take a random sample of rows.  This can be particularlly useful, for example, if your data is large enough to require more expensive clusters to be spun up to work with it all, and you want to use a smaller, less expensive cluster to work on a sample.  Once your code is completed, you can then spin up the more expensive cluster and simply apply your code to the full sample

You can pass three arguments into sample: **the first is a boolean, which is True to sample with replacement, False without**.
The second is the **fraction of the dataset to take**, in this case 5%, and the third is an **optional random seed**.  If
you specify any integer here then someone else performing the same random operation that specifies the same seed
will get the same result.  If no seed is passed then the exact random sampling can't be duplicated.

```python
df_sample = df.sample(False, 0.05, 99)
```

```python
df_sample.describe('_c6').show()
```

    +-------+------------------+
    |summary|               _c6|
    +-------+------------------+
    |  count|            176015|
    |   mean|354.69058318893275|
    | stddev| 4.028614501676224|
    |    min|               293|
    |    max|               361|
    +-------+------------------+
    


If you compare this to our original summary stats on unfiltered column C6 from above, you'll see it does a pretty good job maintaining the mean and stddev in a sample of only 5% of the data.  You can then write this to a new file in an S3 bucket and work with it instead of the whole data.
