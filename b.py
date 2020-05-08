import requests, json, re, arrow
import pandas as pd

startdt = arrow.now().to('local').shift(days=-29)
fromdt = startdt
startdt.format('YYYY-MM-DD')
while fromdt <= arrow.now():
    todt = fromdt.shift(days=7)
    print(f"Range -> {fromdt.format('YYYY-MM-DD')} - {todt.format('YYYY-MM-DD')}")
    fromdt = todt

params = {}
params['period1']  = arrow.get('2020-04-17').timestamp
params['period2']  = arrow.get('2020-04-24').timestamp
params['interval'] = '1m'
url = f'https://query1.finance.yahoo.com/v8/finance/chart/HDFCBANK.BO'
response = requests.get(url, params=params)
json.loads(response.text)
data = json.loads(response.text).get('chart').get('result')[0]
quotes = data.get('indicators').get('quote')[0]
hist = {}
hist['date'] = data.get('timestamp')
hist['symbol'] = data.get('meta').get('symbol')
hist['exchange'] = data.get('meta').get('exchangeName')
hist['open'] = quotes.get('open')
hist['low'] = quotes.get('low')
hist['high'] = quotes.get('high')
hist['close'] = quotes.get('close')
hist['volume'] = quotes.get('volume')
df = pd.DataFrame(hist)
df['date'] = df['date'].apply(lambda x: arrow.get(x).to('local').format('YYYY-MM-DD hh:mm:SS A'))
df
