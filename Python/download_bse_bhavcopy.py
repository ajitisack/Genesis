import requests
import zipfile
import io
import pandas as pd
import time
import arrow
import sqlite3
import sda
import sys
from timeit import default_timer as timer


### Function to read csv file zipped in a folder from URL without downloading the file
def readUrlZipFile(dt):
	try:
		dt = dt.format("DDMMYY")
		url = "https://www.bseindia.com/download/BhavCopy/Equity/"
		URL = url + "EQ" + dt + "_CSV.ZIP"
		response = requests.get(URL)
		response.raise_for_status()
	except requests.exceptions.HTTPError as e:
		print("Not able to find equity file for", dt.format("YYYY-MM-DD"))
		print(e)
		return pd.DataFrame()
	else:
		zf = zipfile.ZipFile(io.BytesIO(response.content))
		fname = zf.infolist()[0]
		df = pd.read_csv(zf.open(fname))
		return df


def prepare_equity_df(df, dt):
	df.insert(loc=0, column = "DATE", value=dt.format("YYYY-MM-DD"))
	df = df.drop(['TDCLOINDI', 'SC_NAME'], axis=1)
	df.columns = ['dt', 'seccd', 'secgrp', 'sectp', 'open', 'high', 'low', 'close', 'last', 'prevclose', 'trds', 'shrs', 'trnovr']
	df['secgrp'] = df['secgrp'].str.strip()
	df['sectp'] = df['sectp'].str.strip()
	return df


def getEquityData(year=arrow.now().format('YYYY')):
	eq = pd.DataFrame()
	dt = start_dt = arrow.get(str(year) + "-01-01")
	end_dt = arrow.get(str(year) + "-12-31")
	today = arrow.now()
	while dt <= end_dt and dt <= today:
		if dt.weekday() not in (5,6):
			df = readUrlZipFile(dt)
			if not df.empty:
				df = prepare_equity_df(df, dt)
				print(dt.format("YYYY-MM-DD"), df.shape)
				eq = eq.append(df, ignore_index=True)
		dt = dt.shift(days=1)
	return eq


def main():
	year = sys.argv[1]
	file = "../data/bse_bhavcopy_eq_" + year + ".csv"
	df = getEquityData(year)
	df.to_csv(file, index = False)
	print(df.shape)
	print(df.head())


if __name__ == "__main__":
	start = timer()
	main()
	end = timer()
	print("Execution time : " + str(round(end - start, 3)) + "s")
