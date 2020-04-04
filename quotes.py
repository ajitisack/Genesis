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
    def getchartresult(securityid):
        params = {}
        params['period1']  = arrow.get(Equity.startdt).timestamp
        params['period2']  = arrow.now().timestamp
        params['interval'] = Equity.interval
        params['events']   = 'history,div,split'
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{securityid.upper()}.BO"
        data = requests.get(url=url, params=params)
        return data.json()

    @staticmethod
    def getquotes(data):
        x = data['chart']['result'][0]
        if x['indicators']['quote']== [{}] :
            return pd.DataFrame()
        date = [arrow.get(i).format('YYYY-MM-DD') for i in x['timestamp']]
        adjclose = x['indicators']['adjclose'][0]['adjclose']
        open = x['indicators']['quote'][0]['open']
        high = x['indicators']['quote'][0]['high']
        low = x['indicators']['quote'][0]['low']
        close = x['indicators']['quote'][0]['close']
        volume = x['indicators']['quote'][0]['volume']
        df = pd.DataFrame({'date':date, 'open':open, 'high':high, 'low':low, 'close':close, 'adjclose': adjclose, 'volume':volume}, index= x['timestamp']).dropna()
        return df

    @staticmethod
    def getdividends(data):
        x = data['chart']['result'][0]
        if 'events' not in x or 'dividends' not in x['events']:
            return pd.DataFrame(columns=['dividend'])
        df = pd.DataFrame(x['events']['dividends']).T[['amount']]
        df.columns = ['dividend']
        df.index = df.index.astype(int)
        return df

    @staticmethod
    def getsplits(data):
        x = data['chart']['result'][0]
        if 'events' not in x or 'splits' not in x['events']:
             return pd.DataFrame(columns=['splits'])
        df = pd.DataFrame(data['chart']['result'][0]['events']['splits']).T
        df['splits'] = df['numerator']/df['denominator']
        df.index = df.index.astype(int)
        return df[['splits']]


    @staticmethod
    def gethistprice(securityid):
        securityid = securityid.upper()
        data = Equity.getchartresult(securityid)
        if data['chart']['error'] is not None:
            Equity.nodatalist.append(securityid)
            return pd.DataFrame()
        quotes, dividends, splits = Equity.getquotes(data), Equity.getdividends(data), Equity.getsplits(data)
        if quotes.empty:
            Equity.nodatalist.append(securityid)
            return pd.DataFrame()
        df = pd.concat([quotes, dividends, splits], axis=1, sort=True)
        df['dividend'].fillna(0, inplace=True)
        df['splits'].fillna(0, inplace=True)
        df.dropna(how='any', inplace=True)
        df.insert(loc=0, column = 'securityid', value=securityid)
        df.insert(loc=1, column = 'exchange', value='BSE')
        df = Utility.adddatefeatures(df)
        df = Utility.reducesize(df)
        df.reset_index(drop=True, inplace=True)
        return df

    @staticmethod
    @SqlLite.connector
    def getequitylist(n_equitites=5000):
    	sql = f"SELECT securityid FROM security where status = 'A' limit {n_equitites}"
    	equitylist = pd.read_sql_query(sql, SqlLite.conn).securityid.to_list()
    	return equitylist

    @Utility.timer
    @classmethod
    def getallhistprice(cls, n_securities=5000):
        equitylist = Equity.getequitylist(n_securities)
        nthreads = min(len(equitylist), 20)
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(Equity.gethistprice, equitylist)
        df = pd.concat(results, ignore_index=True)
        return df

    @staticmethod
    @SqlLite.connector
    def loadhistpricedata(df):
        df.to_sql(Equity.tblname, SqlLite.conn, if_exists='replace', index=False)
        print(f'Table {tblname} has been refreshed with {df.shape[0]} records')
