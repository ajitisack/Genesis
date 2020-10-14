import dash_table
import dash_html_components as html

tab_style = {
      'padding': '8px'
    , 'backgroundColor': 'black'
    , 'color': 'rgb(200, 200, 200)'
    , 'border' : '0px'
    , 'font-size' : 14
    , 'font-family' : 'Verdana'
    , 'border': '1px solid rgb(40, 40, 40)'
}

tab_selected_style = {
      'padding': '8px'
    , 'backgroundColor': 'dodgerblue'
    , 'color': 'white'
    , 'border' : '0px'
    , 'font-size' : 14
    , 'font-family' : 'Verdana'
    , 'border': '1px solid rgb(40, 40, 40)'
}

def printtitle(title):
    return html.Div(title, style = {'color': 'rgb(200, 200, 200)', 'text-align':'center', 'font-family' : 'Verdana', 'font-weight' : '14', 'padding':'20px'})

def sectortitle(title):
    return html.Div(title, style = {'color': 'rgb(200, 200, 200)', 'text-align':'left', 'font-family' : 'Verdana', 'padding-top': '20px', 'font-weight' : '14'})


tbl_header_style = {
      'backgroundColor': 'rgb(35, 35, 35)'
    , 'color': 'rgb(180, 180, 180)'
    , 'font-family' : 'Verdana'
    , 'font-size' : 11
    , 'fontWeight': 'bold'
}

tbl_cell_style = {
    'backgroundColor': 'rgb(20, 20, 20)'
    , 'color': 'rgb(160, 160, 160)'
    , 'font-size' : 11
    , 'font-family' : 'Verdana'
    , 'border': '1px solid rgb(40, 40, 40)'
}

def pricetbl(table_id, df):
    cols = [
          {'name':'Symbol', 'id': 'symbol'}
        , {'name':'LTP' , 'id': 'ltp'}
        , {'name':'%Chng' , 'id': 'changepct'}
        , {'name':'Qty' , 'id': 'qty'}
        , {'name':'SL' , 'id': 'slb'}
    ]
    if table_id in ('up_tbl', 'down_tbl', 'nifty_up_tbl', 'nifty_down_tbl'):
        cols = [{'name':'Sector', 'id': 'sector'}] + cols

    return dash_table.DataTable(
        id = table_id,
        columns= cols,
        # fixed_rows={'headers': True},
        # style_table={
        #     'width' : 500
        # },
        style_header = tbl_header_style,
        style_cell = tbl_cell_style,
        style_cell_conditional=[
            {
                'if': {'column_id': ['sector', 'symbol', 'pricelevel']}
                , 'textAlign': 'left'
                , 'padding-left': 5
            },
            {
                'if': {'column_id': ['sector', 'symbol', 'ltp', 'changepct', 'volume']}
                , 'color' : 'lightgreen'
            },
            {
                'if': {'column_id': ['slb', 'sls', 'qty', 'changepct', 'ltp']},
                'textAlign': 'right',
                'padding-right': 10
            },
            {
                'if': {'column_id': ['qty']}
                , 'color' : 'dodgerblue'
            },
        ],
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{changepct} >= 0',
                    'column_id': ['sector', 'symbol', 'ltp', 'changepct', 'volume']
                }
                , 'color' : 'lightgreen'
            },
            {
                'if': {
                    'filter_query': '{changepct} < 0',
                    'column_id': ['sector', 'symbol', 'ltp', 'changepct', 'volume']
                }
                , 'color' : 'tomato'
            },
            {
                'if': {
                    'filter_query': '{ohl} = "OL"',
                    # 'filter_query': '{ltp} > {pdh}',
                    'column_id': ['symbol']
                }
                , 'backgroundColor': 'lightgreen'
                , 'color' : 'black'
            },
            {
                'if': {
                    'filter_query': '{ohl} = "OH"',
                    # 'filter_query': '{ltp} < {pdl}',
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
        , {'name':'%Chng' , 'id': 'changepct'}
        ],
        style_table={
            'width' : 200
        },
        style_header = tbl_header_style,
        style_cell = tbl_cell_style,
        style_cell_conditional=[
            {
                'if': {'column_id': ['symbol']}
                , 'textAlign': 'left'
                , 'padding-left': 10
            },
            {
                'if': {'column_id': ['changepct', 'ltp']}
                , 'textAlign': 'right'
                , 'padding-right': 10
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