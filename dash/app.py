import stockdata as sd
import pandas as pd
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

pd.options.display.float_format = '{:,.2f}'.format


def pricetbl(table_id, df):
    return dash_table.DataTable(
        id = table_id,
        columns= [
          {'name':'Sector', 'id': 'sector'}
        , {'name':'Symbol', 'id': 'symbol'}
        , {'name':'LTP' , 'id': 'ltp'}
        , {'name':'%Change' , 'id': 'changepct'}
        , {'name':'Vol', 'id':'volume'}
        , {'name':'PriceLevel', 'id':'pricelevel'}
        , {'name':'Qty' , 'id': 'qty'}
        , {'name':'SL-Buy' , 'id': 'slb'}
        , {'name':'SL-Sell' , 'id': 'sls'}
        ],
        # fixed_rows={'headers': True},
        # style_table={
        #     'width' : 400
        # },
        style_header={
              'backgroundColor': 'rgb(35, 35, 35)'
            , 'color': 'rgb(210, 210, 210)'
            , 'font-family' : 'Verdana'
            , 'font-size' : 13
            , 'fontWeight': 'bold'
            , 'height' : 6
        },
        style_cell={
            'backgroundColor': 'rgb(20, 20, 20)'
            , 'color': 'rgb(200, 200, 200)'
            , 'height' : 6
            , 'font-size' : 12
            , 'font-family' : 'Verdana'
            , 'border': '1px solid rgb(40, 40, 40)'
        },
        style_cell_conditional=[
            {
                'if': {'column_id': ['sector', 'symbol', 'pricelevel']}
                , 'textAlign': 'left'
                , 'padding-left': 15
                , 'font-family' : 'Verdana'
            },
            {
                'if': {'column_id': 'sls'},
                'textAlign': 'right',
                'padding-right': 15
            },
            {
                'if': {'column_id': ['qty']}
                , 'color' : 'rgb(255,255,100)'
            },
        ],
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{changepct} < 0',
                    'column_id': ['sector', 'symbol', 'ltp', 'changepct', 'volume']
                }
                , 'color' : 'tomato'
            },
            {
                'if': {
                    'filter_query': '{changepct} >= 0',
                    'column_id': ['sector', 'symbol', 'ltp', 'changepct', 'volume']
                }
                , 'color' : 'lightgreen'
            },
            {
                'if': {
                    'filter_query': '{pricelevel} contains "R"',
                    'column_id': ['pricelevel']
                }
                , 'color' : 'dodgerblue'
            },
            {
                'if': {
                    'filter_query': '{pricelevel} contains "S"',
                    'column_id': ['pricelevel']
                }
                , 'color' : 'darkorange'
            },
            {
                'if': {
                    'filter_query': '{pricelevel} contains "Within"',
                    'column_id': ['pricelevel']
                }
                , 'color' : 'orchid'
            },
            {
                'if': {
                    'filter_query': '{pricelevel} contains "(O" && {changepct} >= 0',
                    'column_id': ['symbol']
                }
                , 'backgroundColor': 'lightgreen'
                , 'color' : 'black'
            },
            {
                'if': {
                    'filter_query': '{pricelevel} contains "(O" && {changepct} < 0',
                    'column_id': ['symbol']
                }
                , 'backgroundColor': 'tomato'
                , 'color' : 'black'
            },
        ],
        style_as_list_view=True,
        data = df.to_dict('records'),
    )

