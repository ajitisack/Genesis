from configparser import ConfigParser
from configparser import ExtendedInterpolation

from stockdata.technical_indicators.trend import TrendIndicators
from stockdata.config import Config

class Indicators(Config, TrendIndicators):

    def __init__(self):
        self.indicators = []
        Config.__init__(self)

    def getIndicators(self):
        with open(self.indicatorsfile) as f:
            for line in f:
                line = line.strip()
                if line == '' or line.startswith('['): continue
                x = line.split('=')
                x = (x[0].strip(), x[1].strip())
                self.indicators.append(x)

    def createIndicators(self, df):
        self.getIndicators()
        # print(self.indicators)
        for indicators in self.indicators:
            func = indicators[0]
            func_param = indicators[1]
            exec(f'df = self.{func}(df, {func_param})')
        return df

# EWMA
# n = 3
# weights= list(reversed([(n - i) * n for i in range(n)]))
#
# def wma(w):
#     def g(x):
#         return sum(w*x)/sum(w)
#     return g
#
# x.close.rolling(n).apply(wma(weights))
