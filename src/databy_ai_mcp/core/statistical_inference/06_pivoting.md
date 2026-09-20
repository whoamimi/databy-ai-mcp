---
source_repo: https://github.com/whoamimi/pyspark-statistical-inference.git
source_commit: db970f3bc3dec59147f327b066e07f43d61d09da
source_branch: master
source_path: 06_pivoting.ipynb
source_url: https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/06_pivoting.ipynb
generated_at: 2026-09-20T03:46:55+00:00
generated_by: scripts/notebooks_to_md.py
---

> Converted from [`06_pivoting.ipynb`](https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/06_pivoting.ipynb) in [https://github.com/whoamimi/pyspark-statistical-inference.git](https://github.com/whoamimi/pyspark-statistical-inference.git) at commit `db970f3bc3de`. Edit the notebook in the submodule, not this file — re-run `scripts/notebooks_to_md.py` to refresh it.

**_pySpark Basics: Pivoting Data_**

_by Jeff Levy (jlevy@urban.org)_

_Last Updated: 5 Aug 2016, Spark v2.0_

_Abstract: This guide will discuss the differences between pivoting and reshaping, and illustrate what capabilities exist within Spark._

_Main operations used: `groupBy`, `pivot`, `sum`_

***

# Reshaping

In pySpark pivoting involves an aggregation.  If what you're looking for is reshaping, where a dataset is turned from wide to long or vice versa without the loss of any information, then that is not currently *explicitly* implemented in Spark.  As we will show at the end however, **it is possible to make the `pivot` function work like a reshape from long to wide**, but not in reverse.  It is possible to "melt" a dataset from wide to long, but it would require the writing of a loop to do it manually, which we do not demonstrate here.

The likely reason for this lack of functionality is that it's an incredibly costly operation; if you've performed it in Stata or SAS, for example, it probably took a while to compute even on a small dataset.  Doing it on very large data that is distributed across many nodes would involve a lot of shuffling and duplicating.  

**It is also important to note that many of the results you might be looking for out of a reshape can be accomplished via other, more efficient means,** such as `groupby`, particularly if your goal is various types of summary statistics.  So while we can accomplish a reshape in some cases, if your data is very large it's best to think about ways to avoid having to completely restructure it.

# Pivoting

To illustrate how pivoting works, we create a simple dataset to experiment with:

```
from pyspark.sql import Row

row = Row("state", "industry", "hq", "jobs")

df = sc.parallelize(
    [
        row("MI", "auto", "domestic", 716),
        row("MI", "auto", "foreign", 123),
        row("MI", "auto", "domestic", 1340),
        row("MI", "retail", "foreign", 12),
        row("MI", "retail", "foreign", 33),
        row("OH", "auto", "domestic", 349),
        row("OH", "auto", "foreign", 101),
        row("OH", "auto", "foreign", 77),
        row("OH", "retail", "domestic", 45),
        row("OH", "retail", "foreign", 12),
    ]
).toDF()
```

```
df.show()
```

    +-----+--------+--------+----+
    |state|industry|      hq|jobs|
    +-----+--------+--------+----+
    |   MI|    auto|domestic| 716|
    |   MI|    auto| foreign| 123|
    |   MI|    auto|domestic|1340|
    |   MI|  retail| foreign|  12|
    |   MI|  retail| foreign|  33|
    |   OH|    auto|domestic| 349|
    |   OH|    auto| foreign| 101|
    |   OH|    auto| foreign|  77|
    |   OH|  retail|domestic|  45|
    |   OH|  retail| foreign|  12|
    +-----+--------+--------+----+
    


Pivot operations must always be preceeded by a groupBy operation.  In our first case we will simply pivot to show total domestic versus foreign jobs in each of our two states:

```
df_pivot1 = df.groupby("state").pivot("hq", values=["domestic", "foreign"]).sum("jobs")
```

```
df_pivot1.show()
```

    +-----+--------+-------+
    |state|domestic|foreign|
    +-----+--------+-------+
    |   MI|    2056|    168|
    |   OH|     394|    190|
    +-----+--------+-------+
    


**Note that the `values=['domestic', 'foreign']` part of the pivot method is optional.**  If we do not supply a list then pySpark will attempt to infer the values by looking through the pivot column we specified, but naturally that requires more processing than if we specify its contents up front.  It's important `values` is specified correctly however; **pySpark will not look to see if you've left any possible values out, and will just discard any observations that don't match what you told it to look for.**  If in doubt, it may be better to accept the inefficiency and let pySpark automatically determine them.

As your datasets get larger this sort of optimization becomes more important.  Also note that Spark has a hard limit of 10,000 columns created as a result of a pivot command.

Here's another example, this time pivoting by both `state` and by `industry` by simply changing the groupby criteria:

```
df_pivot = (
    df.groupBy("state", "industry")
    .pivot("hq", values=["domestic", "foreign"])
    .sum("jobs")
)
```

```
df_pivot.show()
```

    +-----+--------+--------+-------+
    |state|industry|domestic|foreign|
    +-----+--------+--------+-------+
    |   OH|  retail|      45|     12|
    |   MI|    auto|    2056|    123|
    |   OH|    auto|     349|    178|
    |   MI|  retail|    null|     45|
    +-----+--------+--------+-------+
    


The `sum` method at the end **can be replaced with other aggregators as necessary**, for example with `avg`.

# Using Pivot to Reshape Long to Wide

Pivot requires an aggregation argument at the end, as we have been using.  However, what if *each row is uniquely defined* by the `groupby` and `pivot` columns?

```
row = Row("state", "industry", "hq", "jobs", "firm")

df = sc.parallelize(
    [
        row("MI", "auto", "domestic", 716, "A"),
        row("MI", "auto", "foreign", 123, "B"),
        row("MI", "auto", "domestic", 1340, "C"),
        row("MI", "retail", "foreign", 12, "D"),
        row("MI", "retail", "foreign", 33, "E"),
        row("OH", "retail", "mixed", 978, "F"),
        row("OH", "auto", "domestic", 349, "G"),
        row("OH", "auto", "foreign", 101, "H"),
        row("OH", "auto", "foreign", 77, "I"),
        row("OH", "retail", "domestic", 45, "J"),
        row("OH", "retail", "foreign", 12, "K"),
        row("OH", "retail", "mixed", 1, "L"),
        row("OH", "auto", "other", 120, "M"),
        row("OH", "auto", "domestic", 96, "A"),
        row("MI", "auto", "foreign", 1117, "A"),
        row("MI", "retail", "mixed", 9, "F"),
        row("MI", "auto", "foreign", 11, "B"),
    ]
).toDF()
```

```
df.show()
```

    +-----+--------+--------+----+----+
    |state|industry|      hq|jobs|firm|
    +-----+--------+--------+----+----+
    |   MI|    auto|domestic| 716|   A|
    |   MI|    auto| foreign| 123|   B|
    |   MI|    auto|domestic|1340|   C|
    |   MI|  retail| foreign|  12|   D|
    |   MI|  retail| foreign|  33|   E|
    |   OH|  retail|   mixed| 978|   F|
    |   OH|    auto|domestic| 349|   G|
    |   OH|    auto| foreign| 101|   H|
    |   OH|    auto| foreign|  77|   I|
    |   OH|  retail|domestic|  45|   J|
    |   OH|  retail| foreign|  12|   K|
    |   OH|  retail|   mixed|   1|   L|
    |   OH|    auto|   other| 120|   M|
    |   OH|    auto|domestic|  96|   A|
    |   MI|    auto| foreign|1117|   A|
    |   MI|  retail|   mixed|   9|   F|
    |   MI|    auto| foreign|  11|   B|
    +-----+--------+--------+----+----+
    


We've now added a unique identifier for each firm, which we will use instead of state and industry as our groupby criteria.  We also expanded the number of values in the `hq` column:

We can now uniquely identify each row observation by the combination of its `firm`, `state` and `industry` entries, then show the different entries for `hq` for that observation as their own columns.  It drops any columns that we don't use anywhere, but if we wanted to keep them we could just include them in the groupby criteria without changing the logic of the operation:

```
df_pivot = (
    df.groupBy("firm", "state", "industry")
    .pivot("hq", values=["domestic", "foreign", "mixed", "other"])
    .sum("jobs")
)
```

```
df_pivot.show()
```

    +----+-----+--------+--------+-------+-----+-----+
    |firm|state|industry|domestic|foreign|mixed|other|
    +----+-----+--------+--------+-------+-----+-----+
    |   D|   MI|  retail|    null|     12| null| null|
    |   I|   OH|    auto|    null|     77| null| null|
    |   G|   OH|    auto|     349|   null| null| null|
    |   J|   OH|  retail|      45|   null| null| null|
    |   C|   MI|    auto|    1340|   null| null| null|
    |   A|   MI|    auto|     716|   1117| null| null|
    |   K|   OH|  retail|    null|     12| null| null|
    |   B|   MI|    auto|    null|    134| null| null|
    |   F|   MI|  retail|    null|   null|    9| null|
    |   E|   MI|  retail|    null|     33| null| null|
    |   M|   OH|    auto|    null|   null| null|  120|
    |   H|   OH|    auto|    null|    101| null| null|
    |   F|   OH|  retail|    null|   null|  978| null|
    |   L|   OH|  retail|    null|   null|    1| null|
    |   A|   OH|    auto|      96|   null| null| null|
    +----+-----+--------+--------+-------+-----+-----+
    


All we're doing is telling it to `sum` each grouping of values, but **each grouping only has a single entry.**  Our data is now reshaped from long to wide.  If we replaced the `sum` operator with `mean` or `max` or `min`, it wouldn't change anything.

**Note one potential problem here:** performing this operation in software like Stata will raise an error if your specified reshape criteria isn't unique.  When using `pivot` like this in pySpark there wouldn't be an error; it would just perform the aggregation.  This may be problematic if it happens and you were not expecting it to, so it may be necessary to write in some validity tests after the operation completes.  
