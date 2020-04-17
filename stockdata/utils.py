import pandas as pd
import numpy as np
import functools
import time

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

    @staticmethod
    def adddatefeatures(df):
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['wkday'] = df['date'].dt.dayofweek + 1
        df['wknr'] = df['date'].dt.week
        df['qrtr'] = df['date'].dt.quarter
        return df

    @staticmethod
    def reducesize(df):
        for i in df.columns:
            if 'date' not in i:
                df[i] = pd.to_numeric(df[i], errors='ignore', downcast='integer')
                df[i] = pd.to_numeric(df[i], errors='ignore', downcast='float')
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
