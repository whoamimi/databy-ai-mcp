---
source_repo: https://github.com/whoamimi/pyspark-statistical-inference.git
source_commit: db970f3bc3dec59147f327b066e07f43d61d09da
source_branch: master
source_path: 05_moving-average-imputation.ipynb
source_url: https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/05_moving-average-imputation.ipynb
generated_at: 2026-09-20T03:46:55+00:00
generated_by: scripts/notebooks_to_md.py
---

> Converted from [`05_moving-average-imputation.ipynb`](https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/05_moving-average-imputation.ipynb) in [https://github.com/whoamimi/pyspark-statistical-inference.git](https://github.com/whoamimi/pyspark-statistical-inference.git) at commit `db970f3bc3de`. Edit the notebook in the submodule, not this file — re-run `scripts/notebooks_to_md.py` to refresh it.

**_pySpark Basics: Moving Average Imputation_**

_by Jeff Levy (jlevy@urban.org)_

_Last Updated: 31 Jul 2017, Spark v2.1_

_**Abstract:** In this guide we will demonstrate pySpark's windowing function by imputing missing values using a moving average._

_**Main operations used:** `window`, `partitionBy`, `orderBy`, `over`, `when`, `otherwise`_

***

Think of windowing as **defining a range around any given row that counts as the window**, then **performing an operation just within that window.**  So if we define our window range as -1 to +1, then it will go over the data and examine every row along with its preceeding and following rows.  If we define it as 0 to +3, it will look at every row and the three following rows.  Obviously for this to make sense **the rows must be in a meaningful order**, and we have to **deliniate any groups within the data.**  That is to say, if we have panel data with 12 monthly observations for all 50 states, and we don't group before we define a window, then a -1 to +1 window might include November and December for one state, then January for the next state.

There are many ways to handle imputing missing data, and many uses for pySpark's windowing function.  We will demonstrate the intersection of these two concepts using a modified version of the dimaonds dataset, where several values in the `'price'` column have been deleted:

```python
df = spark.read.csv(
    "s3://ui-spark-social-science-public/data/diamonds_nulls.csv",
    inferSchema=True,
    header=True,
    sep=",",
    nullValue="",
)
```

```python
df.show()
```

    +-----+---------+-----+-------+-----+-----+-----+----+----+----+
    |carat|      cut|color|clarity|depth|table|price|   x|   y|   z|
    +-----+---------+-----+-------+-----+-----+-----+----+----+----+
    | 0.23|    Ideal|    E|    SI2| 61.5| 55.0|  326|3.95|3.98|2.43|
    | 0.21|  Premium|    E|    SI1| 59.8| 61.0|  326|3.89|3.84|2.31|
    | 0.23|     Good|    E|    VS1| 56.9| 65.0|  327|4.05|4.07|2.31|
    | 0.29|  Premium|    I|    VS2| 62.4| 58.0|  334| 4.2|4.23|2.63|
    | 0.31|     Good|    J|    SI2| 63.3| 58.0|  335|4.34|4.35|2.75|
    | 0.24|Very Good|    J|   VVS2| 62.8| 57.0|  336|3.94|3.96|2.48|
    | 0.24|Very Good|    I|   VVS1| 62.3| 57.0|  336|3.95|3.98|2.47|
    | 0.26|Very Good|    H|    SI1| 61.9| 55.0|  337|4.07|4.11|2.53|
    | 0.22|     Fair|    E|    VS2| 65.1| 61.0|  337|3.87|3.78|2.49|
    | 0.23|Very Good|    H|    VS1| 59.4| 61.0|  338| 4.0|4.05|2.39|
    |  0.3|     Good|    J|    SI1| 64.0| 55.0|  339|4.25|4.28|2.73|
    | 0.23|    Ideal|    J|    VS1| 62.8| 56.0|  340|3.93| 3.9|2.46|
    | 0.22|  Premium|    F|    SI1| 60.4| 61.0|  342|3.88|3.84|2.33|
    | 0.31|    Ideal|    J|    SI2| 62.2| 54.0|  344|4.35|4.37|2.71|
    |  0.2|  Premium|    E|    SI2| 60.2| 62.0|  345|3.79|3.75|2.27|
    | 0.32|  Premium|    E|     I1| 60.9| 58.0|  345|4.38|4.42|2.68|
    |  0.3|    Ideal|    I|    SI2| 62.0| 54.0|  348|4.31|4.34|2.68|
    |  0.3|     Good|    J|    SI1| 63.4| 54.0|  351|4.23|4.29| 2.7|
    |  0.3|     Good|    J|    SI1| 63.8| 56.0|  351|4.23|4.26|2.71|
    |  0.3|Very Good|    J|    SI1| 62.7| 59.0|  351|4.21|4.27|2.66|
    +-----+---------+-----+-------+-----+-----+-----+----+----+----+
    only showing top 20 rows
    


We can also show the subset where the value for `'price'` has been replaced with `null`:

```python
df.where(df["price"].isNull()).show(50)
```

    +-----+---------+-----+-------+-----+-----+-----+----+----+----+
    |carat|      cut|color|clarity|depth|table|price|   x|   y|   z|
    +-----+---------+-----+-------+-----+-----+-----+----+----+----+
    | 0.24|  Premium|    I|    VS1| 62.5| 57.0| null|3.97|3.94|2.47|
    | 0.35|    Ideal|    I|    VS1| 60.9| 57.0| null|4.54|4.59|2.78|
    |  0.7|     Good|    F|    VS1| 59.4| 62.0| null|5.71|5.76| 3.4|
    |  0.7|     Fair|    F|    VS2| 64.5| 57.0| null|5.57|5.53|3.58|
    |  0.7|  Premium|    E|    SI1| 61.2| 57.0| null|5.73|5.68|3.49|
    | 0.73|  Premium|    F|    VS2| 62.5| 57.0| null|5.75| 5.7|3.58|
    | 1.01|    Ideal|    F|    SI1| 62.7| 55.0| null|6.45| 6.4|4.03|
    | 1.03|    Ideal|    H|    SI1| 61.1| 56.0| null| 6.5|6.53|3.98|
    | 1.28|    Ideal|    I|    SI2| 61.7| 59.0| null|6.96|6.92|4.28|
    | 0.37|  Premium|    D|    SI1| 60.4| 59.0| null|4.68|4.62|2.81|
    |  0.5|    Ideal|    J|    VS2| 61.7| 57.0| null|5.09|5.12|3.15|
    | 0.34|    Ideal|    E|    VS1| 61.2| 55.0| null|4.52|4.56|2.77|
    | 0.52|    Ideal|    D|    VS2| 61.8| 55.0| null|5.19|5.23|3.22|
    | 0.71|Very Good|    J|   VVS2| 61.1| 58.0| null| 5.7|5.75| 3.5|
    | 0.76|  Premium|    H|    SI1| 59.8| 57.0| null|5.93|5.91|3.54|
    | 0.58|    Ideal|    F|    VS1| 60.3| 57.0| null|5.47|5.44|3.29|
    |  0.7|Very Good|    E|    VS1| 63.4| 62.0| null|5.64|5.56|3.55|
    | 0.92|  Premium|    D|     I1| 63.0| 58.0| null|6.18|6.13|3.88|
    | 0.88|Very Good|    I|    SI1| 62.5| 56.0| null|6.06|6.19|3.83|
    |  0.7|     Good|    H|   VVS2| 58.9| 61.5| null|5.77|5.84|3.42|
    |  0.7|Very Good|    D|    SI1| 62.8| 60.0| null|5.66|5.68|3.56|
    +-----+---------+-----+-------+-----+-----+-----+----+----+----+
    


# Defining a Window

The first step to windowing is to **define the window parameters.**  We do this by combining three elements: the grouping (`partitionBy`), the ordering (`orderBy`) and the range (`rowsBetween`).  The window we define is then assigned to a variable, which we will use to perform computations.

```python
from pyspark.sql import Window
```

```python
window = Window.partitionBy("cut", "clarity").orderBy("price").rowsBetween(-3, 3)
```

```python
window
```




    <pyspark.sql.window.WindowSpec at 0x7faf3ca68690>



**We now have an object of type `WindowSpec` that knows what the window should look like.  **

The first portion, `partionBy('cut', 'clarity')` is somewhat misleadningly named, as it is not related to *partitions* in Spark, which are segments of the distributed data, roughly analogous to individual computers within the cluster.  It is much more closely related to `groupBy`, as discussed for example in the *basics 2.ipynb* tutorial.  It tells pySpark that the windows should only be computed within each grouping of the columns `'cut'` and `'clarity'`.  Like `groupBy`, `partitionBy` can take one or more criteria.

The second portion, `orderBy('price')` simply sorts the data by price *within each partitionBy column*.

And finally, `rowsBetween(-3, 3)` specifies the size of the window.  In this case it includes seven rows in each window - the current row plus the three before and the three after.

# Operations Over a Window

The next step is to apply this window to an operation, which we can do using the `over` method.  Here we will use `mean` as our aggregator, but you can do this with any valid aggregator function.

```python
from pyspark.sql.functions import mean
```

```python
moving_avg = mean(df["price"]).over(window)
moving_avg
```




    Column<avg(price) OVER (PARTITION BY cut, clarity ORDER BY price ASC NULLS FIRST ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING)>



What this creates is a *column object* that contains the set of SQL instructions needed to create the data.  It hasn't been discussed in these tutorials, but pySpark is capable of taking SQL formatted instructions for most operations, and in the case of windowing, SQL is what underlies the Python code.

**Remember that pySpark dataframes are immutable, so we cannot just fill in missing values.**  Instead we have to create a new column, then recast the dataframe to include it:

```python
df = df.withColumn("moving_avg", moving_avg)
df.show()
```

    +-----+-------+-----+-------+-----+-----+-----+----+----+----+------------------+
    |carat|    cut|color|clarity|depth|table|price|   x|   y|   z|        moving_avg|
    +-----+-------+-----+-------+-----+-----+-----+----+----+----+------------------+
    | 0.73|Premium|    F|    VS2| 62.5| 57.0| null|5.75| 5.7|3.58|             356.0|
    | 0.29|Premium|    I|    VS2| 62.4| 58.0|  334| 4.2|4.23|2.63|            358.75|
    |  0.2|Premium|    E|    VS2| 59.8| 62.0|  367|3.79|3.77|2.26|             360.4|
    |  0.2|Premium|    E|    VS2| 59.0| 60.0|  367|3.81|3.78|2.24|             361.5|
    |  0.2|Premium|    E|    VS2| 61.1| 59.0|  367|3.81|3.78|2.32| 362.2857142857143|
    |  0.2|Premium|    E|    VS2| 59.7| 62.0|  367|3.84| 3.8|2.28|             367.0|
    |  0.2|Premium|    F|    VS2| 62.6| 59.0|  367|3.73|3.71|2.33|367.14285714285717|
    |  0.2|Premium|    D|    VS2| 62.3| 60.0|  367|3.73|3.68|2.31| 367.2857142857143|
    |  0.2|Premium|    D|    VS2| 61.7| 60.0|  367|3.77|3.72|2.31|369.14285714285717|
    |  0.3|Premium|    J|    VS2| 62.2| 58.0|  368|4.28| 4.3|2.67|             371.0|
    |  0.3|Premium|    J|    VS2| 60.6| 59.0|  368|4.34|4.38|2.64| 373.7142857142857|
    | 0.31|Premium|    J|    VS2| 62.5| 60.0|  380|4.31|4.36|2.71|376.42857142857144|
    | 0.31|Premium|    J|    VS2| 62.4| 60.0|  380|4.29|4.33|2.69|379.14285714285717|
    | 0.21|Premium|    E|    VS2| 60.5| 59.0|  386|3.87|3.83|2.33| 381.7142857142857|
    | 0.21|Premium|    E|    VS2| 59.6| 56.0|  386|3.93|3.89|2.33| 384.2857142857143|
    | 0.21|Premium|    D|    VS2| 61.6| 59.0|  386|3.82|3.78|2.34|385.14285714285717|
    | 0.21|Premium|    D|    VS2| 60.6| 60.0|  386|3.85|3.81|2.32|             387.0|
    | 0.21|Premium|    D|    VS2| 59.1| 62.0|  386|3.89|3.86|2.29|             388.0|
    | 0.21|Premium|    D|    VS2| 58.3| 59.0|  386|3.96|3.93| 2.3|389.57142857142856|
    | 0.32|Premium|    J|    VS2| 61.9| 58.0|  393|4.35|4.38| 2.7|392.14285714285717|
    +-----+-------+-----+-------+-----+-----+-----+----+----+----+------------------+
    only showing top 20 rows
    


And it returns a dataframe sorted by the specifications from our window function with the new column fully calculated.  Note that the first entry computes a window of 0, +3, the second entry a window of -1, +3, the third -2, +3 and the fourth finally -3, +3.  It would be reasonable to expect it to compute `null` values where the full window range can't be operated over; neither way is necessarily wrong, but make sure you note how pySpark handles it.

# Imputation

Due to immutability, we will recast the dataframe with yet another column that takes the value from the `'price'` column if it **is not `null`**, and fills in the value from the `'moving_avg'` column if it **is `null`**.  We will do this using pySpark's built in *`when... otherwise`* conditionals.  It is an intuitive, if not very Pythonic, formulation.  Then we cast the condition into a new column named `'imputed'`.  Note that the `withColumn` code is split onto multiple lines just for readability; the open brackets tell Python automatically that the command is meant to continue seamlessly to the next line, ignoring leading whitespace.

```python
from pyspark.sql.functions import when, col


def replace_null(orig, ma):
    return when(orig.isNull(), ma).otherwise(orig)
```

```python
df_new = df.withColumn("imputed", replace_null(col("price"), col("moving_avg")))
```

```python
df_new.show()
```

    +-----+-------+-----+-------+-----+-----+-----+----+----+----+------------------+-------+
    |carat|    cut|color|clarity|depth|table|price|   x|   y|   z|        moving_avg|imputed|
    +-----+-------+-----+-------+-----+-----+-----+----+----+----+------------------+-------+
    | 0.73|Premium|    F|    VS2| 62.5| 57.0| null|5.75| 5.7|3.58|             356.0|  356.0|
    | 0.29|Premium|    I|    VS2| 62.4| 58.0|  334| 4.2|4.23|2.63|            358.75|  334.0|
    |  0.2|Premium|    E|    VS2| 59.8| 62.0|  367|3.79|3.77|2.26|             360.4|  367.0|
    |  0.2|Premium|    E|    VS2| 59.0| 60.0|  367|3.81|3.78|2.24|             361.5|  367.0|
    |  0.2|Premium|    E|    VS2| 61.1| 59.0|  367|3.81|3.78|2.32| 362.2857142857143|  367.0|
    |  0.2|Premium|    E|    VS2| 59.7| 62.0|  367|3.84| 3.8|2.28|             367.0|  367.0|
    |  0.2|Premium|    F|    VS2| 62.6| 59.0|  367|3.73|3.71|2.33|367.14285714285717|  367.0|
    |  0.2|Premium|    D|    VS2| 62.3| 60.0|  367|3.73|3.68|2.31| 367.2857142857143|  367.0|
    |  0.2|Premium|    D|    VS2| 61.7| 60.0|  367|3.77|3.72|2.31|369.14285714285717|  367.0|
    |  0.3|Premium|    J|    VS2| 62.2| 58.0|  368|4.28| 4.3|2.67|             371.0|  368.0|
    |  0.3|Premium|    J|    VS2| 60.6| 59.0|  368|4.34|4.38|2.64| 373.7142857142857|  368.0|
    | 0.31|Premium|    J|    VS2| 62.5| 60.0|  380|4.31|4.36|2.71|376.42857142857144|  380.0|
    | 0.31|Premium|    J|    VS2| 62.4| 60.0|  380|4.29|4.33|2.69|379.14285714285717|  380.0|
    | 0.21|Premium|    E|    VS2| 60.5| 59.0|  386|3.87|3.83|2.33| 381.7142857142857|  386.0|
    | 0.21|Premium|    E|    VS2| 59.6| 56.0|  386|3.93|3.89|2.33| 384.2857142857143|  386.0|
    | 0.21|Premium|    D|    VS2| 61.6| 59.0|  386|3.82|3.78|2.34|385.14285714285717|  386.0|
    | 0.21|Premium|    D|    VS2| 60.6| 60.0|  386|3.85|3.81|2.32|             387.0|  386.0|
    | 0.21|Premium|    D|    VS2| 59.1| 62.0|  386|3.89|3.86|2.29|             388.0|  386.0|
    | 0.21|Premium|    D|    VS2| 58.3| 59.0|  386|3.96|3.93| 2.3|389.57142857142856|  386.0|
    | 0.32|Premium|    J|    VS2| 61.9| 58.0|  393|4.35|4.38| 2.7|392.14285714285717|  393.0|
    +-----+-------+-----+-------+-----+-----+-----+----+----+----+------------------+-------+
    only showing top 20 rows
    


We can see in the above, on the first row the price is `null`, and the imputed column shows the moving average value.  On all the other rows the price has an actual value, and the imputed column uses those values.  Below we can look again at all the rows where price is `null`:

```python
df_new.where(df["price"].isNull()).show(50)
```

    +-----+---------+-----+-------+-----+-----+-----+----+----+----+-----------------+-----------------+
    |carat|      cut|color|clarity|depth|table|price|   x|   y|   z|       moving_avg|          imputed|
    +-----+---------+-----+-------+-----+-----+-----+----+----+----+-----------------+-----------------+
    | 0.73|  Premium|    F|    VS2| 62.5| 57.0| null|5.75| 5.7|3.58|            356.0|            356.0|
    | 0.92|  Premium|    D|     I1| 63.0| 58.0| null|6.18|6.13|3.88|394.3333333333333|394.3333333333333|
    | 0.71|Very Good|    J|   VVS2| 61.1| 58.0| null| 5.7|5.75| 3.5|            356.0|            356.0|
    | 0.35|    Ideal|    I|    VS1| 60.9| 57.0| null|4.54|4.59|2.78|            340.0|            340.0|
    | 0.34|    Ideal|    E|    VS1| 61.2| 55.0| null|4.52|4.56|2.77|            349.0|            349.0|
    | 0.58|    Ideal|    F|    VS1| 60.3| 57.0| null|5.47|5.44|3.29|            357.0|            357.0|
    |  0.7|     Good|    F|    VS1| 59.4| 62.0| null|5.71|5.76| 3.4|353.6666666666667|353.6666666666667|
    |  0.7|  Premium|    E|    SI1| 61.2| 57.0| null|5.73|5.68|3.49|            326.0|            326.0|
    | 0.37|  Premium|    D|    SI1| 60.4| 59.0| null|4.68|4.62|2.81|            334.0|            334.0|
    | 0.76|  Premium|    H|    SI1| 59.8| 57.0| null|5.93|5.91|3.54|343.6666666666667|343.6666666666667|
    | 0.24|  Premium|    I|    VS1| 62.5| 57.0| null|3.97|3.94|2.47|            386.0|            386.0|
    | 0.88|Very Good|    I|    SI1| 62.5| 56.0| null|6.06|6.19|3.83|            344.0|            344.0|
    |  0.7|Very Good|    D|    SI1| 62.8| 60.0| null|5.66|5.68|3.56|            347.0|            347.0|
    |  0.7|     Good|    H|   VVS2| 58.9| 61.5| null|5.77|5.84|3.42|408.3333333333333|408.3333333333333|
    |  0.7|     Fair|    F|    VS2| 64.5| 57.0| null|5.57|5.53|3.58|444.6666666666667|444.6666666666667|
    |  0.7|Very Good|    E|    VS1| 63.4| 62.0| null|5.64|5.56|3.55|349.3333333333333|349.3333333333333|
    | 1.28|    Ideal|    I|    SI2| 61.7| 59.0| null|6.96|6.92|4.28|339.3333333333333|339.3333333333333|
    |  0.5|    Ideal|    J|    VS2| 61.7| 57.0| null|5.09|5.12|3.15|            367.0|            367.0|
    | 0.52|    Ideal|    D|    VS2| 61.8| 55.0| null|5.19|5.23|3.22|            367.0|            367.0|
    | 1.01|    Ideal|    F|    SI1| 62.7| 55.0| null|6.45| 6.4|4.03|            360.0|            360.0|
    | 1.03|    Ideal|    H|    SI1| 61.1| 56.0| null| 6.5|6.53|3.98|361.3333333333333|361.3333333333333|
    +-----+---------+-----+-------+-----+-----+-----+----+----+----+-----------------+-----------------+
    


And we see that in all cases, the `'imputed'` column has the moving average value listed.
