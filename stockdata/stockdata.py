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

def downloadhistdata(startdt='2015-01-01'):
    symbols = Symbols()
    symbols.download()
    del symbols
    i = Indices()
    i.loadindicesdata(startdt)
    del i
    hd = HistData()
    hd.download('NSE', n_symbols=0, loadtotable=True, startdt=startdt)
    hd.download('BSE', n_symbols=0, loadtotable=True, startdt=startdt)
    del hd

def downloadrealtimedata():
    rt = RealTimeData()
    rt.download('NSE', n_symbols=0, loadtotable=True)
    rt.download('BSE', n_symbols=0, loadtotable=True)
    del rt

def downloadprofile():
    mc = MoneyControl()
    mc.downloaddetails(n_symbols=0, loadtotable=True)
    del mc
    yf = YahooFinance()
    yf.downloaddetails('NSE', n_symbols=0, loadtotable=True)
    yf.downloaddetails('BSE', n_symbols=0, loadtotable=True)
    del yf

def downloadnserealtimedata(n_symbols=0, loadtotable=True):
    return RealTimeData().download('NSE', n_symbols, loadtotable)

def downloadbserealtimedata(n_symbols=0, loadtotable=True):
    return RealTimeData().download('BSE', n_symbols, loadtotable)

def downloadsymbols():
    return Symbols().download()

def downloadindices(startdt='2020-01-01'):
    return Indices().loadindicesdata(startdt)

def downloadnsehistdata(n_symbols=0, loadtotable=True, startdt='2020-01-01'):
    return HistData().download('NSE', n_symbols, loadtotable, startdt)

def downloadbsehistdata(n_symbols=0, loadtotable=True, startdt='2020-01-01'):
    return HistData().download('BSE', n_symbols, loadtotable, startdt)

def downloadnsesymboldetailsyf(n_symbols=0, loadtotable=True):
    return YahooFinance().downloaddetails('NSE', n_symbols, loadtotable)

def downloadbsesymboldetailsyf(n_symbols=0, loadtotable=True):
    return YahooFinance().downloaddetails('BSE', n_symbols, loadtotable)

def downloadsymboldetailsmc(n_symbols=0, loadtotable=True):
    return MoneyControl().downloaddetails(n_symbols, loadtotable)

def downloadsectorclassify():
    return MoneyControl().getsectorclassif()
