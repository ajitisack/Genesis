import pandas as pd
import sqlite3
import datetime



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


def get_unique_dates_from_equity_table(conn, query):
	df = pd.read_sql_query(query, conn)
	print("Info : Selected distinct dates into 'date' dataframe")
	return df


def enhance_date_df(df):
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
	print("Info : Enhanced 'date' dataframe")
	return df


def load_df_to_table(conn, df, tblname):
	df.to_sql(tblname, conn, if_exists='replace', index=False)
	print("Info : Inserted 'date' dataframe into", tblname, "table")


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
	tblname = "date"
	query = "SELECT distinct dt from equity"
	conn = create_sqlite_connection(dbfile)
	df = get_unique_dates_from_equity_table(conn, query)
	df = enhance_date_df(df)
	drop_index(conn, tblname, index_nm="index_date_dt")
	drop_index(conn, tblname, index_nm="index_date_year")
	drop_index(conn, tblname, index_nm="index_date_month")
	load_df_to_table(conn, df, tblname)
	create_index(conn, tblname, index_nm="index_date_dt", index_key="dt")
	create_index(conn, tblname, index_nm="index_date_year", index_key="year")
	create_index(conn, tblname, index_nm="index_date_month", index_key="month")


if __name__ == "__main__":
	main()
