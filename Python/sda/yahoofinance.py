import requests
import re
from . import datefeatures as d

def get_cookies_crumb():
	url = "https://in.finance.yahoo.com/quote/^BSESN/history"
	with requests.session():
		website = requests.get(url)
	crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', website.text)[0]
	cookies = website.cookies
	print("Info : Collected cookies and crumb from yahoo finance")
	return cookies, crumb


def query_yahoo_finance(secid, startdt, enddt, cookies, crumb):
	url = "https://query1.finance.yahoo.com/v7/finance/download/" + secid
	url = url + ".BO?period1=" + d.get_UNIX_dt(startdt)
	url = url + "&period2=" + d.get_UNIX_dt(enddt)
	url = url + "&interval=1d&events=history&crumb=" + crumb
	with requests.session():
		website = requests.get(url, cookies = cookies)
	return website.text
