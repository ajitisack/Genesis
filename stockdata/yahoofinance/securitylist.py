import requests as requests
import pandas as pd
import json
import arrow
import re
import requests
from collections import defaultdict

from ..utils import Utility
from ..sdlogger import SDLogger

class SecurityList(SDLogger):

    def getbselist(self):
        df = pd.read_csv(self.bselist)
        df = df[df['Status']=='Active']
        df.drop(['Instrument', 'Issuer Name', 'Status', 'Security Code'], axis=1, inplace=True)
        df.columns = ['symbol', 'name', 'grp', 'facevalue', 'isin', 'industry']
        df['industry'] = df.apply(lambda x: x['industry'] if x['industry'].strip() != '' else 'Index Fund', axis=1)
        df = df.applymap(lambda x: Utility.cleanstr(x) if type(x) == str else x)
        df.fillna('', inplace=True)
        df.sort_values('symbol', inplace=True)
        return df

    def getnselist(self):
        df = pd.read_csv(self.nselist)
        df.drop([' SERIES', ' DATE OF LISTING', ' PAID UP VALUE', ' MARKET LOT'], axis=1, inplace=True)
        df.columns = ['symbol', 'name', 'isin', 'facevalue']
        df = df.applymap(lambda x: Utility.cleanstr(x) if type(x) == str else x)
        df.fillna('', inplace=True)
        df.sort_values('symbol', inplace=True)
        return df

    def getsecuritylist(self):
        bse = self.getbselist()
        nse = self.getnselist()
        value = lambda x, y: y if pd.isnull(x) else x
        df = pd.merge(bse, nse, how='outer', on='symbol')
        df['name'] = df.apply(lambda x: value(x['name_x'], x['name_y']), axis=1)
        df['facevalue'] = df.apply(lambda x: value(x['facevalue_x'], x['facevalue_y']), axis=1)
        df['isin'] = df.apply(lambda x: value(x['isin_x'], x['isin_y']), axis=1)
        df['inbse'] = df.apply(lambda x: 1 if x['symbol'] in list(bse.symbol) else 0, axis=1)
        df['innse'] = df.apply(lambda x: 1 if x['symbol'] in list(nse.symbol) else 0, axis=1)
        df.drop(['name_x', 'name_y', 'facevalue_x', 'facevalue_y', 'isin_x', 'isin_y'], axis=1, inplace=True)
        df.fillna('', inplace=True)
        df.sort_values('symbol', inplace=True)
        columns = ['symbol', 'inbse', 'innse', 'name', 'grp', 'industry', 'facevalue', 'isin']
        df = df[columns]
        # with pd.ExcelWriter(self.excel_seclist) as writer:
        #     bse.to_excel(writer, sheet_name='BSE', index=False, freeze_panes=(1,0))
        #     nse.to_excel(writer, sheet_name='NSE', index=False, freeze_panes=(1,0))
        #     df.to_excel(writer, sheet_name='All', index=False, freeze_panes=(1,0))
        return df
