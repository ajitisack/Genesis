import pandas as pd
import requests
import re
import time
import datetime
import sqlite3

def create_sqlite_connection(dbfile:str):
	"""This function creates and returns connection string to sqlite3 database file.
	If there is an error while connecting to database file then exception error
	will be echoed and returns an empty connection string.
	Parameters
	----------
	1. dbfile : str : Path and name of the sqlite3 database file
	Return Value
	------------
	1. conn : str : Connection string to given sqlite3 database file
	Syntax
	-----
	conn = create_sqlite_connection("data/bse.db")
	"""
	conn = None
	try:
		conn = sqlite3.connect(dbfile)
		print("Info : Created connection to sqlite db ", dbfile)
		return(conn)
	except Error as e:
		print(e)
	return conn


def get_active_listed_sec(conn, query, no_of_securities=0):
	if no_of_securities != 0: query = query + " limit " + str(no_of_securities)
	df = pd.read_sql_query(query, conn)
	security = df.values.tolist()
	return security


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
	df["qrtr"] = df["date"].dt.quarter
	df["iswkend"] = 0
	df["ismthend"] = 0
	df["isqrtrend"] = 0
	df["isyrend"] = 0
	df.drop(columns=['date'], inplace = True)
	return df


def get_cookies_crumb():
	url = "https://in.finance.yahoo.com/quote/^BSESN/history"
	with requests.session():
		website = requests.get(url)
	crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', website.text)[0]
	cookies = website.cookies
	return cookies, crumb


def query_yahoo_finance(secid, startdt, enddt, cookies, crumb):
	url = "https://query1.finance.yahoo.com/v7/finance/download/" + secid
	url = url + ".BO?period1=" + get_UNIX_dt(startdt)
	url = url + "&period2=" + get_UNIX_dt(enddt)
	url = url + "&interval=1d&events=history&crumb=" + crumb
	with requests.session():
		website = requests.get(url, cookies = cookies)
	return website.text


def prepare_hist_data_df(seccd, hist_data_list):
	list = [line.split(',') for line in hist_data_list]
	df=pd.DataFrame(list)
	df.columns = ["dt", "open", "high", "low", "close", "adjclose", 'vol']
	df.drop(df.index[0], inplace = True)
	df.drop(df[df.dt==""].index, inplace = True)
	df.insert(loc=0, column = "seccd", value=seccd)
	df = enhance_df_with_date_features(df)
	return(df)


def get_yahoo_finance_hist_data(sec, retry_delay, startdt, enddt, cookies, crumb):
	if type(enddt) != str: enddt = enddt.strftime("%Y-%m-%d")
	seccd, secid = sec[0], sec[1]
	hist_data_text = query_yahoo_finance(secid, startdt, enddt, cookies, crumb)
	if re.search("error", hist_data_text):
		error_txt = re.findall('"code": *"(.+?)"', hist_data_text)[0]
		if error_txt == "Not Found":
			print("Err  : Data not found for", sec)
			return pd.DataFrame()
	hist_data = hist_data_text.split('\n')
	df = prepare_hist_data_df(seccd, hist_data)
	return df


def load_security_hist_data(conn, securities, tblname, retry_delay=10, startdt="2000-01-03", enddt=datetime.date.today()):
	cookies, crumb = get_cookies_crumb()
	for sec in securities:
		df = get_yahoo_finance_hist_data(sec, retry_delay, startdt, enddt, cookies, crumb)
		if df.empty: continue
		df.to_sql(tblname, conn, if_exists='append', index=False)
		print("Info : Downloaded and loaded data for", sec, df.shape)
	return df


def drop_table(conn, tblname):
	drop_tbl = "drop table if exists " + tblname
	sqlite = conn.cursor()
	sqlite.execute(drop_tbl)
	print("Info : Dropped table", tblname)


def drop_index(conn, tblname, index_nm):
	drop_index = "drop index if exists " + index_nm
	sqlite = conn.cursor()
	sqlite.execute(drop_index)
	print("Info : Dropped index", index_nm, "on", tblname, "table")


def create_index(conn, tblname, index_nm, index_key):
	create_index = "create index if not exists " + index_nm + " on " + tblname + "(" + index_key + ");"
	sqlite = conn.cursor()
	sqlite.execute(create_index)
	print("Info : Created " + index_nm + " on " + index_key + " in " + tblname + " table")


def main():
	dbfile = "../data/bse.db"
	tblname = "bse_equity_yf"
	delay_in_sec = 10
	no_of_securities_to_download = 0
	query = "SELECT seccd, secid FROM security where secstatus = 'A'"
	# query = "SELECT seccd, secid FROM security where secstatus = 'A' and seccd >= 503349"
	conn = create_sqlite_connection(dbfile)
	securities = get_active_listed_sec(conn, query, no_of_securities_to_download)
	drop_index(conn, tblname, index_nm="index_bse_eq_yf_seccd")
	drop_index(conn, tblname, index_nm="index_bse_eq_yf_dt")
	drop_table(conn, tblname)
	load_security_hist_data(conn, securities, tblname, retry_delay=delay_in_sec)
	create_index(conn, tblname, index_nm="index_bse_eq_yf_seccd", index_key="seccd")
	create_index(conn, tblname, index_nm="index_bse_eq_yf_dt", index_key="dt")
	create_index(conn, tblname, index_nm="index_bse_eq_yf_year", index_key="year")
	create_index(conn, tblname, index_nm="index_bse_eq_yf_month", index_key="month")


if __name__ == "__main__":
	main()
