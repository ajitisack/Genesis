
https://www.moneycontrol.com/india/stockmarket/sector-classification/marketstatistics/nse/automotive.html
https://www.moneycontrol.com/stocks/marketstats/sector-scan/nse/today.html


from selectolax.parser import HTMLParser
import requests
import re

url = 'https://www.moneycontrol.com/india/stockmarket/sector-classification/marketstatistics/nse/automotive.html'
html = requests.get(url).text

html
tree = HTMLParser(html)
for tag in tree.css('script') + tree.css('style'): tag.decompose()

node = tree.css('td')
len(node)
node[1].attrs['class']
node[1].html
node[1].text()


list = [n.text() for n in node]

for n in node:
    print(n.html)
