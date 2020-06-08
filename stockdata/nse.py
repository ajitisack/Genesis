from stockdata.historicaldata.loadhistdata import HistData
from stockdata.intraday.downloadintradaydata import IntraDayData
from stockdata.indices.download_indices_symbols import IndicesSymbols
from stockdata.indices.download_indices_histdata import IndicesHistData
from stockdata.yahoofinance.yf_downloader import YahooFinance
from stockdata.moneycontrol.mc_downloader import MoneyControl

# to download historical prices and events of NSE symbols
def downloadnsehistdata(n_symbols=0, loadtotable=True, startdt='1970-01-01'):
    return HistData().download('NSE', n_symbols, loadtotable, startdt)

def downloadnseintradaydata(date, n_symbols=0):
    return IntraDayData().download('NSE', date, n_symbols)

def downloadnseindices(loadtotable=True):
    return IndicesSymbols().downloadindicessymbols('NSE', loadtotable)

def downloadnseindiceshistdata(loadtotable=True, startdt='1970-01-01'):
    return IndicesHistData().downloadindiceshistdata('NSE', loadtotable, startdt)

def downloadnsesymboldetailsyf(n_symbols=0, loadtotable=True):
    return YahooFinance().downloaddetails('NSE', n_symbols, loadtotable)

def downloadnsesymboldetailsmc(n_symbols=0, loadtotable=True):
    return MoneyControl().downloaddetails('NSE', n_symbols, loadtotable)
