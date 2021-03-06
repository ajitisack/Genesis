import json
import requests
import arrow
import time
from requests.adapters import HTTPAdapter

from nsedata.lib.logger import Logger
from nsedata.lib.config import Config
from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils  import Utility

class EquityHistDataDict(Logger):

    def __init__(self):
        Config.__init__(self)

    def getquotes(self, data):
        try:
            quotes = data.get('indicators').get('quote')[0]
            if quotes == {}: return {}
            hist = {}
            hist['date'] = data.get('timestamp')
            hist['symbol'] = data.get('meta').get('symbol')
            hist['open'] = quotes.get('open')
            hist['low'] = quotes.get('low')
            hist['high'] = quotes.get('high')
            hist['close'] = quotes.get('close')
            hist['adjclose'] = data.get('indicators').get('adjclose')[0].get('adjclose')
            hist['volume'] = quotes.get('volume')
            return hist
        except:
            return {}

    def getdividends(self, data):
        events = data.get('events')
        div = events.get('dividends') if events else ''
        if div is None or div == '': return {}
        dividends = {'symbol' : data.get('meta').get('symbol')}
        dividends['date'] = [div.get(k).get('date') for k, v in div.items()]
        dividends['action'] = 'dividend'
        dividends['value'] = [div.get(k).get('amount') for k, v in div.items()]
        return dividends

    def getsplits(self, data):
        events = data.get('events')
        splits = events.get('splits') if events else ''
        if splits is None or splits == '': return {}
        d_splits = {'symbol' : data.get('meta').get('symbol')}
        d_splits['date'] = [splits.get(k).get('date') for k, v in splits.items()]
        d_splits['action'] = 'splits'
        d_splits['value'] = [splits.get(k).get('numerator')/splits.get(k).get('denominator') for k, v in splits.items()]
        return d_splits


    def getchartresult(self, symbol, startdt, interval):
        params = {}
        params['period1']  = int(arrow.get(startdt).timestamp())
        params['period2']  = 9999999999
        # params['period2']  = arrow.now().shift(days=1).timestamp
        params['interval'] = interval
        if interval == '1d': params['events'] = 'div,split'
        params['includePrePost'] = 'true'
        url = f'{self.url_yfprice}/{symbol}'
        with requests.Session() as session:
            session.mount(url, HTTPAdapter(max_retries=self.request_max_retries))
            response = session.get(url, params=params)
        return json.loads(response.text)


    def gethistdata(self, symbol, startdt):
        symbol = symbol.upper()
        try:
            dlydata = self.getchartresult(symbol, startdt, '1d')
            wlydata = self.getchartresult(symbol, startdt, '1wk')
            mlydata = self.getchartresult(symbol, startdt, '1mo')
            dlydata = dlydata.get('chart').get('result')[0]
            wlydata = wlydata.get('chart').get('result')[0]
            mlydata = mlydata.get('chart').get('result')[0]
            if dlydata == '' or dlydata is None :
                return [{}, {}, {}, {}, {}]
            dlyquotes, wlyquotes, mlyquotes = self.getquotes(dlydata), self.getquotes(wlydata), self.getquotes(mlydata)
            dividends, splits = self.getdividends(dlydata), self.getsplits(dlydata)
            if dlyquotes == {}:
                self.msglogger.info(f'no hist price for {symbol}')
                return [{}, {}, {}, {}, {}]
            return [dlyquotes, wlyquotes, mlyquotes, dividends, splits]
        except:
            return [{}, {}, {}, {}, {}]
