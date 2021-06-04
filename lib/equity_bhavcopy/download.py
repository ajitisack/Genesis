import arrow
import requests
import pandas as pd

from nsedata.lib.config import Config
from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils  import Utility

class EquityBhavcopy(Config, Utility):

    def __init__(self):
        Config.__init__(self)
        self.startdt = f"{arrow.now().format('YYYY')}-05-01"


    def getEquityBhavcopy(self, date):
        url = f'{self.url_eqbhavcopy}{date.format("DDMMYYYY")}.csv'
        print(f'{date.format("YYYY-MMM-DD")}', end=' : ', flush=True)
        try:
            r = requests.get(url)
            if r.status_code == 404: return pd.DataFrame()
            df = pd.read_csv(url)
            cols = ['symbol', 'series', 'date', 'prevclose', 'open', 'high', 'low', 'ltp', ' close', 'avgprice', 'quantity', 'turnoverinlakhs', 'totaltrades', 'deliveryqty', 'deliverypct']
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
        dt = arrow.get(startdt) if startdt else self.getmaxdate(self.tbl_eqbhavcopy)
        enddt = arrow.get(enddt) if enddt else arrow.now()
        dates = self.getworkingdays(dt, enddt)
        if not dates:
            print('Indices Historical Prices - All upto date!')
            return None
        print(f"Downloading Equity Bhavcopy data from {dt.format('YYYY-MMM-DD')} to {enddt.format('YYYY-MMM-DD')}")
        dfs = [self.getEquityBhavcopy(date) for date in dates]
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            df = Utility.adddatefeatures(df)
        if not df.empty : SqLite.appendtable(df, self.tbl_eqbhavcopy)
