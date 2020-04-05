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
        new_dtypes = {'open':np.float32, 'high':np.float32, 'low':np.float32, 'close':np.float32, 'adjclose':np.float32, 'volume':np.int32
                    , 'year':np.int16, 'month':np.int16, 'day':np.int16, 'wkday':np.int16, 'wknr':np.int16, 'qrtr':np.int16}
        df = df.astype(new_dtypes)
        return df

    @staticmethod
    def getdomainkeyvalue(json_str, domain, key):
        return [json_str[domain][key]] if domain in json_str and json_str[domain] and key in json_str[domain] else ['']

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
