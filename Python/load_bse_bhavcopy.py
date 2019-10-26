import pandas as pd
import sqlite3
import sda
import numpy as np
import os
import fnmatch
import timeit


def read_bse_bhavcopy_files(file_path, file_ptrn):
	eq_files = fnmatch.filter(os.listdir(file_path), file_ptrn)
	new_dtypes = {
	  "seccd":np.int32
	, "open":np.float32
	, "high":np.float32
	, "low":np.float32
	, "close":np.float32
	, "last":np.float32
	, "prevclose":np.float32
	, "trds":np.int32
	, "shrs":np.int32
	, "trnovr":np.float32
	}
	eq = pd.DataFrame()
	for file in eq_files:
		print("Info : Read", file)
		df = pd.read_csv(file_path + file)
		df = df.astype(new_dtypes)
		eq = eq.append(df, ignore_index=True)
	return(eq)


def main():
	dbfile = "/Users/ajit/GitHub/StockMarketAnalysis/data/bse.db"
	file_path = "/Users/ajit/GitHub/StockMarketAnalysis/data/"
	file_ptrn = "bse_bhavcopy_eq_*.csv"
	tblname = "bhavcopy"
	df = read_bse_bhavcopy_files(file_path, file_ptrn)
	df = sda.enhance_df_with_date_features(df)
	print("Info : Enhanced dataframe with date features")
	conn = sda.create_sqlite_connection(dbfile)
	print("Info : Loading bhavcopy datafarme to sqlite3")
	sda.replace_table_with_df(conn, df, tblname)
	sda.create_index(conn, tblname, "index_bhavcopy_dt", "dt")
	sda.create_index(conn, tblname, "index_bhavcopy_seccd", "seccd")
	sda.create_index(conn, tblname, "index_bhavcopy_year", "year")
	sda.create_index(conn, tblname, "index_bhavcopy_month", "month")


if __name__ == "__main__":
	start = timeit.default_timer()
	main()
	end = timeit.default_timer()
	print("Execution time : " + str(round(end - start, 3)) + "s")
