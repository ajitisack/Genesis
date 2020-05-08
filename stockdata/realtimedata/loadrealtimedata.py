import pandas as pd
import arrow
from concurrent.futures import ThreadPoolExecutor

from .getrealtimedata import RealTimeDataDict
from ..config import Config
from ..sqlite import SqLite
from ..utils import Utility


class RealTimeData(RealTimeDataDict):

    def __init__(self):
        Config.__init__(self)

    @SqLite.connector
    def getsymbols(self, n_symbols):
        query = f"select symbol || '.NS' as symbol from symbols where innse = 1 union all select symbol || '.BO' as symbol from symbols where inbse = 1 "
        if n_symbols > 0: query += f'limit {n_symbols}'
        df = pd.read_sql(query, SqLite.conn)
        return list(df.symbol)

    def processdf(self, df):
        df['time'] = df['time'].apply(lambda x: arrow.get(x).to('local').format('YYYY-MM-DD hh:mm:SS A'))
        df['exchange'] = df['symbol'].apply(lambda x: 'BSE' if x.split('.')[1] == 'BO' else 'NSE')
        df['symbol'] = df['symbol'].apply(lambda x: x.split('.')[0].replace('^', ''))
        # df = Utility.adddatefeatures(df)
        df = Utility.reducesize(df)
        return df

    @Utility.timer
    def download(self, n_symbols):
        symbols = self.getsymbols(n_symbols)
        print(f'Downloading realtime prices from yahoo finance for {len(symbols)} symbols', end='...', flush=True)
        nthreads = min(len(symbols), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.getrealtimedata, symbols)
        values = list(results)
        dfs = [pd.DataFrame(d) for lst in values for d in lst]
        df = pd.concat(dfs, ignore_index=True)
        df = self.processdf(df)
        print('Completed!')
        return df
