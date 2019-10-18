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
