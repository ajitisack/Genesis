import pandas as pd

from .symbols.getsymbols import Symbols
from .historicaldata.loadhistdata import HistData
from .realtimedata.loadrealtimedata import RealTimeData
from .indices.loaddata import Indices
from .yahoofinance.yf_downloader import YahooFinance
from .moneycontrol.mc_downloader import MoneyControl
from .sqlite import SqLite
from .utils import Utility


@SqLite.connector
def getdata(query):
    df = pd.read_sql(query, SqLite.conn)
    df = Utility.reducesize(df)
    return df

def loadtotable(df, tblname):
    df = Utility.reducesize(df)
    SqLite.loadtable(df, tblname)

def download(startdt='2015-01-01'):
    symbols = Symbols()
    symbols.download()
    del symbols
    i = Indices()
    i.loadindicesdata(startdt)
    del i
    hd = HistData()
    hd.download(n_symbols=0, loadtotable=True, startdt=startdt)
    del hd
    yf = YahooFinance()
    yf.downloaddetails(n_symbols=0, loadtotable=True)
    del yf
    mc = MoneyControl()
    mc.downloaddetails(n_symbols=0, loadtotable=True)
    del mc

def downloadrealtimedata(n_symbols=0):
    return RealTimeData().download(n_symbols)

def downloadsymbols():
    return Symbols().download()

def downloadindices(startdt='2020-01-01'):
    return Indices().loadindicesdata(startdt)

def downloaddlyhistdata(n_symbols=0, loadtotable=True, startdt='2020-01-01'):
    return HistData().download(n_symbols, loadtotable, startdt)

def downloadsymboldetailsyf(n_symbols=0, loadtotable=True):
    return YahooFinance().downloaddetails(n_symbols, loadtotable)

def downloadsymboldetailsmc(n_symbols=0, loadtotable=True):
    return MoneyControl().downloaddetails(n_symbols, loadtotable)

def downloadsectorclassify():
    return MoneyControl().getsectorclassif()
