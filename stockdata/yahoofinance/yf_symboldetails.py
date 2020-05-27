import json
import re
import requests
from requests.adapters import HTTPAdapter

class SymbolDetails():

    def getitems(self):
        x = []
        with open(self.yfdetailsfile) as f:
            for line in f:
                line = line.strip()
                if line == '': continue
                if line.startswith('['):
                    key = line.replace('[','').replace(']','')
                    continue
                x.append((key, line))
        return x

    def getquotesummary(self, symbol):
        url = f'{self.yfquoteurl}/{symbol}?modules=defaultKeyStatistics,details,summaryProfile,recommendationTrend,financialsTemplate,earnings,price,financialData,quoteType,calendarEvents,summaryDetail,symbol,esgScores,upgradeDowngradeHistory,pageViews'
        with requests.Session() as session:
            session.mount(url, HTTPAdapter(max_retries=self.request_max_retries))
            response = session.get(url)
        json_str = json.loads(response.text).get('quoteSummary').get('result')[0]
        return json_str

    def getitemvalue(self, json_str, section, item):
        try:
            value = json_str.get(section).get(item) or ''
            value = value.get('raw') if type(value) == dict else value
        except:
            value = ''
        return value

    def getdetails(self, symbol):
        exchange = 'BSE' if symbol.endswith('.BO') else 'NSE'
        details = {'symbol' : symbol[:-3], 'exchange' : exchange}
        json_str = self.getquotesummary(symbol)
        if json_str:
            for section, item in self.details_items:
                details[item.lower()] = self.getitemvalue(json_str, section, item)
        return details
