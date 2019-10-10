
import pandas as pd
import sqlite3


def create_sqlite_connection(dbfile):
	conn = None
	try:
		conn = sqlite3.connect(dbfile)
		return(conn)
	except Error as e:
		print(e)
	print("Info : Created connection to sqlite db ", dbfile)
	return conn


def create_bse_equity_view_1y(conn):
	create_view = """
	create view equity_1y
	as
	select A.*, B.secid, B.secnm, B.secstatus, B.industry
	from eq_2019 A
	left outer join security B on A.seccd = B.seccd
	and B.secstatus = 'A'
	"""
	sqlite = conn.cursor()
	sqlite.execute("drop view if exists equity_1y")
	sqlite.execute(create_view)
	print("Info : Created view equity_1y")


def create_bse_equity_view_3y(conn):
	create_view = """
	create view equity_3y
	as
	select A.*, B.secid, B.secnm, B.secstatus, B.industry
	from (
		select * from eq_2019 union
		select * from eq_2018 union
		select * from eq_2017
	)A
	left outer join security B on A.seccd = B.seccd
	"""
	sqlite = conn.cursor()
	sqlite.execute("drop view if exists equity_3y")
	sqlite.execute(create_view)
	print("Info : Created view equity_3y")


def create_bse_equity_view_5y(conn):
	create_view = """
	create view equity_5y
	as
	select A.*, B.secid, B.secnm, B.secstatus, B.industry
	from (
		select * from eq_2019 union
		select * from eq_2018 union
		select * from eq_2017 union
		select * from eq_2016 union
		select * from eq_2015
	)A
	left outer join security B on A.seccd = B.seccd
	"""
	sqlite = conn.cursor()
	sqlite.execute("drop view if exists equity_5y")
	sqlite.execute(create_view)
	print("Info : Created view equity_5y")


def create_bse_equity_view(conn):
	create_view = """
	create view equity
	as
	select A.*, B.secid, B.secnm, B.secstatus, B.industry
	from (
		select * from eq_2019 union
		select * from eq_2018 union
		select * from eq_2017 union
		select * from eq_2016 union
		select * from eq_2015 union
		select * from eq_2014 union
		select * from eq_2013 union
		select * from eq_2012 union
		select * from eq_2011 union
		select * from eq_2010
	)A
	left outer join security B on A.seccd = B.seccd
	"""
	sqlite = conn.cursor()
	sqlite.execute("drop view if exists equity")
	sqlite.execute(create_view)
	print("Info : Created view equity")



def main():
	dbfile = "../data/bse.db"
	sqlite_conn = create_sqlite_connection(dbfile)
	create_bse_equity_view_1y(sqlite_conn)
	create_bse_equity_view_3y(sqlite_conn)
	create_bse_equity_view_5y(sqlite_conn)
	create_bse_equity_view(sqlite_conn)


if __name__ == "__main__":
	main()
