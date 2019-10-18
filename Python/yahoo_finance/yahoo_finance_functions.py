import datetime
import time
import requests
import re

def get_UNIX_dt(dtstr):
	if dtstr == "": return ""
	dt = datetime.datetime.strptime(dtstr, "%Y-%m-%d")
	t = time.mktime(dt.timetuple())
	t = str(t).split('.')[0]
	return t


def get_cookies_crumb():
	url = "https://in.finance.yahoo.com/quote/^BSESN/history"
	with requests.session():
		website = requests.get(url)
	crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', website.text)[0]
	cookies = website.cookies
	return cookies, crumb


def query_yahoo_finance(secid, startdt, enddt, cookies, crumb):
	url = "https://query1.finance.yahoo.com/v7/finance/download/" + secid
	url = url + ".BO?period1=" + get_UNIX_dt(startdt)
	url = url + "&period2=" + get_UNIX_dt(enddt)
	url = url + "&interval=1d&events=history&crumb=" + crumb
	with requests.session():
		website = requests.get(url, cookies = cookies)
	return website.text
