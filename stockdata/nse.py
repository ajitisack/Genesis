import arrow

from stockdata.historicaldata.loadhistdata import HistData
from stockdata.currentprice.loadequitycurrentprice import CurrentPriceEquity
from stockdata.currentprice.loadindicescurrentprice import CurrentPriceIndices
from stockdata.intraday.downloadintradaydata import IntraDayData
from stockdata.intraday.streamintradaydata import StreamIntraDayData
from stockdata.preopendata.download_nsepreopendata import MarketPreOpen
from stockdata.indices.download_indices_symbols import IndicesSymbols
from stockdata.yahoofinance.yf_downloader import YahooFinance
from stockdata.moneycontrol.mc_downloader import MoneyControl

# to download historical prices and events of NSE symbols
def downloadnsehistdata(n_symbols=0, loadtotable=True, startdt='1970-01-01'):
    return HistData().download('NSE', n_symbols, loadtotable, startdt)

def downloadnseintradaytoday(date=arrow.now().format('YYYY-MM-DD'), n_symbols=0):
    return StreamIntraDayData().stream('NSE', date, n_symbols)

def downloadnsecurrentprice(n_symbols=0, loadtotable=True):
    return CurrentPriceEquity().download('NSE', n_symbols, loadtotable)

def downloadnseindicescurrentprice(n_symbols=0, loadtotable=True):
    return CurrentPriceIndices().download('NSE', n_symbols, loadtotable)

def downloadnseintradaydata(date, n_symbols=0):
    return IntraDayData().download('NSE', date, n_symbols)

def createnseintradaymonthlyfile(yyyymm):
    return IntraDayData().processmonthlyfiles('NSE', yyyymm)

def loadnseintradayfile(yyyymm):
    return IntraDayData().loadintradayfile('NSE', yyyymm)

def downloadnsepreopendata():
    return MarketPreOpen().download()

def downloadnseindices(loadtotable=True):
    return IndicesSymbols().downloadindicessymbols('NSE', loadtotable)

def downloadnsesymboldetailsyf(n_symbols=0, loadtotable=True):
    return YahooFinance().downloaddetails('NSE', n_symbols, loadtotable)

def downloadnsesymboldetailsmc(n_symbols=0, loadtotable=True):
    return MoneyControl().downloaddetails('NSE', n_symbols, loadtotable)
