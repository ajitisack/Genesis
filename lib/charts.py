import pandas as pd
pd.options.plotting.backend = "plotly"

from stockdata.main import getdata
from stockdata.main import getnsehistprice

def chart(x):
    plt = x.plot.area(template='plotly_white', y=x.name)
    plt.show()

def nsechart(symbols):
    if type(symbols) == list:
        symbols = list(map(lambda x: x.upper().strip(), symbols))
    else:
        symbols = [symbols.upper().strip()]
    df = getnsehistprice(symbols)
    for symbol in symbols:
        x = getdata(f"select name, industry from symbols where symbol = '{symbol}'")
        name = x['name'][0]
        industry = x['industry'][0]
        dfx = df[df.symbol==symbol]
        plt = dfx.close.plot.area(template='plotly_white', title=f'{name} [{symbol}] - {industry}', y='close')
        plt.show()

def nseindexsymbolschart(index_name):
    df = getdata(f"select exchange, symbol from indices where indexname = '{index_name}'")
    nsechart(df.symbol.to_list())
