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
		return(conn)
	except Error as e:
		print(e)
	print("Info : Created connection to sqlite db ", dbfile)
	return conn


def insert_df_table(conn, df):
	delete_table = "delete from security;"
	sqlite = conn.cursor()
	sqlite.execute(delete_table)
	df.to_sql("security", conn, if_exists='replace', index=False)
	print("Info : Inserted dataframe into security table")


def create_sec_index(conn):
	create_index = "create index if not exists index_seccd on security(seccd);"
	sqlite = conn.cursor()
	sqlite.execute(create_index)
	print("Info : Created index on seccd in security table")


def main():
	filename = "../data/ListOfScrips.csv"
	dbfile = "../data/bse.db"
	df = read_bse_scripts(filename)
	sqlite_conn = create_sqlite_connection(dbfile)
	insert_df_table(sqlite_conn, df)
	create_sec_index(sqlite_conn)


if __name__ == "__main__":
	main()
