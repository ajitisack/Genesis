import json
import requests
import arrow
from requests.adapters import HTTPAdapter
import pandas as pd

def getquotes(data):
    try:
        quotes = data.get('indicators').get('quote')[0]
        if quotes == {}: return {}
        hist = {}
        hist['time'] = data.get('timestamp')
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

def getchartresult(symbol, startdt, enddt):
    try:
        params = {}
        params['period1']  = startdt.timestamp
        params['period2']  = enddt.timestamp
        params['interval'] = '1m'
        # url = f'{self.yfqueryurl}/{symbol}'
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}'
        with requests.Session() as session:
            # session.mount(url, HTTPAdapter(max_retries=self.request_max_retries))
            session.mount(url, HTTPAdapter(max_retries=5))
            response = session.get(url, params=params)
        chartdata = json.loads(response.text).get('chart').get('result')[0]
        return chartdata
    except:
        return None

def getrealtimedata(symbol):
    quotes = []
    symbol = symbol.upper()
    startdt = arrow.now().to('local').shift(days=-29)
    while startdt <= arrow.now():
        enddt = startdt.shift(days=7)
        # print(f"Range -> {startdt.format('YYYY-MM-DD')} - {enddt.format('YYYY-MM-DD')}")
        data = getchartresult(symbol, startdt, enddt)
        quotes.append(getquotes(data))
        startdt = enddt
    return quotes

q = getrealtimedata('HDFCBANK.BO')
df = pd.concat([pd.DataFrame(prices) for prices in q], ignore_index=True)
df['time'] = df['time'].apply(lambda x: arrow.get(x).to('local').format('YYYY-MM-DD hh:mm:SS A'))
df
