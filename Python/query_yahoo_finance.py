import pandas as pd
import requests
import re
from bs4 import BeautifulSoup








with requests.session():
	header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
	url1 = "https://in.finance.yahoo.com/quote/HDFC.BO/history"
	website = requests.get(url1, headers=header)
	crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', website.text)[0]
	cookies = website.cookies
	url2 = "https://query1.finance.yahoo.com/v7/finance/download/HDFC.BO?period1=1412879400&period2=1570645800&interval=1d&events=history&crumb=" + crumb
	website = requests.get(url2, headers=header, cookies=cookies)

website.text.split('\n')
