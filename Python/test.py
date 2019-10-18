import pandas as pd
import re
import time
import datetime
import sqlite3

def create_sqlite_connection(dbfile:str):
	conn = sqlite3.connect(dbfile)
	return conn


secid = "SUNDARAM"
startdt = "2019-01-01"
enddt = "2019-10-01"


url1 = "https://in.finance.yahoo.com/quote/" + secid + ".BO/history"
url2 = "https://query1.finance.yahoo.com/v7/finance/download/" + secid
url2 = url2 + ".BO?period1=" + get_UNIX_dt(startdt)
url2 = url2 + "&period2=" + get_UNIX_dt(enddt)
url2 = url2 + "&interval=1d&events=history&crumb="


with requests.session():
	website = requests.get(url1)
	crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', website.text)
	url2 = url2 + crumb[0]
	website = requests.get(url2, cookies = website.cookies)

website.text.split('\n')

dbfile = "data/bse.db"
query = "SELECT seccd, secid FROM security where secstatus = 'A'"
conn = create_sqlite_connection(dbfile)
df = pd.read_sql_query(query, conn)
security = df.values.tolist()

x=len(security)+3
len(security)
x
n = int(len(security)/4)
n = int(x/4)
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
n
x = list(divide_chunks(security, n))
len(x[0])
len(x[1])
len(x[2])
len(x[3])
len(x[4])
