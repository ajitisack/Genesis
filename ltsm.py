import stockdata as sd
import pandas as pd
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM

df = sd.getdata("select date, close from nsehistprice where symbol = 'INDUSINDBK'")

# Using Train and Test

df['date'] = pd.to_datetime(df.date)
df.set_index('date', inplace=True)

n_test_days = 5
train, test = df[:-n_test_days], df[-n_test_days:]

len(train)
len(test)

scaler = MinMaxScaler()
xtrain = scaler.fit_transform(train)
xtest  = scaler.fit_transform(test)

n_input    = 1
n_features = 1
xtrain = TimeseriesGenerator(xtrain, xtrain, length=n_input, batch_size=1)
xtest  = TimeseriesGenerator(xtest, xtest, length=n_input, batch_size=1)

model = Sequential()
model.add(LSTM(100, activation='relu', input_shape=(n_input, n_features)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

model.fit_generator(xtrain, epochs=10, verbose=2)


preds = model.predict(xtest)
preds = np.round(scaler.inverse_transform(preds),2)
test['pred_close'] = np.append(preds, 0)


# Predict Test incrementally
pred_list = []
batch = xtrain[-n_input:]
for i in range(n_test_days):
    batch = batch.reshape((1, n_input, n_features))
    pred_val = model.predict(batch)[0]
    pred_list.append(pred_val)
    batch = pred_val
test['sequence_pred'] = np.round(scaler.inverse_transform(pred_list), 2)

test
