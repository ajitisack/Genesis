import pandas as pd
import time
import datetime
import sqlite3

sqlite_conn = sqlite3.connect("data/bse.db")
df = pd.read_sql_query("SELECT * FROM equity_1y", sqlite_conn)


df.head()


df.shape
df[df["secstatus"]=='A'].shape
filter1 =
filter2 =

df = df[(df.dt =='2019-10-07') & (df.secstatus =='A')]

df.shape

df.loc[df.groupby(["industry"])["close"].idxmax()]

df[df.industry == 'Airlines'].sort_values('close', ascending=False)
