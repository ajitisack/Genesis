import requests
from io import StringIO
import pandas as pd
from requests.adapters import HTTPAdapter

class IndexSymbols():

    def getnseindexsymbols(self, params):
        # print(f'{params}', end='...', flush=True)
        exchange, type, indexname, url = params
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0' }
        with requests.Session() as session:
            session.mount(url, HTTPAdapter(max_retries=self.request_max_retries))
            response = session.get(url, headers=headers)
        data = StringIO(response.text)
        df = pd.read_csv(data)
        df.insert(0, 'indexname', indexname)
        return df

    def getbseindexsymbols(self, params):
        pass
