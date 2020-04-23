import pandas as pd

from .yahoofinance.downloader import Downloader
from .symbols.getsymbols import Symbols
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
    s = Symbols()
    s.download()
    del s
    d = Downloader()
    d.downloadhistprice(n_symbols=5000, loadtotable=True, startdt=startdt, interval='1d')
    d.downloaddetails(n_symbols=5000, loadtotable=True)
    del d

def downloadsymbols():
    '''This function downloads all symbols of NSE and BSE into sqlite3 db'''
    return Symbols().download()

def downloaddlyhistprice(n_symbols=5000, loadtotable=True, startdt='2020-01-01'):
    '''This function downloads daily historical price of all symbols of NSE and BSE from yahoo finance into sqlite3 db'''
    return Downloader().downloadhistprice(n_symbols, loadtotable, startdt, interval='1d')

def downloadmlyhistprice(n_symbols=5000, loadtotable=True, startdt='2020-01-01'):
    '''This function downloads monthly historical price of all symbols of NSE and BSE from yahoo finance into sqlite3 db'''
    return Downloader().downloadhistprice(n_symbols, loadtotable, startdt, interval='1mo')

def downloaddetails(n_symbols=5000, loadtotable=True):
    '''This function downloads details of all symbols of NSE and BSE from yahoo finance into sqlite3 db'''
    return Downloader().downloaddetails(n_symbols, loadtotable)
