import pandas as pd

from stockdata.technical_indicators.indicators import Indicators

def addIndicators(df):
    return Indicators().createIndicators(df)

def addMA(df, n):
    return Indicators().MA(df, n)

def addEMA(df, n):
    return Indicators().EsssMA(df, n)
