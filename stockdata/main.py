import pandas as pd
import plotly.graph_objects as go

from stockdata.symbols.getsymbols import Symbols
from stockdata.sqlite import SqLite
from stockdata.utils import Utility

# to download NSE and BSE symbols
def downloadsymbols():
    return Symbols().download()

@SqLite.connector
def getdata(query):
    df = pd.read_sql(query, SqLite.conn)
    df = Utility.reducesize(df)
    return df

@SqLite.connector
def getnsehistprice(symbol):
    query = f"select * from nsehistprice where symbol = '{symbol.upper()}'"
    df = pd.read_sql(query, SqLite.conn)
    df = Utility.reducesize(df)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

def loadtotable(df, tblname):
    df = Utility.reducesize(df)
    SqLite.loadtable(df, tblname)

def searchsymbol(name):
    df = getdata(f"select * from symbols where name like '%{name.upper()}%'")
    return df
    # fig = go.Figure(data=[go.Table(
    # header=dict(values=['Symbol', 'Name', 'Industry', 'Group', 'NSE Date of Listing', 'Listed in NSE', 'Listed in BSE'],
    #             fill_color='skyblue',
    #             font=dict(size=14),
    #             align='left'),
    # cells=dict(values=[df.symbol, df.name, df.industry, df.group, df.dateoflisting, df.innse, df.inbse],
    #            fill_color='lavender',
    #            align='left'))
    # ])
    # fig.show()
