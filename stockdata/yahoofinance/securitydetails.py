import requests as requests
import pandas as pd
import json
import arrow
import re
import requests
from requests.adapters import HTTPAdapter

from ..utils import Utility
from ..sdlogger import SDLogger

class SecurityDetails(SDLogger):

    def getitems(self):
        x = []
        with open(self.secdetailsfile) as f:
            for line in f:
                line = line.strip()
                if line == '': continue
                if line.startswith('['):
                    key = line.replace('[','').replace(']','')
                    continue
                x.append((key, line))
        return x

    def getquotejson(self, symbol):
        url = f'{self.quoteurl}/{symbol}'
        with requests.Session() as session:
            session.mount(url, HTTPAdapter(max_retries=self.request_max_retries))
            response = session.get(url)
        if 'QuoteSummaryStore' not in response.text:
            return {}
        json_str = response.text.split('root.App.main =')[1].split('(this)')[0].split(';\n}')[0].strip()
        data = json.loads(json_str)['context']['dispatcher']['stores']['QuoteSummaryStore']
        new_data = json.dumps(data).replace('{}', 'null')
        new_data = re.sub(r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)
        return json.loads(new_data)

    def getdetails(self, symbol):
        exchange = 'BSE' if symbol.endswith('.BO') else 'NSE'
        details = {'symbol' : symbol[:-3], 'exchange' : exchange}
        json_str = self.getquotejson(symbol)
        for section, item in self.details_items:
            attrib = json_str.get(section)
            details[item.lower()] = attrib.get(item) if attrib else ''
        return details
