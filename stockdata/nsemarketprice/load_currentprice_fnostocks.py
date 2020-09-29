import json
import arrow
import requests
import pandas as pd

from requests.adapters import HTTPAdapter

from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility
from stockdata.nsemarketprice.getcurrentprice import CurrentPrice

class CurrentPriceFNOSymbols(CurrentPrice, Config):

    def __init__(self):
        Config.__init__(self)

    @Utility.timer
    def download(self):
        tblname = self.tbl_nseeqcurrent
        url = self.nse_equitypriceurl
        print(f'Downloading Current Price of NSE SECURITIES IN F&O', end='...', flush=True)
        json_str = self.getjsonstr(url)
        df = self.getsymbolscurrentprice(json_str)
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
        print(f'Completed !')
        SqLite.loadtable(df, tblname)
