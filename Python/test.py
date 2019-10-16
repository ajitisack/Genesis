

import pandas as pd
import requests
import re
import time
import datetime
import sqlite3

def get_UNIX_dt(dtstr):
	if dtstr == "": return ""
	dt = datetime.datetime.strptime(dtstr, "%Y-%m-%d")
	t = time.mktime(dt.timetuple())
	t = str(t).split('.')[0]
	return t

secid = "ZSVTRADI"
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

if len(crumb)==0:
	print("Empty crumb")
