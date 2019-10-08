# import libraries
import urllib.request
import datetime
import pandas as pd
import os
import time
from urllib.error import URLError, HTTPError
from io import BytesIO
from zipfile import ZipFile

weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# function to download NSE equity data
def downloadNSE(datafile, start_dt, end_dt):
	nse = None
	dt = start_dt
	if start_dt == end_dt: return(0)
	while dt <= end_dt:

		# continue with next iteration if weekday is Sat or Sun
		w = dt.weekday()
		if w in (5,6):
			print(dt, "is weekend!")
			dt = dt + datetime.timedelta(days=1)
			continue

		# prepare date part
		dmy = dt.strftime("%d%b%Y").upper()
		y = dt.strftime("%Y").upper()
		m = dt.strftime("%b").upper()

		# prepare nse url, header, request
		nse_url = 'https://www.nseindia.com/content/historical/EQUITIES/' + y + '/' + m + '/cm' + dmy + 'bhav.csv.zip'
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
		req = urllib.request.Request(nse_url, headers=hdr)

		# request url with exception for http error if file doesn't exist for a particular date ie, holiday
		try:
			url = urllib.request.urlopen(req)
			time.sleep(2)
		except HTTPError as e:
			pass
		else:
			# loop through file in the zipped file
			with ZipFile(BytesIO(url.read())) as my_zip_file:
				for contained_file in my_zip_file.namelist():
					print(weekday[w], dmy, "- Downloaded")
					# read into pandas dataframe and append to main dataframe
					df = pd.read_csv(my_zip_file.open(contained_file))
					if nse is None:
						nse = df
					else:
						nse = nse.append(df, ignore_index=True)[df.columns.tolist()]

		# increment date with 1 day
		dt = dt + datetime.timedelta(days=1)


	# drop the last column of the dataframe which is '/n' and append to datafile
	nse = nse.drop('Unnamed: 13', axis = 1)
	nse.to_csv(datafile, header = True, index = False)


# MAIN function
if __name__ == "__main__":

		# declare datafile
		datafile = '/Users/ajit/Projects/Genesis/nse.csv'

		# define start date and end date(today)
		# if datafile exists then start date is the latest downloaded date ie, date of last record of datafile
		start_dt = datetime.datetime.strptime("20160101", "%Y%m%d").date()
		end_dt = datetime.date.today()
		#end_dt = datetime.datetime.strptime("20180131", "%Y%m%d").date()
		if os.path.isfile(datafile):
			f = open(datafile)
			for line in f:
				pass
			f.close()
			start_dt = datetime.datetime.strptime(line.split(",")[10], '%d-%b-%Y').date() + datetime.timedelta(days=1)

		# call function to download NSE data
		downloadNSE(datafile, start_dt, end_dt)
		print("Data file is upto date!")
