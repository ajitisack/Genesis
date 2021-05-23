# import arrow
#
# from lib.historicaldata.loadhistdata import HistData
# from lib.intraday.downloadintradaydata import IntraDayData
# from lib.intraday.streamintradaydata import StreamIntraDayData
# from lib.nsepreopendata.download_nsepreopendata import NSEMarketPreOpen
# from lib.nsemarketprice.load_currentprice_fnostocks import CurrentPriceFNOSymbols
# from lib.nsemarketprice.load_currentprice_allindices import CurrentPriceAllIndices
# from lib.indices.download_indices_symbols import IndicesSymbols
# from lib.yahoofinance.yf_downloader import YahooFinance
# from lib.moneycontrol.mc_downloader import MoneyControl
# from lib.technicals.load_technicals import Technicals
# from lib.yahoofinance.load_currentprice import CurrentMarketPrice
#
# # to download historical prices and events of NSE symbols
# def downloadnsehistdata(n_symbols=0, loadtotable=True, startdt='1970-01-01'):
#     return HistData().download('NSE', n_symbols, loadtotable, startdt)
#
#
# # to download intraday prices per minute of NSE symbols for today
# def downloadnseintradaytoday(date=arrow.now().format('YYYY-MM-DD'), n_symbols=0):
#     return StreamIntraDayData().stream('NSE', date, n_symbols)
#
#
# # to download intraday prices FNO activated NSE symbols for given date with intervals of 1min, 5min, 15min, 30min, 1h
# def downloadnseintradaydata(date, n_symbols=0):
#     return IntraDayData().downloadallfiles('NSE', date, n_symbols)
#
# def createnseintradaymonthlyfile(yyyymm):
#     return IntraDayData().processmonthlyfiles('NSE', yyyymm)
#
# def loadnseintradayfile(yyyymm):
#     return IntraDayData().loadintradayfile('NSE', yyyymm)
#
# def downloadnsepreopendata():
#     return NSEMarketPreOpen().download()
#
# def downloadnsefnostockscurrentprice():
#     return CurrentPriceFNOSymbols().download()
#
# def downloadmysymbolscurrentprice():
#     return CurrentMarketPrice().download()
#
# def downloadnseallindicescurrentprice():
#     return CurrentPriceAllIndices().download()
#
# def downloadnseindices(loadtotable=True):
#     return IndicesSymbols().downloadindicessymbols('NSE', loadtotable)
#
# def downloadnsesymboldetailsyf(n_symbols=0, loadtotable=True):
#     return YahooFinance().downloaddetails('NSE', n_symbols, loadtotable)
#
# def downloadnsesymboldetailsmc(n_symbols=0, loadtotable=True):
#     return MoneyControl().downloaddetails('NSE', n_symbols, loadtotable)
#
# def loadtechnicals(date=arrow.now().format('YYYY-MM-DD'), loadtotable=True):
#     return Technicals().loadtechnicals(date, loadtotable)
