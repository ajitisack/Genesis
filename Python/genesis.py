
# download EQ file based on date
# read content into a dataframe
# return dataframe
#
# append returned df into a master df
#
# pre-process master df


import requests
import zipfile
import io
import pandas as pd
import time
import datetime



def readUrlZipFile(url, fname):
	try:
		req = url + fname + "_CSV.ZIP"
		req = requests.get(req)
	except HTTPError as e:
		return(pd.DataFrame())
	else:
		zf = zipfile.ZipFile(io.BytesIO(req.content))
		df = pd.read_csv(zf.open(fname + ".CSV"))
		return(df)


def getEquityFiles(url, start_dt="20190128", end_dt=datetime.date.today()):
	if start_dt == end_dt: return(0)
	eq = None
	dt = datetime.datetime.strptime(start_dt, "%Y%m%d").date()
	while dt <= end_dt:
		if dt.weekday() in (5,6):
			pass
		else:
			fname = "EQ" + dt.strftime("%d%m%y")
			df = readUrlZipFile(url, fname)
			if not df.empty:
				df.insert(loc=0, column = "DATE", value=dt)
				if eq is None:
					eq = df
				else:
					eq = eq.append(df, ignore_index=True)[df.columns.tolist()]
		# increment date with 1 day
		dt = dt + datetime.timedelta(days=1)
	return(eq)


url = "https://www.bseindia.com/download/BhavCopy/Equity/"
df = getEquityFiles(url)


df.head()
