import pandas as pd
import plotly.graph_objects as go

from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils import Utility

from nsedata.lib.symbols.getsymbols import Symbols
from nsedata.lib.equityhistdata.loadhistdata import EquityHistData
from nsedata.lib.indices.indices_symbols import IndicesSymbols
from nsedata.lib.preopen.download import MarketPreOpen
from nsedata.lib.intraday.download import IntraDayData

from nsedata.lib.participantdata.download import ParticipantData
from nsedata.lib.fno_bhavcopy.download import FNOBhavcopy
from nsedata.lib.equity_bhavcopy.download import EquityBhavcopy
from nsedata.lib.indices.indices_price import IndicesPrice

# to download NSE symbols
def downloadsymbols():
    return Symbols().download()

def downloadequityhistdata(n_symbols=0, loadtotable=True, startdt='1970-01-01'):
    return EquityHistData().download(n_symbols, loadtotable, startdt)

def downloadindicesdetails(loadtotable=True):
    return IndicesSymbols().download(loadtotable)

def downloadpreopendata(loadtotable=True):
    return MarketPreOpen().download(loadtotable)

def downloadequityintraday(date, n_symbols=0):
    return IntraDayData().downloadallfiles(date, n_symbols)

def createequityintradaymonthlyfile(date):
    return IntraDayData().createmonthlyfile(date)

def downloadparticipantwisedata(startdt=None, enddt=None):
    x = ParticipantData()
    x.download('oi', startdt, enddt)
    x.download('vol', startdt, enddt)
    x.download('fiistat', startdt, enddt)

def downloadFNOBhavcopy(startdt=None, enddt=None):
    return FNOBhavcopy().download(startdt, enddt)

def downloadEquityBhavcopy(startdt=None, enddt=None):
    return EquityBhavcopy().download(startdt, enddt)

def downloadIndicesPrice(startdt=None, enddt=None):
    return IndicesPrice().download(startdt, enddt)


#
# @SqLite.connector
# def getdata(query):
#     df = pd.read_sql(query, SqLite.conn)
#     df = Utility.reducesize(df)
#     return df
#
# def getnsehistprice(symbol):
#     if type(symbol) == list:
#         symbol = map(lambda x: x.upper().strip(), symbol)
#         symbol = "','".join(symbol)
#     symbol = symbol.upper().strip()
#     df = getdata(f"select * from histprice where symbol in ('{symbol}')")
#     df['date'] = pd.to_datetime(df['date'])
#     df.set_index('date', inplace=True)
#     return df
#
# # needs to be corrected
# def getweeklynsehistprice(symbol):
#     df = getnsehistprice(symbol)
#     cols = df.columns
#     df = df.reset_index()
#     df = df.groupby(['symbol', 'year', 'wknr']).last().reset_index().set_index('date')
#     return df[cols]
#
# # needs to be corrected
# def getmonthlynsehistprice(symbol):
#     df = getnsehistprice(symbol)
#     cols = df.columns
#     df = df.reset_index()
#     df = df.groupby(['symbol', 'year', 'month']).last().reset_index().set_index('date')
#     return df[cols]
#
# # needs to be corrected
# def getyearlynsehistprice(symbol):
#     df = getnsehistprice(symbol)
#     cols = df.columns
#     df = df.reset_index()
#     df = df.groupby(['symbol', 'year']).last().reset_index().set_index('date')
#     return df[cols]
#
# def loadtotable(df, tblname):
#     df = Utility.reducesize(df)
#     SqLite.loadtable(df, tblname)
#
# def searchsymbol(name):
#     df = getdata(f"select * from symbols where name like '%{name.upper()}%' or symbol like '%{name.upper()}%'   ")
#     return df
