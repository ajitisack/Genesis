import pandas as pd

from .symbols.getsymbols import Symbols
from .yahoofinance.yf_downloader import YahooFinance
from .moneycontrol.mc_downloader import MoneyControl
from .sqlite import SqLite
from .utils import Utility

@SqLite.connector
def getdata(query):
    df = pd.read_sql('', SqLite.conn)
    df = Utility.reducesize(df)
    return df

def download(startdt='2015-01-01'):
    '''This function downloads all NSE and BSE symbols, history price from given startdt
    with interval of 1 day and details of all symbols from yahoo finance into sqlite3 db'''
    symbols = Symbols()
    symbols.download()
    del symbols
    yf = YahooFinance()
    # yf.downloadhistprice(n_symbols=6000, loadtotable=True, startdt=startdt, interval='1d')
    yf.downloaddetails(n_symbols=6000, loadtotable=True)
    del yf
    mc = MoneyControl()
    mc.downloaddetails(n_symbols=6000)
    del mc

def downloadsymbols():
    '''This function downloads all symbols of NSE and BSE into sqlite3 db'''
    return Symbols().download()

def downloaddlyhistprice(n_symbols=5000, loadtotable=True, startdt='2020-01-01'):
    '''This function downloads daily historical price of all symbols of NSE and BSE from yahoo finance into sqlite3 db'''
    return YahooFinance().downloadhistprice(n_symbols, loadtotable, startdt, interval='1d')

def downloadmlyhistprice(n_symbols=5000, loadtotable=True, startdt='2020-01-01'):
    '''This function downloads monthly historical price of all symbols of NSE and BSE from yahoo finance into sqlite3 db'''
    return YahooFinance().downloadhistprice(n_symbols, loadtotable, startdt, interval='1mo')

def downloaddetailsyf(n_symbols=0, loadtotable=True):
    '''This function downloads details of all symbols of NSE and BSE from yahoo finance into sqlite3 db'''
    return YahooFinance().downloaddetails_yf(n_symbols, loadtotable)

def downloaddetailsmc(n_symbols=0, loadtotable=True):
    return MoneyControl().downloaddetails_mc(n_symbols, loadtotable)

def downloadsectorclassify():
    return MoneyControl().getsectorclassif()

def loadtable(df, tblname):
    df = Utility.reducesize(df)
    SqLite.loadtable(df, tblname)
