import pandas as pd
import arrow
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from .gethistdata import HistDataDict
from ..config import Config
from ..sqlite import SqLite
from ..utils import Utility


class HistData(HistDataDict):

    def __init__(self):
        Config.__init__(self)

    @SqLite.connector
    def getsymbols(self, n_symbols):
        query = f"select symbol || '.NS' as symbol from symbols where innse = 1 union all select symbol || '.BO' as symbol from symbols where inbse = 1 "
        if n_symbols > 0: query += f'limit {n_symbols}'
        df = pd.read_sql(query, SqLite.conn)
        return list(df.symbol)

    def loadtotable(self, df, tblname):
        df['date'] = df['date'].apply(lambda x: arrow.get(x).format('YYYY-MM-DD'))
        df['symbol'] = df['symbol'].apply(lambda x: x[:-3])
        df['exchange'] = df['exchange'].apply(lambda x: x.replace('NSI', 'NSE'))
        df = Utility.adddatefeatures(df)
        df = Utility.reducesize(df)
        SqLite.loadtable(df, tblname)
        SqLite.createindex(tblname, 'symbol')

    @Utility.timer
    def download(self, n_symbols, loadtotable, startdt):
        symbols = self.getsymbols(n_symbols)
        print(f'Downloading historical prices and actions from yahoo finance for {len(symbols)} symbols from {startdt}', end='...', flush=True)
        nthreads = min(len(symbols), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.gethistdata, symbols, repeat(startdt))
        values = list(results)
        return values
        histprice = pd.concat([pd.DataFrame(i[0]) for i in values], ignore_index=True)
        dividends = pd.concat([pd.DataFrame(i[1]) for i in values], ignore_index=True)
        splits    = pd.concat([pd.DataFrame(i[2]) for i in values], ignore_index=True)
        actions   = pd.concat([dividends, splits], ignore_index=True)
        print('Completed!')
        if not loadtotable: return histprice, actions
        self.loadtotable(histprice, self.tbl_hpricedly)
        self.loadtotable(actions, self.tbl_actions)
