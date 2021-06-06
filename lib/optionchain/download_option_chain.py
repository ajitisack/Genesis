import json
import arrow
import requests
import pandas as pd
import numpy as np
import schedule
import time
from pprint import pprint

from nsedata.lib.config import Config
from nsedata.lib.sqlite import SqLite
from nsedata.lib.utils import Utility

from nsedata.lib.optionchain.get_option_chain import OptionChain

class IndexOptionChain(OptionChain, Config):

    def __init__(self):
        Config.__init__(self)
        self.time_format = 'HH:mm'

    @Utility.timer
    def downloadIndexOptionChain(self):
        print(f"{arrow.now().to(self.tz).format('DD-MMM-YYYY HH:mm:ss')} : Downloading Index Option Chain", end='...', flush=True)
        df1 = self.getOptionChain('NIFTY')
        df2 = self.getOptionChain('BANKNIFTY')
        df = pd.concat([df1, df2], ignore_index=True)
        print('Completed')
        SqLite.appendtable(df, self.tbl_optionchain)

    def scheduleJob(self, start_time, end_time, freq, func):
        t = arrow.get(start_time, self.time_format)
        execution_timestamp = []
        while True:
            timestamp = t.format(self.time_format)
            execution_timestamp += [timestamp]
            t = t.shift(minutes=+freq)
            if timestamp == end_time: break
        [schedule.every().day.at(t).do(func).tag('optionchain') for t in execution_timestamp]

    def startDownload(self, start_time, end_time, freq):
        schedule.clear('optionchain')
        self.scheduleJob(start_time, end_time, freq=freq, func=self.downloadIndexOptionChain)
        # pprint(schedule.get_jobs('optionchain'))
        time = arrow.now().to(self.tz).format(self.time_format)
        while end_time >= time:
            schedule.run_pending()
            time = arrow.now().to('Asia/Calcutta').format(self.time_format)
        print(f"Current time is {arrow.now().to(self.tz).format('YYYY-MMM-DD HH:mm:ss ZZZ')}. Process Completed!")
