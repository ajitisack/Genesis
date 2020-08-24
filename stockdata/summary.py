import pandas as pd
import numpy as np
import arrow
from statistics import mean
from stockdata.main import getdata
from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

nse_eq_hist_view = 'nseeq_histprice'

def pricechange(df, n=1):
    prevclose = 'prevclose' if n==1  else f'prevclose_{n}d'
    pricechange = 'pricechange' if n==1 else f'pricechange_{n}d'
    pricechangepct = 'pricechangepct' if n==1 else f'pricechangepct_{n}d'
    df[prevclose] = df.groupby('symbol').close.transform(lambda x: x.shift(n))
    df[pricechange] = df.close - df.prevclose
    df[pricechangepct] = df.groupby('symbol').close.transform(lambda x: round(x.pct_change(n) * 100,2))
    df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    df.fillna(0, inplace=True)
    return df

def volumechange(df, n=1):
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

def nsenr479():
    x = getdata(f"select distinct date from {nse_eq_hist_view} order by 1 desc limit 9").date.to_list()
    dts = "'"+ "','".join(x) + "'"
    df = getdata(f"select date, symbol, open, low, high, close from {nse_eq_hist_view} where date in ({dts})")
    df['prevhigh'] = df.groupby('symbol').high.transform(lambda x: x.shift(1))
    df['prevlow']  = df.groupby('symbol').low.transform(lambda x: x.shift(1))
    df['tr']   = df['high'] - df['low']
    df['tr1d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(1))
    df['tr2d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(2))
    df['tr3d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(3))
    df['tr4d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(4))
    df['tr5d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(5))
    df['tr6d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(6))
    df['tr7d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(7))
    df['tr8d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(8))
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['lowerhigh'] = df.apply(lambda x: 1 if x['high'] < x['prevhigh'] else 0, axis=1)
    df['higherlow'] = df.apply(lambda x: 1 if x['low']  > x['prevlow']  else 0, axis=1)
    df['NR4'] = df.apply(lambda x: 1 if x['tr'] < x['tr1d'] and x['tr'] < x['tr2d'] and x['tr'] < x['tr3d'] else 0, axis=1)
    df['NR7'] = df.apply(lambda x: 1 if x['tr'] < x['tr1d'] and x['tr'] < x['tr2d'] and x['tr'] < x['tr3d'] and x['tr'] < x['tr4d'] and x['tr'] < x['tr5d'] and x['tr'] < x['tr6d'] else 0, axis=1)
    df['NR9'] = df.apply(lambda x: 1 if x['tr'] < x['tr1d'] and x['tr'] < x['tr2d'] and x['tr'] < x['tr3d'] and x['tr'] < x['tr4d'] and x['tr'] < x['tr5d'] and x['tr'] < x['tr6d'] and x['tr'] < x['tr7d'] and x['tr'] < x['tr8d'] else 0, axis=1)
    df.drop(['date', 'open', 'low', 'high', 'close'], axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def pivotpoints(df):
    df['pp'] = (df['high'] + df['low'] + df['close'])/3
    df['bc'] = (df['high'] + df['low'])/2
    df['tc'] = 2 * df['pp'] - df['bc']
    df['cpr'] = round(abs(df['tc'] - df['bc']),2)
    df['r1'] = 2 * df['pp'] - df['low']
    df['r2'] = df['pp'] + df['high'] - df['low']
    df['r3'] = df['high'] + 2 * (df['pp'] - df['low'])
    df['s1'] = (2 * df['pp']) - df['high']
    df['s2'] = df['pp'] - (df['high'] - df['low'])
    df['s3'] = df['low'] - 2 * (df['high'] - df['pp'])
    return df

def basissum():
    currdt, prevdt = getdata(f"select distinct date from {nse_eq_hist_view} order by 1 desc limit 2").date.to_list()
    df = getdata(f"select date, symbol, open, low, high, close, volume from {nse_eq_hist_view} where date in ('{currdt}', '{prevdt}')")
    df = pricechange(df)
    df = volumechange(df)
    df = pivotpoints(df)
    df = df[df.date == currdt]
    df = df[df.prevclose!=0]
    df['openinggap']  = df['open'] - df['prevclose']
    df['openingtype'] = df['openinggap'].apply(lambda x: 'No-Gap' if x == 0 else ('Gap-Up' if x > 0 else 'Gap-Down'))
    df['closinggap'] = df['close'] - df['open']
    df['closingtype'] = df['closinggap'].apply(lambda x: 'No-Gap' if x == 0 else ('Above-Open' if x > 0 else 'Below-Open'))
    df['pricevolumeratio'] = df['volume'] / (df['open'] + df['low'] + df['high'] + df['close'])/3
    df.reset_index(drop=True, inplace=True)
    return df

@Utility.timer
def loadbasicsummary(loadtotable=True):
    tblname = 'NSE_EquitySummary'
    df1 = basissum()
    df2 = nsenr479()
    df = pd.merge(df1, df2, how='outer', on='symbol')
    df = Utility.reducesize(df)
    if not loadtotable: return df
    df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
    SqLite.loadtable(df, tblname)
    # SqLite.createindex(tblname, 'symbol')
