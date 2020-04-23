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

    @staticmethod
    def getdomainkeyvalue(json_str, domain, key):
        return json_str[domain][key] if domain in json_str and json_str[domain] and key in json_str[domain] else ''

    @staticmethod
    def getitems(secdetailsfile):
        x = []
        with open(secdetailsfile) as f:
            for line in f:
                if line.strip() == '': continue
                if line.strip().startswith('['):
                    key = line.strip().replace('[','').replace(']','')
                    continue
                x.append((key, line.strip()))
        return x

    def getquotejson(self, symbol):
        url = f'{self.quoteurl}/{symbol}'
        with requests.Session() as s:
            s.mount(url, HTTPAdapter(max_retries=self.request_max_rtries))
            response = s.get(url)
        if "QuoteSummaryStore" not in response.text:
            return {}
        json_str = response.text.split('root.App.main =')[1].split('(this)')[0].split(';\n}')[0].strip()
        data = json.loads(json_str)['context']['dispatcher']['stores']['QuoteSummaryStore']
        new_data = json.dumps(data).replace('{}', 'null')
        new_data = re.sub(r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)
        return json.loads(new_data)

    def getdetails(self, symbol):
        try:
            json_str = self.getquotejson(symbol)
            items = SecurityDetails.getitems(self.secdetailsfile)
            result = [symbol] + [SecurityDetails.getdomainkeyvalue(json_str, item[0], item[1]) for item in items]
            columns = ['symbol'] + [item[1].lower() for item in items]
            df = pd.DataFrame([result], columns=columns)
            if df.empty: self.msglogger.info('no hist price for {symbol}')
            return df
        except:
            self.msglogger.error('no hist price for {symbol}')
