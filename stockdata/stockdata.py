import pandas as pd

from .downloader import Downloader
from .sqlite import SqlLite

@SqlLite.connector
def getdata(sql):
    df = pd.read_sql(sql, SqlLite.conn)
    return df

def download(startdt='2020-01-01'):
    '''This function downloads all NSE and BSE symbols, history price from given startdt
    with interval of 1 day and details of all symbols from yahoo finance into sqlite3 db'''
    d = Downloader()
    d.downloadsymbols()
    d.downloadhistprice(n_symbols=5000, loadtotable=True, startdt=startdt, interval='1d')
    d.downloaddetails(n_symbols=5000, loadtotable=True)
    del d

def downloadsymbols():
    '''This function downloads all symbols of NSE and BSE into sqlite3 db'''
    d = Downloader()
    d.downloadsymbols()
    del d

def downloaddlyhistprice(n_symbols=5000, loadtotable=True, startdt='2020-01-01'):
    '''This function downloads daily historical price of all symbols of NSE and BSE from yahoo finance into sqlite3 db'''
    d = Downloader()
    df = d.downloadhistprice(n_symbols, loadtotable, startdt, interval='1d')
    del d
    return df

def downloadmlyhistprice(n_symbols=5000, loadtotable=True, startdt='2020-01-01'):
    '''This function downloads monthly historical price of all symbols of NSE and BSE from yahoo finance into sqlite3 db'''
    d = Downloader()
    df = d.downloadhistprice(n_symbols, loadtotable, startdt, interval='1mo')
    del d
    return df

def downloaddetails(n_symbols=5000, loadtotable=True):
    '''This function downloads details of all symbols of NSE and BSE from yahoo finance into sqlite3 db'''
    d = Downloader()
    df = d.downloaddetails(n_symbols, loadtotable)
    del d
    return df
