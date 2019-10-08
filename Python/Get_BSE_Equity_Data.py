import requests
import zipfile
import io
import pandas as pd
import time
import datetime


### Function to read csv file zipped in a folder from URL without downloading the file
def readUrlZipFile(fname):
	try:
		url = "https://www.bseindia.com/download/BhavCopy/Equity/"
		URL = url + fname + "_CSV.ZIP"
		response = requests.get(URL)
		response.raise_for_status()
	except requests.exceptions.HTTPError as e:
		return(pd.DataFrame())
	else:
		zf = zipfile.ZipFile(io.BytesIO(response.content))
		df = pd.read_csv(zf.open(fname + ".CSV"))
		return(df)

### Function to get BSE Equity Bhacvcopy data for a given date range
### if end date is not provided then "today" will be end date
def getEquityData(start_dt="20191001", end_dt=datetime.date.today()):
	if start_dt == end_dt: return(0)
	eq = None
	dt = datetime.datetime.strptime(start_dt, "%Y%m%d").date()
	if type(end_dt) == str: end_dt = datetime.datetime.strptime(end_dt, "%Y%m%d").date()
	while dt <= end_dt:
		if dt.weekday() in (5,6): pass
		else:
			fname = "EQ" + dt.strftime("%d%m%y")
			df = readUrlZipFile(fname)
			if not df.empty:
				print(dt)
				df.insert(loc=0, column = "DATE", value=dt)
				df = df.drop(labels='TDCLOINDI', axis=1)
				if eq is None: eq = df
				else: eq = eq.append(df, ignore_index=True)[df.columns.tolist()]
		# increment date with 1 day
		dt = dt + datetime.timedelta(days=1)
	return(eq)


### Read single days data into a DataFrame
dt = "20190507"
dt = datetime.datetime.strptime(dt, "%Y%m%d").date()
df1 = pd.read_csv("EQ070519.csv")
df1 = df1.drop(labels='TDCLOINDI', axis=1)
df1.insert(loc=0, column = "DATE", value=dt)
df1

### Call function to get BSE Equity Daily Data
df = getEquityData("20190508")
# df.to_csv("data/bse_2019.csv", index=False)


df.shape
df
