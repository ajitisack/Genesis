import json
import requests
import arrow
import time
import pandas as pd
import io
from zipfile import ZipFile

from nsedata.lib.logger import Logger
from nsedata.lib.config import Config
from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils  import Utility


class FNOBhavcopy(Logger, Config, Utility):

    def __init__(self):
        Config.__init__(self)
        self.startdt = f"{arrow.now().format('YYYY')}-05-01"


    def getFNOBhavcopy(self, date):
        url = f'{self.url_fnobhavcopy}/{date.format("YYYY")}/{date.format("MMM").upper()}/fo{date.format("DDMMMYYYY").upper()}bhav.csv.zip'
        print(f'{date.format("YYYY-MMM-DD")}', end=' : ', flush=True)
        try:
            r = requests.get(url)
            if r.status_code == 404: return pd.DataFrame()
            cols = ['instrument', 'symbol', 'expirydt', 'strikeprice', 'optiontp', 'open', 'high', 'low', 'close', 'settleprice', 'contracts', 'valueinlakhs', 'oi', 'oichng', 'colx', 'coly']
            df = pd.read_csv(url, skiprows = 1, names = cols)
            df.drop(['colx', 'coly'], axis=1, inplace=True)
            df.insert(loc = 0, column = 'date', value = date.format("YYYY-MM-DD"))
        except:
            df = pd.DataFrame()
        print('Completed!')
        return df


    @Utility.timer
    def download(self):
        df = pd.DataFrame()
        dt = self.getmaxdate(self.tbl_fnobhavcopy)
        enddt = arrow.now()
        dates = self.getworkingdays(dt, enddt)
        if not dates:
            print('FNO Bhavcopy - All upto date!')
            return None
        print(f"Downloading FNO Bhavcopy data from {dt.format('YYYY-MM-DD')} to {arrow.now().format('YYYY-MM-DD')}")
        dfs = [self.getFNOBhavcopy(date) for date in dates]
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            df = Utility.adddatefeatures(df)
        if not df.empty : SqLite.appendtable(df, self.tbl_fnobhavcopy)
