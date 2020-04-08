
from sqlite import SqlLite
from utils import Utility

class DBLoader():

    @staticmethod
    def loadtable(df, tblname, conn):
        print(f'Refreshing table [{tblname}] with {df.shape[0]} symbols', end='...', flush=True)
        df.to_sql(tblname, conn, if_exists='replace', index=False)
        print('Completed')

    @staticmethod
    def createindex(tblname, indexcol, conn):
        indexname = f'index_{tblname}_{indexcol}'
        print(f'Creating index on {tblname}({indexcol})', end='...', flush=True)
        create_index = f'create index if not exists {indexname} on {tblname}({indexcol});'
        SqlLite.conn.cursor().execute(create_index)
        print('Completed')

    @Utility.timer
    @SqlLite.connector
    def loadsecuritylist(self):
        tblname   = self.tbl_seclist
        indexcol  = self.indxcol_seclist
        print(f'Fetching list of all BSE and NSE Equities', end='...', flush=True)
        df = self.getsecuritylist()
        print('Completed')
        DBLoader.loadtable(df, tblname, SqlLite.conn)
        DBLoader.createindex(tblname, indexcol, SqlLite.conn)

    @Utility.timer
    @SqlLite.connector
    def loadhistprice(self, n_symbols=5000):
        tblname = self.tbl_quotesdly
        print(f'Downloading historical prices from yahoo finance for {n_symbols} symbols', end='...', flush=True)
        df = self.downloadhistprice(n_symbols)
        print('Completed')
        DBLoader.loadtable(df, tblname, SqlLite.conn)
