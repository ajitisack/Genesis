import requests, json, re
url = 'https://finance.yahoo.com/quote/HDFCBANK.BO'
response = requests.get(url)
json_str = response.text.split('root.App.main =')[1].split('(this)')[0].split(';\n}')[0].strip()
data = json.loads(json_str)['context']['dispatcher']['stores']['QuoteSummaryStore']
new_data = json.dumps(data).replace('{}', 'null')
new_data = re.sub(r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)
x = json.loads(new_data)

x.keys()

x['defaultKeyStatistics']

for i in x.keys():
    if 'isin' in str(x[i]):
        print(i)
