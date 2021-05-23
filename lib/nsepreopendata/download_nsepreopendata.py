import os
import sys
import json
import arrow
import requests
import pandas as pd
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED

from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

class NSEMarketPreOpen(Config):

    def __init__(self):
        Config.__init__(self)

    def getjsonstr(self):
        headers = { "User-Agent": self.user_agent}
        response = requests.get(self.nse_preopenurl, headers=headers)
        if response.status_code != 200:
            sys.exit(response)
        json_str = json.loads(response.text)
        return json_str['data']

    def getnsepreopendf(self, data):
        plist = []
        for i in range(len(data)):
            x = {}
            d = data[i]
            x['symbol']         = d['symbol']
            x['prevclose']      = Utility.asfloat(d['pCls'])
            x['open']           = Utility.asfloat(d['iep'])
            x['pricechange']    = float(d['chn'])
            x['pricechangepct'] = float(d['perChn'])
            x['yearlow']        = Utility.asfloat(d['yLow'])
            x['yearhigh']       = Utility.asfloat(d['yHigh'])
            x['volume']         = Utility.asint(d['trdQnty'])
            x['marketcap']      = Utility.asfloat(d['mktCap'])
            plist.append(x)
        df = pd.DataFrame(plist)
        return df

    @Utility.timer
    def download(self):
        tblname = self.tbl_nsepreopen
        print(f'Downloading NSE Pre-open prices', end='...', flush=True)
        data = self.getjsonstr()
        df = self.getnsepreopendf(data)
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
        print(f'Completed !')
        SqLite.loadtable(df, tblname)
