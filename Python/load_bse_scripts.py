import pandas as pd
import sqlite3


def read_bse_scripts(filename):
	df=pd.read_csv(filename)
	df = df.drop(['Instrument'], axis=1)
	df.columns = ['seccd', 'secid', 'secnm', 'secstatus', 'secgrp', 'faceval', 'isin', 'industry']
	df['secgrp'] = df['secgrp'].str.strip()
	df['isin'] = df['isin'].str.strip()
	df['industry'] = df['industry'].str.strip()
	df['industry'] = df['industry'].str.replace('&amp;','&', regex=False)
	df['secnm'] = df['secnm'].str.replace('&amp;','&', regex=False)
	df['secnm'] = df['secnm'].str.replace('-$','', regex=False)
	df['secnm'] = df['secnm'].str.replace('&#39;','\'', regex=False)
	df['secnm'] = df['secnm'].str.replace('(','', regex=False)
	df['secnm'] = df['secnm'].str.replace(')','', regex=False)
	df['secnm'] = df['secnm'].str.replace('LTD.','LTD', regex=False)
	df['secid'] = df['secid'].str.replace('&amp;','&', regex=False)
	df['secstatus'] = df['secstatus'].str.replace('Active','A', regex=False)
	df['secstatus'] = df['secstatus'].str.replace('Suspended','S', regex=False)
	df['secstatus'] = df['secstatus'].str.replace('Delisted','D', regex=False)
	print("Info : Read", filename, "into dataframe")
	return(df)


def create_sqlite_connection(dbfile):
	conn = None
	try:
		conn = sqlite3.connect(dbfile)
		print("Info : Created connection to sqlite db ", dbfile)
		return(conn)
	except Error as e:
		print(e)
	return conn


def insert_df_table(conn, df, tblname, index_nm):
	drop_index = "drop index if exists " + index_nm
	sqlite = conn.cursor()
	sqlite.execute(drop_index)
	print("Info : Dropped index", index_nm, "on", tblname, "table")
	df.to_sql(tblname, conn, if_exists='replace', index=False)
	print("Info : Inserted dataframe into", tblname, "table")


def create_index(conn, index_nm, tblname, index_key):
	create_index = "create index if not exists " + index_nm + " on " + tblname + "(" + index_key + ");"
	sqlite = conn.cursor()
	sqlite.execute(create_index)
	print("Info : Created " + index_nm + " on " + index_key + " in " + tblname + " table")


def main():
	filename = "../data/ListOfScrips.csv"
	dbfile = "../data/bse.db"
	tblname = "security"
	index_nm = "index_security_seccd"
	index_key = "seccd"
	df = read_bse_scripts(filename)
	conn = create_sqlite_connection(dbfile)
	insert_df_table(conn, df, tblname, index_nm)
	create_index(conn, index_nm, tblname, index_key)


if __name__ == "__main__":
	main()
