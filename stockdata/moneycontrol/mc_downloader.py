import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from .mc_sectorclassify import SectorClassify
from .mc_symboldetails import SymbolDetails
from ..config import Config
from ..sqlite import SqLite
from ..utils import Utility
from ..sdlogger import SDLogger

class MoneyControl(SDLogger, Config, SectorClassify, SymbolDetails):

    def __init__(self):
        self.nodatalist = []
        Config.__init__(self)
        self.terms = self.getkeyterms()

    def getkeyterms(self):
        items={}
        with open(self.mcdetailsfile) as f:
            for line in f:
                line = line.strip()
                if line == '': continue
                if line.startswith('['):
                    key = line.replace('[','').replace(']','')
                    items[key] = {}
                else:
                    k = line.split('=')[0].strip()
                    v = line.split('=')[1].strip()
                    items[key][k] = v
        return items

    @Utility.timer
    def downloaddetails(self, n_symbols, loadtotable):
        x = 'all' if n_symbols == 0 else n_symbols
        print(f'Downloading details of {x} symbols from Money Control', end='...', flush=True)
        df1 = self.getsectorclassif()
        if n_symbols > 0: df1 = df1.head(n_symbols)
        symbols = zip(df1.exchange, df1.symbolurl)
        nthreads = min(len(df1), int(self.maxthreads))
        with ThreadPoolExecutor(max_workers=nthreads) as executor:
            results = executor.map(self.getsymboldetails, symbols)
        df2 = pd.DataFrame(results)
        df = pd.merge(df1, df2, how='left', on=['symbolcd', 'exchange'])
        df = Utility.reducesize(df)
        print('Completed')
        if not loadtotable: return df
        df_nse = df.query("exchange == 'NSE'")
        df_bse = df.query("exchange == 'BSE'")
        SqLite.loadtable(df_nse, self.tbl_nsemcprofile)
        SqLite.loadtable(df_bse, self.tbl_bsemcprofile)
