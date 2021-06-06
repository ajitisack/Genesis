import arrow
import requests
import pandas as pd

from nsedata.lib.config import Config
from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils  import Utility

class IndicesPrice(Config, Utility):

    def __init__(self):
        Config.__init__(self)
        self.startdt = f"{arrow.now().format('YYYY')}-05-01"


    def getIndicesHist(self, date):
        url = f'{self.url_indiceshprice}{date.format("DDMMYYYY")}.csv'
        print(f'{date.format("YYYY-MMM-DD")}', end=' : ', flush=True)
        try:
            r = requests.get(url)
            if r.status_code == 404: return pd.DataFrame()
            cols = ['indexname', 'date', 'open', 'high', 'low', 'close', 'chng', 'chng_pct', 'vol', 'turnoverincr', 'pe', 'pb', 'divyield']
            df = pd.read_csv(url, skiprows = 1, names = cols)
            df.drop(['date'], axis=1, inplace=True)
            df.insert(loc = 0, column = 'date', value = date.format("YYYY-MM-DD"))
        except:
            df = pd.DataFrame()
        print('Completed!')
        return df


    @Utility.timer
    def download(self, startdt=None, enddt=None):
        df = pd.DataFrame()
        dt = arrow.get(startdt) if startdt else self.getmaxdate(self.tbl_indiceshistprice)
        enddt = arrow.get(enddt) if enddt else arrow.now()
        dates = self.getworkingdays(dt, enddt)
        if not dates:
            print('Indices Historical Prices - All upto date!')
            return None
        print(f"Downloading Indices Prices from {dt.format('YYYY-MMM-DD')} to {enddt.format('YYYY-MMM-DD')}")
        dfs = [self.getIndicesHist(date) for date in dates]
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            df = Utility.adddatefeatures(df)
            df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm:ss')
        if not df.empty : SqLite.appendtable(df, self.tbl_indiceshistprice)
