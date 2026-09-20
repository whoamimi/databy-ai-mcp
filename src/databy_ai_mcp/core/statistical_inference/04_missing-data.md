---
source_repo: https://github.com/whoamimi/pyspark-statistical-inference.git
source_commit: db970f3bc3dec59147f327b066e07f43d61d09da
source_branch: master
source_path: 04_missing-data.ipynb
source_url: https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/04_missing-data.ipynb
generated_at: 2026-09-20T03:46:55+00:00
generated_by: scripts/notebooks_to_md.py
---

> Converted from [`04_missing-data.ipynb`](https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/04_missing-data.ipynb) in [https://github.com/whoamimi/pyspark-statistical-inference.git](https://github.com/whoamimi/pyspark-statistical-inference.git) at commit `db970f3bc3de`. Edit the notebook in the submodule, not this file — re-run `scripts/notebooks_to_md.py` to refresh it.

**_pySpark Basics: Missing Data_**

_by Jeff Levy (jlevy@urban.org)_

_Last Updated: 31 Jul 2017, Spark v2.1_

_Abstract: In this guide we'll look at how to handle null and missing values in pySpark, with a brief discussion of imputation_

_Main operations used: where, isNull, dropna, fillna_

***

We'll load some real data from CSV to work with.  It helps to know in advance how the dataset handles missing values - are they an empty string, or something else?  Most CSVs will use empty strings, but we can't compute anything on a column that is mixed strings and numbers.  The `null` object in pySpark is what we want, and we can tell it when we import the data to replace the value our data uses to denote missing data with it.

```python
df = spark.read.csv('s3://ui-spark-social-science-public/data/Performance_2015Q1.txt', 
                    header=False, inferSchema=True, sep='|', nullValue='')
```

Note that on the `nullValue=''` line, the empty string can be replaced by whatever your dataset uses - this is telling Spark which values in the dataframe it should convert to `null`.

# Exploring Null Values

First let's see how many rows the entire dataframe has:

```python
df.count()
```




    3526154



To explore missing data in pySpark, we need to make sure we're looking in a numerical column - **the system does not insert `null` values into a column that has a string datatype.**  The general point of `null` is so the system knows to skip those rows when doing calculations down a column.  

For example, the mean of the series [3, 4, 2, null, 5] is: 

14 / 4 = 3.5 

not: 

14 / 5 = 2.8

In other words, with proper `null` handling, [3, 4, 2, null, 5] is not the same as [3, 4, 2, 0, 5].  This distinction is not relevant in a column of strings.

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



For our practice purposes it doesn't matter what this data actually is, so we'll arbitrarily select a numerical column:

```python
df.where( df['_c12'].isNull() ).count()
```




    3510294



This command takes the form `df.where(___).count()` where the blank is replaced with the desired condition - or in a sentance, *"Count the dataframe where `___` is True".*  In the code I used some extra spaces in between the brackets just to make this stand out - Python ignores extra horizonal space nested in commands like that.  So here we're counting how many rows have `null` values in column `_c12`.

Note that if we left the `count()` method off the end then **it would return an actual dataframe of all rows where column `C12` is `null`.**  So if you wanted more than just the count you could explore that subset.

When we compare the null count to our earlier command, `df.count()`, we can see that column `C12` is mostly null values - there are 15,860 actual values in here, out of 3,526,154 rows.  A common need when exploring a dataset might be to check _all_ our numeric rows for null values.  However, the `isNull()` method can only be called on a column, not an entire dataframe, so I'll write a convenient Python function to do this for us with some comments to explain each step:

```python
def count_nulls(df):
    null_counts = []          #make an empty list to hold our results
    for col in df.dtypes:     #iterate through the column data types we saw above, e.g. ('C0', 'bigint')
        cname = col[0]        #splits out the column name, e.g. 'C0'    
        ctype = col[1]        #splits out the column type, e.g. 'bigint'
        if ctype != 'string': #skip processing string columns for efficiency (can't have nulls)
            nulls = df.where( df[cname].isNull() ).count()
            result = tuple([cname, nulls])  #new tuple, (column name, null count)
            null_counts.append(result)      #put the new tuple in our result list
    return null_counts

null_counts = count_nulls(df)
```

```python
null_counts
```




    [('_c0', 0),
     ('_c3', 0),
     ('_c4', 1945752),
     ('_c5', 0),
     ('_c6', 0),
     ('_c7', 1),
     ('_c9', 0),
     ('_c12', 3510294),
     ('_c26', 3526153)]



A quick note about Python programming in general, for those who may be new(er) to the language: **one of the core precepts of Python is that most code needs to be _read_ even more often than it needs to be _run_.**  For the purpose of clairty I spread the code in that last function out vertically far more than was strictly necessary.  This bit of code would do the exact same thing:

```python
"""
null_counts = []
for col in df.dtypes:
    if col[1] != 'string':
        null_counts.append(tuple([col[0], df.where(df[col[0]].isNull()).count()])))
""";
```

But despite accomplishing the same thing in 4 lines instead of 8, it could be argued that it violates the rules of Python style by looking like an unreadable jumble.  Much more on this can be found in the official Python PEP8 style guide, located at:

https://www.python.org/dev/peps/pep-0008/

If you'll be writing much Python code it's definitely worth looking over.  Note, however, that pySpark frequently violates its guidelines.

# Dropping Null Values

There are three things we can do with our `null` values now that we know what's in our dataframe.  We can **ignore them**, we can **drop them**, or we can **replace them**.  Remember, pySpark dataframes are immutable, so we can't actually change the original dataset.  All operations return an entirely new dataframe, though we can tell it to overwrite the existing one with `df = df.some_operation()` which ends up functionaly equivalent.

```python
df_drops = df.dropna(how='all', subset=['_c4', '_c12', '_c26'])
```

```python
df_drops.count()
```




    1580403



The `df.dropna()` method has two arguments here:  `how` can equal `'any'` or `'all'`; the first drops a row if _any_ value in it is `null`, the second drops a row only if _all_ values are.  

The `subset` argument takes a list of columns that you want to look in for `null` values.  It does not actually subset the dataframe; it just checks in those three columns, then drops the row for the entire dataframe if that subset meets the criteria.  This can be left off if it should check all columns for `null`.

So we can see above that once we drop all rows that have `null` values in columns `_c4`, `_c12` and `_c26`, we're left with 1,580,403 rows out of the original 3,526,154 we saw when we called `count` on the whole dataframe.

Note: There is a third argument that `dropna()` can take; the `thresh` argument sets a threshold for the number of `null` entries in a row before it drops it.  It is set to an integer that **specifies how many non-null arguments the row must have; if it has less than that figure it drops the row.**  If you specify this argument as we do below, it returns a dataframe where any row with less than 2 non-null values in the specified subset are dropped:

```python
df_drops2 = df.dropna(thresh=2, subset=['_c4', '_c12', '_c26'])
```

```python
df_drops2.count()
```




    15860



This leaves us with a lot less columns than the `how='all'` version, which is what we would expect.  In the first a row must have *all three columns* as `null` to be dropped; in the second only *any one of the three* must be null to be dropped.

# Replacing Null Values

```python
df_fill = df.fillna(0, subset=['_c12'])
```

The above line goes through all of column `_c12` and replaces `null` values with the value we specified, in this case a zero.  To verify we re-run the command on our new dataframe to count nulls that we used above:

```python
df_fill.where( df_fill['_c12'].isNull() ).count()
```




    0



We see it replaced all 3,510,294 nulls we found earlier.  The first term in `fillna()` can be most any type and any value, and the subset list can be left off if the fill should be applied to all columns (though be sure the dtype is consistent with what is already in that column).  Note that `df.replace(a, b)` does this same thing, only you specify `a` as the value to be replaced and `b` as the replacement.  It also accepts the optional subset list, but does not take advantage of optimized null handling.

# Imputation

There are many methods for imputing missing data based upon the values around those missing.  This includes, for example, moving average windows and fitting local linear models.  In pySpark, most of these methods will be handled by _window functions_, which you can read more about here:

    https://databricks.com/blog/2015/07/15/introducing-window-functions-in-spark-sql.html
    
These methods go beyond what we'll cover in this tutorial, though they may be covered in a future tutorial.

```python

```
