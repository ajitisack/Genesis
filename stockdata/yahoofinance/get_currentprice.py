import json
import requests
import arrow
import time
from requests.adapters import HTTPAdapter

from stockdata.sdlogger import SDLogger

d = {'^NSEI':'Nifty 50', '^CNXAUTO':'Auto', '^NSEBANK':'Banks', '^CNXPHARMA':'Pharma', '^CNXMETAL':'Metal', '^CNXIT':'IT'}

class CurrentPrice(SDLogger):

    def getquotes(self, data, sector, symbol):
        try:
            quotes = data.get('indicators').get('quote')[0]
            if quotes == {}: return {}
            price = {}
            price['sector'] = sector
            price['symbol'] = d.get(symbol) or symbol
            price['open'] = quotes.get('open')[0]
            price['low'] = quotes.get('low')[0]
            price['high'] = quotes.get('high')[0]
            price['ltp'] = quotes.get('close')[0]
            price['volume'] = quotes.get('volume')[0]
            return price
        except:
            return {}

    def getchartresult(self, sector, symbol):
        symbol   = f'{symbol}' if sector == 'Index' else f'{symbol}.NS'
        interval = '1d'
        url      = f'{self.yfqueryurl}/{symbol}?symbol={symbol}&interval={interval}'
        response = requests.get(url)
        return json.loads(response.text)

    def gethistdata(self, sector_symbol):
        sector, symbol = sector_symbol[0], sector_symbol[1]
        try:
            data = self.getchartresult(sector, symbol)
            data = data.get('chart').get('result')[0]
            quotes = self.getquotes(data, sector, symbol)
            return quotes
        except:
            return {}
