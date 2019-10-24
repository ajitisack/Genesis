import datetime
import time
import pandas as pd


def get_UNIX_dt(dtstr):
	if dtstr == "": return ""
	dt = datetime.datetime.strptime(dtstr, "%Y-%m-%d")
	t = time.mktime(dt.timetuple())
	t = str(t).split('.')[0]
	return t


def enhance_df_with_date_features(df):
	df["date"] = pd.to_datetime(df["dt"], format="%Y-%m-%d")
	df["year"] = df["date"].dt.year
	df["month"] = df["date"].dt.month
	df["day"] = df["date"].dt.day
	df["wkday"] = df["date"].dt.dayofweek + 1
	df["wknr"] = df["date"].dt.week
	df["qrtr"] = df["date"].dt.quarter
	df.drop(columns=['date'], inplace = True)
	return df
