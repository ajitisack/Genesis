import pandas as pd
import arrow
from glob import glob
from itertools import repeat
from concurrent.futures import ThreadPoolExecutor

from nsedata.lib.intraday.getintradaydata import IntraDayDataDict
from nsedata.lib.config import Config
from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils  import Utility


class IntraDayData(IntraDayDataDict, Config):

    def __init__(self):
        Config.__init__(self)

    @SqLite.connector
    def getsymbols(self, n_symbols):
        tblname = 'symbols'
        query = f"select distinct symbol || '.NS' as symbol from {tblname} where innifty100 = 1 or fnoactivated = 1 "
        if n_symbols > 0: query += f'limit {n_symbols}'
        df = pd.read_sql(query, SqLite.conn)
        return list(df.symbol)

    def processdf(self, df):
        # df['timestamp'] = df['timestamp'].apply(lambda x: arrow.get(x).to('local').format('YYYY-MM-DD HH:mm'))
        df['symbol'] = df['symbol'].apply(lambda x: x.split('.')[0].replace('^', ''))
        df = Utility.addtimefeatures(df)
        return df

    def download(self, date, symbols, interval):
        nthreads = min(len(symbols), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.getintradaydata, symbols, repeat(date), repeat(interval))
        values = list(results)
        dfs = [pd.DataFrame(d) for d in values]
        df = pd.concat(dfs, ignore_index=True).dropna()
        if df.empty:
            print(f'{interval} - No data !')
            return None
        df = self.processdf(df)
        df = df.astype({'volume': int})
        df.insert(0, 'freq', interval)
        return df


    @Utility.timer
    def downloadallfiles(self, date, n_symbols):
        symbols = ['^NSEI', '^NSEBANK'] + self.getsymbols(n_symbols)
        print(f'Downloading equity intraday prices from yahoo finance for {date} NSE FNO & Nifty 100 {len(symbols)} symbols', end='...', flush=True)
        df_1m  = self.download(date, symbols, '1m')
        df_5m  = self.download(date, symbols, '5m')
        df_15m = self.download(date, symbols, '15m')
        df_30m = self.download(date, symbols, '30m')
        df_1h  = self.download(date, symbols, '1h')
        df = pd.concat([df_1m, df_5m, df_15m, df_30m, df_1h])
        file = f"{self.intraday_dir}/NSE_{date.replace('-','')}.zip"
        df.to_csv(file, index=False, compression='zip')
        print('Completed!')
        print(f'Rows and Columns in downloaded data file - {df.shape}')
        print('Rows and Columns of NIFTY and BANKNIFTY data for each interval...')
        print(df[(df.symbol.isin(['NSEI', 'NSEBANK']))][['freq', 'symbol']].value_counts())


    @Utility.timer
    def createmonthlyfile(self, yyyymm):
        yyyymm = yyyymm.replace('-', '')
        infiles = glob(rf'{self.intraday_dir}/NSE_{yyyymm}*.zip')
        outfile = f'{self.intraday_dir}/NSE_{yyyymm}.zip'
        if not infiles:
            print('Error!')
            print(f'No file(s) matching with {self.intraday_dir}/NSE_{yyyymm}*.zip')
            return None
        print(f'Combining NSE intraday daily files for month {yyyymm}', end='...', flush=True)
        dfs = [pd.read_csv(file) for file in infiles]
        df = pd.concat(dfs, ignore_index=True)
        df.to_csv(outfile, index=False, compression='zip')
        print('Completed!')

    # @Utility.timer
    # def loadintradayfile(self, exchange, yyyymm):
    #     print(f'Reading {exchange.upper()} intraday daily files for month {yyyymm}', end='...', flush=True)
    #     yyyymm = yyyymm.replace('-', '')
    #     infiles = glob(rf'{self.intraday_dir}/{exchange}_{yyyymm}*.zip')
    #     if exchange == 'NSE': tblname = f'{self.tbl_nseintraday}_{yyyymm}'
    #     if not infiles:
    #         print('Error!')
    #         print(f'No file(s) matching with {self.intraday_dir}/{exchange}_{yyyymm}*.zip')
    #         return None
    #     dfs = [pd.read_csv(file) for file in infiles]
    #     df = pd.concat(dfs, ignore_index=True)
    #     df = Utility.reducesize(df)
    #     print('Completed!')
    #     SqLite.loadtable(df, tblname)
    #     # SqLite.createindex(tblname, 'symbol')
