import requests
import json
import arrow
import pandas as pd
from itertools import repeat
from requests.adapters import HTTPAdapter
from selectolax.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor

from stockdata.historicaldata.loadhistdata import HistData
from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

class Indices(HistData, Config):

    def __init__(self):
        Config.__init__(self)

    def getmcdata(self, params):
        try:
            exchange, type, name, url = params
            with requests.Session() as session:
                session.mount(url, HTTPAdapter(max_retries=self.request_max_retries))
                html = session.get(url).text
            tree = HTMLParser(html)
            for tag in tree.css('script') + tree.css('style'): tag.decompose()
            data = []
            nodes = tree.css('td')
            for node in nodes[1:]:
                text = node.text()
                if text == 'SENSEX': break
                data.append(text)
                if 'href' in node.html:
                    data.append(node.child.child.attributes['href'].split('/')[-1])
            n = 9
            df = pd.DataFrame([data[x:x+n] for x in range(0, len(data), n)])
            df.columns = ['company', 'code', 'ltp', 'pctchange', 'volume', 'buyprice', 'sellprice', 'buyqty', 'sellqty']
            df.insert(loc=0, column = 'exchange', value=exchange)
            df.insert(loc=1, column = 'type', value=type)
            df.insert(loc=2, column = 'name', value=name)
            return df
        except:
            return pd.DataFrame()

    def getindiceshistdata(self, symbol, startdt):
        try :
            data = self.getchartresult(symbol, startdt)
            data = data.get('chart').get('result')[0]
            quotes = self.getquotes(data)
            return quotes
        except :
            return {}

    def loadindicesdetails(self, indices):
        nthreads = min(len(indices), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.getmcdata, indices)
        df = pd.concat(results, ignore_index=True)
        df = Utility.reducesize(df)
        return df

    def loadindiceshistprices(self, symbols, startdt):
        nthreads = min(len(symbols), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.getindiceshistdata, symbols, repeat(startdt))
        df = pd.concat([pd.DataFrame(d) for d in results], ignore_index=True)
        df = df.dropna()
        df = df.astype({'volume': int})
        df = self.processdf(df)
        return df

    @Utility.timer
    def loadindicesdata(self, startdt):
        print(f'Downloading details and historical prices of BSE and NSE Indices from {startdt}', end='...', flush=True)
        df_indices = pd.read_csv(self.indices_file)
        indices = list(zip(df_indices.exchange, df_indices.type, df_indices.name, df_indices.mcurl))
        symbols = list(df_indices.symbol)
        indices = self.loadindicesdetails(indices)
        indiceshist = self.loadindiceshistprices(symbols, startdt)
        print('Completed')
        nse_indices     = indices.query("exchange == 'NSE'")
        bse_indices     = indices.query("exchange == 'BSE'")
        nse_indiceshist = indiceshist.query("exchange == 'NSE'")
        bse_indiceshist = indiceshist.query("exchange == 'BSE'")
        SqLite.loadtable(nse_indices, self.tbl_nseindices)
        SqLite.loadtable(bse_indices, self.tbl_bseindices)
        SqLite.loadtable(nse_indiceshist, self.tbl_nseindiceshist)
        SqLite.loadtable(bse_indiceshist, self.tbl_bseindiceshist)
