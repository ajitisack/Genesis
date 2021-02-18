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


conditional_cell_style = [
    {
        'if': {'column_id': ['sector', 'symbol', 'pricelevel']}
        , 'textAlign': 'left'
        , 'padding-left': 6
    },
    {
        'if': {'column_id': ['sl', 'qty', 'changepct', 'ltp', 'r2r', 'value', 'gappct']}
        , 'textAlign': 'right'
        , 'padding-right': 8
    },
    {
        'if': {'column_id': ['qty', 'r2r']}
        , 'color' : 'dodgerblue'
    },
]

conditional_data_style = [
    {
        'if': {
            'filter_query': '{changepct} >= 0',
            'column_id': ['sector', 'symbol', 'ltp', 'changepct']
        }
        , 'color' : 'lightgreen'
    },
    {
        'if': {
            'filter_query': '{changepct} < 0',
            'column_id': ['sector', 'symbol', 'ltp', 'changepct']
        }
        , 'color' : 'tomato'
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
]

def printtitle(title):
    return html.Div(title, style = {'color': 'rgb(200, 200, 200)', 'text-align':'center', 'font-family' : 'Verdana', 'font-weight' : '12', 'padding':'20px'})


def sectortitle(title):
    return html.Div(title, style = {'color': 'rgb(200, 200, 200)', 'text-align':'center', 'font-family' : 'Verdana', 'font-weight' : '12', 'padding-top': '10px', 'padding-left':'10px'})


def sectortbl(table_id, df):
    cols = [
            {'name':'Symbol', 'id': 'symbol'}
          , {'name':'LTP' , 'id': 'ltp'}
          , {'name':'%Chng' , 'id': 'changepct'}
          , {'name':'Qty' , 'id': 'qty'}
          , {'name':'R2R' , 'id': 'r2r'}
    ]
    return dash_table.DataTable(
          id = table_id
        , columns = cols
        , style_table = {'width' : 280}
        , style_header = tbl_header_style
        , style_cell = tbl_cell_style
        , style_cell_conditional = conditional_cell_style
        , style_data_conditional = conditional_data_style
        , style_as_list_view = True
        , data = df.to_dict('records')
    )


def pricetbl(table_id, df):
    cols = [
          {'name':'Sector', 'id': 'sector'}
        , {'name':'Symbol', 'id': 'symbol'}
        , {'name':'LTP' , 'id': 'ltp'}
        , {'name':'%Chng' , 'id': 'changepct'}
        , {'name':'%Gap' , 'id': 'gappct'}
        , {'name':'Qty' , 'id': 'qty'}
        , {'name':'R2R' , 'id': 'r2r'}
    ]
    return dash_table.DataTable(
          id = table_id
        , columns = cols
        , style_table = {'width' : 500}
        , style_header = tbl_header_style
        , style_cell = tbl_cell_style
        , style_cell_conditional = conditional_cell_style
        , style_data_conditional = conditional_data_style
        , style_as_list_view=True
        , data = df.to_dict('records')
    )


def valuetbl(table_id, df):
    cols = [
          {'name':'Sector', 'id': 'sector'}
        , {'name':'Symbol', 'id': 'symbol'}
        , {'name':'LTP' , 'id': 'ltp'}
        , {'name':'%Chng' , 'id': 'changepct'}
        , {'name':'%Gap' , 'id': 'gappct'}
        , {'name':'Qty' , 'id': 'qty'}
        , {'name':'R2R' , 'id': 'r2r'}
        , {'name':'Value' , 'id': 'value'}
    ]
    return dash_table.DataTable(
          id = table_id
        , columns = cols
        , style_table = {'width' : 700}
        , style_header = tbl_header_style
        , style_cell = tbl_cell_style
        , style_cell_conditional = conditional_cell_style
        , style_data_conditional = conditional_data_style
        , style_as_list_view=True
        , data = df.to_dict('records')
    )


def indicestbl(table_id, df):
    cols = [
          {'name':'Index', 'id': 'symbol'}
        , {'name':'LTP' , 'id': 'ltp'}
        , {'name':'%Chng' , 'id': 'changepct'}
    ]
    return dash_table.DataTable(
          id = table_id
        , columns = cols
        , style_table = {'width' : 200}
        , style_header = tbl_header_style
        , style_cell = tbl_cell_style
        , style_cell_conditional = conditional_cell_style
        , style_data_conditional = conditional_data_style
        , style_as_list_view=True
        , data = df.to_dict('records'),
    )
