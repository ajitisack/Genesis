import os
import sys
import json
import arrow
import requests
import pandas as pd
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED

from nsedata.lib.config import Config
from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils import Utility

class MarketPreOpen(Config):

    def __init__(self):
        Config.__init__(self)

    def getjsonstr(self):
        headers = { "User-Agent": self.user_agent}
        cookies = { 'nsit' : self.nsit, 'nseappid': self.nseappid}
        response = requests.get(self.url_preopen, headers=headers, cookies=cookies)
        if response.status_code != 200:
            sys.exit(response)
        json_str = json.loads(response.text)
        return json_str['data']

    def getnsepreopendf(self, data):
        plist = []
        for i in range(len(data)):
            x = {}
            d = data[i]['metadata']
            x['symbol']         = d['symbol']
            x['prevclose']      = Utility.asfloat(d['previousClose'])
            x['open']           = Utility.asfloat(d['lastPrice'])
            x['pricechange']    = Utility.asfloat(d['change'])
            x['pricechangepct'] = Utility.asfloat(d['pChange'])
            x['yearlow']        = Utility.asfloat(d['yearLow'])
            x['yearhigh']       = Utility.asfloat(d['yearHigh'])
            x['volume']         = Utility.asint(d['finalQuantity'])
            x['marketcap']      = Utility.asfloat(d['marketCap'])
            plist.append(x)
        df = pd.DataFrame(plist)
        return df

    @Utility.timer
    def download(self, loadtotable):
        tblname = self.tbl_preopen
        print(f'Downloading NSE Pre-open prices', end='...', flush=True)
        data = self.getjsonstr()
        df = self.getnsepreopendf(data)
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm:ss')
        print(f'Completed !')
        if not loadtotable: return df
        SqLite.loadtable(df, tblname)
