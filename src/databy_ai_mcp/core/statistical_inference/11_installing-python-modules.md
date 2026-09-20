---
source_repo: https://github.com/whoamimi/pyspark-statistical-inference.git
source_commit: db970f3bc3dec59147f327b066e07f43d61d09da
source_branch: master
source_path: 11_installing-python-modules.ipynb
source_url: https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/11_installing-python-modules.ipynb
generated_at: 2026-09-20T03:46:55+00:00
generated_by: scripts/notebooks_to_md.py
---

> Converted from [`11_installing-python-modules.ipynb`](https://github.com/whoamimi/pyspark-statistical-inference/blob/db970f3bc3dec59147f327b066e07f43d61d09da/11_installing-python-modules.ipynb) in [https://github.com/whoamimi/pyspark-statistical-inference.git](https://github.com/whoamimi/pyspark-statistical-inference.git) at commit `db970f3bc3de`. Edit the notebook in the submodule, not this file — re-run `scripts/notebooks_to_md.py` to refresh it.

**_pySpark Basics: Installing Python Modules_**

_by Jeff Levy (jlevy@urban.org)_

_Last Updated: 2 Aug 2016, Spark v1.6.1_

_Abstract: When a new cluster is spun up on AWS, it comes with only a few Python modules installed.  This guide will go over adding more as necessary._

_Main operations used:_ `pip`

***

Those with experience in Python are probably accustomed to using a distribution with many modules pre-packaged, for example from Anaconda or Enthought.  However, every time a cluster is spun up on AWS the installation of Python must be ported over from permanent storage, and the more it has to move and configure the longer the spinup process becomes.  Based on the assumption that most users will not need very many modules not already provided by pySpark, we have opted to minimize startup time by not pre-configuring Python with lots of modules.

# Installing Modules

The current boostrap script installs `pip`, (module installation manager), `numpy` (many math operations), `requests` (tools for accessing the web) and `matplotlib` (graphing).  It also comes with the [Python standard library](https://docs.python.org/2/library/) that all installs have access to, such as `datetime`, `random`, `collections` and so on.  Any other modules you may need can be installed as follows:

```python
import pip
```

```python
pip.main(['install', 'pandas'])
```

    Collecting pandas
      Downloading pandas-0.18.1.tar.gz (7.3MB)
    Requirement already satisfied (use --upgrade to upgrade): python-dateutil in ./venv/lib/python2.7/site-packages (from pandas)
    Requirement already satisfied (use --upgrade to upgrade): pytz>=2011k in ./venv/lib/python2.7/site-packages (from pandas)
    Requirement already satisfied (use --upgrade to upgrade): numpy>=1.7.0 in ./venv/lib64/python2.7/site-packages (from pandas)
    Requirement already satisfied (use --upgrade to upgrade): six>=1.5 in ./venv/lib/python2.7/site-packages (from python-dateutil->pandas)
    Installing collected packages: pandas
      Running setup.py install for pandas: started
        Running setup.py install for pandas: still running...
        Running setup.py install for pandas: still running...
        Running setup.py install for pandas: finished with status 'done'
    Successfully installed pandas-0.18.1





    0



Note in the output that this command also checked on all the dependencies for `pandas`, and would have installed them if they had been lacking.  You can do this for any package listed in the PyPi index, the official repository for Pthon modules.

# Installing Specific Versions

We can also use this to get specific versions of modules; by default it installs the newest:

```python
pip.main(['install', 'statsmodels==0.6.0'])
```

    Collecting statsmodels==0.6.0
      Downloading statsmodels-0.6.0.zip (7.3MB)
    Collecting scipy (from statsmodels==0.6.0)
      Downloading scipy-0.17.1-cp27-cp27mu-manylinux1_x86_64.whl (39.5MB)
    Requirement already satisfied (use --upgrade to upgrade): pandas in ./venv/lib64/python2.7/site-packages (from statsmodels==0.6.0)
    Collecting patsy (from statsmodels==0.6.0)
      Downloading patsy-0.4.1-py2.py3-none-any.whl (233kB)
    Requirement already satisfied (use --upgrade to upgrade): python-dateutil in ./venv/lib/python2.7/site-packages (from pandas->statsmodels==0.6.0)
    Requirement already satisfied (use --upgrade to upgrade): pytz>=2011k in ./venv/lib/python2.7/site-packages (from pandas->statsmodels==0.6.0)
    Requirement already satisfied (use --upgrade to upgrade): numpy>=1.7.0 in ./venv/lib64/python2.7/site-packages (from pandas->statsmodels==0.6.0)
    Requirement already satisfied (use --upgrade to upgrade): six in ./venv/lib/python2.7/site-packages (from patsy->statsmodels==0.6.0)
    Installing collected packages: scipy, patsy, statsmodels
      Running setup.py install for statsmodels: started
        Running setup.py install for statsmodels: finished with status 'done'
    Successfully installed patsy-0.4.1 scipy-0.17.1 statsmodels-0.6.0





    0



Note that this ended up installing two dependencies, `patsy` and `scipy`.  

# Upgrading Modules

And finally, we can use `pip` to upgrade modules if necessary:

```python
pip.main(['install', '--upgrade', 'statsmodels'])
```

    Collecting statsmodels
      Downloading statsmodels-0.6.1.tar.gz (7.0MB)
    Requirement already up-to-date: pandas in ./venv/lib64/python2.7/site-packages (from statsmodels)
    Requirement already up-to-date: python-dateutil in ./venv/lib/python2.7/site-packages (from pandas->statsmodels)
    Requirement already up-to-date: pytz>=2011k in ./venv/lib/python2.7/site-packages (from pandas->statsmodels)
    Requirement already up-to-date: numpy>=1.7.0 in ./venv/lib64/python2.7/site-packages (from pandas->statsmodels)
    Requirement already up-to-date: six>=1.5 in ./venv/lib/python2.7/site-packages (from python-dateutil->pandas->statsmodels)
    Installing collected packages: statsmodels
      Found existing installation: statsmodels 0.6.0
        Uninstalling statsmodels-0.6.0:
          Successfully uninstalled statsmodels-0.6.0
      Running setup.py install for statsmodels: started
        Running setup.py install for statsmodels: finished with status 'done'
    Successfully installed statsmodels-0.6.1





    0



All of the packages you install this way will remain installed as long as this cluster is spun up.  You can open multiple notebooks, or close all of them and open a new one, and they will all have access to the modules you've installed.  Only when the cluster is spun down through the AWS Console will you need to start over.

And finally, it's important to keep in mind that some packages may not be compatible with distributed data.  The `pandas` module, for example, is for working with dataframes in a standard desktop environment - if you try to load a very large distributed dataset into a Pandas dataframe, *it will attempt to put all the data in one location*, and it will fail.  If you have reduced your data down to a reasonable size, however, you can load it into a Pandas dataframe.  Whether a module will work for you or not depends entirely on the module and the situation, so feel free to consult with Research Programming if in doubt.

```python

```
