import pandas as pd

from securitylist import SecurityList
from securityhistprice import SecurityHistPrice
from securitydetails import SecurityDetails
from config import Config
from sqlite import SqlLite
from utils import Utility

class StockData(Config, SecurityList, SecurityHistPrice, SecurityDetails):
    def __init__(self):
        self.nodatalist = []
        Config.__init__(self)

    @SqlLite.connector
    def getsymbols(self, n_symbols=5000):
        query = f'select symbol, inbse, innse from security where 1 = 1 limit {n_symbols}'
        df = pd.read_sql(query, SqlLite.conn)
        df['ticker'] = df.apply(lambda x: x['symbol'] + '.BO' if x['innse']==0 and x['inbse']==1 else x['symbol'] + '.NS' , axis=1)
        return list(df.ticker)

    @Utility.timer
    def downloadsymbols(self):
        tblname   = self.tbl_seclist
        indexcol  = self.indxcol_seclist
        print(f'Fetching list of all BSE and NSE Equities', end='...', flush=True)
        df = self.getsecuritylist()
        print('Completed')
        SqlLite.loadtable(df, tblname)
        SqlLite.createindex(tblname, indexcol)

    @Utility.timer
    def downloadhistprice(self, n_symbols=5000):
        tblname = self.tbl_quotesdly
        print(f'Downloading historical prices from yahoo finance for {n_symbols} symbols', end='...', flush=True)
        df = self.getallhistprice(n_symbols)
        print('Completed')
        SqlLite.loadtable(df, tblname)

    @Utility.timer
    def downloaddetails(self, n_symbols=5000):
        tblname = self.tbl_secdetails
        print(f'Downloading details of {n_symbols} symbols from yahoo finance', end='...', flush=True)
        df = self.getsecuritydetails(n_symbols)
        print('Completed')
        SqlLite.loadtable(df, tblname)

if __name__ == '__main__':
    sd = StockData()
    sd.downloadsymbols()
    sd.downloadhistprice()
    sd.downloaddetails()
