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
        query = f"select symbol, inbse, innse from {self.tbl_seclist} where 1 = 1 limit {n_symbols}"
        df = pd.read_sql(query, SqlLite.conn)
        df['ticker'] = df.apply(lambda x: x['symbol'] + '.NS' if x['innse']==1 else x['symbol'] + '.BO' , axis=1)
        return list(df.ticker)

    @Utility.timer
    def downloadsymbols(self):
        tblname = self.tbl_seclist
        print(f'Fetching list of all BSE and NSE Equities', end='...', flush=True)
        df = self.getsecuritylist()
        print('Completed')
        SqlLite.loadtable(df, tblname)
        SqlLite.createindex(tblname, 'symbol')

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
        SqlLite.loadtable(actions, tblname)
        SqlLite.createindex(tblname, 'symbol')

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
        SqlLite.loadtable(histprice, tblname)
        SqlLite.createindex(tblname, 'symbol')
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
        if not loadtotable: return df, df_esg
        SqlLite.loadtable(df, self.tbl_secdetails)
        SqlLite.createindex(self.tbl_secdetails, 'symbol')
        SqlLite.loadtable(df_esg, self.tbl_esgdetail)
        SqlLite.createindex(self.tbl_esgdetail, 'symbol')
