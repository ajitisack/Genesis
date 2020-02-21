
import pandas as pd
import re
import sqlite3
from timeit import default_timer as timer
import datetime
import sys
import numpy as np
import arrow


dbfile = "data/bse.db"
conn = sqlite3.connect(dbfile)
query = """
select
  seccd
, secid
, secnm
, secgrp
, faceval
, industry
, dt
, open
, high
, low
, close
, adjclose
, vol
, year
, month
, day
, wkday
, wknr
, qrtr
from equity
where freq = 1
"""


df = pd.read_sql_query(query, conn)

datatypes1 = {"faceval":np.float16, "open":np.float16, "high":np.float32, "low":np.float32, "close":np.float32, "adjclose":np.float32}
df = df.astype(datatypes1)
df = df.astype({"year":np.uint16, "month":np.uint8, "day":np.uint8, "wkday":np.uint8, "wknr":np.uint8, "qrtr":np.uint8})

df.info()
df.dtypes

df.info()
df.dtypes
df.head(10)
