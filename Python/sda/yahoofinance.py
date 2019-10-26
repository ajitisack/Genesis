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


# https://query1.finance.yahoo.com/v7/finance/download/HDFC.BO?period1=1546281000&period2=1571855400&interval=1d&events=history&crumb=vsEK.HY6ciA
# https://query1.finance.yahoo.com/v7/finance/download/HDFC.BO?period1=1546281000&period2=1571855400&interval=1wk&events=history&crumb=vsEK.HY6ciA
# https://query1.finance.yahoo.com/v7/finance/download/HDFC.BO?period1=1546281000&period2=1571855400&interval=1mo&events=history&crumb=vsEK.HY6ciA
def query_yahoo_finance(secid, f, startdt, enddt, cookies, crumb):
	"""freq - daily(d), weekly(wk), monthly(mo)
	"""
	frequency = {'d':'d', 'w':'wk', 'm':'mo'}
	url  = "https://query1.finance.yahoo.com/v7/finance/download/" + secid + ".BO"
	url += "?period1=" + d.get_UNIX_dt(startdt)
	url += "&period2=" + d.get_UNIX_dt(enddt)
	url += "&interval=1" + frequency[f]
	url += "&events=history&crumb=" + crumb
	with requests.session():
		website = requests.get(url, cookies = cookies)
	return website.text
