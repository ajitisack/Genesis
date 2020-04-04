import sqlite3
import pandas as pd
import numpy as np
import arrow
import yfinance as yf
from timeit import default_timer as timer
from sqlite import SqlLite

# https://query1.finance.yahoo.com/v7/finance/download/HDFC.BO?period1=1546281000&period2=1571855400&interval=1d&events=history
# https://query1.finance.yahoo.com/v7/finance/download/HDFC.BO?period1=1546281000&period2=1571855400&interval=1wk&events=history
# https://query1.finance.yahoo.com/v7/finance/download/HDFC.BO?period1=1546281000&period2=1571855400&interval=1mo&events=history

class BSE():

	@staticmethod
	def processdf(df, securitycd):
		df = df.copy()
		df.dropna(how='all', inplace=True)
		df.reset_index(level=0, inplace=True)
		df.insert(loc=0, column = "securitycd", value=securitycd.split('.')[0])
		df.columns = map(lambda x: x.lower().replace(' ',''), df.columns)
		df.fillna(0, inplace=True)
		df["year"] = df["date"].dt.year
		df["month"] = df["date"].dt.month
		df["day"] = df["date"].dt.day
		df["wkday"] = df["date"].dt.dayofweek + 1
		df["wknr"] = df["date"].dt.week
		df["qrtr"] = df["date"].dt.quarter
		new_dtypes = {"open":np.float32, "high":np.float32, "low":np.float32, "close":np.float32, "adjclose":np.float32, 'volume':np.int32, \
		"year":np.int16, "month":np.int16, 'day':np.int16, 'wkday':np.int16, 'wknr':np.int16, 'qrtr':np.int16}
		df = df.astype(new_dtypes)
		columns = ['securitycd', 'date', 'open', 'high', 'low', 'close', 'adjclose', 'volume', 'dividends', 'stocksplits', 'year', 'month', 'day', 'wkday', 'wknr', 'qrtr']
		return df


	@staticmethod
	@SqlLite.connector
	def getequitylist(n_equities):
		query = f"SELECT securityid FROM security where status = 'A' limit {n_equities}"
		equitylist = pd.read_sql_query(query, SqlLite.conn)
		return equitylist.securityid.to_list()
		

	@staticmethod
	def gethistpricedata(n_equities=5000, lastnyears=5):
		startdt = arrow.now().shift(years=-lastnyears).format('YYYY-MM-DD')
		enddt = arrow.now().format('YYYY-MM-DD')
		equitylist = BSE.getequitylist(n_equities)
		tickers = [t +'.BO' for t in equitylist]
		eq = yf.download(tickers, start=startdt, end=enddt, interval = '1d', group_by='ticker', prepost=True, actions=True, rounding=True)
		df = pd.concat([BSE.processdf(eq[t], t) for t in tickers], ignore_index=True)
		print("Downloaded price history from yahoo finance.")
		return df

	@staticmethod	
	@SqlLite.connector
	def loadhistpricedata(df):
		tblname   = 'equitydly'
		df.to_sql(tblname, SqlLite.conn, if_exists='replace', index=False)
		print(f'Table {tblname} has been refreshed with {df.shape[0]} records')


if __name__ == "__main__":
	start = timer()
	df = BSE.gethistpricedata()
	BSE.loadhistpricedata(df)
	end = timer()
	print("Execution time : " + str(round(end - start, 3)) + "s")

