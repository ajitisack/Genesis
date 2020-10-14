import stockdata as sd
import pandas as pd

pd.options.display.float_format = '{:,.2f}'.format

query = """
select symbol, innifty50, high pdh, low pdl
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
    df['slb'] = df['ltp'].apply(lambda x: round(x-(x*risk),2))
    df['sls'] = df['ltp'].apply(lambda x: round(x+(x*risk),2))
    df_indices1 = df[df.symbol == 'Nifty 50']
    df_indices2 = df[(df.sector == 'Index') & (df.symbol != 'Nifty 50')]
    df_indices2 = df_indices2.sort_values(by='changepct', ascending=False)
    df_niftysymbols = df[df.innifty50 == 1]
    df_symbols = df[df.sector != 'Index']
    df_banks   = df[df.sector == 'Bank']
    df_it      = df[df.sector == 'IT']
    df_auto    = df[df.sector == 'Auto']
    df_pharma  = df[df.sector == 'Pharma']
    df_metal   = df[df.sector == 'Metal']
    df_oilgas  = df[df.sector == 'Oil & Gas']
    df_finserv = df[df.sector == 'FinServ']
    df_telecom = df[df.sector == 'Telecom']
    df_trans   = df[df.sector == 'Transportation']
    df_cement  = df[df.sector == 'Cement']
    df_chemic  = df[df.sector == 'Chemicals']
    df_media   = df[df.sector == 'Media']
    df_power   = df[df.sector == 'Power']
    return_lst = [df_symbols, df_indices1, df_indices2, df_niftysymbols,
                  df_banks, df_it, df_auto, df_pharma, df_metal, df_oilgas,
                  df_finserv, df_telecom, df_trans, df_cement, df_chemic,
                  df_media, df_power]
    return return_lst
