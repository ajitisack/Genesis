import pandas as pd
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from .yf_symboldetails import SymbolDetails
from ..config import Config
from ..sqlite import SqLite
from ..utils import Utility

class YahooFinance(Config, SymbolDetails):

    def __init__(self):
        Config.__init__(self)
        self.details_items = self.getitems()

    @SqLite.connector
    def getsymbols(self, exchange, n_symbols):
        if exchange == 'NSE': query = f"select symbol || '.NS' as symbol from symbols where innse = 1 "
        if exchange == 'BSE': query = f"select symbol || '.BO' as symbol from symbols where inbse = 1 "
        if n_symbols > 0: query += f'limit {n_symbols}'
        df = pd.read_sql(query, SqLite.conn)
        return list(df.symbol)

    @Utility.timer
    def downloaddetails(self, exchange, n_symbols, loadtotable):
        symbols = self.getsymbols(exchange.upper(), n_symbols)
        if exchange == 'NSE': tbl_details   = self.tbl_nsesecdtls
        if exchange == 'NSE': tbl_esgscores = self.tbl_nseesg
        if exchange == 'BSE': tbl_details   = self.tbl_bsesecdtls
        if exchange == 'BSE': tbl_esgscores = self.tbl_bseesg
        print(f'Downloading details and esg scores of {len(symbols)} {exchange.upper()} symbols from Yahoo Finance', end='...', flush=True)
        nthreads = min(len(symbols), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.getdetails, symbols)
        df = pd.DataFrame(results)
        df = df.drop(df.loc[df.shortname==''].index).reset_index(drop=True)
        print('Completed')
        esgcols = ['peergroup', 'peercount', 'environmentscore', 'socialscore', 'governancescore', 'totalesg', 'percentile', 'esgperformance', 'highestcontroversy'
        , 'palmoil', 'controversialweapons', 'gambling', 'nuclear', 'furleather', 'alcoholic', 'gmo', 'catholic'
        , 'animaltesting', 'tobacco', 'coal', 'pesticides', 'adult', 'smallarms', 'militarycontract']
        df_esg = df[['symbol', 'exchange'] + esgcols]
        df_esg = df_esg.drop(df_esg.loc[df_esg.peergroup==''].index).reset_index(drop=True)
        df.drop(esgcols, axis=1, inplace=True)
        df     = Utility.reducesize(df)
        df_esg = Utility.reducesize(df_esg)
        if not loadtotable: return df, df_esg
        SqLite.loadtable(df, tbl_details)
        SqLite.createindex(tbl_details, 'symbol')
        if not df_esg.empty :
            SqLite.loadtable(df_esg, tbl_esgscores)
            SqLite.createindex(tbl_esgscores, 'symbol')
