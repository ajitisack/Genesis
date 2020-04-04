import pandas as pd
import re
import sqlite3
import multiprocessing as mp
from sda import *
from timeit import default_timer as timer
from functools import partial
import datetime
import arrow
import sys
import numpy as np
import logging

def print_info(message):
	t = arrow.now().format('YYYY-MM-DD HH:MM:SS')
	print(t + " : Info : " + message)

def get_active_securities(conn, query, no_of_securities=0):
	if no_of_securities != 0: query = query + " limit " + str(no_of_securities)
	df = pd.read_sql_query(query, conn)
	security = df.values.tolist()
	print_info("Fetched " + str(len(security)) + " active BSE securities")
	return security


def prepare_hist_data_df(seccd, hist_data_text):
	hist_data = hist_data_text.split('\n')
	hist_list = [line.split(',') for line in hist_data]
	df=pd.DataFrame(hist_list[1:])
	if df.shape[1] != 7:
		print(seccd)
		print(df.head())
	df.columns = ["dt", "open", "high", "low", "close", "adjclose", "vol"]
	df = df[(df["open"] != "null") & (df["dt"] != "")]
	new_dtypes = {"open":float, "high":float, "low":float, "close":float, "adjclose":float, 'vol':int}
	df = df.astype(new_dtypes)
	rounding = {"open":2, "high":2, "low":2, "close":2, "adjclose":2}
	df = df.round(rounding)
	df.insert(loc=0, column = "seccd", value=seccd)
	return(df)


def get_security_histdata(sec, freq, startdt, enddt, cookies, crumb):
	if type(enddt) != str: enddt = enddt.strftime("%Y-%m-%d")
	seccd, secid = sec[0], sec[1]
	hist_data_text = query_yahoo_finance(secid, freq, startdt, enddt, cookies, crumb)
	while re.search("error", hist_data_text):
		error_txt = re.findall('"code": *"(.+?)"', hist_data_text)[0]
		if error_txt == "Not Found":
			return pd.DataFrame()
		if error_txt == "Unauthorized":
			hist_data_text = query_yahoo_finance(secid, freq, startdt, enddt, cookies, crumb)
	df = prepare_hist_data_df(seccd, hist_data_text)

	return df


def get_bse_equity_histdata_yf(securities, freq, fname, startdt, enddt, cookies, crumb):
	eq = pd.DataFrame()
	for sec in securities:
		df = get_security_histdata(sec, freq, startdt, enddt, cookies, crumb)
		if df.empty: continue
		eq = eq.append(df, ignore_index=True)
		logging.info("Downloaded data of " + sec[1])
	return eq


def divide_into_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_histdata_yf_mp(fname, securities, freq, nthreads, startdt="2000-01-03", enddt=datetime.date.today()):
	cookies, crumb = get_cookies_crumb()
	nitems = int(len(securities)/nthreads) + 1
	security_chunks = list(divide_into_chunks(securities, nitems))
	print_info("Created " + str(nthreads) + " chunks of " + str(len(securities)) + " securities")
	print_info("Initiating " + str(nthreads) + " processes to download histdata securities from yahoo finance")
	target_func = partial(get_bse_equity_histdata_yf, freq=freq, fname=fname, startdt=startdt, enddt=enddt, cookies=cookies, crumb=crumb)
	pool = mp.Pool(processes = nthreads)
	df_list = pool.map(target_func, security_chunks)
	df_final = pd.DataFrame()
	for df in df_list:
		df_final = df_final.append(df, ignore_index=True)
	print_info("Downloaded historical BSE equity data from yahoo finance [" + str(df_final.shape[0]) + ',' + str(df_final.shape[1]) + "]")
	return df_final


def main():
	if len(sys.argv) < 2:
		print("Argument Error! Not enough arguments are provided.")
		print("Syntax: " + sys.argv[0] + " d/w/m [nthreads] [no_of_securities]")
		return 1
	try:
		freq, nthreads, nsecurities = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
	except:
		freq, nthreads, nsecurities = 'd', 4, 0
	logging.basicConfig(filename='a.log', filemode='w',format='%(asctime)s - %(process)d - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
	dbfile = "data/bse.db"
	tblname = "equity" + freq + 'ly'
	query = "SELECT seccd, secid FROM security where secstatus = 'A'"
	conn = create_sqlite_connection(dbfile)
	securities = get_active_securities(conn, query, nsecurities)
	df = get_histdata_yf_mp(tblname, securities, freq, nthreads)
	df = enhance_df_with_date_features(df)
	replace_table_with_df(conn, df, tblname)
	create_index(conn, tblname, index_nm="index_" + tblname + "_seccd", index_key="seccd")
	create_index(conn, tblname, index_nm="index_" + tblname + "_dt", index_key="dt")
	create_index(conn, tblname, index_nm="index_" + tblname + "_year", index_key="year")
	create_index(conn, tblname, index_nm="index_" + tblname + "_month", index_key="month")


if __name__ == "__main__":
	start = timer()
	main()
	end = timer()
	print("Execution time : " + str(round(end - start, 3)) + "s")
