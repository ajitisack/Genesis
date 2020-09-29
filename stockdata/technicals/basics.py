import arrow
import pandas as pd
import numpy as np
from statistics import mean

from stockdata.sqlite import SqLite

class BasicTechnicals():

    def getprevdayvalues(self, df):
        n = 1
        df['prevopen']   = df.groupby('symbol').open.transform(lambda x: x.shift(n))
        df['prevlow']    = df.groupby('symbol').low.transform(lambda x: x.shift(n))
        df['prevhigh']   = df.groupby('symbol').high.transform(lambda x: x.shift(n))
        df['prevclose']  = df.groupby('symbol').close.transform(lambda x: x.shift(n))
        df['prevvolume'] = df.groupby('symbol').volume.transform(lambda x: x.shift(n))
        return df

    def pricechange(self, df):
        df['pricechange'] = df.close - df.prevclose
        df['pricechangepct'] = df.groupby('symbol').close.transform(lambda x: round(x.pct_change(1), 4))
        df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
        df.fillna(0, inplace=True)
        return df

    def volumechange(self, df):
        df['volumechange'] = df.volume - df.prevvolume
        df['volumechangepct'] = df.groupby('symbol').volume.transform(lambda x: round(x.pct_change(1), 2))
        df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
        df['prevvolume'] = df['prevvolume'].astype(int)
        df['volumechange'] = df['volumechange'].astype(int)
        df.fillna(0, inplace=True)
        return df

    def othertechnicals(self, df):
        df['openinggap']  = df['open'] - df['prevclose']
        df['openingtype'] = df['openinggap'].apply(lambda x: 'No-Gap' if x == 0 else ('Gap-Up' if x > 0 else 'Gap-Down'))
        df['openinggappct'] = round(df['openinggap']/df['prevclose'], 4)
        df['closinggap'] = df['close'] - df['open']
        df['closinggappct'] = round(df['closinggap']/df['open'], 4)
        df['closingtype'] = df['closinggap'].apply(lambda x: 'No-Gap' if x == 0 else ('Above-Open' if x > 0 else 'Below-Open'))
        df['totalvalue'] = df['volume'] * (df['open'] + df['low'] + df['high'] + df['close'])/4
        df['prevtotalvalue'] = df['prevvolume'] * (df['prevopen'] + df['prevlow'] + df['prevhigh'] + df['prevclose'])/4
        df.drop(['prevopen'], axis=1, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df


    @SqLite.connector
    def createbasictechnicals(self, date):
        tblname = self.tbl_nsehprice
        query = f"select distinct date from {tblname} where date <= '{date}' order by 1 desc limit 2"
        currdt, prevdt  = pd.read_sql(query, SqLite.conn).date.to_list()
        query = f"select date, symbol, open, low, high, close, volume from {tblname} where date in ('{currdt}', '{prevdt}')"
        df = pd.read_sql(query, SqLite.conn)
        df = self.getprevdayvalues(df)
        df = self.pricechange(df)
        df = self.volumechange(df)
        df = df[df.date == currdt]
        # df = df[df.prevclose!=0]
        df = self.othertechnicals(df)
        return df
