import arrow
from statistics import mean

class PivotPoints():

    def createpivotpoints(self, df):
        df['pp'] = (df['high'] + df['low'] + df['close'])/3
        df['bc'] = (df['high'] + df['low'])/2
        df['tc'] = 2 * df['pp'] - df['bc']
        df['cpr'] = round(abs(df['tc'] - df['bc']),2)
        df['r1'] = 2 * df['pp'] - df['low']
        df['r2'] = df['pp'] + df['high'] - df['low']
        df['r3'] = df['high'] + 2 * (df['pp'] - df['low'])
        df['s1'] = (2 * df['pp']) - df['high']
        df['s2'] = df['pp'] - (df['high'] - df['low'])
        df['s3'] = df['low'] - 2 * (df['high'] - df['pp'])
        return df
