---
source_repo: https://github.com/whoamimi/pyspark-statistical-inference.git
source_commit: db970f3bc3dec59147f327b066e07f43d61d09da
source_branch: master
source_path: 07_resampling.ipynb
source_url: https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/07_resampling.ipynb
generated_at: 2026-09-20T03:46:55+00:00
generated_by: scripts/notebooks_to_md.py
---

> Converted from [`07_resampling.ipynb`](https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/07_resampling.ipynb) in [https://github.com/whoamimi/pyspark-statistical-inference.git](https://github.com/whoamimi/pyspark-statistical-inference.git) at commit `db970f3bc3de`. Edit the notebook in the submodule, not this file — re-run `scripts/notebooks_to_md.py` to refresh it.

**_pySpark Basics: Resampling_**

_by Jeff Levy (jlevy@urban.org)_

_Last Updated: 31 Jul 2017, Spark v2.1_

_Abstract: This guide will demonstrate changing the frequency of observations by aggregating daily data into monthly._

_Main operations used: `dtypes`, `udf`, `drop`, `groupBy`, `agg`, `withColumn`, `dateFormat`, `select`_

***

We begin by creating a simple dataset, where we first define a row as having three fields (columns) and then define each individual row by specifying its three entries:

```python
import datetime
from pyspark.sql import Row
from pyspark.sql.functions import col

row = Row("date", "name", "production")

df = sc.parallelize([
    row("08/01/2014", "Kim", 5),
    row("08/02/2014", "Kim", 14),
    row("08/01/2014", "Bob", 6),
    row("08/02/2014", "Bob", 3),
    row("08/01/2014", "Sue", 0),
    row("08/02/2014", "Sue", 22),
    row("08/01/2014", "Dan", 4),
    row("08/02/2014", "Dan", 4),
    row("08/01/2014", "Joe", 37),
    row("09/01/2014", "Kim", 6),
    row("09/02/2014", "Kim", 6),
    row("09/01/2014", "Bob", 4),
    row("09/02/2014", "Bob", 20),
    row("09/01/2014", "Sue", 11),
    row("09/02/2014", "Sue", 2),
    row("09/01/2014", "Dan", 1),
    row("09/02/2014", "Dan", 3),
    row("09/02/2014", "Joe", 29)
    ]).toDF()
```

```python
df.show()
```

    +----------+----+----------+
    |      date|name|production|
    +----------+----+----------+
    |08/01/2014| Kim|         5|
    |08/02/2014| Kim|        14|
    |08/01/2014| Bob|         6|
    |08/02/2014| Bob|         3|
    |08/01/2014| Sue|         0|
    |08/02/2014| Sue|        22|
    |08/01/2014| Dan|         4|
    |08/02/2014| Dan|         4|
    |08/01/2014| Joe|        37|
    |09/01/2014| Kim|         6|
    |09/02/2014| Kim|         6|
    |09/01/2014| Bob|         4|
    |09/02/2014| Bob|        20|
    |09/01/2014| Sue|        11|
    |09/02/2014| Sue|         2|
    |09/01/2014| Dan|         1|
    |09/02/2014| Dan|         3|
    |09/02/2014| Joe|        29|
    +----------+----+----------+
    


```python
df.dtypes
```




    [('date', 'string'), ('name', 'string'), ('production', 'bigint')]



While we have dates for each observation, you can see they are just string objects.  Defaulting to strings is quite common in pySpark dataframes, and while we can convert them to date objects using the standard Python datetime module (demonstrated below), it is often not necessary.  Whether it is worth the conversion likely depends on what other timeseries functions you plan on working with.  As an example, let's resample this data to find monthly production for each individual.

First we create a new column that contains just the month and year.  This isn't quite as elegant in pySpark as it is for smaller, non-distributed data done in Pandas, but I'll comment each step carefully as we go:

```python
#'udf' stands for 'user defined function', and is simply a wrapper for functions you write and 
#want to apply to a column that knows how to iterate through pySpark dataframe columns. it should
#be more clear after we use it below
from pyspark.sql.functions import udf

#we define our own function that knows how to split apart a MM/DD/YYYY string and return a 
#MM/YYYY string.  everything in here is standard Python, and not specific to pySpark
def split_date(whole_date):
    
    #this try-except handler provides some minimal fault tolerance in case one of our date 
    #strings is malformed, as we might find with real-world data. if it fails to split the
    #date into three parts it just returns 'error', which we could later subset the data on
    #to see what went wrong
    try:
        mo, day, yr = whole_date.split('/')
    except ValueError:
        return 'error'
    
    #lastly we return the month and year strings joined together
    return mo + '/' + yr

#this is where we wrap the function we wrote above in the udf wrapper
udf_split_date = udf(split_date)

#here we create a new dataframe by calling the original dataframe and specifying the new
#column.  unlike with Pandas or R, pySpark dataframes are immutable, so we cannot simply assign
#to a new column on the original dataframe
df_new = df.withColumn('month_year', udf_split_date('date'))
```

Note that we could easily use our `split_date` function above to use datetime objects.  This could be useful if we wanted to resample our data to, say, quarterly or weekly, both of which datetime objects (https://docs.python.org/2/library/datetime.html) can easily keep track of for us.  In the case of a monthly split, we would gain nothing from the extra operation.

Below we see the results in our new dataframe, then we drop the original date column:

```python
df_new.show()
```

    +----------+----+----------+----------+
    |      date|name|production|month_year|
    +----------+----+----------+----------+
    |08/01/2014| Kim|         5|   08/2014|
    |08/02/2014| Kim|        14|   08/2014|
    |08/01/2014| Bob|         6|   08/2014|
    |08/02/2014| Bob|         3|   08/2014|
    |08/01/2014| Sue|         0|   08/2014|
    |08/02/2014| Sue|        22|   08/2014|
    |08/01/2014| Dan|         4|   08/2014|
    |08/02/2014| Dan|         4|   08/2014|
    |08/01/2014| Joe|        37|   08/2014|
    |09/01/2014| Kim|         6|   09/2014|
    |09/02/2014| Kim|         6|   09/2014|
    |09/01/2014| Bob|         4|   09/2014|
    |09/02/2014| Bob|        20|   09/2014|
    |09/01/2014| Sue|        11|   09/2014|
    |09/02/2014| Sue|         2|   09/2014|
    |09/01/2014| Dan|         1|   09/2014|
    |09/02/2014| Dan|         3|   09/2014|
    |09/02/2014| Joe|        29|   09/2014|
    +----------+----+----------+----------+
    


```python
df_new = df_new.drop('date')
```

Now we perform two steps on one line.  First we group the data - this can be done along multiple categories if desired.  So if we want to aggregate every employee's data together, leaving us with just values for August and September, we would group by `monthYear` alone.  In this case let's say we want totals for each employee within each month, so we group by `monthYear` and by `name` together.

After that we aggregate the resulting grouped dataframe; pySpark automatically knows the operations should be performed within groups only.  We just pass a dictionary into the `.agg` method, with the key being the column name of interest and the value being the operation used to aggregate.  We'll use `sum`, but we can also use, for example, `avg`, `min` or `max`.  Note that this is done by passing the operation as a string.

```python
df_agg = df_new.groupBy('month_year', 'name').agg({'production' : 'sum'})
```

The aggregation can be done on more than one field using different types, just by adding the appropriate entry to the dictionary.  For example, if there was an "hours worked" column, we might pass a dictionary that looked like this: `{'production' : 'sum', 'hours' : 'avg'}`

```python
df_agg.show()
```

    +----------+----+---------------+
    |month_year|name|sum(production)|
    +----------+----+---------------+
    |   09/2014| Sue|             13|
    |   09/2014| Kim|             12|
    |   09/2014| Bob|             24|
    |   09/2014| Joe|             29|
    |   09/2014| Dan|              4|
    |   08/2014| Kim|             19|
    |   08/2014| Joe|             37|
    |   08/2014| Dan|              8|
    |   08/2014| Sue|             22|
    |   08/2014| Bob|              9|
    +----------+----+---------------+
    


If you definitely want datetime objects in your dataframe (Spark currently has very limited timeseries functionality), you can accomplish it with another `udf`:

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import DateType
from datetime import datetime

dateFormat = udf(lambda x: datetime.strptime(x, '%M/%d/%Y'), DateType())
    
df_d = df.withColumn('new_date', dateFormat(col('date')))
```

```python
df_d.dtypes
```




    [('date', 'string'),
     ('name', 'string'),
     ('production', 'bigint'),
     ('new_date', 'date')]



```python
df_d.select('new_date').take(1)
```




    [Row(new_date=datetime.date(2014, 1, 1))]



In this case we take advantage of the `strptime` feature of the standard Python datetime module, which takes a string and a format string and returns a datetime object.  Datetime objects can be far more useful than a date as a string if you plan a lot of other timeseries operations; they allow things like subtracting two dates to get elapsed time, or separating by quarters or weeks, or accounting for time zones or leap years.

Better time series functionality appears to be a priority in Spark development, and multiple options have already been proposed that would make their use far more effecient.  Expect to see future versions taking better advantage of this.

```python

```
