import json
import requests
import arrow
from requests.adapters import HTTPAdapter

from nsedata.lib.config import Config

class IntraDayDataDict():

    def __init__(self):
        Config.__init__(self)

    def getquotes(self, data):
        try:
            quotes = data.get('indicators').get('quote')[0]
            if quotes == {}: return {}
            hist = {}
            hist['timestamp'] = data.get('timestamp')
            hist['symbol'] = data.get('meta').get('symbol')
            hist['open'] = quotes.get('open')
            hist['low'] = quotes.get('low')
            hist['high'] = quotes.get('high')
            hist['close'] = quotes.get('close')
            hist['volume'] = quotes.get('volume')
            return hist
        except:
            return {}

    def getchartresult(self, symbol, date, interval):
        try:
            p1   = str(arrow.get(f'{date} 09:00:00 Asia/Calcutta', 'YYYY-MM-DD HH:mm:ss ZZZ').timestamp()).split('.')[0]
            p2   = str(arrow.get(f'{date} 16:00:00 Asia/Calcutta', 'YYYY-MM-DD HH:mm:ss ZZZ').timestamp()).split('.')[0]
            freq = interval
            url = f'{self.url_yfprice}/{symbol}?period1={p1}&period2={p2}&interval={freq}'
            with requests.Session() as session:
                session.mount(url, HTTPAdapter(max_retries=self.request_max_retries))
                response = session.get(url)
            chartdata = json.loads(response.text).get('chart').get('result')[0]
            return chartdata
        except:
            return None

    def getintradaydata(self, symbol, date, interval):
        quotes = []
        symbol = symbol.upper()
        data = self.getchartresult(symbol, date, interval)
        quotes = self.getquotes(data)
        return quotes
