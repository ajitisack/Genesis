import pandas as pd

from ..utils import Utility
from ..sdlogger import SDLogger
from ..sqlite import SqLite

class TrendIndicators():

    def MA(self, df, n):
        name=f'ma{n}d'
        x = df.close.rolling(n).mean().fillna(0)
        df[name] = x
        return df

    def EMA(self, df, n):
        name=f'ema{n}d'
        x = df.close.ewm(span=n, adjust=False).mean().fillna(0)
        df[name] = x
        return df
