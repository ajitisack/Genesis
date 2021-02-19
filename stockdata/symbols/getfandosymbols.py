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

class MarketPreOpen1(Config):

    def __init__(self):
        Config.__init__(self)

    def getjsonstr(self):
        headers = { "User-Agent": self.user_agent}
        params = {}
        params['index']  = 'NIFTY 50'
        response = requests.get(self.nse_eqpriceurl, headers=headers, params=params)
        json_str = json.loads(response.text)
        return json_str['data']

    def getfandosymbols(self, data):
        plist = []
        for i in range(len(data)):
            x = {}
            d = data[i]
            x['symbol'] = d['symbol']
            # x['name'] = d['meta']['companyName']
            # x['industry'] = d.get(['meta']).get(['industry'])
            x['open'] = d['open']
            x['lastprice'] = d['lastPrice']
            x['prevclose'] = d['previousClose']
            plist.append(x)
        df = pd.DataFrame(plist)
        # df['time'] = pd.to_datetime(df['time'])
        # df['openingtype'] = df['pricechange'].apply(lambda x: 'No-Gap' if x == 0 else ('Gap-Up' if x > 0 else 'Gap-Down'))
        return df

    @Utility.timer
    def download(self):
        tblname = self.tbl_nsepreopen
        print(f'Downloading NSE Pre-open prices', end='...', flush=True)
        data = self.getjsonstr()
        df = self.getfandosymbols(data)
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
        # date = arrow.get(df.iloc[0,1]).format('YYYYMMDD')
        # print(f'Completed [{date}]')
        # SqLite.loadtable(df, tblname)
        return df

x = MarketPreOpen()

df = x.download()


df
