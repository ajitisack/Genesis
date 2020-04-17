import pandas as pd

from ..utils import Utility
from ..sdlogger import SDLogger
from ..sqlite import SqLite

class TrendIndicators():

    def MA(self, df, n):
        name=f'ma{n}d'
        ma = df.close.rolling(n).mean().fillna(0)
        df[name] = ma
        return df
