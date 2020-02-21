
from io import BytesIO
from zipfile import ZipFile
import urllib.request
import datetime
import pandas as pd
from urllib.error import URLError, HTTPError
import os

nse = None
datafile = '/Users/ajit/Google Drive/Genesis/nse.csv'


dt = datetime.datetime.strptime("20150101", "%Y%m%d")
if os.path.isfile(datafile):
    f = open(datafile)
    for line in f:
        pass
    dt = datetime.datetime.strptime(line.split(",")[10], '%d-%b-%Y') + datetime.timedelta(days=1)


end_dt = datetime.datetime.now()
#end_dt = datetime.datetime.strptime("20171211", "%Y%m%d")

while dt <= end_dt:
    dmy = dt.strftime("%d%b%Y").upper()
    y = dt.strftime("%Y").upper()
    m = dt.strftime("%b").upper()

    nse_url = 'https://www.nseindia.com/content/historical/EQUITIES/' + y + '/' + m + '/cm' + dmy + 'bhav.csv.zip'
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    req = urllib.request.Request(nse_url, headers=hdr)
    try:
        url = urllib.request.urlopen(req)
    except HTTPError as e:
        pass
    else:
        with ZipFile(BytesIO(url.read())) as my_zip_file:
            for contained_file in my_zip_file.namelist():
                print(dmy)
                df = pd.read_csv(my_zip_file.open(contained_file))
                if nse is None:
                    nse = df
                else:
                    nse = nse.append(df, ignore_index=True)[df.columns.tolist()]
    dt = dt + datetime.timedelta(days=1)

nse = nse.drop('Unnamed: 13', axis = 1)
nse.to_csv(datafile, header = True, index = False)
