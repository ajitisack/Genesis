import json
import arrow
import requests
import pandas as pd

from requests.adapters import HTTPAdapter

from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

class CurrentPriceAllIndices(Config):

    def __init__(self):
        Config.__init__(self)

    def getjsonstr(self):
        headers = { "User-Agent": self.user_agent}
        response = requests.get(self.nse_allindicespriceurl, headers=headers)
        json_str = json.loads(response.text)
        return json_str

    def getcurrentprice(self, json_str):
        plist = []
        data = json_str['data']
        for i in range(len(data)):
            x = {}
            d = data[i]
            x['key']            = d['key'].title()
            x['index']          = d['index']
            x['indexsymbol']    = d['indexSymbol']
            x['prevclose']      = d['previousClose']
            x['open']           = d['open']
            x['lastprice']      = d['last']
            x['pricechange']    = d['variation']
            x['pricechangepct'] = d['percentChange']
            x['low']            = d['low']
            x['high']           = d['high']
            x['yearhigh']       = d['yearHigh']
            x['yearlow']        = d['yearLow']
            x['advances']       = d.get('advances') or 0
            x['declines']       = d.get('declines') or 0
            x['unchanged']      = d.get('unchanged') or 0
            x['oneweekago']     = d.get('oneWeekAgo') or 0
            x['onemonthago']    = d.get('oneMonthAgo') or 0
            x['oneyearago']     = d.get('oneYearAgo') or 0
            plist.append(x)
        df = pd.DataFrame(plist)
        df['time'] = pd.to_datetime(json_str['timestamp'])
        df['openingchange'] = df['open'] - df['prevclose']
        df['openingtype'] = df['openingchange'].apply(lambda x: 'No-Gap' if x == 0 else ('Gap-Up' if x > 0 else 'Declines'))
        df['movement'] = df['pricechange'].apply(lambda x: 'No-Change' if x == 0 else ('Advances' if x > 0 else 'Declines'))
        return df

    @Utility.timer
    def download(self):
        tblname = self.tbl_nseindicescurrent
        print(f'Downloading Current Price of All NSE Indices', end='...', flush=True)
        json_str = self.getjsonstr()
        df = self.getcurrentprice(json_str)
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
        print(f'Completed')
        SqLite.loadtable(df, tblname)
