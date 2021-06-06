import json
import arrow
import requests
import pandas as pd
import numpy as np
import time

from nsedata.lib.config import Config
from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils import Utility

class OptionChain(Config):

    def __init__(self):
        Config.__init__(self)

    def getOptionChainJson(self, symbol):
        headers = { "User-Agent" : self.user_agent}
        cookies = { 'nsit' : self.nsit, 'nseappid' : self.nseappid}
        url = f'{self.url_indexoptchain}={symbol}'
        response = requests.get(url, headers=headers, cookies=cookies)
        while response.status_code != 200:
            response = requests.get(url, headers=headers, cookies=cookies)
            time.sleep(1)
        return json.loads(response.text)

    def getOptionChain(self, symbol):
        optionchain = self.getOptionChainJson(symbol)
        data = optionchain['records']['data']
        timestamp = f"{optionchain['records']['timestamp']} Asia/Calcutta"
        timestamp = int(arrow.get(timestamp, 'DD-MMM-YYYY HH:mm:ss ZZZ').timestamp())
        l = []
        for d in data:
            if d.get('CE'):
                x = d.get('CE')
                x['option'] = 'CE'
                l.append(x)
            if d.get('PE'):
                x = d.get('PE')
                x['option'] = 'PE'
                l.append(x)
        df = pd.DataFrame(l)
        df.columns = ['strike', 'expirydt', 'symbol', 'id', 'oi', 'oichng', 'oichngpct', 'vol', 'iv', 'ltp', 'ltpchng', 'ltpchngpct', 'buyqty', 'sellqty', 'bidqty', 'bidprice', 'askqty', 'askprice', 'spot', 'option']
        reqdcols = ['symbol', 'spot', 'expirydt', 'strike', 'option', 'oi', 'oichng', 'oichngpct', 'vol', 'iv', 'ltp', 'ltpchng', 'ltpchngpct', 'buyqty', 'sellqty', 'bidqty', 'bidprice', 'askqty', 'askprice']
        df = df[reqdcols]
        df.insert(loc = 0, column='timestamp', value=timestamp)
        df.expirydt = df.expirydt.apply(lambda x: arrow.get(x, 'DD-MMM-YYYY').format('YYYY-MM-DD'))
        df = df.sort_values(by=['expirydt', 'option', 'strike'], ignore_index=True)
        df['bidaskspread'] = df['askprice'] - df['bidprice']
        df['oichngpct'] = df['oichngpct'].apply(lambda x: np.round(x,2))
        df['ltpchngpct'] = df['ltpchngpct'].apply(lambda x: np.round(x,2))
        df = Utility.addtimefeatures(df)
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm:ss')
        return df
