
from .downloader import Downloader

def downloadsymbols():
    return Downloader().downloadsymbols()

def downloaddlyhistprice(n_symbols=5000, loadtotable=True, startdt='2020-01-01'):
    return Downloader().downloadhistprice(n_symbols, loadtotable, startdt, interval='1d')

def downloadmlyhistprice(n_symbols=5000, loadtotable=True, startdt='2020-01-01'):
    return Downloader().downloadhistprice(n_symbols, loadtotable, startdt, interval='1mo')

def downloaddetails(n_symbols=5000, loadtotable=True):
    return Downloader().downloaddetails(n_symbols, loadtotable)
