import pandas as pd

from .technical_indicators.indicators import Indicators

def addIndicators(df):
    return Indicators().createIndicators(df)

def addMA(df, n):
    return Indicators().MA(df, n)
