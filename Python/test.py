import pandas as pd
import numpy as np
import requests
import re

url = "https://in.finance.yahoo.com/quote/^BSESN/history"
with requests.session():
	website = requests.get(url)
crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', website.text)[0]
cookies = website.cookies
url = "https://query1.finance.yahoo.com/v7/finance/download/HSIL.BO?period1=1546281000&period2=1571855400&interval=1mo&events=history&crumb="
url += crumb
with requests.session():
	website = requests.get(url, cookies = cookies)
list = website.text.split('\n')
list = [line.split(',') for line in list]
list
df=pd.DataFrame(list[1:])
df.head()
df.dtypes
df.columns = ["dt", "open", "high", "low", "close", "adjclose", "vol"]
df = df[(df["open"] != "null") & (df["dt"] != "")]
new_dtypes = {"open":float, "high":float, "low":float, "close":float, "adjclose":float}
df = df.astype(new_dtypes)
rounding = {"open":2, "high":2, "low":2, "close":2, "adjclose":2}
df = df.round(2)
df.head()

df.info()

df.dtypes
dfnew = df.astype({"Open":np.float16, "High":np.float32, "Low":np.float32, "Close":np.float32, "Adj Close":np.float32})

dfnew.dtypes
dfnew.info()

np.finfo(np.float16).max
np.finfo(np.float32).max
