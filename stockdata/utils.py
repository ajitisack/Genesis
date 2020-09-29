import pandas as pd
import numpy as np
import functools
import time
import datetime

class Utility():

    @staticmethod
    def cleanstr(str):
        return str.strip()\
        .replace('&amp;','&')\
        .replace('&amp;','&')\
        .replace('-$','')\
        .replace('&#39;','\'')\
        .replace('&#160;', '')\
        .replace('(','')\
        .replace(')','')\
        .replace('*', '')\
        .replace('LTD.','LTD')

    def asfloat(n):
        if n == '-': return 0
        return float(n.replace(',', ''))

    def asint(n):
        if n == '-': return 0
        return int(n.replace(',', ''))

    @staticmethod
    def adddatefeatures(df):
        df['date']  = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df['year']  = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day']   = df['date'].dt.day
        df['wkday'] = df['date'].dt.dayofweek + 1
        df['wknr']  = df['date'].dt.isocalendar().week
        df['qrtr']  = df['date'].dt.quarter
        df['date']  = df['date'].dt.date
        return df

    @staticmethod
    def hoursbinning(t):
        if t >= datetime.time(15,0) : return 7
        if t > datetime.time(14,0)  : return 6
        if t > datetime.time(13,0)  : return 5
        if t > datetime.time(12,0)  : return 4
        if t > datetime.time(11,0)  : return 3
        if t > datetime.time(10,0)  : return 2
        return 1

    @staticmethod
    def addtimefeatures(df):
        df['timestamp']  = df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x))
        df['date']    = df['timestamp'].dt.date
        df['year']    = df['timestamp'].dt.year
        df['month']   = df['timestamp'].dt.month
        df['day']     = df['timestamp'].dt.day
        df['wkday']   = df['timestamp'].dt.dayofweek + 1
        df['wknr']    = df['timestamp'].dt.isocalendar().week
        df['qrtr']    = df['timestamp'].dt.quarter
        df['time']    = df['timestamp'].dt.time
        df['after12'] = df['time'].apply(lambda x: 1 if x >= datetime.time(12,0) else 0)
        df['dayhour'] = df['time'].apply(lambda x: Utility.hoursbinning(x))
        df['timestamp'] = df['timestamp'].apply(lambda x: x.strftime("%a %b-%d-%Y %H:%M"))
        df['time'] = df['time'].apply(lambda x: x.strftime("%H:%M"))
        return df

    @staticmethod
    def reducesize(df):
        # downsize int columns of the dataframe
        int_cols = df.select_dtypes(include=['int64', 'int32', 'int16']).columns
        df[int_cols] = df[int_cols].apply(lambda x: pd.to_numeric(x, errors='ignore', downcast='integer'))
        # round float columns to 2 decimal places
        float_cols = df.select_dtypes(include=['float64', 'float32']).columns
        float_cols = float_cols[~float_cols.str.endswith('pct')]
        df[float_cols] = df[float_cols].apply(lambda x: round(x, 2))
        return df

    @staticmethod
    def timer(func):
        """Print the runtime of the decorated function"""
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time = time.perf_counter()    # 1
            value = func(*args, **kwargs)
            end_time = time.perf_counter()      # 2
            run_time = end_time - start_time    # 3
            print(f'Finished [{func.__name__}] in {run_time:.4f} secs')
            return value
        return wrapper_timer
