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


class Security():

    @staticmethod
    def getyfjson(securityid):
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
    def getdomainkeyvalue(json_str, domain, key):
        return json_str[domain][key] if domain in json_str and json_str[domain] and key in json_str[domain] else ['']


    @staticmethod
    def getdetails(securityid):
        json_str = Security.getyfjson(securityid)
        x = Utility.securitydetailsitems()
        result = [Security.getdomainkeyvalue(json_str, i[0], i[1]) for i in x]
        return result


    @staticmethod
    @SqlLite.connector
    def getequitylist(n_equitites=5000):
    	sql = f"SELECT symbol FROM security where industry <> 'Index Fund' and inbse=1 limit {n_equitites}"
    	equitylist = pd.read_sql_query(sql, SqlLite.conn).symbol.to_list()
    	return equitylist

    @staticmethod
    @Utility.timer
    def getalldetails(n_securities=5000):
        columns = x = [i[1].lower() for i in Utility.securitydetailsitems()]
        column_names = ['symbol', 'shortname', 'longname', 'symbol', 'sector', 'industry', 'profitmargins', 'grossmargins', 'revenuegrowth', 'operatingmargins', 'grossprofits'
        , 'earningsgrowth' , 'returnonassets', 'returnonequity', 'totalcash', 'totaldebt', 'totalrevenue', 'totalcashpershare', 'revenuepershare'
        , 'regularmarketchange', 'marketcap', 'dividendyield', 'regularmarketchangepercent', 'enterprisetorevenue', 'profitmargins', 'sharesoutstanding', 'bookvalue'
        , 'netincometocommon', 'pricetobook', 'floatshares', 'enterprisevalue']
        equitylist = Security.getequitylist(10)
        nthreads = min(len(equitylist), 20)
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(Security.getdetails, equitylist)
        df = pd.DataFrame(list(results), columns=columns)
        return df[column_names]


Security.getalldetails()
