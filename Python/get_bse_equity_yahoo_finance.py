import pandas as pd
import re
import sqlite3
import multiprocessing as mp
from sda import *
from timeit import default_timer as timer
from functools import partial
import datetime


def get_active_securities(conn, query, no_of_securities=0):
	if no_of_securities != 0: query = query + " limit " + str(no_of_securities)
	df = pd.read_sql_query(query, conn)
	security = df.values.tolist()
	print("Info : Fetched", len(security), "active BSE securities")
	return security


def prepare_hist_data_df(seccd, hist_data_list):
	list = [line.split(',') for line in hist_data_list]
	df=pd.DataFrame(list)
	if df.shape[1] != 7:
		print(seccd)
		print(df.head())
	df.columns = ["dt", "open", "high", "low", "close", "adjclose", 'vol']
	df.drop(df.index[0], inplace = True)
	df.drop(df[df.dt==""].index, inplace = True)
	df.insert(loc=0, column = "seccd", value=seccd)
	return(df)


# def get_security_histdata(sec, startdt, enddt, cookies, crumb):
# 	if type(enddt) != str: enddt = enddt.strftime("%Y-%m-%d")
# 	seccd, secid = sec[0], sec[1]
# 	hist_data_text = query_yahoo_finance(secid, startdt, enddt, cookies, crumb)
# 	if re.search("error", hist_data_text):
# 		error_txt = re.findall('"code": *"(.+?)"', hist_data_text)[0]
# 		if error_txt == "Not Found":
# 			# print("Err  : Data not found for", sec)
# 			return pd.DataFrame()
# 		if error_txt == "Unauthorized":
# 			# print("Err  : Data not found for", sec)
# 			return pd.DataFrame()
# 	hist_data = hist_data_text.split('\n')
# 	df = prepare_hist_data_df(seccd, hist_data)
# 	return df

def get_security_histdata(sec, startdt, enddt, cookies, crumb):
	if type(enddt) != str: enddt = enddt.strftime("%Y-%m-%d")
	seccd, secid = sec[0], sec[1]
	hist_data_text = query_yahoo_finance(secid, startdt, enddt, cookies, crumb)
	while re.search("error", hist_data_text):
		error_txt = re.findall('"code": *"(.+?)"', hist_data_text)[0]
		if error_txt == "Not Found":
			return pd.DataFrame()
		if error_txt == "Unauthorized":
			# time.sleep(1)
			hist_data_text = query_yahoo_finance(secid, startdt, enddt, cookies, crumb)
	hist_data = hist_data_text.split('\n')
	df = prepare_hist_data_df(seccd, hist_data)
	return df


def get_bse_equity_histdata_yf(securities, fname, startdt, enddt, cookies, crumb):
	eq = pd.DataFrame()
	for sec in securities:
		df = get_security_histdata(sec, startdt, enddt, cookies, crumb)
		if df.empty: continue
		eq = eq.append(df, ignore_index=True)
		# print("Info : Downloaded data for", sec, df.shape)
	return eq


def divide_into_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_histdata_yf_mp(fname, securities, nthreads, startdt="2000-01-03", enddt=datetime.date.today()):
	cookies, crumb = get_cookies_crumb()
	nitems = int(len(securities)/nthreads) + 1
	security_chunks = list(divide_into_chunks(securities, nitems))
	print("Info : Created", nthreads, "chunks of", len(securities), "securities")
	print("Info : Initiating", nthreads, "processes to download histdata securities from yahoo finance")
	target_func = partial(get_bse_equity_histdata_yf, fname=fname, startdt=startdt, enddt=enddt, cookies=cookies, crumb=crumb)
	pool = mp.Pool(processes = nthreads)
	df_list = pool.map(target_func, security_chunks)
	df_final = pd.DataFrame()
	for df in df_list:
		# print(df.shape)
		df_final = df_final.append(df, ignore_index=True)
	print("Info : Downloaded historical BSE equity data from yahoo finance", df_final.shape)
	return df_final


def main():
	dbfile = "../data/bse.db"
	tblname = "equity"
	nsecurities = 0
	nthreads = 8
	query = "SELECT seccd, secid FROM security where secstatus = 'A'"
	conn = create_sqlite_connection(dbfile)
	securities = get_active_securities(conn, query, nsecurities)
	df = get_histdata_yf_mp(tblname, securities, nthreads)
	df = enhance_df_with_date_features(df)
	replace_table_with_df(conn, df, tblname)
	# df.to_sql(tblname, conn, if_exists='replace', index=False)
	create_index(conn, tblname, index_nm="index_bse_eq_yf_seccd", index_key="seccd")
	create_index(conn, tblname, index_nm="index_bse_eq_yf_dt", index_key="dt")
	create_index(conn, tblname, index_nm="index_bse_eq_yf_year", index_key="year")
	create_index(conn, tblname, index_nm="index_bse_eq_yf_month", index_key="month")


if __name__ == "__main__":
	start = timer()
	main()
	end = timer()
	print("Execution time : " + str(round(end - start, 3)) + "s")
