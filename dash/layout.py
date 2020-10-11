import dash_table
import dash_html_components as html

def printtitle(title):
    return html.H3(title, style = {'color': 'rgb(200, 200, 200)', 'font-family' : 'Verdana', 'text-align':'center'})


def pricetbl(table_id, df):
    return dash_table.DataTable(
        id = table_id,
        columns= [
          # {'name':'Sector', 'id': 'sector'}
          {'name':'Symbol', 'id': 'symbol'}
        , {'name':'LTP' , 'id': 'ltp'}
        , {'name':'%Change' , 'id': 'changepct'}
        # , {'name':'Vol', 'id':'volume'}
        # , {'name':'PriceLevel', 'id':'pricelevel'}
        # , {'name':'OHL', 'id':'ohl'}
        , {'name':'Qty' , 'id': 'qty'}
        , {'name':'SL-Buy' , 'id': 'slb'}
        , {'name':'SL-Sell' , 'id': 'sls'}
        ],
        # style_table={
        #     'width' : 380
        # },
        style_header={
              'backgroundColor': 'rgb(35, 35, 35)'
            , 'color': 'rgb(180, 180, 180)'
            , 'font-family' : 'Verdana'
            , 'font-size' : 12
            , 'fontWeight': 'bold'
            , 'height' : 2
        },
        style_cell={
            'backgroundColor': 'rgb(20, 20, 20)'
            , 'color': 'rgb(160, 160, 160)'
            , 'height' : 2
            , 'font-size' : 11
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
                # , 'color' : 'rgb(255,255,100)'
                , 'color' : 'dodgerblue'
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
                    'filter_query': '{ohl} = "OL"',
                    'column_id': ['symbol']
                }
                , 'backgroundColor': 'lightgreen'
                , 'color' : 'black'
            },
            {
                'if': {
                    'filter_query': '{ohl} = "OH"',
                    'column_id': ['symbol']
                }
                , 'backgroundColor': 'tomato'
                , 'color' : 'black'
            },
        ],
        style_as_list_view=True,
        data = df.to_dict('records'),
    )


def trendtbl(table_id, df):
    return dash_table.DataTable(
        id = table_id,
        columns= [
          {'name':'Sector', 'id': 'sector'}
        , {'name':'Symbol', 'id': 'symbol'}
        , {'name':'LTP' , 'id': 'ltp'}
        , {'name':'%Change' , 'id': 'changepct'}
        # , {'name':'Vol', 'id':'volume'}
        # , {'name':'PriceLevel', 'id':'pricelevel'}
        , {'name':'Qty' , 'id': 'qty'}
        , {'name':'SL-Buy' , 'id': 'slb'}
        , {'name':'SL-Sell' , 'id': 'sls'}
        ],
        # fixed_rows={'headers': True},
        # style_table={
        #     'width' : 500
        # },
        style_header={
              'backgroundColor': 'rgb(35, 35, 35)'
            , 'color': 'rgb(180, 180, 180)'
            , 'font-family' : 'Verdana'
            , 'font-size' : 12
            , 'fontWeight': 'bold'
            , 'height' : 2
        },
        style_cell={
            'backgroundColor': 'rgb(20, 20, 20)'
            , 'color': 'rgb(160, 160, 160)'
            , 'height' : 2
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
                # , 'color' : 'rgb(255,255,100)'
                , 'color' : 'dodgerblue'
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
                    'filter_query': '{ohl} = "OL"',
                    'column_id': ['symbol']
                }
                , 'backgroundColor': 'lightgreen'
                , 'color' : 'black'
            },
            {
                'if': {
                    'filter_query': '{ohl} = "OH"',
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
        # style_table={
        #     'width' : 300
        # },
        style_header={
              'backgroundColor': 'rgb(35, 35, 35)'
            , 'color': 'rgb(210, 210, 210)'
            , 'font-family' : 'Verdana'
            , 'font-size' : 12
            , 'fontWeight': 'bold'
            , 'height' : 4
        },
        style_cell={
            'backgroundColor': 'rgb(20, 20, 20)'
            , 'color': 'rgb(180, 180, 180)'
            , 'height' : 4
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
