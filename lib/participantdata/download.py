import json
import requests
import arrow
import time
import pandas as pd
from requests.adapters import HTTPAdapter

from nsedata.lib.logger import Logger
from nsedata.lib.config import Config
from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils  import Utility


class ParticipantData(Logger, Config):

    def __init__(self):
        Config.__init__(self)
        self.startdt = f"{arrow.now().format('YYYY')}-01-01"
        self.tbl = {
              'oi'  : self.tbl_partywiseoi
            , 'vol' : self.tbl_partywisevol
            , 'fiistat' : self.tbl_fiistats }
        self.func = {
              'oi'  : self.getoi
            , 'vol' : self.getvol
            , 'fiistat' : self.getfiistats }
        self.msg = {
              'oi'  : 'participant wise OI'
            , 'vol' : 'participant wise volume'
            , 'fiistat' : 'FII Stats' }
        self.oicols = ['date', 'clienttp'
            , 'indexfutlong', 'indexfutshort'
            , 'stockfutlong', 'stockfutshort'
            , 'indexcalllong', 'indexputlong', 'indexcallshort', 'indexputshort'
            , 'stockcalllong', 'stockputlong', 'stockcallshort', 'stockputshort']


    def getoi(self, date):
        dt  = date.format('DDMMYYYY')
        url = f'{self.url_partywiseoi}_{dt}.csv'
        try:
            df  = pd.read_csv(url, skiprows=1).iloc[:, :-2]
            df.insert(loc = 0, column = 'date', value = date.format("YYYY-MM-DD"))
            df.columns = self.oicols
        except:
            df = pd.DataFrame()
        return df


    def getvol(self, date):
        dt  = date.format('DDMMYYYY')
        url = f'{self.url_partywisevol}_{dt}.csv'
        try:
            df  = pd.read_csv(url,  skiprows=1).iloc[:, :-2]
            df.insert(loc = 0, column = 'date', value = date.format("YYYY-MM-DD"))
            df.columns = self.oicols
        except:
            df = pd.DataFrame()
        return df


    def getfiistats(self, date):
        dt  = date.format('DD-MMM-YYYY')
        url = f'{self.url_fiistats}_{dt}.xls'
        try:
            df = pd.read_excel(url).iloc[2:6]
            df.insert(loc = 0, column = 'date', value = date.format("YYYY-MM-DD"))
            df.columns = ['date', 'type', 'contractsbought', 'buyamt', 'contractssold', 'sellamt', 'eodoi', 'netamt']
        except:
            df = pd.DataFrame()
        return df


    @SqLite.connector
    def getmaxdate(self, tbl):
        try :
            query = f"select max(date) date from {tbl}"
            dt = pd.read_sql(query, SqLite.conn).date.to_list()[0]
            dt = arrow.get(f'{dt} 19:00')
            dt = dt.shift(days=+1)
        except:
            dt = self.startdt
            dt = arrow.get(dt+' 19:00')
        return dt

    @Utility.timer
    def download(self, type, loadtotable):
        df = pd.DataFrame()
        dt = self.getmaxdate(self.tbl[type])
        print(f"Downloading {self.msg[type]} data from {dt.format('YYYY-MM-DD')} to {arrow.now().format('YYYY-MM-DD')}", end='...', flush=True)
        dates = Utility.getworkingdays(dt, arrow.now())
        dfs = [self.func[type](date) for date in dates]
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            df = Utility.adddatefeatures(df)
        print('Completed !')
        if not df.empty : SqLite.appendtable(df, self.tbl[type])
        if not loadtotable: return df
