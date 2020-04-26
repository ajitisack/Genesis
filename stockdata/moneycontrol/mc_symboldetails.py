import re
import requests
import json
import pandas as pd
from requests.adapters import HTTPAdapter
from selectolax.parser import HTMLParser

SCID_REGEX = re.compile(r'id="scid" name="scid" value=([\'\"])(.*?)\1', re.IGNORECASE)

class SymbolDetails():

    def getsymboldetails(self, params):
        exchange, symbolurl = params
        url = f'{self.mcbaseurl}/{symbolurl}'
        values = {'symbolcd' : symbolurl.split('/')[2], 'exchange' : exchange}
        try:
            with requests.Session() as session:
                session.mount(url, HTTPAdapter(max_retries=self.request_max_retries))
                html = session.get(url).text
            symbolid = SCID_REGEX.findall(html)[0][1]
            if symbolid == '': return values
            values['symbolid'] = symbolid
            for section in self.terms.keys():
                api = f'{self.mcpriceapiurl}/{exchange}/{section}/{symbolid}'
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
