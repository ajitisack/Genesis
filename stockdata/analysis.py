import pandas as pd

def addpricechange(df, n=1):
    prevclose = f'prevclose_{n}d'
    pctchange = f'pctchange_{n}d'
    df[prevclose] = df.groupby('symbol').close.transform(lambda x: x.shift(n))
    df[pctchange] = df.groupby('symbol').close.transform(lambda x: round(x.pct_change(n) * 100,2))
    df.fillna(0, inplace=True)
    return df
