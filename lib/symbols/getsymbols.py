import pandas as pd
import arrow
import requests
import json
from collections import defaultdict

from nsedata.lib.utils   import Utility
from nsedata.lib.logger  import Logger
from nsedata.lib.config  import Config
from nsedata.lib.sqlite  import SqLite

class Symbols(Logger, Config):

    def __init__(self):
        Config.__init__(self)

    def getfnosymbols(self):
        headers = { "User-Agent": self.user_agent}
        response = requests.get(self.url_symbolsltp, headers=headers)
        json_str = json.loads(response.text)
        fnosymbols = pd.DataFrame(json_str['data'])['symbol'].to_list()
        return fnosymbols

    def cleanstr(self, str):
        return str.strip()\
        .replace('&amp;','&')\
        .replace('&amp;','&')\
        .replace('-$','')\
        .replace('&#39;','\'')\
        .replace('&#160;', '')\
        .replace('(','')\
        .replace(')','')\
        .replace('*', '')\
        .replace('LTD.','')\
        .replace('Limited', '')

    def getnsesymbols(self):
        cols = ['symbol', 'name', 'series', 'dateoflisting', 'paidupvalue', 'marketlot', 'isin', 'facevalue']
        df = pd.read_csv(self.url_equitylist, names = cols, header=0)
        df['name'] = df['name'].apply(lambda x : self.cleanstr(x))
        # df['dateoflisting'] = df['dateoflisting'].astype('datetime64[D]')
        df.fillna('', inplace=True)
        fnosymbols = self.getfnosymbols()
        df[['fnoactivated']] = df.apply(lambda x: 1 if x['symbol'] in fnosymbols else 0, axis=1)
        new_cols = ['isin', 'symbol', 'name', 'fnoactivated', 'series', 'dateoflisting', 'paidupvalue', 'marketlot', 'facevalue']
        return df[new_cols]

    def getallsymbols(self):
        df = self.getnsesymbols()
        df = Utility.reducesize(df)
        df.fillna('', inplace=True)
        df['dateoflisting'] = df['dateoflisting'].apply(lambda x: '1900-01-01' if x == '' else x)
        df['dateoflisting'] = pd.to_datetime(df['dateoflisting'])
        # re-order columns
        df.sort_values('symbol', inplace=True, ignore_index=True)
        new_cols = ['isin', 'symbol', 'name', 'fnoactivated', 'facevalue', 'series', 'dateoflisting', 'paidupvalue', 'marketlot']
        df = df[new_cols]
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
        return df

    @Utility.timer
    def download(self):
        tblname = self.tbl_symbols
        print(f'Fetching list of all NSE Equities', end='...', flush=True)
        df = self.getallsymbols()
        print('Completed')
        SqLite.loadtable(df, tblname)
        # SqLite.createindex(tblname, 'symbol')
