import arrow
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from stockdata.indices.readindices import IndicesList
from stockdata.indices.getindexsymbols import IndexSymbols

from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

class IndicesSymbols(IndicesList, IndexSymbols, Config):

    def __init__(self):
        Config.__init__(self)

    @Utility.timer
    def downloadindicessymbols(self, exchange, loadtotable):
        if exchange == 'NSE':
            func_indexsymbols = self.getnseindexsymbols
            tbl_indices       = self.tbl_nseindices
        if exchange == 'BSE':
            func_indexsymbols = self.getbseindexsymbols
            tbl_indices       = self.tbl_bseindices
        indices = self.readIndices(exchange)
        print(f'Downloading symbols of {indices.shape[0]} {exchange.upper()} indices from nseindia.com', end='...', flush=True)
        params = zip(indices.exchange, indices.type, indices.name, indices.url)
        nthreads = min(indices.shape[0], int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(func_indexsymbols, params)
        df = pd.concat(list(results), ignore_index=True)
        df.columns = map(str.lower, df.columns)
        df.drop(['series'], axis=1, inplace=True)
        df.insert(0, 'exchange', exchange.upper())
        df.rename(columns={'company name':'company', 'isin code':'isin'}, inplace=True)
        df['industry'] = df['industry'].apply(lambda x: x.title() if x != 'IT' else x)
        df['company'] = df['company'].apply(lambda x: x.replace(' Ltd.', ''))
        df['rundt'] = arrow.now().format('YYYY-MM-DD')
        print('Completed')
        if not loadtotable: return df
        SqLite.loadtable(df, tbl_indices)
