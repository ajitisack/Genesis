import requests
from io import StringIO
import pandas as pd
from requests.adapters import HTTPAdapter

class IndexSymbols():

    def getnseindexsymbols(self, params):
        # print(f'{params}', end='...', flush=True)
        exchange, type, indexname, url = params
        # headers = { 'User-Agent': self.user_agent }
        # with requests.Session() as session:
        #     session.mount(url, HTTPAdapter(max_retries=self.request_max_retries))
        #     response = session.get(url, headers=headers)
        # data = StringIO(response.text)
        df = pd.read_csv(url)
        df.insert(0, 'indextype', type)
        df.insert(1, 'indexname', indexname)
        return df

    def getbseindexsymbols(self, params):
        pass
