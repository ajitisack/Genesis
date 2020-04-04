import requests as requests
import pandas as pd
import json
import arrow
import re
import requests

from sqlite import SqlLite
from utils import Utility
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor


class Equity():

    startdt  = '2020-01-01'
    interval = '1d'
    nodatalist = []
    tblname   = 'equitydly'

    bse_equityfile = "/Users/ajit/projects/stockmarket_analysis/Equity.csv"
    bse_securitytbl = 'security'
    securitystatus = defaultdict(lambda: 'N', {'Active':'A', 'Delisted':'D', 'Suspended':'S'})


    @staticmethod
    def getquote(securityid):
    	url = f'https://finance.yahoo.com/quote/{securityid}.BO'
    	html = requests.get(url=url).text
    	if "QuoteSummaryStore" not in html:
    		html = requests.get(url=url).text
    		if "QuoteSummaryStore" not in html:
    			return {}
    	json_str = html.split('root.App.main =')[1].split('(this)')[0].split(';\n}')[0].strip()
    	data = json.loads(json_str)['context']['dispatcher']['stores']['QuoteSummaryStore']
    	new_data = json.dumps(data).replace('{}', 'null')
    	new_data = re.sub(r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)
    	return json.loads(new_data)

    @staticmethod
    def getdetails(securityid):
    	json_str = getyfjson(securityid)
    	result = []
    	result += getdomainkeyvalue(json_str, 'quoteType', 'shortName')
    	result += getdomainkeyvalue(json_str, 'price', 'longName')
    	result += getdomainkeyvalue(json_str, 'price', 'symbol')
    	result += getdomainkeyvalue(json_str, 'summaryProfile', 'sector')
    	result += getdomainkeyvalue(json_str, 'summaryProfile', 'industry')
    	result += getdomainkeyvalue(json_str, 'financialData', 'profitMargins')
    	result += getdomainkeyvalue(json_str, 'financialData', 'grossMargins')
    	result += getdomainkeyvalue(json_str, 'financialData', 'revenueGrowth')
    	result += getdomainkeyvalue(json_str, 'financialData', 'operatingMargins')
    	result += getdomainkeyvalue(json_str, 'financialData', 'grossProfits')
    	result += getdomainkeyvalue(json_str, 'financialData', 'earningsGrowth')
    	result += getdomainkeyvalue(json_str, 'financialData', 'returnOnAssets')
    	result += getdomainkeyvalue(json_str, 'financialData', 'returnOnEquity')
    	result += getdomainkeyvalue(json_str, 'financialData', 'totalCash')
    	result += getdomainkeyvalue(json_str, 'financialData', 'totalDebt')
    	result += getdomainkeyvalue(json_str, 'financialData', 'totalRevenue')
    	result += getdomainkeyvalue(json_str, 'financialData', 'totalCashPerShare')
    	result += getdomainkeyvalue(json_str, 'financialData', 'revenuePerShare')
    	result += getdomainkeyvalue(json_str, 'price', 'regularMarketChange')
    	result += getdomainkeyvalue(json_str, 'price', 'marketCap')
    	result += getdomainkeyvalue(json_str, 'price', 'dividendYield')
    	result += getdomainkeyvalue(json_str, 'price', 'regularMarketChangePercent')
    	result += getdomainkeyvalue(json_str, 'defaultKeyStatistics', 'enterpriseToRevenue')
    	result += getdomainkeyvalue(json_str, 'defaultKeyStatistics', 'profitMargins')
    	result += getdomainkeyvalue(json_str, 'defaultKeyStatistics', 'sharesOutstanding')
    	result += getdomainkeyvalue(json_str, 'defaultKeyStatistics', 'bookValue')
    	result += getdomainkeyvalue(json_str, 'defaultKeyStatistics', 'netIncomeToCommon')
    	result += getdomainkeyvalue(json_str, 'defaultKeyStatistics', 'priceToBook')
    	result += getdomainkeyvalue(json_str, 'defaultKeyStatistics', 'floatShares')
    	result += getdomainkeyvalue(json_str, 'defaultKeyStatistics', 'enterpriseValue')
    	result += getdomainkeyvalue(json_str, 'defaultKeyStatistics', 'earningsQuarterlyGrowth')
    	return result

    @Utility.timer
    @classmethod
    def getalldetails(cls, n_securities=5000):
        column_names = ['securityid', 'shortname', 'longname', 'symbol', 'sector', 'industry', 'profitmargins', 'grossmargins', 'revenuegrowth', 'operatingmargins', 'grossprofits'
        , 'earningsgrowth' , 'returnonassets', 'returnonequity', 'totalcash', 'totaldebt', 'totalrevenue', 'totalcashpershare', 'revenuepershare'
        , 'regularmarketchange', 'marketcap', 'dividendyield', 'regularmarketchangepercent', 'enterprisetorevenue', 'profitmargins', 'sharesoutstanding', 'bookvalue'
        , 'netincometocommon', 'pricetobook', 'floatshares', 'enterprisevalue']
        equitylist = getequitylist(10)
        nthreads = min(len(equitylist), 20)
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(getsecuritydetails, equitylist)
        df = pd.DataFrame(list(results), columns=column_names)
        return df
