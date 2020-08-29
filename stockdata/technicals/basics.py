import arrow
import pandas as pd
import numpy as np
from statistics import mean

from stockdata.sqlite import SqLite

class BasicTechnicals():

    def pricechange(self, df, n=1):
        prevclose = 'prevclose' if n==1  else f'prevclose_{n}d'
        pricechange = 'pricechange' if n==1 else f'pricechange_{n}d'
        pricechangepct = 'pricechangepct' if n==1 else f'pricechangepct_{n}d'
        df[prevclose] = df.groupby('symbol').close.transform(lambda x: x.shift(n))
        df[pricechange] = df.close - df.prevclose
        df[pricechangepct] = df.groupby('symbol').close.transform(lambda x: round(x.pct_change(n) * 100,2))
        df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
        df.fillna(0, inplace=True)
        return df

    def volumechange(self, df, n=1):
        prevvolume = 'prevvolume' if n==1 else f'prevvolume_{n}d'
        volumechange = 'volumechange' if n==1 else f'volumechange_{n}d'
        volumechangepct = 'volumechangepct' if n==1 else f'volumechangepct_{n}d'
        df[prevvolume] = df.groupby('symbol').volume.transform(lambda x: x.shift(n))
        df[volumechange] = df.volume - df.prevvolume
        df[volumechangepct] = df.groupby('symbol').volume.transform(lambda x: round(x.pct_change(n) * 100,2))
        df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
        df['prevvolume'] = df['prevvolume'].astype(int)
        df['volumechange'] = df['volumechange'].astype(int)
        df.fillna(0, inplace=True)
        return df

    @SqLite.connector
    def createbasictechnicals(self):
        tblname = self.tbl_nsehprice
        query = f"select distinct date from {tblname} order by 1 desc limit 2"
        currdt, prevdt = pd.read_sql(query, SqLite.conn).date.to_list()
        query = f"select date, symbol, open, low, high, close, volume from {tblname} where date in ('{currdt}', '{prevdt}')"
        df = pd.read_sql(query, SqLite.conn)
        df = self.pricechange(df)
        df = self.volumechange(df)
        df = df[df.date == currdt]
        df = df[df.prevclose!=0]
        df['openinggap']  = df['open'] - df['prevclose']
        df['openingtype'] = df['openinggap'].apply(lambda x: 'No-Gap' if x == 0 else ('Gap-Up' if x > 0 else 'Gap-Down'))
        df['closinggap'] = df['close'] - df['open']
        df['closingtype'] = df['closinggap'].apply(lambda x: 'No-Gap' if x == 0 else ('Above-Open' if x > 0 else 'Below-Open'))
        df['pricevolumeratio'] = df['volume'] / (df['open'] + df['low'] + df['high'] + df['close'])/3
        df.reset_index(drop=True, inplace=True)
        return df
