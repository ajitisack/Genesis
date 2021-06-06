import json
import arrow
import requests
import pandas as pd

from requests.adapters import HTTPAdapter

from nsedata.lib.config import Config
from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils  import Utility
from nsedata.lib.livemarket.getltp import LastTradedPrice

class LiveMarket(LastTradedPrice, Config):

    def __init__(self):
        Config.__init__(self)

    @Utility.timer
    def downloadindicesltp(self):
        print(f'Downloading Current Price of All NSE Indices', end='...', flush=True)
        json_str = self.getjsonstr(self.url_symbolsltp)
        df = self.getindicesltp(json_str)
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm:ss')
        print(f'Completed !')
        SqLite.loadtable(df, self.tbl_symbolsltp)

    @Utility.timer
    def downloadsymbolsltp(self):
        print(f'Downloading Current Price of NSE SECURITIES IN F&O', end='...', flush=True)
        json_str = self.getjsonstr(self.url_indicesltp)
        df = self.getsymbolsltp(json_str)
        return df
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm:ss')
        print(f'Completed !')
        SqLite.loadtable(df, self.tbl_indicesltp)
