import arrow

from stockdata.historicaldata.loadhistdata import HistData
from stockdata.intraday.downloadintradaydata import IntraDayData
from stockdata.intraday.streamintradaydata import StreamIntraDayData
from stockdata.nsepreopendata.download_nsepreopendata import NSEMarketPreOpen
from stockdata.nsemarketprice.load_currentprice_fnostocks import CurrentPriceFNOSymbols
from stockdata.nsemarketprice.load_currentprice_allindices import CurrentPriceAllIndices
from stockdata.indices.download_indices_symbols import IndicesSymbols
from stockdata.yahoofinance.yf_downloader import YahooFinance
from stockdata.moneycontrol.mc_downloader import MoneyControl
from stockdata.technicals.load_technicals import Technicals

# to download historical prices and events of NSE symbols
def downloadnsehistdata(n_symbols=0, loadtotable=True, startdt='1970-01-01'):
    return HistData().download('NSE', n_symbols, loadtotable, startdt)


# to download intraday prices per minute of NSE symbols for today
def downloadnseintradaytoday(date=arrow.now().format('YYYY-MM-DD'), n_symbols=0):
    return StreamIntraDayData().stream('NSE', date, n_symbols)


# to download intraday prices per minute of NSE symbols for given date
def downloadnseintradaydata(date, n_symbols=0):
    return IntraDayData().download('NSE', date, n_symbols)


def createnseintradaymonthlyfile(yyyymm):
    return IntraDayData().processmonthlyfiles('NSE', yyyymm)

def loadnseintradayfile(yyyymm):
    return IntraDayData().loadintradayfile('NSE', yyyymm)

def downloadnsepreopendata():
    return NSEMarketPreOpen().download()

def downloadnsefnostockscurrentprice():
    return CurrentPriceFNOSymbols().download()

def downloadnseallindicescurrentprice():
    return CurrentPriceAllIndices().download()

def downloadnseindices(loadtotable=True):
    return IndicesSymbols().downloadindicessymbols('NSE', loadtotable)

def downloadnsesymboldetailsyf(n_symbols=0, loadtotable=True):
    return YahooFinance().downloaddetails('NSE', n_symbols, loadtotable)

def downloadnsesymboldetailsmc(n_symbols=0, loadtotable=True):
    return MoneyControl().downloaddetails('NSE', n_symbols, loadtotable)

def loadtechnicals(loadtotable=True):
    return Technicals().loadtechnicals(loadtotable)
