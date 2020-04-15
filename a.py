import stockdata as sd
import pandas as pd

sd.downloaddlyhistprice(1000)




# df = sd.downloaddlyhistprice(500, False)

# df.head()
#
# splits = df[df.splits != 0][['symbol', 'date', 'splits', 'year', 'month', 'day', 'wkday', 'wknr', 'qrtr']]
# splits.insert(loc=2, column = 'action', value='splits')
# splits.rename(columns = {'splits':'value'}, inplace = True)
# splits.reset_index(drop=True, inplace=True)
# dividend = df[df.dividend != 0][['symbol', 'date', 'dividend', 'year', 'month', 'day', 'wkday', 'wknr', 'qrtr']]
# dividend.insert(loc=2, column = 'action', value='dividend')
# dividend.rename(columns = {'dividend':'value'}, inplace = True)
# dividend.reset_index(drop=True, inplace=True)
# x = pd.concat([splits, dividend])
#
# x.dtypes