def indicestbl(table_id, df):
    return dash_table.DataTable(
        id = table_id,
        columns= [
          {'name':'Index', 'id': 'symbol'}
        , {'name':'LTP' , 'id': 'ltp'}
        , {'name':'%Change' , 'id': 'changepct'}
        ],
        style_header={
              'backgroundColor': 'rgb(35, 35, 35)'
            , 'color': 'rgb(210, 210, 210)'
            , 'font-family' : 'Verdana'
            , 'font-size' : 13
            , 'fontWeight': 'bold'
            , 'height' : 6
        },
        style_cell={
            'backgroundColor': 'rgb(20, 20, 20)'
            , 'color': 'rgb(180, 180, 180)'
            , 'height' : 6
            , 'font-size' : 12
            , 'font-family' : 'Verdana'
            , 'border': '1px solid rgb(40, 40, 40)'
        },
        style_cell_conditional=[
            {
                'if': {'column_id': ['symbol']}
                , 'textAlign': 'left'
                , 'padding-left': 20
                , 'font-family' : 'Verdana'
            },
            {
                'if': {'column_id': ['changepct', 'ltp']}
                , 'textAlign': 'right'
                , 'padding-right': 15
            }
        ],
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{changepct} < 0',
                    'column_id': ['symbol', 'ltp', 'changepct']
                },
                'color' : 'tomato'
            },
            {
                'if': {
                    'filter_query': '{changepct} >= 0',
                    'column_id': ['symbol', 'ltp', 'changepct']
                },
                'color' : 'lightgreen'
            },
        ],
        style_as_list_view=True,
        data = df.to_dict('records'),
    )

query = """
select symbol, r3, r2, r1, tc, pp, bc, s1, s2, s3
from technicals
where inhotlist =1
"""
pivots = sd.getdata(query)

def getpricelevel(x):
    pricelevel = 'Below S3'
    if x['ltp'] >= x['s3']: pricelevel = 'Above S3'
    if x['ltp'] >= x['s2']: pricelevel = 'Above S2'
    if x['ltp'] >= x['s1']: pricelevel = 'Above S1'
    if x['ltp'] >= x['bc'] and x['ltp'] <= x['tc']: pricelevel = 'Within CPR'
    if x['ltp'] >  x['tc']: pricelevel = 'Above CPR'
    if x['ltp'] >= x['r1']: pricelevel = 'Above R1'
    if x['ltp'] >= x['r2']: pricelevel = 'Above R2'
    if x['ltp'] >= x['r3']: pricelevel = 'Above R3'
    if x['open'] == x['low']:  pricelevel += ' (OL)'
    if x['open'] == x['high']: pricelevel += ' (OH)'
    return pricelevel

def getprice(rpt=80, riskpct=0.3):
    risk = riskpct/100
    df = sd.getdata("select * from  NSE_MyWatchlistCurrentPrice")
    # df = sd.getdata("select sector, symbol, open, 0 low, 0 high, open ltp, volume, changepct from preopen where inhotlist = 1")
    df = pd.merge(df, pivots, how = 'outer', on = 'symbol')
    df['pricelevel'] = df.apply(lambda x: getpricelevel(x), axis = 1)
    df['volume']     = df['volume'].apply(lambda x: round(x/100000, 2))
    df['qty']        = df.apply(lambda x: round(rpt/(x['ltp']*risk), 0), axis = 1)
    df['slb']        = df['ltp'].apply(lambda x: round(x-(x*risk),0))
    df['sls']        = df['ltp'].apply(lambda x: round(x+(x*risk),0))
    cols = ['symbol', 'ltp', 'changepct']
    df_indices1 = df[df.symbol == 'Nifty 50'][cols]
    df_indices2 = df[(df.sector == 'Index') & (df.symbol != 'Nifty 50')][cols]
    df_indices2 = df_indices2.sort_values(by='changepct', ascending=False)
    cols = ['sector', 'symbol', 'ltp', 'volume', 'changepct', 'qty', 'slb', 'sls', 'pricelevel']
    df_symbols = df[df.sector != 'Index'][cols]
    df_banks   = df[df.sector == 'Bank'][cols].sort_values(by='changepct', ascending=False)
    df_it      = df[df.sector == 'IT'][cols].sort_values(by='changepct', ascending=False)
    df_auto    = df[df.sector == 'Auto'][cols].sort_values(by='changepct', ascending=False)
    df_pharma  = df[df.sector == 'Pharma'][cols].sort_values(by='changepct', ascending=False)
    df_metal   = df[df.sector == 'Metal'][cols].sort_values(by='changepct', ascending=False)
    return df_symbols, df_indices1, df_indices2, df_banks, df_it, df_auto, df_pharma, df_metal


