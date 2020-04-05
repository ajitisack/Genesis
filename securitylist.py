import requests as requests
import pandas as pd
import json
import arrow
import re
import requests

from sqlite import SqlLite
from utils import Utility
from collections import defaultdict

class Security():

    tblname    = 'security'
    indexcol   = 'symbol'

    basepath = 'c:\\ajit\\stockanalysis'
    bselist = f'{basepath}\\Equity.csv'
    nselist = 'https://www1.nseindia.com/content/equities/EQUITY_L.csv'
    excelfile = f'{basepath}\\SecurityList.xlsx'

    @staticmethod
    def getbselist():
        df = pd.read_csv(Security.bselist)
        df = df[df['Status']=='Active']
        df.drop(['Instrument', 'Issuer Name', 'Status', 'Security Code'], axis=1, inplace=True)
        df.columns = ['symbol', 'name', 'group', 'facevalue', 'isin', 'industry']
        df['industry'] = df.apply(lambda x: x['industry'] if x['industry'].strip() != '' else 'Index Fund', axis=1)
        df = df.applymap(lambda x: Utility.cleanstr(x) if type(x) == str else x)
        df.fillna('', inplace=True)
        df.sort_values('symbol', inplace=True)
        return df

    @staticmethod
    def getnselist():
        df = pd.read_csv(Security.nselist)
        df.drop([' SERIES', ' DATE OF LISTING', ' PAID UP VALUE', ' MARKET LOT'], axis=1, inplace=True)
        df.columns = ['symbol', 'name', 'isin', 'facevalue']
        df = df.applymap(lambda x: Utility.cleanstr(x) if type(x) == str else x)
        df.fillna('', inplace=True)
        df.sort_values('symbol', inplace=True)
        return df

    @staticmethod
    def getlist():
        bse = Security.getbselist()
        nse = Security.getnselist()
        value = lambda x, y: y if pd.isnull(x) else x
        df = pd.merge(bse, nse, how='outer', on='symbol')
        df['name'] = df.apply(lambda x: value(x['name_x'], x['name_y']), axis=1)
        df['facevalue'] = df.apply(lambda x: value(x['facevalue_x'], x['facevalue_y']), axis=1)
        df['isin'] = df.apply(lambda x: value(x['isin_x'], x['isin_y']), axis=1)
        df.drop(['name_x', 'name_y', 'facevalue_x', 'facevalue_y', 'isin_x', 'isin_y'], axis=1, inplace=True)
        df['inbse'] = df.apply(lambda x: 1 if x['symbol'] in list(bse.symbol) else 0, axis=1)
        df['innse'] = df.apply(lambda x: 1 if x['symbol'] in list(nse.symbol) else 0, axis=1)
        df.fillna('', inplace=True)
        df.sort_values('symbol', inplace=True)
        columns = ['symbol', 'inbse', 'innse', 'name', 'group', 'industry', 'facevalue', 'isin']
        df = df[columns]
        with pd.ExcelWriter(Security.excelfile) as writer:
            bse.to_excel(writer, sheet_name='BSE', index=False, freeze_panes=(1,0))
            nse.to_excel(writer, sheet_name='NSE', index=False, freeze_panes=(1,0))
            df.to_excel(writer, sheet_name='All', index=False, freeze_panes=(1,0))
        return df

    @staticmethod
    @Utility.timer
    @SqlLite.connector
    def loadlist():
        tblname   = Security.tblname
        indexcol  = Security.indexcol
        indexname = f'index_{tblname}_{indexcol}'
        print(f'Fetching list of all BSE and NSE Equities', end='...', flush=True)
        df = Security.getlist()
        print('Completed')
        print(f'Refreshing table [{tblname}] with {df.shape[0]} symbols', end='...', flush=True)
        df.to_sql(tblname, SqlLite.conn, if_exists='replace', index=False)
        print('Completed')
        print(f'Creating index on {tblname}({indexcol})', end='...', flush=True)
        create_index = f'create index if not exists {indexname} on {tblname}({indexcol});'
        SqlLite.conn.cursor().execute(create_index)
        print('Completed')

if __name__ == '__main__':
    Security.loadlist()
