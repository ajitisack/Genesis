import pandas as pd
import arrow
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
        if exchange == 'NSE': query = f"select symbol || '.NS' as symbol from {tblname} where infno = 1 "
        if n_symbols > 0: query += f'limit {n_symbols}'
        df = pd.read_sql(query, SqLite.conn)
        return list(df.symbol)

    def processdf(self, df):
        df['date'] = df['date'].apply(lambda x: arrow.get(x).format('YYYY-MM-DD'))
        df['symbol'] = df['symbol'].apply(lambda x: x.split('.')[0].replace('^', ''))
        df = Utility.adddatefeatures(df)
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
        return df

    @Utility.timer
    def download(self, exchange, n_symbols, loadtotable, startdt):
        symbols = self.getsymbols(exchange, n_symbols)
        if exchange == 'NSE': tbl_hprice  = self.tbl_nsehprice
        if exchange == 'NSE': tbl_actions = self.tbl_nseactions
        if exchange == 'BSE': tbl_hprice  = self.tbl_bsehprice
        if exchange == 'BSE': tbl_actions = self.tbl_bseactions
        print(f'Downloading historical prices and actions from yahoo finance for {len(symbols)} {exchange.upper()} symbols from {startdt}', end='...', flush=True)
        nthreads = min(len(symbols), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.gethistdata, symbols, repeat(startdt))
        values = list(results)
        histprice = pd.concat([pd.DataFrame(i[0]) for i in values], ignore_index=True)
        dividends = pd.concat([pd.DataFrame(i[1]) for i in values], ignore_index=True)
        splits    = pd.concat([pd.DataFrame(i[2]) for i in values], ignore_index=True)
        events    = pd.concat([dividends, splits], ignore_index=True)
        histprice = self.processdf(histprice).dropna()
        events    = self.processdf(events).dropna()
        histprice = histprice.astype({'volume': int})
        print('Completed!')
        if not loadtotable: return histprice, events
        SqLite.loadtable(histprice, tbl_hprice)
        # SqLite.createindex(tbl_hprice, 'symbol')
        SqLite.loadtable(events, tbl_actions)
        # SqLite.createindex(tbl_actions, 'symbol')