def layout():
    body = dbc.Container([
          dbc.Row([
            dbc.Col(html.Div(pricetbl('tbl3', getprice()[2]), id='stock-data3'), width=0),
            dbc.Col(html.Div(pricetbl('tbl4', getprice()[1]), id='stock-data4'), width=0)
          ])
        , dbc.Row([
            dbc.Col([
                  html.H2('Symbols - Above Open', style = {'color': 'rgb(200, 200, 200)', 'font-family' : 'Verdana', 'text-align':'center'})
                , html.Div(pricetbl('tbl1', getprice()[0]), id='stock-data1')
            ], width=6),
            dbc.Col([
                  html.H2('Symbols - Below Open', style = {'color': 'rgb(200, 200, 200)', 'font-family' : 'Verdana', 'text-align':'center'})
                , html.Div(pricetbl('tbl2', getprice()[0]), id='stock-data2'
            )], width=6),
          ])
        , dbc.Row([
            dbc.Col([
                  html.H1('Banks', style = {'color': 'rgb(200, 200, 200)', 'font-family' : 'Verdana', 'text-align':'center'})
                , html.Div(pricetbl('tbl5', getprice()[3]), id='stock-data5')
            ], width=6),
            dbc.Col([
                  html.H1('IT', style = {'color': 'rgb(200, 200, 200)', 'font-family' : 'Verdana', 'text-align':'center'})
                , html.Div(pricetbl('tbl6', getprice()[4]), id='stock-data6')
            ], width=6),
          ])
        , dbc.Row([
            dbc.Col([
                  html.H1('Auto', style = {'color': 'rgb(200, 200, 200)', 'font-family' : 'Verdana', 'text-align':'center'})
                , html.Div(pricetbl('tbl7', getprice()[5]), id='stock-data7')
            ], width=6),
            dbc.Col([
                  html.H1('Pharma', style = {'color': 'rgb(200, 200, 200)', 'font-family' : 'Verdana', 'text-align':'center'})
                , html.Div(pricetbl('tbl8', getprice()[6]), id='stock-data8')
            ], width=6),
          ])
        , dcc.Interval(
                    id = 'interval-component',
                    interval = 1 * 1000, # in milliseconds ie, 1 x 1000 means 1 sec
                    n_intervals = 0
        )
    ], fluid = True)
    return html.Div(body, style={'backgroundColor': 'rgb(18, 18, 18)'})

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID])
app.layout = layout


@app.callback([
      Output('stock-data1', 'children')
    , Output('stock-data2', 'children')
    , Output('stock-data3', 'children')
    , Output('stock-data4', 'children')
    , Output('stock-data5', 'children')
    , Output('stock-data6', 'children')
    , Output('stock-data7', 'children')
    , Output('stock-data8', 'children')
], [Input('interval-component', 'n_intervals')])
def update_table(x):
    df, df_indices1, df_indices2, df_banks, df_it, df_auto, df_pharma, df_metal = getprice()
    dfu = df[df.changepct >=0].sort_values(by='changepct', ascending=False)
    dfd = df[df.changepct < 0].sort_values(by='changepct', ascending=True)
    return pricetbl('tbl1', dfu), pricetbl('tbl2', dfd), indicestbl('tbl3', df_indices1), indicestbl('tbl4', df_indices2), pricetbl('tbl5', df_banks), pricetbl('tbl6', df_it), pricetbl('tbl7', df_auto), pricetbl('tbl8', df_pharma)


if __name__ == '__main__':
    app.run_server(debug=True)
