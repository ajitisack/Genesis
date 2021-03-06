import os
import sqlite3
import functools
import pkgutil
from configparser import ConfigParser
from configparser import ExtendedInterpolation

class SqLite():
	conn = None
	cp = ConfigParser(interpolation=ExtendedInterpolation())
	config_file = f'{os.path.dirname(__file__)}/config.ini'
	cp.read(config_file)
	dbfile = cp.get('database', 'dbfile')

	def connector(func):
		@functools.wraps(func)
		def wrapper(*args):
			SqLite.conn = sqlite3.connect(SqLite.dbfile)
			return func(*args)
			SqLite.conn.close
		return wrapper

	@staticmethod
	def createconn():
		return sqlite3.connect(SqLite.dbfile)

	@staticmethod
	@connector
	def loadtable(df, tblname):
		if df.empty:
			print('Dataframe is empty!')
			return None
		print(f'Refreshing table [{tblname}] with {df.shape[0]} records', end='...', flush=True)
		df.to_sql(tblname, SqLite.conn, if_exists='replace', index=False)
		print('Completed')

	@staticmethod
	@connector
	def appendtable(df, tblname):
		if df.empty:
			print('Dataframe is empty!')
			return None
		print(f'Appending table [{tblname}] with {df.shape[0]} records', end='...', flush=True)
		df.to_sql(tblname, SqLite.conn, if_exists='append', index=False)
		print('Completed')

	@staticmethod
	@connector
	def createindex(tblname, indexcol):
		indexname = f'index_{tblname}_{indexcol}'
		print(f'Creating index on {tblname}({indexcol})', end='...', flush=True)
		create_index = f'create index if not exists {indexname} on {tblname}({indexcol});'
		SqLite.conn.cursor().execute(create_index)
		print('Completed')
