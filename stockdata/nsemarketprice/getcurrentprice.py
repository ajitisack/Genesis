import json
import arrow
import requests
import pandas as pd

from requests.adapters import HTTPAdapter

from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

class CurrentPrice():

    def getjsonstr(self, index):
        headers = { "User-Agent": self.user_agent}
        params = {'index' : index.upper()}
        response = requests.get(self.nse_equitypriceurl, headers=headers, params=params)
        json_str = json.loads(response.text)
        return json_str

    def getcurrentprice(self, json_str):
        plist = []
        data = json_str['data']
        for i in range(len(data)):
            x = {}
            d = data[i]
            x['symbol']         = d['symbol']
            x['industry']       = d.get('meta').get('industry') or ''
            x['open']           = d['open']
            x['low']            = d['dayLow']
            x['high']           = d['dayHigh']
            x['lastprice']      = d['lastPrice']
            x['prevclose']      = d['previousClose']
            x['pricechange']    = d['change']
            x['pricechangepct'] = d['pChange']
            x['volume']         = d['totalTradedVolume']
            x['value']          = d['totalTradedValue']
            x['yearhigh']       = d['yearHigh']
            x['yearlow']        = d['yearLow']
            plist.append(x)
        df = pd.DataFrame(plist)
        df['industry'] = df['industry'].apply(lambda x: x.title())
        df['time'] = pd.to_datetime(json_str['metadata']['timeVal'])
        df['open'] = df['open'].astype(float)
        df['prevclose'] = df['prevclose'].astype(float)
        df['openingchange'] = df['open'] - df['prevclose']
        df['openingtype'] = df['openingchange'].apply(lambda x: 'No-Gap' if x == 0 else ('Gap-Up' if x > 0 else 'Declines'))
        df['movement'] = df['pricechange'].apply(lambda x: 'No-Change' if x == 0 else ('Advances' if x > 0 else 'Declines'))
        return df
