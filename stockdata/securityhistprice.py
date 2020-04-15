import pandas as pd
import json
import arrow
import re
import requests
from requests.adapters import HTTPAdapter

from .utils import Utility
from .sdlogger import SDLogger

class SecurityHistPrice(SDLogger):

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

    def getchartresult(self, symbol, startdt, interval):
        params = {}
        params['period1']  = arrow.get(startdt).timestamp
        params['period2']  = arrow.now().timestamp
        params['interval'] = '1d'
        params['events']   = 'history,div,split'
        url = f'{self.queryurl}/{symbol}'
        with requests.Session() as s:
            s.mount(url, HTTPAdapter(max_retries=self.request_max_rtries))
            chart = s.get(url, params=params)
        return chart.json()

    def gethistprice(self, symbol, startdt, interval):
        try:
            symbol = symbol.upper()
            exchange = 'BSE' if symbol.endswith('.BO') else 'NSE'
            data = self.getchartresult(symbol, startdt, interval)
            if data['chart']['error'] is not None:
                self.msglogger.info(f'no hist price for {symbol}')
                return pd.DataFrame()
            quotes, dividends, splits = SecurityHistPrice.getquotes(data), SecurityHistPrice.getdividends(data), SecurityHistPrice.getsplits(data)
            if quotes.empty:
                self.msglogger.info(f'no hist price for {symbol}')
                return pd.DataFrame()
            df = pd.concat([quotes, dividends, splits], axis=1, sort=True)
            df['dividend'].fillna(0, inplace=True)
            df['splits'].fillna(0, inplace=True)
            df.dropna(how='any', inplace=True)
            df.insert(loc=0, column = 'symbol', value=symbol[:-3])
            df.insert(loc=1, column = 'exchange', value=exchange)
            df = Utility.adddatefeatures(df)
            df = Utility.reducesize(df)
            df.reset_index(drop=True, inplace=True)
            return df
        except:
            self.msglogger.error(f'no hist price for {symbol}')
