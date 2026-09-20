---
source_repo: https://github.com/whoamimi/pyspark-statistical-inference.git
source_commit: db970f3bc3dec59147f327b066e07f43d61d09da
source_branch: master
source_path: 03_merging.ipynb
source_url: https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/03_merging.ipynb
generated_at: 2026-09-20T03:46:55+00:00
generated_by: scripts/notebooks_to_md.py
---

> Converted from [`03_merging.ipynb`](https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/03_merging.ipynb) in [https://github.com/whoamimi/pyspark-statistical-inference.git](https://github.com/whoamimi/pyspark-statistical-inference.git) at commit `db970f3bc3de`. Edit the notebook in the submodule, not this file — re-run `scripts/notebooks_to_md.py` to refresh it.

**_pySpark Basics: Merging and Joining Data_**

_by Jeff Levy (jlevy@urban.org)_

_Last Updated: 31 Jul 2017, Spark v2.1_

_Abstract: This guide will go over the various ways to concatenate two or more dataframes_

_Main operations used: unionAll, join_

***

We begin with some basic setup to import the SQL structure that supports the dataframes we'll be using:

# Stacking Rows with Matching Columns

You may have the same columns in each dataframe and just want to stack one on top of the other, row-wise.  We can make this happen with a helper function, after we first build three simple toy dataframes:

```python
from pyspark.sql import Row

row = Row("name", "pet", "count")

df1 = sc.parallelize([
    row("Sue", "cat", 16),
    row("Kim", "dog", 1),    
    row("Bob", "fish", 5)
    ]).toDF()

df2 = sc.parallelize([
    row("Fred", "cat", 2),
    row("Kate", "ant", 179),    
    row("Marc", "lizard", 5)
    ]).toDF()

df3 = sc.parallelize([
    row("Sarah", "shark", 3),
    row("Jason", "kids", 2),    
    row("Scott", "squirrel", 1)
    ]).toDF()
```

If we just want to stack two of them, we can use `unionAll`:

```python
df_union = df1.unionAll(df2)
```

```python
df_union.show()
```

    +----+------+-----+
    |name|   pet|count|
    +----+------+-----+
    | Sue|   cat|   16|
    | Kim|   dog|    1|
    | Bob|  fish|    5|
    |Fred|   cat|    2|
    |Kate|   ant|  179|
    |Marc|lizard|    5|
    +----+------+-----+
    


The `unionAll` method only allows us to stack two dataframes at a time.  We could do that repeatedly if there were more than one to stack in this way, but we can also use a helper function to make it easier.  

The standard Python command `reduce` applies a function to a list of items in order to "reduce" it down to one output.  With this you can pass as many dataframes as you like into our helper function and they will come out stacked in one:

```python
from pyspark.sql import DataFrame
from functools import reduce

def union_many(*dfs):
    #this function can have as many dataframes as you want passed into it
    #the asterics before the name `dfs` tells Python that `dfs` will be a list
    #containing all of the arguments we pass into union_many when it is called
    
    return reduce(DataFrame.unionAll, dfs)

df_union = union_many(df1, df2, df3)
```

```python
df_union.show()
```

    +-----+--------+-----+
    | name|     pet|count|
    +-----+--------+-----+
    |  Sue|     cat|   16|
    |  Kim|     dog|    1|
    |  Bob|    fish|    5|
    | Fred|     cat|    2|
    | Kate|     ant|  179|
    | Marc|  lizard|    5|
    |Sarah|   shark|    3|
    |Jason|    kids|    2|
    |Scott|squirrel|    1|
    +-----+--------+-----+
    


# Merging Columns by Matching Rows

The other way to merge is by combining columns on certain keys across rows.  If you are familiar with SQL, pySpark )and Pandas for non-distributed data) draws its merging terminology from that.  If you are coming from Stata, this is a generally more intuitive way to think about many-to-one, one-to-one and many-to-many merges.  

After we build our data there are four ways to specify the logic of the operation:

```python
row1 = Row("name", "pet", "count")
row2 = Row("name", "pet2", "count2")

df1 = sc.parallelize([
    row1("Sue", "cat", 16),
    row1("Kim", "dog", 1),    
    row1("Bob", "fish", 5),
    row1("Libuse", "horse", 1)
    ]).toDF()

df2 = sc.parallelize([
    row2("Sue", "eagle", 2),
    row2("Kim", "ant", 179),    
    row2("Bob", "lizard", 5),
    row2("Ferdinand", "bees", 23)
    ]).toDF()
```

First we'll do an `inner join`, which *merges rows that have a match in both dataframes* and **drops** all others.  This is the default type of join, so the `how` argument could be omitted here if you didn't wish to be explicit (being explicit is almost always better, however).  We will merge on the entries in the `name` column, which you can see is the second argument in the method; this can also be a `list` if the merge should happen on more than one matching value:

```python
df1.join(df2, 'name', how='inner').show()
```

    +----+----+-----+------+------+
    |name| pet|count|  pet2|count2|
    +----+----+-----+------+------+
    | Sue| cat|   16| eagle|     2|
    | Bob|fish|    5|lizard|     5|
    | Kim| dog|    1|   ant|   179|
    +----+----+-----+------+------+
    


The "left" dataframe here is `df1`, the "right" dataframe is `df2` - the names simply desribe their relative locations in the line of code.  Notice that the entries for Libuse and Ferdinand are dropped, because they do not appear in *both* dataframes.

An **outer join**, which *uses all rows from both dataframes regardless of matches*, fills in `null` for missing observations.  Using the same two dataframes:

```python
df1.join(df2, 'name', how='outer').show()
```

    +---------+-----+-----+------+------+
    |     name|  pet|count|  pet2|count2|
    +---------+-----+-----+------+------+
    |      Sue|  cat|   16| eagle|     2|
    |Ferdinand| null| null|  bees|    23|
    |      Bob| fish|    5|lizard|     5|
    |      Kim|  dog|    1|   ant|   179|
    |   Libuse|horse|    1|  null|  null|
    +---------+-----+-----+------+------+
    


Libuse and Ferdinand both made it into the output now, but each has `null` values filled in where necessary.

And finally a **left join** uses *all keys from the left dataframe* (in this case `df1`).  Data from the right dataframe only shows up if it matches something in the left:

```python
df1.join(df2, 'name', how='left').show()
```

    +------+-----+-----+------+------+
    |  name|  pet|count|  pet2|count2|
    +------+-----+-----+------+------+
    |   Sue|  cat|   16| eagle|     2|
    |   Bob| fish|    5|lizard|     5|
    |   Kim|  dog|    1|   ant|   179|
    |Libuse|horse|    1|  null|  null|
    +------+-----+-----+------+------+
    


So the entry for Ferdinand was dropped because it has no match in the left dataframe.  

A **right join** would just be the opposte of that, and would drop Libuse but keep Ferdinand with `null` entries where necessary.  A `right` join is equivalent to performing a `left` join but switching the places of `df1` and `df2` in the code block, that is: 

    df2.join(df1, 'name', how='left')

is logically the same as:

    df1.join(df2, 'name', how='right')

```python

```
