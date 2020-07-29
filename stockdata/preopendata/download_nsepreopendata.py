import requests
import json
import arrow
import os
import pandas as pd
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED

from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

class MarketPreOpen(Config):

    def __init__(self):
        Config.__init__(self)

    def getjsonstr(self):
        headers = { "User-Agent": self.user_agent}
        response = requests.get(self.nse_preopenurl, headers=headers)
        json_str = json.loads(response.text)
        return json_str['data']

    def getnsepreopendf(self, data):
        plist = []
        for i in range(len(data)):
            x = {}
            x['symbol'] = data[i]['metadata']['symbol']
            x['time']   = data[i]['detail']['preOpenMarket']['lastUpdateTime']
            x['prevclose']   = data[i]['metadata']['previousClose']
            x['open']  = data[i]['detail']['preOpenMarket']['finalPrice']
            x['pricechange'] = data[i]['metadata']['change']
            x['pricechangepct'] = data[i]['metadata']['pChange']
            x['yearlow'] = data[i]['metadata']['yearLow']
            x['yearhigh'] = data[i]['metadata']['yearHigh']
            x['volume'] = data[i]['detail']['preOpenMarket']['totalTradedVolume']
            x['sellqty']= data[i]['detail']['preOpenMarket']['totalSellQuantity']
            x['buyqty'] = data[i]['detail']['preOpenMarket']['totalBuyQuantity']
            plist.append(x)
        df = pd.DataFrame(plist)
        df['time'] = pd.to_datetime(df['time'])
        df['openingtype'] = df['pricechange'].apply(lambda x: 'No-Gap' if x == 0 else ('Gap-Up' if x > 0 else 'Gap-Down'))
        return df

    @Utility.timer
    def download(self):
        tblname = self.tbl_nsepreopen
        print(f'Downloading NSE Pre-open prices', end='...', flush=True)
        data = self.getjsonstr()
        df = self.getnsepreopendf(data)
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
        date = arrow.get(df.iloc[0,1]).format('YYYYMMDD')
        print(f'Completed [{date}]')
        SqLite.loadtable(df, tblname)
