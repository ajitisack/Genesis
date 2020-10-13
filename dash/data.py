import stockdata as sd
import pandas as pd

pd.options.display.float_format = '{:,.2f}'.format

query = """
select symbol, high pdh, low pdl
from technicals
where infno = 1
"""
pdhl = sd.getdata(query)


def getpricelevel(x):
    pricelevel = 'Below S3'
    if x['ltp'] >= x['s3']: pricelevel = 'Above S3'
    if x['ltp'] >= x['s2']: pricelevel = 'Above S2'
    if x['ltp'] >= x['s1']: pricelevel = 'Above S1'
    if x['ltp'] >= x['bc'] and x['ltp'] <= x['tc']: pricelevel = 'Within CPR'
    if x['ltp'] >  x['tc']: pricelevel = 'Above CPR'
    if x['ltp'] >= x['r1']: pricelevel = 'Above R1'
    if x['ltp'] >= x['r2']: pricelevel = 'Above R2'
    if x['ltp'] >= x['r3']: pricelevel = 'Above R3'
    if x['open'] == x['low']:  pricelevel += ' (OL)'
    if x['open'] == x['high']: pricelevel += ' (OH)'
    return pricelevel

def getohlstatus(x):
    if x['open'] == x['low']:  return 'OL'
    if x['open'] == x['high']: return 'OH'
    return ''


def getprice(rpt=100, risk=0.5):
    risk = risk/100
    df = sd.getdata("select * from  NSE_MyWatchlistCurrentPrice")
    not_reqd_symbols = ['MRF', 'SHREECEM', 'PAGEIND', 'NESTLEIND', 'BOSCHLTD', 'IDEA']
    df = df[~df.symbol.isin(not_reqd_symbols)]
    # df = sd.getdata("select sector, symbol, open, 0 low, 0 high, open ltp, volume, changepct from preopen where inhotlist = 1")
    # df = pd.merge(df, pivots, how = 'outer', on = 'symbol')
    # df['pricelevel'] = df.apply(lambda x: getpricelevel(x), axis = 1)
    # df['volume']     = df['volume'].apply(lambda x: round(x/100000, 2))
    df = pd.merge(df, pdhl, how = 'outer', on = 'symbol')
    df['ohl'] = df.apply(lambda x: getohlstatus(x), axis = 1)
    df['qty'] = df.apply(lambda x: round(rpt/(x['ltp']*risk), 0), axis = 1)
    df['slb'] = df['ltp'].apply(lambda x: round(x+(x*risk),2))
    df['sls'] = df['ltp'].apply(lambda x: round(x-(x*risk),2))
    cols = ['symbol', 'ltp', 'changepct']
    df_indices1 = df[df.symbol == 'Nifty 50'][cols]
    df_indices2 = df[(df.sector == 'Index') & (df.symbol != 'Nifty 50')][cols]
    df_indices2 = df_indices2.sort_values(by='changepct', ascending=False)
    cols = ['sector', 'symbol', 'ltp', 'changepct', 'qty', 'slb', 'sls', 'ohl', 'pdh', 'pdl']
    df_symbols = df[df.sector != 'Index'][cols]
    df_banks   = df[df.sector == 'Bank'][cols].sort_values(by='changepct', ascending=False)
    df_it      = df[df.sector == 'IT'][cols].sort_values(by='changepct', ascending=False)
    df_auto    = df[df.sector == 'Auto'][cols].sort_values(by='changepct', ascending=False)
    df_pharma  = df[df.sector == 'Pharma'][cols].sort_values(by='changepct', ascending=False)
    df_metal   = df[df.sector == 'Metal'][cols].sort_values(by='changepct', ascending=False)
    df_oilgas  = df[df.sector == 'Oil & Gas'][cols].sort_values(by='changepct', ascending=False)
    df_finserv = df[df.sector == 'FinServ'][cols].sort_values(by='changepct', ascending=False)
    df_others  = df[df.sector.isin(['Cement','Chemicals','Consumer'])][cols].sort_values(by='changepct', ascending=False)
    return df_symbols, df_indices1, df_indices2, df_banks, df_it, df_auto, df_pharma, df_metal, df_oilgas, df_finserv, df_others
