import re
import requests
import json
from requests.adapters import HTTPAdapter
from selectolax.parser import HTMLParser


class SymbolDetails():

    def getsymboldetails(self, params, exchange):
        isin, symbolid, symbolcd = params
        values = {'isin':isin, 'symbolid':symbolid, 'symbolcd':symbolcd, 'exchange':exchange}
        try:
            for section in self.terms.keys():
                api = f'{self.mcpriceapiurl}/{exchange.lower()}/{section}/{symbolid}'
                with requests.Session() as session:
                    session.mount(api, HTTPAdapter(max_retries=self.request_max_retries))
                    response = session.get(api, allow_redirects=False)
                    data = json.loads(response.text).get('data')
                    if data is not None:
                        for k,v in self.terms.get(section).items():
                            values[v] = data.get(k)
            return values
        except:
            return values
