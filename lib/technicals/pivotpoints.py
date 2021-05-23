import arrow
from statistics import mean

# https://www.investarindia.com/blog/pivot-points/

class PivotPoints():

    def createtomorrowpivotpoints(self, df):
        df['hl']  = (df['high'] + df['low'])/2
        df['pp']  = (df['high'] + df['low'] + df['close'])/3
        df['tc']  = df.apply(lambda x: x['hl'] if x['hl'] > x['pp'] else 0, axis=1)
        df['bc']  = df.apply(lambda x: x['hl'] if x['hl'] < x['pp'] else 0, axis=1)
        df['tc']  = df.apply(lambda x: x['pp'] + (x['pp'] - x['bc']) if x['tc'] == 0 else x['tc'], axis=1)
        df['bc']  = df.apply(lambda x: x['pp'] - (x['tc'] - x['pp']) if x['bc'] == 0 else x['bc'], axis=1)
        df['cpr'] = round(abs(df['tc'] - df['bc']),2)
        df['r1']  = (2 * df['pp']) - df['low']
        df['s1']  = (2 * df['pp']) - df['high']
        df['r2']  = df['pp'] + (df['high'] - df['low'])
        df['s2']  = df['pp'] - (df['high'] - df['low'])
        df['r3']  = df['high'] + 2 * (df['pp']   - df['low'])
        df['s3']  = df['low']  - 2 * (df['high'] - df['pp'])
        return df

    def createpivotpoints(self, df):
        df['hl0']  = (df['prevhigh'] + df['prevlow'])/2
        df['pp0']  = (df['prevhigh'] + df['prevlow'] + df['prevclose'])/3
        df['tc0']  = df.apply(lambda x: x['hl0'] if x['hl0'] > x['pp0'] else 0, axis=1)
        df['bc0']  = df.apply(lambda x: x['hl0'] if x['hl0'] < x['pp0'] else 0, axis=1)
        df['tc0']  = df.apply(lambda x: x['pp0'] + (x['pp0'] - x['bc0']) if x['tc0'] == 0 else x['tc0'], axis=1)
        df['bc0']  = df.apply(lambda x: x['pp0'] - (x['tc0'] - x['pp0']) if x['bc0'] == 0 else x['bc0'], axis=1)
        df['cpr0'] = round(abs(df['tc0'] - df['bc0']),2)
        df['r10']  = (2 * df['pp0']) - df['prevlow']
        df['s10']  = (2 * df['pp0']) - df['prevhigh']
        df['r20']  = df['pp0'] + (df['prevhigh'] - df['prevlow'])
        df['s20']  = df['pp0'] - (df['prevhigh'] - df['prevlow'])
        df['r30']  = df['prevhigh'] + 2 * (df['pp0']   - df['prevlow'])
        df['s30']  = df['prevlow']  - 2 * (df['prevhigh'] - df['pp0'])
        return df
