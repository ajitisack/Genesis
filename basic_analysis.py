import stockdata as sd

df = sd.getdata("select * from nsehistprice where symbol in ('INDUSINDBK')")


df['change'] = df.groupby('symbol').close.transform(lambda x: x - x.shift(1))
df['pct_change'] = df.groupby(['symbol']).close.pct_change().round(4) * 100
df = df.sort_values(['symbol', 'date'], ignore_index=True)


df.tail(20)



dfwkly = df.groupby(['symbol', 'year', 'month']).last().reset_index().set_index('date')

dfwkly

dfwkly = sd.addMA(dfwkly, 10)

import matplotlib.pyplot as plt
%matplotlib inline
plt.figure(figsize=(20,20))

dfwkly['close'].plot()
