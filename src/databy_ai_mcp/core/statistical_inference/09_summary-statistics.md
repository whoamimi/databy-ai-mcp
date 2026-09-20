---
source_repo: https://github.com/whoamimi/pyspark-statistical-inference.git
source_commit: db970f3bc3dec59147f327b066e07f43d61d09da
source_branch: master
source_path: 09_summary-statistics.ipynb
source_url: https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/09_summary-statistics.ipynb
generated_at: 2026-09-20T03:46:55+00:00
generated_by: scripts/notebooks_to_md.py
---

> Converted from [`09_summary-statistics.ipynb`](https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/09_summary-statistics.ipynb) in [https://github.com/whoamimi/pyspark-statistical-inference.git](https://github.com/whoamimi/pyspark-statistical-inference.git) at commit `db970f3bc3de`. Edit the notebook in the submodule, not this file — re-run `scripts/notebooks_to_md.py` to refresh it.

**_pySpark Basics: Summary Statistics_**

_by Jeff Levy (jlevy@urban.org)_

_Last Updated: 8 Aug 2016, Spark v2.0_

_Abstract: Here we will cover several common ways to summarize data.  Many of these methods have been dicussed in other tutorials in different contexts._

_Main operations used: `describe`, `skewness`, `kurtosis`, `collect`, `select`_

***

First we will load the same csv data we've been using in many other tutorials, then pare it down to a manageable subset for ease of use:

```python
df = spark.read.csv('s3://ui-spark-social-science-public/data/Performance_2015Q1.txt', header=False, inferSchema=True, sep='|')
```

```python
df = df[['_c0', '_c2', '_c3', '_c4', '_c5', '_c6']]
```

```python
df.show(5)
```

    +------------+-----+-----+----+---+---+
    |         _c0|  _c2|  _c3| _c4|_c5|_c6|
    +------------+-----+-----+----+---+---+
    |100002091588|OTHER|4.125|null|  0|360|
    |100002091588| null|4.125|null|  1|359|
    |100002091588| null|4.125|null|  2|358|
    |100002091588| null|4.125|null|  3|357|
    |100002091588| null|4.125|null|  4|356|
    +------------+-----+-----+----+---+---+
    only showing top 5 rows
    


Note that the format `_c0`, `_c1`, `...`, `_cN` is the default column names Spark uses if your data doesn't come with headers.  For more on this, and renaming them, see the pySpark tutorial named *basics 1.ipynb*

# Describe

The first thing we'll do is use the `describe` method to get some basics.  Note that **describe will return a new dataframe** with the parameters, so we'll assign the results to a new variable and then call `show` on it:

```python
df_described = df.describe()
df_described.show()
```

    +-------+--------------------+--------------------+-------------------+------------------+------------------+-----------------+
    |summary|                 _c0|                 _c2|                _c3|               _c4|               _c5|              _c6|
    +-------+--------------------+--------------------+-------------------+------------------+------------------+-----------------+
    |  count|             3526154|              382039|            3526154|           1580402|           3526154|          3526154|
    |   mean|5.503885995001908E11|                null|  4.178168090219519|234846.78065481762| 5.134865351881966|354.7084951479714|
    | stddev|2.596112361975214...|                null|0.34382335723646673|118170.68592261661|3.3833930336063465| 4.01181251079202|
    |    min|        100002091588|  CITIMORTGAGE, INC.|               2.75|              0.85|                -1|              292|
    |    max|        999995696635|WELLS FARGO BANK,...|              6.125|        1193544.39|                34|              480|
    +-------+--------------------+--------------------+-------------------+------------------+------------------+-----------------+
    


Aside from the five included in `describe`, there are a handful of other built-in aggregators that can be applied to a column.  Here we'll apply the `skewness` function to column `_c3`:

```python
from pyspark.sql.functions import skewness, kurtosis
from pyspark.sql.functions import var_pop, var_samp, stddev, stddev_pop, sumDistinct, ntile
df.select(skewness('_c3')).show()
```

    +------------------+
    |     skewness(_c3)|
    +------------------+
    |0.5197993394959904|
    +------------------+
    


# Expanding the Describe Output

One convenient thing we might want to do is put all our summary statistics together in one spot - in essence, expand the output from `describe`.  Below I'll go into a short example:

```python
from pyspark.sql import Row

columns = df_described.columns  #list of column names: ['summary', '_c0', '_c3', '_c4', '_c5', '_c6']
funcs   = [skewness, kurtosis]  #list of functions we want to include (imported earlier)
fnames  = ['skew', 'kurtosis']  #a list of strings describing the functions in the same order

def new_item(func, column):
    """
    This function takes in an aggregation function and a column name, then applies the aggregation to the
    column, collects it and returns a value.  The value is in string format despite being a number, 
    because that matches the output of describe.
    """
    return str(df.select(func(column)).collect()[0][0])

new_data = []
for func, fname in zip(funcs, fnames):
    row_dict = {'summary':fname}  #each row object begins with an entry for "summary"
    for column in columns[1:]:
        row_dict[column] = new_item(func, column)
    new_data.append(Row(**row_dict))  #using ** tells Python to unpack the entries of the dictionary
    
print(new_data)
```

    [Row(_c0='-0.00183847089866', _c2='None', _c3='0.519799339496', _c4='0.758411576756', _c5='0.286480156084', _c6='-2.69765201567', summary='skew'), Row(_c0='-1.19900726351', _c2='None', _c3='0.126057726847', _c4='0.576085602656', _c5='0.195187780089', _c6='24.7237858944', summary='kurtosis')]


This code iterates through the entries in `funcs` and `fnames` together, then builds a new row object following the format of the standard `describe` output.  You can see from the output that it looks nearly identical to the output of `collect` when applied to a dataframe:

```python
df_described.collect()
```




    [Row(summary=u'count', _c0=u'3526154', _c2=u'382039', _c3=u'3526154', _c4=u'1580402', _c5=u'3526154', _c6=u'3526154'),
     Row(summary=u'mean', _c0=u'5.503885995001908E11', _c2=None, _c3=u'4.178168090219519', _c4=u'234846.78065481762', _c5=u'5.134865351881966', _c6=u'354.7084951479714'),
     Row(summary=u'stddev', _c0=u'2.5961123619752148E11', _c2=None, _c3=u'0.34382335723646673', _c4=u'118170.68592261661', _c5=u'3.3833930336063465', _c6=u'4.01181251079202'),
     Row(summary=u'min', _c0=u'100002091588', _c2=u'CITIMORTGAGE, INC.', _c3=u'2.75', _c4=u'0.85', _c5=u'-1', _c6=u'292'),
     Row(summary=u'max', _c0=u'999995696635', _c2=u'WELLS FARGO BANK, N.A.', _c3=u'6.125', _c4=u'1193544.39', _c5=u'34', _c6=u'480')]



Although the columns are out of order within the rows; this is because we built them from a dictionary, and dictionary entries in Python are inherently unordered.  We will fix that below.

The next step is to join the two sets of data into one, in order to make a modified `describe` output that includes skew and kurtosis.  The same method could be used to include any other aggregations desired.

```python
new_describe = sc.parallelize(new_data).toDF()           #turns the results from our loop into a dataframe
new_describe = new_describe.select(df_described.columns) #forces the columns into the same order

expanded_describe = df_described.unionAll(new_describe)  #merges the new stats with the original describe
expanded_describe.show()
```

    +--------+--------------------+--------------------+-------------------+------------------+------------------+-----------------+
    | summary|                 _c0|                 _c2|                _c3|               _c4|               _c5|              _c6|
    +--------+--------------------+--------------------+-------------------+------------------+------------------+-----------------+
    |   count|             3526154|              382039|            3526154|           1580402|           3526154|          3526154|
    |    mean|5.503885995001908E11|                null|  4.178168090219519|234846.78065481762| 5.134865351881966|354.7084951479714|
    |  stddev|2.596112361975214...|                null|0.34382335723646673|118170.68592261661|3.3833930336063465| 4.01181251079202|
    |     min|        100002091588|  CITIMORTGAGE, INC.|               2.75|              0.85|                -1|              292|
    |     max|        999995696635|WELLS FARGO BANK,...|              6.125|        1193544.39|                34|              480|
    |    skew|   -0.00183847089866|                None|     0.519799339496|    0.758411576756|    0.286480156084|   -2.69765201567|
    |kurtosis|      -1.19900726351|                None|     0.126057726847|    0.576085602656|    0.195187780089|    24.7237858944|
    +--------+--------------------+--------------------+-------------------+------------------+------------------+-----------------+
    


And now we have our expanded `describe` output.

```python

```
