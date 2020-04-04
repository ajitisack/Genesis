import pandas as pd
from sqlite import SqlLite
from collections import defaultdict
from timeit import default_timer as timer
from utils import Utility


class BSE():
	equityfile = "/Users/ajit/projects/stockmarket_analysis/Equity.csv"
	securitytbl = 'security'
	indexcol = 'securitycd'
	securitystatus = defaultdict(lambda: 'N', {'Active':'A', 'Delisted':'D', 'Suspended':'S'})

	@staticmethod
	def readequitieslist():
		df=pd.read_csv(BSE.equityfile)
		df = df.drop(['Instrument', 'Issuer Name'], axis=1)
		df.columns = ['securitycd', 'securityid', 'securitynm', 'status', 'group', 'facevalue', 'isin', 'industry']
		df['securityid'] = df['securityid'].str.replace('*', '')
		df = df.applymap(lambda x: Utility.cleanstr(x) if type(x) == str else x)
		df['status'] = df.apply(lambda x: BSE.securitystatus[x['status']], axis=1)
		return df

	@classmethod
	@SqlLite.connector
	def loadequitieslist(cls, df):
		tblname   = BSE.securitytbl
		indexcol  = BSE.indexcol
		indexname = f'index_{tblname}_{indexcol}'
		df.to_sql(tblname, SqlLite.conn, if_exists='replace', index=False)
		print(f'Info : Table {tblname} has been refreshed with {df.shape[0]} records')
		create_index = f'create index if not exists {indexname} on {tblname}({indexcol});'
		SqlLite.conn.cursor().execute(create_index)
		print(f'Info : Index created on {tblname}({indexcol})')


if __name__ == "__main__":
	start = timer()
	df = BSE.readequitieslist()
	BSE.loadequitieslist(df)
	end = timer()
	print("Execution time : " + str(round(end - start, 3)) + "s")


# df = BSE.readequitieslist()
# BSE.loadequitieslist(df)
