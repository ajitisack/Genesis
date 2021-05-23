import arrow
import pandas as pd

from lib.config import Config
from lib.sqlite import SqLite
from lib.utils import Utility

from lib.technicals.basics import BasicTechnicals
from lib.technicals.narrowrange import NarrowRange
from lib.technicals.pivotpoints import PivotPoints

class Technicals(Config, BasicTechnicals, NarrowRange, PivotPoints):

    def __init__(self):
        Config.__init__(self)

    @Utility.timer
    def loadtable(self, date=arrow.now().format('YYYY-MM-DD'), loadtotable=True):
        tblname = self.tbl_technicals
        tblname = tblname if date == arrow.now().format('YYYY-MM-DD') else f"{tblname}_{date.replace('-', '')}"
        print(f'Calculating technicals based on price values for NSE symbols as of {date}', end='...', flush=True)
        df1 = self.createbasictechnicals(date)
        df2 = self.createnr479(date)
        df = pd.merge(df1, df2, how='outer', on='symbol')
        df = self.createpivotpoints(df)
        df = self.createtomorrowpivotpoints(df)
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
        print('Completed!')
        if not loadtotable: return df
        SqLite.loadtable(df, tblname)

df = Technicals().loadtable('')
