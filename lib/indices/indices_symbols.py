import arrow
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from nsedata.lib.config import Config
from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils  import Utility

class IndicesSymbols(Config):

    def __init__(self):
        Config.__init__(self)

    def readIndices(self, exchange):
        df = pd.read_excel(self.indices_file, sheet_name=exchange.upper())
        df = df[df.url.notna()]
        return df

    def getnseindexsymbols(self, params):
        exchange, type, indexname, indexsymbol, url = params
        df = pd.read_csv(url)
        df.insert(0, 'indextype', type)
        df.insert(1, 'indexname', indexname)
        df.insert(2, 'indexsymbol', indexsymbol)
        return df

    def processdf(self, df):
        df.columns = map(str.lower, df.columns)
        df.drop(['series'], axis=1, inplace=True)
        df['indexsymbol'] = df['indexsymbol'].fillna('')
        df.rename(columns={'company name':'company', 'isin code':'isin'}, inplace=True)
        df['industry'] = df['industry'].apply(lambda x: x.title() if x != 'IT' else x)
        df['company'] = df['company'].apply(lambda x: x.replace(' Ltd.', ''))
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
        return df

    @Utility.timer
    def download(self, loadtotable):
        indices = self.readIndices('NSE')
        print(f'Downloading symbols of {indices.shape[0]} indices from nseindia.com', end='...', flush=True)
        params = zip(indices.exchange, indices.type, indices.name, indices.yfsymbol, indices.url)
        nthreads = min(indices.shape[0], int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.getnseindexsymbols, params)
        df = pd.concat(list(results), ignore_index=True)
        df = self.processdf(df)
        print('Completed')
        if not loadtotable: return df
        SqLite.loadtable(df, self.tbl_indices)
