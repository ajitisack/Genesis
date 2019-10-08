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


url = 'https://www.nseindia.com/content/historical/EQUITIES/' + y + '/' + m + '/cm' + dmy + 'bhav.csv.zip'
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
