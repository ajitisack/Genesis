# https://www.moneycontrol.com/india/stockmarket/sector-classification/marketstatistics/nse/automotive.html
# https://www.moneycontrol.com/stocks/marketstats/sector-scan/nse/today.html
# https://priceapi-aws.moneycontrol.com/pricefeed/bse/equitycash/BGW
# https://priceapi-aws.moneycontrol.com/pricefeed/nse/equitycash/BGW
import requests
import json
import pandas as pd
from requests.adapters import HTTPAdapter
from selectolax.parser import HTMLParser

from ..utils import Utility

class SectorClassify():

    def getnodedetails(self, node):
        href = node.child.attributes['href'] if 'href' in node.child.attributes else ''
        url = href if 'stockpricequote' in href else ''
        if url == '': return node.text()
        else : return f'{node.text()}>{href}'

    def getsectors(self):
        with open(self.mcsectorsfile) as f:
            sectors = f.read().splitlines()
        return sectors

    def getsectorclassif(self):
        n = 6
        dfs = []
        with requests.Session() as session:
            for exchange in ['nse', 'bse']:
                for sector in self.getsectors():
                    url = f'{self.mcsectorclassifurl}/{exchange}/{sector}.html'
                    session.mount(url, HTTPAdapter(max_retries=self.request_max_retries))
                    html = session.get(url).text
                    tree = HTMLParser(html)
                    for tag in tree.css('script') + tree.css('style'): tag.decompose()
                    node = tree.css('td')
                    data = [self.getnodedetails(n) for n in node][1:-4]
                    row_data = [data[x:x+n] for x in range(0, len(data), n)]
                    df = pd.DataFrame(row_data, columns=['name', 'industry', 'lastprice', 'change', 'changepct', 'mktcap'])
                    df.drop(['change', 'changepct', 'mktcap'], axis=1, inplace=True)
                    df['symbolurl'] = url
                    df.insert(loc=0, column = 'exchange', value=exchange)
                    df.insert(loc=1, column = 'sector', value=sector)
                    dfs.append(df)
        df = pd.concat(dfs, ignore_index=True)
        df['symbolurl'] = df['name'].apply(lambda x: x.split('>')[1].replace('/india/stockpricequote/', ''))
        df['symbolcd'] = df['symbolurl'].apply(lambda x: x.split('/')[2])
        df['name'] = df['name'].apply(lambda x: x.split('>')[0])
        return df
