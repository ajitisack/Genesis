import pandas as pd
import numpy as np

def addpricechange(df, n=1):
    prevclose = 'prevclose' if n==1  else f'prevclose_{n}d'
    pricechange = 'pricechange' if n==1 else f'pricechange_{n}d'
    pricechangepct = 'pricechangepct' if n==1 else f'pricechangepct_{n}d'
    df[prevclose] = df.groupby('symbol').close.transform(lambda x: x.shift(n))
    df[pricechange] = df.close - df.prevclose
    df[pricechangepct] = df.groupby('symbol').close.transform(lambda x: round(x.pct_change(n) * 100,2))
    df.replace([np.inf, -np.inf, np.nan], 0, inplace=True)
    df.fillna(0, inplace=True)
    return df

def addvolumechange(df, n=1):
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
