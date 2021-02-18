import stockdata as sd
import pandas as pd

pd.options.display.float_format = '{:,.2f}'.format

query = """
select a.symbol, a.innifty50, a.infno, a.high pdh, a.low pdl, a.close prevclose
, round( (b.open-a.close)/a.close*100, 2) gappct
from technicals a join preopen b on a.symbol = b.symbol
where a.innifty50 = 1
"""
pdhl = sd.getdata(query)


def getohlstatus(x):
    if x['open'] == x['low']:  return 'OL'
    if x['open'] == x['high']: return 'OH'
    return ''


def getsectorsymbols(df, sector):
    # n50_sector_adv = df[df.sector.isin(sector) & (df.innifty50 == 1) & (df.changepct >=0)].sort_values(by='changepct', ascending=False)
    # n50_sector_dec = df[df.sector.isin(sector) & (df.innifty50 == 1) & (df.changepct < 0)].sort_values(by='changepct', ascending=True)
    # d = { 'adv' : n50_sector_adv, 'dec' : n50_sector_dec}
    # return d
    n50_sector_symbols = df[df.sector.isin(sector) & (df.innifty50 == 1)].sort_values(by='changepct', ascending=False)
    return n50_sector_symbols

def getsl(x, risk):
    ltp  = x['ltp']
    changepct = x['changepct']
    sl_points = ltp * risk
    if changepct >= 0: return round(ltp - sl_points, 2)
    if changepct <  0: return round(ltp + sl_points, 2)

def getprice(rpt=200, risk=0.5):
    risk = risk/100
    df   = sd.getdata("select * from  NSE_MyWatchlistCurrentPrice")
    not_reqd_symbols = ['MRF', 'SHREECEM', 'PAGEIND', 'NESTLEIND', 'BOSCHLTD', 'IDEA']
    df   = df[~df.symbol.isin(not_reqd_symbols)]
    df['value']     = df.apply(lambda x: round((x['ltp'] * x['volume'])/10000000, 2), axis = 1)
    df = pd.merge(df, pdhl, how = 'outer', on = 'symbol')
    df = df[df.sector != '']
    df['ohl'] = df.apply(lambda x: getohlstatus(x), axis = 1)
    df['qty'] = df.apply(lambda x: round(rpt/(x['ltp']*risk), 0), axis = 1)
    df['r2r'] = df['ltp'].apply(lambda x: round((x*risk), 1))
    df['sl']  = df.apply(lambda x: getsl(x, risk), axis = 1)
    dfs = {}
    dfs['nifty50']     = df[df.symbol == 'Nifty 50']
    dfs['indices_adv'] = df[(df.sector == 'Index') & (df.symbol != 'Nifty 50') & (df.changepct >=0)].sort_values(by='changepct', ascending=False)
    dfs['indices_dec'] = df[(df.sector == 'Index') & (df.symbol != 'Nifty 50') & (df.changepct < 0)].sort_values(by='changepct', ascending=True)
    dfs['nifty_adv']   = df[(df.innifty50 == 1) & (df.changepct >=0)].sort_values(by='changepct', ascending=False)
    dfs['nifty_dec']   = df[(df.innifty50 == 1) & (df.changepct < 0)].sort_values(by='changepct', ascending=True)
    dfs['active']      = df[(df.innifty50 == 1) & (df.sector != 'Index')].sort_values(by='value', ascending=False)
    dfs['bank']        = getsectorsymbols(df, ['Bank'])
    dfs['finserv']     = getsectorsymbols(df, ['Fin. Serv.'])
    dfs['auto']        = getsectorsymbols(df, ['Auto'])
    dfs['it']          = getsectorsymbols(df, ['IT'])
    dfs['pharma']      = getsectorsymbols(df, ['Pharma'])
    dfs['metal']       = getsectorsymbols(df, ['Metal'])
    dfs['energy']      = getsectorsymbols(df, ['Oil & Gas', 'Power'])
    dfs['chemi']       = getsectorsymbols(df, ['Chemicals', 'Cement'])
    dfs['others']      = getsectorsymbols(df, ['Telecom', 'Transportation', 'Realty', 'Cons. Durables'])
    dfs['above_pdh']   = df[(df.innifty50 == 1) & (df.changepct >=0) & (df.ltp >= df.pdh)].sort_values(by='changepct', ascending=False)
    dfs['below_pdl']   = df[(df.innifty50 == 1) & (df.changepct >=0) & (df.ltp <= df.pdl)].sort_values(by='changepct', ascending=True)
    return dfs
