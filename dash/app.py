import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from layout import printtitle, sectortitle, indicestbl, tab_style, tab_selected_style
from layout import sectortbl, indicestbl, pricetbl, valuetbl
from data import getprice
import pandas as pd

df = getprice()

def n50symbols():
    return dbc.Container([
          dbc.Row([
              dbc.Col([printtitle('Gainers'), html.Div(pricetbl('nifty_adv_tbl', df['nifty_adv']), id='nifty_adv')], width='auto')
            , dbc.Col([], width = 'auto')
            , dbc.Col([printtitle('Losers'), html.Div(pricetbl('nifty_dec_tbl', df['nifty_dec']), id='nifty_dec')], width='auto')
            ], justify="center")
    ], style={'overflow-y' : 'scroll', 'height':'700px'}, fluid = True)


def n50pdhl():
    return dbc.Container([
          dbc.Row([
              dbc.Col([printtitle('Gainers'), html.Div(pricetbl('above_pdh_tbl', df['above_pdh']), id='above_pdh')], width='auto')
            , dbc.Col([], width = 2)
            , dbc.Col([printtitle('Losers'), html.Div(pricetbl('below_pdl_tbl', df['below_pdl']), id='below_pdl')], width='auto')
            ], justify="center")
    ], style={'overflow-y' : 'scroll', 'height':'700px'}, fluid = True)


def n50totalvalue():
    return dbc.Container([
          dbc.Row([
              dbc.Col([printtitle('By Total Value'), html.Div(valuetbl('nifty_active_tbl', df['active']), id='nifty_active')], width='auto')
            ], justify="center")
    ], style={'overflow-y' : 'scroll', 'height':'700px'}, fluid = True)


def sector_tbl(sector, tbl, tbl_id):
    return dbc.Col([sectortitle(sector), html.Div(sectortbl(tbl, pd.DataFrame()), style={'padding-top': '16px'}, id = tbl_id)], width=3)


def n50sectors():
    return dbc.Container([
              dbc.Row([
                  sector_tbl('Banks', 'n50_bank_tbl', 'n50_bank')
                , dbc.Col(width=1)
                , sector_tbl('FinServ', 'n50_finser_tbl', 'n50_finserv')
                , dbc.Col(width=1)
                , sector_tbl('Auto', 'n50_auto_tbl', 'n50_auto')
              ], justify = 'center'),
              dbc.Row([
                  sector_tbl('IT', 'n50_it_tbl', 'n50_it')
                , dbc.Col(width=1)
                , sector_tbl('Pharma', 'n50_pharma_tbl', 'n50_pharma')
                , dbc.Col(width=1)
                , sector_tbl('Metal', 'n50_metal_tbl', 'n50_metal')
              ], justify = 'center'),
              dbc.Row([
                  sector_tbl('Energy', 'n50_energy_tbl', 'n50_energy')
                , dbc.Col(width=1)
                , sector_tbl('Chemicals', 'n50_chemi_tbl', 'n50_chemi')
                , dbc.Col(width=1)
                , sector_tbl('Others', 'n50_others_tbl', 'n50_others')
              ], justify = 'center'),
    ], style={'overflow-y' : 'scroll', 'height':'700px'}, fluid = True)

df = getprice()

def indices_section():
    return [
        html.Br()
      , html.Br()
      , printtitle('Nifty Indices')
      , html.Div(indicestbl('nifty50_tbl', df['nifty50']), id='nifty50')
      , html.Br()
      , html.Br()
      , html.Div(indicestbl('indices_adv_tbl', df['indices_adv']), id='indices_adv')
      , html.Br()
      , html.Br()
      , html.Div(indicestbl('indices_dec_tbl', df['indices_dec']), id='indices_dec')
    ]


def layout():
    body = dbc.Container([
                dbc.Row([
                    dbc.Col(indices_section(), width='auto')
                  , dbc.Col([
                        dcc.Tabs([
                            dcc.Tab(label='Nifty 50 By Sectors', style=tab_style, selected_style=tab_selected_style, children = [n50sectors()])
                          , dcc.Tab(label='Nifty 50 - Gainers & Loosers', style=tab_style, selected_style=tab_selected_style, children = [n50symbols()])
                          , dcc.Tab(label='Nifty 50 - Prev Day Range', style=tab_style, selected_style=tab_selected_style, children = [n50pdhl()])
                          , dcc.Tab(label='Nifty 50 - By Total Value', style=tab_style, selected_style=tab_selected_style, children = [n50totalvalue()])
                          ])
                    ], width='10')
                  , dcc.Interval(
                              id = 'interval-component',
                              interval = 1 * 1000, # in milliseconds ie, 1 x 1000 means 1 sec
                              n_intervals = 0
                  )
                  ], justify="center")
          ], fluid = True)
    return html.Div(body)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID])
app.layout = layout


@app.callback([
      Output('nifty50', 'children')
    , Output('indices_adv', 'children')
    , Output('indices_dec', 'children')

    , Output('nifty_adv', 'children')
    , Output('nifty_dec', 'children')
    , Output('nifty_active', 'children')

    , Output('above_pdh', 'children')
    , Output('below_pdl', 'children')

    , Output('n50_bank', 'children')
    , Output('n50_finserv', 'children')
    , Output('n50_auto', 'children')
    , Output('n50_it', 'children')
    , Output('n50_pharma', 'children')
    , Output('n50_metal', 'children')
    , Output('n50_energy', 'children')
    , Output('n50_chemi', 'children')
    , Output('n50_others', 'children')

], [Input('interval-component', 'n_intervals')])
def update_table(x):
    df = getprice()
    return_list = [
          indicestbl('nifty50_tbl', df['nifty50'])
        , indicestbl('indices_adv_tbl', df['indices_adv'])
        , indicestbl('indices_dec_tbl', df['indices_dec'])

        , pricetbl('nifty_adv_tbl', df['nifty_adv'])
        , pricetbl('nifty_dec_tbl', df['nifty_dec'])
        , valuetbl('nifty_active_tbl', df['active'])

        , sectortbl('above_pdh_tbl', df['above_pdh'])
        , sectortbl('below_pdl_tbl', df['below_pdl'])

        , sectortbl('n50_bank_tbl', df['bank'])
        , sectortbl('n50_finser_tbl', df['finserv'])
        , sectortbl('n50_auto_tbl', df['auto'])
        , sectortbl('n50_it_tbl', df['it'])
        , sectortbl('n50_pharma_tbl', df['pharma'])
        , sectortbl('n50_metal_tbl', df['metal'])
        , sectortbl('n50_energy_tbl', df['energy'])
        , sectortbl('n50_chemi_tbl', df['chemi'])
        , sectortbl('n50_others_tbl', df['others'])
    ]
    return return_list


if __name__ == '__main__':
    app.run_server(debug=True)
