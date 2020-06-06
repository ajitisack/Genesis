import pandas as pd
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from stockdata.indices.readindices import IndicesList
from stockdata.historicaldata.loadhistdata import HistData

from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

class IndicesHistData(IndicesList, HistData, Config):

    def __init__(self):
        Config.__init__(self)

    def getindiceshistdata(self, symbol, startdt):
        try :
            data = self.getchartresult(symbol, startdt)
            data = data.get('chart').get('result')[0]
            quotes = self.getquotes(data)
            return quotes
        except :
            return {}

    @Utility.timer
    def downloadindiceshistdata(self, exchange, loadtotable, startdt):
        if exchange == 'NSE': tbl_indices = self.tbl_nseindiceshist
        if exchange == 'BSE': tbl_indices = self.tbl_bseindiceshist
        indices = self.readIndices(exchange).query("symbol.notna()")
        symbols = indices.symbol.to_list()
        print(f'Downloading histprice of {len(symbols)} {exchange.upper()} indices from YahooFinance', end='...', flush=True)
        nthreads = min(len(symbols), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.getindiceshistdata, symbols, repeat(startdt))
        df = pd.concat([pd.DataFrame(d) for d in results], ignore_index=True)
        df = df.dropna()
        df = df.astype({'volume': int})
        df = self.processdf(df)
        d = dict(zip(indices['symbol'].apply(lambda x: x.replace('^','').replace('.NS', '')), indices.name))
        df['symbol'] = df['symbol'].apply(lambda x: d[x])
        df.rename(columns={'symbol':'indexname'}, inplace=True)
        print('Completed')
        if not loadtotable: return df
        SqLite.loadtable(df, tbl_indices)
