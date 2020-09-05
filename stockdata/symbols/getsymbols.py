import pandas as pd
import arrow
from collections import defaultdict

from stockdata.utils import Utility
from stockdata.sdlogger import SDLogger
from stockdata.config import Config
from stockdata.sqlite import SqLite

class Symbols(SDLogger, Config):

    def __init__(self):
        Config.__init__(self)

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
        df = pd.read_csv(self.nselist, names = cols, header=0)
        df['name'] = df['name'].apply(lambda x : self.cleanstr(x))
        # df['dateoflisting'] = df['dateoflisting'].astype('datetime64[D]')
        df.fillna('', inplace=True)
        new_cols = ['isin', 'symbol', 'name', 'series', 'dateoflisting', 'paidupvalue', 'marketlot', 'facevalue']
        return df[new_cols]

    def getallsymbols(self):
        df = self.getnsesymbols()
        df = Utility.reducesize(df)
        df.fillna('', inplace=True)
        df['dateoflisting'] = df['dateoflisting'].apply(lambda x: '1900-01-01' if x == '' else x)
        df['dateoflisting'] = pd.to_datetime(df['dateoflisting'])
        # re-order columns
        df.sort_values('symbol', inplace=True, ignore_index=True)
        new_cols = ['isin', 'symbol', 'name', 'facevalue', 'series', 'dateoflisting', 'paidupvalue', 'marketlot']
        df = df[new_cols]
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
        return df
        # with pd.ExcelWriter(self.excel_seclist) as writer:
        #     bse.to_excel(writer, sheet_name='BSE', index=False, freeze_panes=(1,0))
        #     nse.to_excel(writer, sheet_name='NSE', index=False, freeze_panes=(1,0))
        #     df.to_excel(writer, sheet_name='All', index=False, freeze_panes=(1,0))

    @Utility.timer
    def download(self):
        tblname = self.tbl_nsesymbols
        print(f'Fetching list of all NSE Equities', end='...', flush=True)
        df = self.getallsymbols()
        print('Completed')
        SqLite.loadtable(df, tblname)
        # SqLite.createindex(tblname, 'symbol')
