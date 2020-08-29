import arrow
import pandas as pd

from stockdata.config import Config
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

from stockdata.technicals.basics import BasicTechnicals
from stockdata.technicals.narrowrange import NarrowRange
from stockdata.technicals.pivotpoints import PivotPoints

class Technicals(Config, BasicTechnicals, NarrowRange, PivotPoints):

    def __init__(self):
        Config.__init__(self)

    @Utility.timer
    def loadtechnicals(self, loadtotable=True):
        tblname = self.tbl_nsetechnicals
        df1 = self.createbasictechnicals()
        df2 = self.createnr479()
        df = pd.merge(df1, df2, how='outer', on='symbol')
        df = self.createpivotpoints(df)
        df = Utility.reducesize(df)
        df['runts'] = arrow.now().format('ddd MMM-DD-YYYY HH:mm')
        if not loadtotable: return df
        SqLite.loadtable(df, tblname)
