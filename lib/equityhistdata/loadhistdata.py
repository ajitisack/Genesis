import pandas as pd
import arrow
import time
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from nsedata.lib.equityhistdata.gethistdata import EquityHistDataDict
from nsedata.lib.config import Config
from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils import Utility

class EquityHistData(EquityHistDataDict, Config):

    def __init__(self):
        Config.__init__(self)

    @SqLite.connector
    def getsymbols(self, n_symbols):
        tblname = 'symbols'
        query = f"select distinct symbol || '.NS' as symbol from {tblname} where innifty200 = 1 or inniftymidcap100 = 1 or inniftysmallcap100 = 1 "
        if n_symbols > 0: query += f'limit {n_symbols}'
        df = pd.read_sql(query, SqLite.conn)
        symbols = df.symbol.to_list()
        symbols += ['NIFTYBEES.NS', 'BANKBEES.NS', 'GOLDBEES.NS', 'NETFIT.NS', 'N100.NS', 'JUNIORBEES.NS']
        return symbols

    def processdf(self, df):
        df['date'] = df['date'].apply(lambda x: arrow.get(x).to('Asia/Kolkata').format('YYYY-MM-DD'))
        df['symbol'] = df['symbol'].apply(lambda x: x.split('.')[0].replace('^', ''))
        df = Utility.adddatefeatures(df)
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm:ss')
        return df

    def downloadhistprice(self, symbols_list, startdt):
        nthreads = min(len(symbols_list), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.gethistdata, symbols_list, repeat(startdt))
        data = list(results)
        return data

    @Utility.timer
    def download(self, n_symbols, loadtotable, startdt):
        symbols = self.getsymbols(n_symbols)
        print(f'Downloading historical prices(daily, weekly & monthly) and events from yahoo finance for {len(symbols)} NSE symbols from {startdt}', end='...', flush=True)
        data = self.downloadhistprice(symbols, startdt)

        dlyhistprice = pd.concat([pd.DataFrame(i[0]) for i in data], ignore_index=True)
        wlyhistprice = pd.concat([pd.DataFrame(i[1]) for i in data], ignore_index=True)
        mlyhistprice = pd.concat([pd.DataFrame(i[2]) for i in data], ignore_index=True)
        dividends    = pd.concat([pd.DataFrame(i[3]) for i in data], ignore_index=True)
        splits       = pd.concat([pd.DataFrame(i[4]) for i in data], ignore_index=True)
        events       = pd.concat([dividends, splits], ignore_index=True)
        events       = self.processdf(events).dropna()

        dlyhistprice = self.processdf(dlyhistprice).dropna()
        wlyhistprice = self.processdf(wlyhistprice).dropna()
        mlyhistprice = self.processdf(mlyhistprice).dropna()
        dlyhistprice = dlyhistprice.astype({'volume': int})
        wlyhistprice = wlyhistprice.astype({'volume': int})
        mlyhistprice = mlyhistprice.astype({'volume': int})

        print('Completed !')

        if not loadtotable: return dlyhistprice, wlyhistprice, mlyhistprice, events
        SqLite.loadtable(dlyhistprice, self.tbl_hpricedly)
        SqLite.loadtable(wlyhistprice, self.tbl_hpricewly)
        SqLite.loadtable(mlyhistprice, self.tbl_hpricemly)
        # SqLite.createindex(tbl_hprice, 'symbol')
        SqLite.loadtable(events, self.tbl_events)
        # SqLite.createindex(tbl_actions, 'symbol')
