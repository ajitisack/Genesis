import json
import requests
import arrow
import time
import pandas as pd


from nsedata.lib.logger import Logger
from nsedata.lib.config import Config
from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils  import Utility


class ParticipantData(Logger, Config, Utility):

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
        url = f"{self.url_partywiseoi}_{date.format('DDMMYYYY')}.csv"
        print(f'{date.format("YYYY-MMM-DD")}', end=' : ', flush=True)
        try:
            df  = pd.read_csv(url, skiprows=1).iloc[:, :-2]
            df.insert(loc = 0, column = 'date', value = date.format("YYYY-MM-DD"))
            df.columns = self.oicols
        except:
            df = pd.DataFrame()
        print('Completed!')
        return df


    def getvol(self, date):
        url = f"{self.url_partywisevol}_{date.format('DDMMYYYY')}.csv"
        print(f'{date.format("YYYY-MMM-DD")}', end=' : ', flush=True)
        try:
            df  = pd.read_csv(url,  skiprows=1).iloc[:, :-2]
            df.insert(loc = 0, column = 'date', value = date.format("YYYY-MM-DD"))
            df.columns = self.oicols
        except:
            df = pd.DataFrame()
        print('Completed!')
        return df


    def getfiistats(self, date):
        url = f"{self.url_fiistats}_{date.format('DD-MMM-YYYY')}.xls"
        print(f'{date.format("YYYY-MMM-DD")}', end=' : ', flush=True)
        try:
            df = pd.read_excel(url).iloc[2:6]
            df.insert(loc = 0, column = 'date', value = date.format("YYYY-MM-DD"))
            df.columns = ['date', 'type', 'contractsbought', 'buyamt', 'contractssold', 'sellamt', 'eodoi', 'netamt']
        except:
            df = pd.DataFrame()
        print('Completed!')
        return df


    @Utility.timer
    def download(self, type, startdt=None, enddt=None):
        df = pd.DataFrame()
        dt = arrow.get(startdt) if startdt else self.getmaxdate(self.tbl[type])
        enddt = arrow.get(enddt) if enddt else arrow.now()
        dates = self.getworkingdays(dt, enddt)
        if not dates:
            print(f'{type} data - All upto date!')
            return None
        print(f"Downloading {self.msg[type]} data from {dt.format('YYYY-MMM-DD')} to {enddt.format('YYYY-MMM-DD')}")
        dfs = [self.func[type](date) for date in dates]
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            df = Utility.adddatefeatures(df)
            df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm:ss')
        if not df.empty : SqLite.appendtable(df, self.tbl[type])
        return None
