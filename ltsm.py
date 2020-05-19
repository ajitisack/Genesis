import stockdata as sd
import pandas as pd
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

df = sd.getdata("select date, close from nsehistprice where symbol = 'INDUSINDBK'")
df

df.shape

X  = df.close.values.reshape(-1,1)
X1 = df.close.shift(1).values.reshape(-1,1)

X  = X[1:]
X1 = X1[1:]

len(X)
len(X1)

X[1:5]

X1[1:5]

scaler = MinMaxScaler(feature_range=(0, 1))
X  = scaler.fit_transform(X)
X1 = scaler.fit_transform(X1)

len(X)
len(X1)

n = 4200
train_X, train_Y = X[:n], X1[:n]
test_X,  test_Y  = X[n+1:], X1[n+1:]

len(train_X)
len(train_Y)
len(test_X)
len(test_Y)

train_X

train_X.shape
test_X.shape
np.reshape(train_X, (train_X.shape[0], 1, train_X.shape[1]))

train_X = np.reshape(train_X, (train_X.shape[0], 1, train_X.shape[1]))
test_X  = np.reshape(test_X, (test_X.shape[0], 1, test_X.shape[1]))


model = Sequential()
model.add(LSTM(4, input_shape=(1, 1)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(train_X, train_Y, epochs=5, batch_size=1, verbose=2)

df.head()

train_X
test_X[1]


testPredict = model.predict(test_X)
testPredict = scaler.inverse_transform(testPredict)
rmse = sqrt(mean_squared_error(df.close[n:n+211], testPredict))
print('Test Score: %.2f RMSE' % (rmse))

abc = df[['date', 'close']][n:n+211]
abc['predicted'] = testPredict
abc.plot()
