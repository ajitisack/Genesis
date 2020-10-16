import stockdata as sd
import pandas as pd

pd.options.display.float_format = '{:,.2f}'.format

query = """
select symbol, innifty50, infno, high pdh, low pdl
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


def getsectorsymbols(df, sector):
    n50_sector_adv = df[(df.sector == sector) & (df.innifty50 == 1) & (df.changepct >=0)].sort_values(by='changepct', ascending=False)
    n50_sector_dec = df[(df.sector == sector) & (df.innifty50 == 1) & (df.changepct < 0)].sort_values(by='changepct', ascending=True)
    fno_sector_adv = df[(df.sector == sector) & (df.infno == 1) & (df.changepct >= 0)].sort_values(by='changepct', ascending=False)
    fno_sector_dec = df[(df.sector == sector) & (df.infno == 1) & (df.changepct < 0)].sort_values(by='changepct', ascending=True)
    d = {
          'n50' : {'adv' : n50_sector_adv, 'dec' : n50_sector_dec}
        , 'fno' : {'adv' : fno_sector_adv, 'dec' : fno_sector_dec}
    }
    return d

def getsl(x, risk):
    ltp  = x['ltp']
    changepct = x['changepct']
    sl_points = ltp * risk
    if changepct >= 0: return round(ltp - sl_points, 2)
    if changepct <  0: return round(ltp + sl_points, 2)

def getprice(rpt=100, risk=0.5):
    risk = risk/100
    df   = sd.getdata("select * from  NSE_MyWatchlistCurrentPrice")
    not_reqd_symbols = ['MRF', 'SHREECEM', 'PAGEIND', 'NESTLEIND', 'BOSCHLTD', 'IDEA']
    df   = df[~df.symbol.isin(not_reqd_symbols)]
    # df = sd.getdata("select sector, symbol, open, 0 low, 0 high, open ltp, volume, changepct from preopen where inhotlist = 1")
    # df = pd.merge(df, pivots, how = 'outer', on = 'symbol')
    # df['pricelevel'] = df.apply(lambda x: getpricelevel(x), axis = 1)
    # df['volume']     = df['volume'].apply(lambda x: round(x/100000, 2))
    df = pd.merge(df, pdhl, how = 'outer', on = 'symbol')
    df['ohl'] = df.apply(lambda x: getohlstatus(x), axis = 1)
    df['qty'] = df.apply(lambda x: round(rpt/(x['ltp']*risk), 0), axis = 1)
    df['sl']  = df.apply(lambda x: getsl(x, risk), axis = 1)
    dfs = {}
    dfs['nifty50']     = df[df.symbol == 'Nifty 50']
    dfs['indices_adv'] = df[(df.sector == 'Index') & (df.symbol != 'Nifty 50') & (df.changepct >=0)].sort_values(by='changepct', ascending=False)
    dfs['indices_dec'] = df[(df.sector == 'Index') & (df.symbol != 'Nifty 50') & (df.changepct < 0)].sort_values(by='changepct', ascending=True)
    dfs['nifty_adv']   = df[(df.innifty50 == 1) & (df.changepct >=0)].sort_values(by='changepct', ascending=False)
    dfs['nifty_dec']   = df[(df.innifty50 == 1) & (df.changepct < 0)].sort_values(by='changepct', ascending=True)
    dfs['fno_adv']     = df[df.changepct >=0].sort_values(by='changepct', ascending=False)
    dfs['fno_dec']     = df[df.changepct < 0].sort_values(by='changepct', ascending=True)
    dfs['bank']        = getsectorsymbols(df, 'Bank')
    dfs['pharma']      = getsectorsymbols(df, 'Pharma')
    dfs['it']          = getsectorsymbols(df, 'IT')
    dfs['auto']        = getsectorsymbols(df, 'Auto')
    dfs['autoanc']     = getsectorsymbols(df, 'Auto Ancillaries')
    dfs['metal']       = getsectorsymbols(df, 'Metal')
    dfs['oilgas']      = getsectorsymbols(df, 'Oil & Gas')
    dfs['finserv']     = getsectorsymbols(df, 'Fin. Serv.')
    dfs['power']       = getsectorsymbols(df, 'Power')
    dfs['media']       = getsectorsymbols(df, 'Media')
    dfs['chemi']       = getsectorsymbols(df, 'Chemicals')
    dfs['cement']      = getsectorsymbols(df, 'Cement')
    dfs['telecom']     = getsectorsymbols(df, 'Telecom')
    dfs['trans']       = getsectorsymbols(df, 'Transportation')
    dfs['realty']      = getsectorsymbols(df, 'Realty')
    dfs['fmcg']        = getsectorsymbols(df, 'FMCG')
    dfs['consdur']     = getsectorsymbols(df, 'Cons. Durables')
    return dfs
