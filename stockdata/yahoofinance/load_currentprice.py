import pandas as pd
import arrow

from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility
from stockdata.yahoofinance.get_currentprice import CurrentPrice

class CurrentMarketPrice(CurrentPrice, Config):

    def __init__(self):
        Config.__init__(self)

    @SqLite.connector
    def getsymbols(self):
        tblname = 'NSE_MyWatchlist'
        query = f"select sector, symbol symbol from {tblname}"
        df = pd.read_sql(query, SqLite.conn)
        symbols = zip(df.sector, df.symbol)
        return symbols

    @Utility.timer
    def download(self):
        print(f"Downloading current price of intraday watchlist symbols for {arrow.now().format('YYYY-MM-DD')}", end='...', flush=True)
        tblname = 'NSE_MyWatchlistCurrentPrice'
        equitypriceurl = self.nse_equitypriceurl
        symbols = self.getsymbols()
        data = [self.gethistdata(s) for s in symbols]
        df = pd.DataFrame(data)
        df = df.astype({'volume': int})
        df = Utility.reducesize(df)
        df['changepct'] = df.apply(lambda x: round((x['ltp']-x['open'])*100/x['open'], 2), axis = 1)
        print('Completed !')
        SqLite.loadtable(df, tblname)
