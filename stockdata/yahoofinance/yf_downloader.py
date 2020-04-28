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
    def getsymbols(self, n_symbols):
        query = f"select symbol || '.NS' as symbol from symbols where innse = 1 union all select symbol || '.BO' as symbol from symbols where inbse = 1 "
        if n_symbols > 0: query += f'limit {n_symbols}'
        df = pd.read_sql(query, SqLite.conn)
        return list(df.symbol)

    @Utility.timer
    def downloaddetails(self, n_symbols, loadtotable):
        symbols = self.getsymbols(n_symbols)
        print(f'Downloading details and esg scores of {len(symbols)} symbols from Yahoo Finance', end='...', flush=True)
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
        SqLite.loadtable(df, self.tbl_secdetails)
        SqLite.createindex(self.tbl_secdetails, 'symbol')
        SqLite.loadtable(df_esg, self.tbl_esgdetail)
        SqLite.createindex(self.tbl_esgdetail, 'symbol')
