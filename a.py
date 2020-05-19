import stockdata as sd
import pandas as pd
import plotly.graph_objects as go

df = sd.getdata("select * from bsehistprice")


del df1

df = sd.getdata("select * from nsehistprice where symbol = 'INDUSINDBK'")
df.head()

from sklearn.linear_model import LinearRegression
df.shape
train = df.drop(['date', 'symbol', 'exchange'], axis=1).head(4000)
test  = df.drop(['date', 'symbol', 'exchange', 'close'], axis=1).tail(412)

train.shape
test.shape

x = train.drop(['close'], axis=1)
y = train['close']

lr_model = LinearRegression().fit(x, y)

a = model.predict(test).round(2)

df1 = pd.DataFrame()
df1['actual_close']  = df['close'].tail(412)
df1['predicted_close']  = a
df1.to_csv('pred.csv', index=False)




rmse = sqrt(mean_squared_error(df['close'].tail(412), a))


from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
