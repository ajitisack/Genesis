import pandas as pd
import arrow
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility
from stockdata.yahoofinance.get_currentprice import CurrentPrice

class CurrentMarketPrice(CurrentPrice, Config):

    def __init__(self):
        Config.__init__(self)

    @SqLite.connector
    def getsymbols(self):
        tblname = 'symbols'
        query = f"select sector, symbol from {tblname} where inmylist = 1"
        df = pd.read_sql(query, SqLite.conn)
        indices = ['^NSEI', '^NSEBANK', '^CNXIT', '^CNXAUTO', '^CNXPHARMA', '^CNXMETAL', '^CNXFIN']
        indices = pd.DataFrame({'symbol' : indices})
        indices.insert(0, 'sector', 'Index')
        df = df.append(indices, ignore_index=True)
        symbols = zip(df.sector, df.symbol)
        return list(symbols)

    @Utility.timer
    def download(self):
        print(f"Downloading current price of intraday watchlist symbols for {arrow.now().format('YYYY-MM-DD')}", end='...', flush=True)
        tblname = 'NSE_MyWatchlistCurrentPrice'
        equitypriceurl = self.nse_equitypriceurl
        symbols_list = self.getsymbols()
        nthreads = min(len(symbols_list), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.gethistdata, symbols_list)
        data = list(results)
        df = pd.DataFrame(data)
        df = df.astype({'volume': int})
        df = Utility.reducesize(df)
        df['changepct'] = df.apply(lambda x: round((x['ltp']-x['open'])*100/x['open'], 2), axis = 1)
        print('Completed !')
        SqLite.loadtable(df, tblname)
