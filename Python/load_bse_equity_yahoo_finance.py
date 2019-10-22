import pandas as pd
import re
import sqlite3
import multiprocessing as mp
from sda import *
from timeit import default_timer as timer
from functools import partial


def get_active_listed_sec(conn, query, no_of_securities=0):
	if no_of_securities != 0: query = query + " limit " + str(no_of_securities)
	df = pd.read_sql_query(query, conn)
	security = df.values.tolist()
	return security


def prepare_hist_data_df(seccd, hist_data_list):
	list = [line.split(',') for line in hist_data_list]
	df=pd.DataFrame(list)
	df.columns = ["dt", "open", "high", "low", "close", "adjclose", 'vol']
	df.drop(df.index[0], inplace = True)
	df.drop(df[df.dt==""].index, inplace = True)
	df.insert(loc=0, column = "seccd", value=seccd)
	# df = enhance_df_with_date_features(df)
	return(df)


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]



def get_yahoo_finance_hist_data(sec, startdt, enddt, cookies, crumb):
	if type(enddt) != str: enddt = enddt.strftime("%Y-%m-%d")
	seccd, secid = sec[0], sec[1]
	hist_data_text = query_yahoo_finance(secid, startdt, enddt, cookies, crumb)
	if re.search("error", hist_data_text):
		error_txt = re.findall('"code": *"(.+?)"', hist_data_text)[0]
		if error_txt == "Not Found":
			# print("Err  : Data not found for", sec)
			return pd.DataFrame()
	hist_data = hist_data_text.split('\n')
	df = prepare_hist_data_df(seccd, hist_data)
	return df


def get_bse_hist_data_yahoo_finance(securities, fname, startdt, enddt, cookies, crumb):
	eq = pd.DataFrame()
	for sec in securities:
		df = get_yahoo_finance_hist_data(sec, startdt, enddt, cookies, crumb)
		if df.empty: continue
		eq = eq.append(df, ignore_index=True)
		# print("Info : Downloaded data for", sec, df.shape)
	return eq


def get_bse_security_hist_data_yahoo_finance_mp(fname, securities, nthreads, startdt="2000-01-03", enddt=datetime.date.today()):
	cookies, crumb = get_cookies_crumb()
	n = int(len(securities)/nthreads) + 1
	s = list(divide_chunks(securities, n))
	target_func = partial(get_bse_hist_data_yahoo_finance, fname=fname, startdt=startdt, enddt=enddt, cookies=cookies, crumb=crumb)
	pool = mp.Pool(processes = nthreads)
	df_list = pool.map(target_func, s)
	df_final = pd.DataFrame()
	for df in df_list:
		# print(df.shape)
		df_final = df_final.append(df, ignore_index=True)
	return df_final


def main():
	dbfile = "../data/bse.db"
	tblname = "bse_equity_yf"
	fname = "bse_equity_yf"
	no_of_securities_to_download = 0
	nthreads = 20
	query = "SELECT seccd, secid FROM security where secstatus = 'A'"
	conn = create_sqlite_connection(dbfile)
	securities = get_active_listed_sec(conn, query, no_of_securities_to_download)
	df = get_bse_security_hist_data_yahoo_finance_mp(fname, securities, nthreads)
	print(df.shape)
	df = enhance_df_with_date_features(df)
	df.to_sql(tblname, conn, if_exists='replace', index=False)
	# drop_index(conn, tblname, index_nm="index_bse_eq_yf_seccd")
	# drop_index(conn, tblname, index_nm="index_bse_eq_yf_dt")
	create_index(conn, tblname, index_nm="index_bse_eq_yf_seccd", index_key="seccd")
	create_index(conn, tblname, index_nm="index_bse_eq_yf_dt", index_key="dt")
	create_index(conn, tblname, index_nm="index_bse_eq_yf_year", index_key="year")
	create_index(conn, tblname, index_nm="index_bse_eq_yf_month", index_key="month")


if __name__ == "__main__":
	start = timer()
	main()
	end = timer()
	print("Execution time : " + str(round(end - start, 3)) + "s")
