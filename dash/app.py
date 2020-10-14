import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from layout import printtitle, sectortitle, indicestbl, pricetbl, tab_style, tab_selected_style
from data import getprice
import pandas as pd


def nifty50symbols():
    return dbc.Container([
          dbc.Row([
              dbc.Col([printtitle('Above Open'), html.Div(pricetbl('nifty_up_tbl', getprice()[0]), id='nifty_up')], width=5)
            , dbc.Col([], width='auto')
            , dbc.Col([printtitle('Below Open'), html.Div(pricetbl('nifty_down_tbl', getprice()[0]), id='nifty_down')], width=5)
            ], justify="center")
    ], style={'overflow-y' : 'scroll', 'height':'700px'}, fluid = True)


def fnosymbols():
    return dbc.Container([
          dbc.Row([
              dbc.Col([printtitle('Above Open'), html.Div(pricetbl('up_tbl', getprice()[0]), id='uptrend')], width=5)
            , dbc.Col([], width='auto')
            , dbc.Col([printtitle('Below Open'), html.Div(pricetbl('down_tbl', getprice()[0]), id='downtrend')], width=5)
            ], justify="center")
    ], style={'overflow-y' : 'scroll', 'height':'700px'}, fluid = True)

def sector_tbl(sector, up_table_id, up_id, down_table_id, down_id):
    return [
            dbc.Col(sectortitle(sector), width=1)
          , dbc.Col([html.Div(pricetbl(up_table_id, pd.DataFrame()), style={'padding-top': '16px'}, id = up_id)], width=4)
          , dbc.Col("", width=1)
          , dbc.Col([html.Div(pricetbl(down_table_id, pd.DataFrame()), style={'padding-top': '16px'}, id = down_id)], width=4)
          , dbc.Col("", width=2)
          ]

def sectors():
    return dbc.Container([
            dbc.Row(sector_tbl('Banks', 'banks_tbl_up', 'banks_up', 'banks_tbl_down', 'banks_down'), justify="center")
          , dbc.Row(sector_tbl('IT', 'it_tbl_up', 'it_up', 'it_tbl_down', 'it_down'), justify="center")
          , dbc.Row(sector_tbl('Pharma', 'pharma_tbl_up', 'pharma_up', 'pharma_tbl_down', 'pharma_down'), justify="center")
          , dbc.Row(sector_tbl('Auto', 'auto_tbl_up', 'auto_up', 'auto_tbl_down', 'auto_down'), justify="center")
    ], style={'overflow-y' : 'scroll', 'height':'700px'}, fluid = True)


def layout():
    body = dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.Br()
                      , html.Br()
                      , printtitle('Nifty Indices')
                      , html.Div(indicestbl('nifty50_tbl', getprice()[2]), id='nifty50')
                      , html.Br()
                      , html.Br()
                      , html.Div(indicestbl('indices_tbl', getprice()[1]), id='indices')]
                      , width='auto')
                  , dbc.Col([
                        dcc.Tabs([
                            dcc.Tab(label='Pre-Open Nifty 50', style=tab_style, selected_style=tab_selected_style, children = [])
                          , dcc.Tab(label='Pre-Open FNO', style=tab_style, selected_style=tab_selected_style, children = [])
                          , dcc.Tab(label='Nifty 50', style=tab_style, selected_style=tab_selected_style, children = [html.Div(nifty50symbols())])
                          , dcc.Tab(label='Nifty 50 - By Sector', style=tab_style, selected_style=tab_selected_style, children = [])
                          , dcc.Tab(label='FNO', style=tab_style, selected_style=tab_selected_style, children = [html.Div(fnosymbols())])
                          , dcc.Tab(label='FNO - By Sector', style=tab_style, selected_style=tab_selected_style,  children = [html.Div(sectors())])
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
      Output('uptrend', 'children')
    , Output('downtrend', 'children')
    , Output('nifty50', 'children')
    , Output('indices', 'children')
    , Output('nifty_up', 'children')
    , Output('nifty_down', 'children')
    , Output('banks_up', 'children')
    , Output('banks_down', 'children')
    , Output('it_up', 'children')
    , Output('it_down', 'children')
    , Output('auto_up', 'children')
    , Output('auto_down', 'children')
    , Output('pharma_up', 'children')
    , Output('pharma_down', 'children')
], [Input('interval-component', 'n_intervals')])
def update_table(x):
    df, df_indices1, df_indices2, df_niftysymbols, df_banks, df_it, df_auto, df_pharma, df_metal, df_oilgas, df_finserv, df_telecom, df_trans, df_cement, df_chemic, df_media, df_power = getprice()
    dfu = df[df.changepct >=0].sort_values(by='changepct', ascending=False)
    dfd = df[df.changepct < 0].sort_values(by='changepct', ascending=True)
    df_nifty_up   = df_niftysymbols[df_niftysymbols.changepct >=0].sort_values(by='changepct', ascending=False)
    df_nifty_down = df_niftysymbols[df_niftysymbols.changepct < 0].sort_values(by='changepct', ascending=True)
    df_banks_up   = df_banks[df_banks.changepct >=0].sort_values(by='changepct', ascending=False)
    df_banks_down = df_banks[df_banks.changepct < 0].sort_values(by='changepct', ascending=True)
    df_it_up      = df_it[df_it.changepct >=0].sort_values(by='changepct', ascending=False)
    df_it_down    = df_it[df_it.changepct < 0].sort_values(by='changepct', ascending=True)
    df_auto_up    = df_auto[df_auto.changepct >=0].sort_values(by='changepct', ascending=False)
    df_auto_down  = df_auto[df_auto.changepct < 0].sort_values(by='changepct', ascending=True)
    df_pharma_up    = df_pharma[df_pharma.changepct >=0].sort_values(by='changepct', ascending=False)
    df_pharma_down  = df_pharma[df_pharma.changepct < 0].sort_values(by='changepct', ascending=True)
    return_list = \
      pricetbl('up_tbl', dfu) \
    , pricetbl('down_tbl', dfd) \
    , indicestbl('nifty50_tbl', df_indices1) \
    , indicestbl('indices_tbl', df_indices2) \
    , pricetbl('nifty_up_tbl', df_nifty_up) \
    , pricetbl('nifty_down_tbl', df_nifty_down) \
    , pricetbl('banks_tbl_up', df_banks_up) \
    , pricetbl('banks_tbl_down', df_banks_down) \
    , pricetbl('it_tbl_up', df_it_up) \
    , pricetbl('it_tbl_down', df_it_down) \
    , pricetbl('auto_tbl_up', df_auto_up) \
    , pricetbl('auto_tbl_down', df_auto_down) \
    , pricetbl('pharma_tbl_up', df_pharma_up) \
    , pricetbl('pharma_tbl_down', df_pharma_down)
    return return_list


if __name__ == '__main__':
    app.run_server(debug=True)
