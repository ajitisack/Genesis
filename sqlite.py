import sqlite3
import functools

class SqlLite():
	conn = None
	# dbfile = "/Users/ajit/projects/stockmarket_analysis/data/bse.db"
	dbfile = 'C:\\ajit\\equity.db'

	@staticmethod
	def connector(func):
		@functools.wraps(func)
		def wrapper(*args):
			SqlLite.conn = sqlite3.connect(SqlLite.dbfile)
			return func(*args)
			SqlLite.conn.close
		return wrapper

	@staticmethod
	def createconn():
		return sqlite3.connect(SqlLite.dbfile)
