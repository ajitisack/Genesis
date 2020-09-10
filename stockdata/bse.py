
from stockdata.historicaldata.loadhistdata import HistData
from stockdata.intraday.downloadintradaydata import IntraDayData
from stockdata.yahoofinance.yf_downloader import YahooFinance
from stockdata.moneycontrol.mc_downloader import MoneyControl


def downloadbseintradaydata(date, n_symbols=0):
    return IntraDayData().download('BSE', date, n_symbols)

def downloadbsehistdata(n_symbols=0, loadtotable=True, startdt='1970-01-01'):
    return HistData().download('BSE', n_symbols, loadtotable, startdt)

def downloadbsesymboldetailsyf(n_symbols=0, loadtotable=True):
    return YahooFinance().downloaddetails('BSE', n_symbols, loadtotable)

def downloadbsesymboldetailsmc(n_symbols=0, loadtotable=True):
    return MoneyControl().downloaddetails('BSE', n_symbols, loadtotable)
