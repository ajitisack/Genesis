import pandas as pd
import sqlite3
import sda
from timeit import default_timer as timer


def read_bse_scripts(filename):
	df=pd.read_csv(filename)
	df = df.drop(['Instrument', 'Issuer Name'], axis=1)
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


def main():
	dbfile = "data/bse.db"
	filename = "Equity.csv"
	tblname = "security"
	index_nm = "index_security_seccd"
	index_key = "seccd"
	df = read_bse_scripts(filename)
	conn = sda.create_sqlite_connection(dbfile)
	sda.replace_table_with_df(conn, df, tblname)
	sda.create_index(conn, tblname, index_nm, index_key)


if __name__ == "__main__":
	start = timer()
	main()
	end = timer()
	print("Execution time : " + str(round(end - start, 3)) + "s")
