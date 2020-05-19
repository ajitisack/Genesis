import json
import requests
import arrow
from requests.adapters import HTTPAdapter

class RealTimeDataDict():

    def getquotes(self, data):
        try:
            quotes = data.get('indicators').get('quote')[0]
            if quotes == {}: return {}
            hist = {}
            hist['timestamp'] = data.get('timestamp')
            hist['symbol'] = data.get('meta').get('symbol')
            hist['exchange'] = data.get('meta').get('exchangeName')
            hist['open'] = quotes.get('open')
            hist['low'] = quotes.get('low')
            hist['high'] = quotes.get('high')
            hist['close'] = quotes.get('close')
            hist['volume'] = quotes.get('volume')
            return hist
        except:
            return {}

    def getchartresult(self, symbol, startdt, enddt):
        try:
            params = {}
            params['period1']  = startdt.timestamp
            params['period2']  = enddt.timestamp
            params['interval'] = '1m'
            url = f'{self.yfqueryurl}/{symbol}'
            with requests.Session() as session:
                session.mount(url, HTTPAdapter(max_retries=self.request_max_retries))
                response = session.get(url, params=params)
            chartdata = json.loads(response.text).get('chart').get('result')[0]
            return chartdata
        except:
            return None

    def getrealtimedata(self, symbol):
        quotes = []
        symbol = symbol.upper()
        startdt = arrow.now().to('local').shift(days=-29)
        while startdt <= arrow.now():
            enddt = startdt.shift(days=7)
            # print(f"Range -> {startdt.format('YYYY-MM-DD')} - {enddt.format('YYYY-MM-DD')}")
            data = self.getchartresult(symbol, startdt, enddt)
            quotes.append(self.getquotes(data))
            startdt = enddt
        return quotes
