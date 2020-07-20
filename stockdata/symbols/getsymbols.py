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
        .replace('Limited', '')\
        .title()

    def getnsefandosymbols(self):
        df = pd.read_csv(self.nsefosymbols)
        df.columns = ['symbol']
        df = df[~df.symbol.isin(['Code', 'NIFTY', 'BANKNIFTY'])]
        df['innsefo'] = 1
        return df

    def getnsesymbols(self):
        cols = ['symbol', 'name', 'series', 'dateoflisting', 'paidupvalue', 'marketlot', 'isin', 'facevalue']
        df = pd.read_csv(self.nselist, names = cols, header=0)
        df['name'] = df['name'].apply(lambda x : self.cleanstr(x))
        df['dateoflisting'] = df['dateoflisting'].astype('datetime64[D]')
        df.fillna('', inplace=True)
        new_cols = ['isin', 'symbol', 'name', 'series', 'dateoflisting', 'paidupvalue', 'marketlot', 'facevalue']
        return df[new_cols]

    def getbsesymbols(self):
        df = pd.read_csv(self.bselist)
        df.drop(['Security Code', 'Issuer Name', 'Status', 'Instrument'], axis = 1, inplace = True)
        df['Industry'] = df['Industry'].apply(str.strip)
        df = df[df['Industry'] != '']
        df.columns = ['symbol', 'name', 'group', 'facevalue', 'isin', 'industry']
        df['symbol'] = df['symbol'].apply(lambda x: x.replace('*', ''))
        df['name'] = df['name'].apply(self.cleanstr)
        df.fillna('', inplace=True)
        new_cols = ['isin', 'symbol', 'name', 'group', 'facevalue', 'industry']
        return df[new_cols]

    def getallsymbols(self):
        bse = self.getbsesymbols()
        nse = self.getnsesymbols()
        df = pd.merge(nse, bse, how='outer', on='isin')
        value = lambda x, y: y if pd.isnull(x) else x
        df['symbol'] = df.apply(lambda x: value(x['symbol_x'], x['symbol_y']), axis=1)
        df['name'] = df.apply(lambda x: value(x['name_x'], x['name_y']), axis=1)
        df['facevalue'] = df.apply(lambda x: value(x['facevalue_x'], x['facevalue_y']), axis=1)
        df.drop(['name_x', 'name_y', 'facevalue_x', 'facevalue_y'], axis=1, inplace=True)
        df.rename(columns={'symbol_x': 'nsesymbol', 'symbol_y': 'bsesymbol'}, inplace=True)
        df['innse'] = df['nsesymbol'].apply(lambda x: 1 if x in list(nse.symbol) else 0)
        df['inbse'] = df['bsesymbol'].apply(lambda x: 1 if x in list(bse.symbol) else 0)
        df['inall'] = df.apply(lambda x: 1 if x['innse']==1 and x['inbse']==1 else 0, axis=1)
        df = Utility.reducesize(df)
        df.fillna('', inplace=True)
        df['dateoflisting'] = df['dateoflisting'].apply(lambda x: '1900-01-01' if x == '' else x)
        df['dateoflisting'] = pd.to_datetime(df['dateoflisting'])
        # include idenitifer for futures and options listed symbols
        df_fo = self.getnsefandosymbols()
        df = pd.merge(df, df_fo, how='outer', on='symbol')
        df['innsefo'].fillna(0, inplace=True)
        # re-order columns
        df.sort_values('symbol', inplace=True, ignore_index=True)
        new_cols = ['isin', 'symbol', 'innse', 'inbse', 'inall', 'innsefo', 'nsesymbol', 'bsesymbol', 'name', 'industry', 'facevalue', 'group', 'series', 'dateoflisting', 'paidupvalue', 'marketlot']
        df = df[new_cols]
        # include rundate
        df['rundt'] = arrow.now().format('YYYY-MM-DD')
        # with pd.ExcelWriter(self.excel_seclist) as writer:
        #     bse.to_excel(writer, sheet_name='BSE', index=False, freeze_panes=(1,0))
        #     nse.to_excel(writer, sheet_name='NSE', index=False, freeze_panes=(1,0))
        #     df.to_excel(writer, sheet_name='All', index=False, freeze_panes=(1,0))
        return df

    @Utility.timer
    def download(self):
        tblname = self.tbl_symbols
        print(f'Fetching list of all BSE and NSE Equities', end='...', flush=True)
        df = self.getallsymbols()
        print('Completed')
        SqLite.loadtable(df, tblname)
        SqLite.createindex(tblname, 'symbol')
