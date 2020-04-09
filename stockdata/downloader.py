import pandas as pd
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from .securitylist import SecurityList
from .securityhistprice import SecurityHistPrice
from .securitydetails import SecurityDetails
from .config import Config
from .sqlite import SqlLite
from .utils import Utility

class Downloader(Config, SecurityList, SecurityHistPrice, SecurityDetails):

    def __init__(self):
        self.nodatalist = []
        Config.__init__(self)

    @SqlLite.connector
    def getsymbols(self, n_symbols):
        query = f"select symbol, inbse, innse from security where 1 = 1 limit {n_symbols}"
        df = pd.read_sql(query, SqlLite.conn)
        df['ticker'] = df.apply(lambda x: x['symbol'] + '.BO' if x['inbse']==1 else x['symbol'] + '.NS' , axis=1)
        return list(df.ticker)

    @Utility.timer
    def downloadsymbols(self):
        tblname   = self.tbl_seclist
        indexcol  = self.indxcol_seclist
        print(f'Fetching list of all BSE and NSE Equities', end='...', flush=True)
        df = self.getsecuritylist()
        print('Completed')
        SqlLite.loadtable(df, tblname)
        SqlLite.createindex(tblname, indexcol)

    @Utility.timer
    def downloadhistprice(self, n_symbols, loadtotable, startdt, interval):
        tblname = self.tbl_quotesdly if interval == '1d' else self.tbl_quotesmly
        symbols = self.getsymbols(n_symbols)
        print(f'Downloading historical prices from yahoo finance for {len(symbols)} symbols', end='...', flush=True)
        nthreads = min(len(symbols), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.gethistprice, symbols, repeat(startdt), repeat(interval))
        df = pd.concat(results, ignore_index=True)
        print('Completed')
        if not loadtotable: return df
        SqlLite.loadtable(df, tblname)

    @Utility.timer
    def downloaddetails(self, n_symbols, loadtotable):
        tblname = self.tbl_secdetails
        symbols = self.getsymbols(n_symbols)
        print(f'Downloading details of {len(symbols)} symbols from yahoo finance', end='...', flush=True)
        nthreads = min(len(symbols), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.getdetails, symbols)
        df = pd.concat(results, ignore_index=True)
        df.drop(df.loc[df.symbol==''].index, inplace=True)
        print('Completed')
        if not loadtotable: return df
        SqlLite.loadtable(df, tblname)
