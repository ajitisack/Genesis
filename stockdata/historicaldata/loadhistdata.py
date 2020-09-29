import pandas as pd
import arrow
import time
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from stockdata.historicaldata.gethistdata import HistDataDict
from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

class HistData(HistDataDict, Config):

    def __init__(self):
        Config.__init__(self)

    @SqLite.connector
    def getsymbols(self, exchange, n_symbols):
        # tblname = self.tbl_nsesymbols
        tblname = 'symbols'
        if exchange == 'NSE': query = f"select distinct symbol || '.NS' as symbol from {tblname} "
        if n_symbols > 0: query += f'limit {n_symbols}'
        df = pd.read_sql(query, SqLite.conn)
        symbols = df.symbol.to_list()
        return symbols

    def processdf(self, df):
        df['date'] = df['date'].apply(lambda x: arrow.get(x).format('YYYY-MM-DD'))
        df['symbol'] = df['symbol'].apply(lambda x: x.split('.')[0].replace('^', ''))
        df = Utility.adddatefeatures(df)
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
        return df

    # def downloadhistprice(self, symbols_list, startdt):
    #     n = 100
    #     data = []
    #     symbols_chunk = [symbols_list[i:i + n] for i in range(0, len(symbols_list), n)]
    #     for symbols in symbols_chunk:
    #         nthreads = min(len(symbols), int(self.maxthreads))
    #         with ThreadPoolExecutor(max_workers=nthreads) as executor:
    #             results = executor.map(self.gethistdata, symbols, repeat(startdt))
    #         data = data + list(results)
    #         time.sleep(5)
    #     return data

    def downloadhistprice(self, symbols_list, startdt):
        nthreads = min(len(symbols_list), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.gethistdata, symbols_list, repeat(startdt))
        data = list(results)
        return data

    @Utility.timer
    def download(self, exchange, n_symbols, loadtotable, startdt):
        tbl_hprice  = self.tbl_nsehprice
        tbl_actions = self.tbl_nseactions
        symbols = self.getsymbols(exchange, n_symbols)
        print(f'Downloading historical prices and events from yahoo finance for {len(symbols)} {exchange.upper()} symbols from {startdt}', end='...', flush=True)
        data = self.downloadhistprice(symbols, startdt)
        histprice = pd.concat([pd.DataFrame(i[0]) for i in data], ignore_index=True)
        dividends = pd.concat([pd.DataFrame(i[1]) for i in data], ignore_index=True)
        splits    = pd.concat([pd.DataFrame(i[2]) for i in data], ignore_index=True)
        events    = pd.concat([dividends, splits], ignore_index=True)
        histprice = self.processdf(histprice).dropna()
        events    = self.processdf(events).dropna()
        histprice = histprice.astype({'volume': int})
        print('Completed !')
        if not loadtotable: return histprice, events
        SqLite.loadtable(histprice, tbl_hprice)
        # SqLite.createindex(tbl_hprice, 'symbol')
        SqLite.loadtable(events, tbl_actions)
        # SqLite.createindex(tbl_actions, 'symbol')
