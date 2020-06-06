import pandas as pd
import arrow
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from stockdata.moneycontrol.mc_symboldetails import SymbolDetails
from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility
from stockdata.sdlogger import SDLogger

class MoneyControl(SDLogger, Config, SymbolDetails):

    def __init__(self):
        self.nodatalist = []
        Config.__init__(self)
        self.terms = self.getkeyterms()

    def getkeyterms(self):
        items={}
        with open(self.mcdetailsfile) as f:
            for line in f:
                line = line.strip()
                if line == '': continue
                if line.startswith('['):
                    key = line.replace('[','').replace(']','')
                    items[key] = {}
                else:
                    k = line.split('=')[0].strip()
                    v = line.split('=')[1].strip()
                    items[key][k] = v
        return items

    @SqLite.connector
    def getsymbols(self, exchange, n_symbols):
        if exchange == 'NSE': query = f"select isin from symbols where innse = 1 "
        if exchange == 'BSE': query = f"select isin from symbols where inbse = 1 "
        if n_symbols > 0: query += f'limit {n_symbols}'
        df = pd.read_sql(query, SqLite.conn)
        return list(df['isin'])

    @Utility.timer
    def downloaddetails(self, exchange, n_symbols, loadtotable):
        if exchange == 'NSE': tbl_mcprofile = self.tbl_nsemcprofile
        if exchange == 'BSE': tbl_mcprofile = self.tbl_bsemcprofile
        isins = self.getsymbols(exchange.upper(), n_symbols)
        print(f'Downloading details of {len(isins)} {exchange} symbols from Money Control', end='...', flush=True)
        df = pd.read_csv(self.mcurlsfile)
        df = df[df['isin'].isin(isins)]
        params = zip(df['isin'], df['symbolid'], df['symbolcd'])
        nthreads = min(df.shape[0], int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.getsymboldetails, params, repeat(exchange))
        df = pd.DataFrame(results)
        df = Utility.reducesize(df)
        df['rundt'] = arrow.now().format('YYYY-MM-DD')
        print('Completed')
        if not loadtotable: return df
        SqLite.loadtable(df, tbl_mcprofile)
