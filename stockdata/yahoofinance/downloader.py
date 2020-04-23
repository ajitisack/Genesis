import pandas as pd
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from .securityhistprice import SecurityHistPrice
from .securitydetails import SecurityDetails
from ..config import Config
from ..sqlite import SqLite
from ..utils import Utility

class Downloader(Config, SecurityHistPrice, SecurityDetails):

    def __init__(self):
        self.nodatalist = []
        Config.__init__(self)

    @SqLite.connector
    def getsymbols(self, n_symbols):
        query = f"select symbol from {self.tbl_symbols} where 1 = 1 limit {n_symbols}"
        df = pd.read_sql(query, SqLite.conn)
        return list(df.symbol)

    def loadactions(self, df):
        tblname = self.tbl_actions
        splits = df[df.splits != 0][['symbol', 'date', 'splits', 'year', 'month', 'day', 'wkday', 'wknr', 'qrtr']]
        splits.insert(loc=2, column = 'action', value='splits')
        splits.rename(columns = {'splits':'value'}, inplace = True)
        splits.reset_index(drop=True, inplace=True)
        dividend = df[df.dividend != 0][['symbol', 'date', 'dividend', 'year', 'month', 'day', 'wkday', 'wknr', 'qrtr']]
        dividend.insert(loc=2, column = 'action', value='dividend')
        dividend.rename(columns = {'dividend':'value'}, inplace = True)
        dividend.reset_index(drop=True, inplace=True)
        actions = pd.concat([splits, dividend], ignore_index=True)
        dividend = Utility.reducesize(dividend)
        actions  = Utility.reducesize(actions)
        SqLite.loadtable(actions, tblname)
        SqLite.createindex(tblname, 'symbol')

    @Utility.timer
    def downloadhistprice(self, n_symbols, loadtotable, startdt, interval):
        tblname = self.tbl_quotesdly if interval == '1d' else self.tbl_quotesmly
        symbols = self.getsymbols(n_symbols)
        print(f'Downloading historical prices and actions from yahoo finance for {len(symbols)} symbols from {startdt}', end='...', flush=True)
        nthreads = min(len(symbols), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.gethistprice, symbols, repeat(startdt), repeat(interval))
        df = pd.concat(results, ignore_index=True)
        print('Completed')
        if not loadtotable: return df
        histprice = df.drop(['dividend', 'splits'], axis=1)
        SqLite.loadtable(histprice, tblname)
        SqLite.createindex(tblname, 'symbol')
        self.loadactions(df)

    @Utility.timer
    def downloaddetails(self, n_symbols, loadtotable):
        symbols = self.getsymbols(n_symbols)
        print(f'Downloading details and esg scores of {len(symbols)} symbols from yahoo finance', end='...', flush=True)
        nthreads = min(len(symbols), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.getdetails, symbols)
        df = pd.concat(results, ignore_index=True)
        df = df.drop(df.loc[df.shortname==''].index).reset_index(drop=True)
        print('Completed')
        esgcols = ['peergroup', 'peercount', 'environmentscore', 'socialscore', 'governancescore', 'totalesg', 'percentile', 'esgperformance', 'highestcontroversy'
        , 'palmoil', 'controversialweapons', 'gambling', 'nuclear', 'furleather', 'alcoholic', 'gmo', 'catholic', 'animaltesting', 'tobacco', 'coal', 'pesticides', 'adult', 'smallarms', 'militarycontract']
        df_esg = df[['symbol'] + esgcols]
        df_esg = df_esg.drop(df_esg.loc[df_esg.peergroup==''].index).reset_index(drop=True)
        df.drop(esgcols, axis=1, inplace=True)
        df     = Utility.reducesize(df)
        df_esg = Utility.reducesize(df_esg)
        if not loadtotable: return df, df_esg
        SqLite.loadtable(df, self.tbl_secdetails)
        SqLite.createindex(self.tbl_secdetails, 'symbol')
        SqLite.loadtable(df_esg, self.tbl_esgdetail)
        SqLite.createindex(self.tbl_esgdetail, 'symbol')
