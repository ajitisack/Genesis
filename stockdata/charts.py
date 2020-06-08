import pandas as pd
pd.options.plotting.backend = "plotly"

from stockdata.main import getdata
from stockdata.main import getnsehistprice

def nsechart(symbol):
    symbol = symbol.upper().strip()
    name = getdata(f"select name from symbols where symbol = '{symbol}'").name[0]
    df = getnsehistprice(symbol)
    plt = df.close.plot.area(template='plotly_white', title=f'{name} [{symbol}]', y='close')
    plt.show()

def nseindexsymbolschart(index_name):
    symbols = getdata(f"select exchange, symbol from nseindices where indexname = '{index_name}'").symbol.to_list()
    [nsechart(i) for i in symbols]
