import arrow
import pandas as pd
import numpy as np

from stockdata.sqlite import SqLite

class NarrowRange():

    @SqLite.connector
    def createnr479(self, date):
        tblname = self.tbl_nsehpricedly
        query = f"select distinct date from {tblname} where date <= '{date}' order by 1 desc limit 9"
        x = pd.read_sql(query, SqLite.conn).date.to_list()
        dts = "'"+ "','".join(x) + "'"
        query = f"select date, symbol, open, low, high, close from {tblname} where date in ({dts})"
        df = pd.read_sql(query, SqLite.conn)
        df['prevhigh'] = df.groupby('symbol').high.transform(lambda x: x.shift(1))
        df['prevlow']  = df.groupby('symbol').low.transform(lambda x: x.shift(1))
        df['tr']   = df['high'] - df['low']
        df['tr1d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(1))
        df['tr2d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(2))
        df['tr3d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(3))
        df['tr4d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(4))
        df['tr5d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(5))
        df['tr6d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(6))
        df['tr7d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(7))
        df['tr8d'] = df.groupby('symbol').tr.transform(lambda x: x.shift(8))
        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)
        df['lowerhigh'] = df.apply(lambda x: 1 if x['high'] < x['prevhigh'] else 0, axis=1)
        df['higherlow'] = df.apply(lambda x: 1 if x['low']  > x['prevlow']  else 0, axis=1)
        df['NR4'] = df.apply(lambda x: 1 if x['tr'] < x['tr1d'] and x['tr'] < x['tr2d'] and x['tr'] < x['tr3d'] else 0, axis=1)
        df['NR7'] = df.apply(lambda x: 1 if x['NR4'] == 1 and x['tr'] < x['tr4d'] and x['tr'] < x['tr5d'] and x['tr'] < x['tr6d'] else 0, axis=1)
        df['NR9'] = df.apply(lambda x: 1 if x['NR7'] == 1 and x['tr'] < x['tr7d'] and x['tr'] < x['tr8d'] else 0, axis=1)
        df.drop(['date', 'open', 'low', 'high', 'close', 'prevhigh', 'prevlow'], axis=1, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
