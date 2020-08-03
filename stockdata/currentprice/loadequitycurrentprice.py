import pandas as pd
import arrow
import datetime
from glob import glob
from concurrent.futures import ThreadPoolExecutor

from stockdata.currentprice.getcurrentprice import CurrentPriceDict
from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

class CurrentPriceEquity(CurrentPriceDict, Config):

    def __init__(self):
        Config.__init__(self)

    @SqLite.connector
    def getsymbols(self, exchange, n_symbols):
        tblname = self.tbl_symbols
        if exchange == 'NSE': query = f"select symbol || '.NS' as symbol from {tblname} where innsefo = 1 "
        if n_symbols > 0: query += f'limit {n_symbols}'
        df = pd.read_sql(query, SqLite.conn)
        return list(df.symbol)

    def processdf(self, df):
        df['timestamp']  = df['timestamp'].apply(lambda x: arrow.get(x).format('ddd MMM-DD-YYYY'))
        df['symbol'] = df['symbol'].apply(lambda x: x.split('.')[0])
        df['change'] = df.apply(lambda x: x['close'] - x['open'], axis=1)
        df['changepct'] = df.apply(lambda x: round((x['close'] - x['open'])/x['close'] * 100, 2), axis=1)
        df = Utility.reducesize(df)
        df = df.astype({'volume': int})
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
        return df

    @Utility.timer
    def download(self, exchange, n_symbols, loadtotable):
        if exchange == 'NSE': tblname = self.tbl_nseeqcurrent
        symbols = self.getsymbols(exchange, n_symbols)
        print(f'Downloading current prices from yahoo finance for {exchange} {len(symbols)} symbols', end='...', flush=True)
        nthreads = min(len(symbols), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.getintradaydata, symbols)
        values = list(results)
        dfs = [pd.DataFrame(d) for d in values]
        df = pd.concat(dfs, ignore_index=True).dropna()
        if df.empty:
            print('No data!')
            return None
        df = self.processdf(df)
        print('Completed!')
        if not loadtotable: return df
        SqLite.loadtable(df, tblname)
