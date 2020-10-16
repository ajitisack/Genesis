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
              dbc.Col([printtitle('Advances'), html.Div(pricetbl('nifty_adv_tbl', df['nifty_adv']), id='nifty_adv')], width=5)
            , dbc.Col([], width='auto')
            , dbc.Col([printtitle('Declines'), html.Div(pricetbl('nifty_dec_tbl', df['nifty_dec']), id='nifty_dec')], width=5)
            ], justify="center")
    ], style={'overflow-y' : 'scroll', 'height':'700px'}, fluid = True)


def fnosymbols():
    return dbc.Container([
          dbc.Row([
              dbc.Col([printtitle('Advances'), html.Div(pricetbl('fno_adv_tbl', df['fno_adv']), id='fno_adv')], width=5)
            , dbc.Col([], width='auto')
            , dbc.Col([printtitle('Declines'), html.Div(pricetbl('fno_dec_tbl', df['fno_dec']), id='fno_dec')], width=5)
            ], justify="center")
    ], style={'overflow-y' : 'scroll', 'height':'700px'}, fluid = True)


def sector_tbl(sector, adv_tbl, adv, dec_tbl, dec):
    return [
            dbc.Col(sectortitle(sector), width=1)
          , dbc.Col([html.Div(pricetbl(adv_tbl, pd.DataFrame()), style={'padding-top': '16px'}, id = adv)], width=4)
          , dbc.Col("", width=1)
          , dbc.Col([html.Div(pricetbl(dec_tbl, pd.DataFrame()), style={'padding-top': '16px'}, id = dec)], width=4)
          , dbc.Col("", width=2)
          ]

def n50sectors():
    return dbc.Container([
              dbc.Row(sector_tbl('Banks', 'n50_bank_adv_tbl', 'n50_bank_adv', 'n50_bank_dec_tbl', 'n50_bank_dec'), justify = 'center')
            , dbc.Row(sector_tbl('IT', 'n50_it_adv_tbl', 'n50_it_adv', 'n50_it_dec_tbl', 'n50_it_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Pharma', 'n50_pharma_adv_tbl', 'n50_pharma_adv', 'n50_pharma_dec_tbl', 'n50_pharma_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Auto', 'n50_auto_adv_tbl', 'n50_auto_adv', 'n50_auto_dec_tbl', 'n50_auto_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Auto Ancillaries', 'n50_autoanc_adv_tbl', 'n50_autoanc_adv', 'n50_autoanc_dec_tbl', 'n50_autoanc_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Metal', 'n50_metal_adv_tbl', 'n50_metal_adv', 'n50_metal_dec_tbl', 'n50_metal_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Oil & Gas', 'n50_oilgas_adv_tbl', 'n50_oilgas_adv', 'n50_oilgas_dec_tbl', 'n50_oilgas_dec'), justify = 'center')
            , dbc.Row(sector_tbl('FinServ', 'n50_finserv_adv_tbl', 'n50_finserv_adv', 'n50_finserv_dec_tbl', 'n50_finserv_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Power', 'n50_power_adv_tbl', 'n50_power_adv', 'n50_power_dec_tbl', 'n50_power_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Media', 'n50_media_adv_tbl', 'n50_media_adv', 'n50_media_dec_tbl', 'n50_media_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Chemicals', 'n50_chemi_adv_tbl', 'n50_chemi_adv', 'n50_chemi_dec_tbl', 'n50_chemi_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Cement', 'n50_cement_adv_tbl', 'n50_cement_adv', 'n50_cement_dec_tbl', 'n50_cement_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Telecom', 'n50_telecom_adv_tbl', 'n50_telecom_adv', 'n50_telecom_dec_tbl', 'n50_telecom_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Transportation', 'n50_trans_adv_tbl', 'n50_trans_adv', 'n50_trans_dec_tbl', 'n50_trans_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Realty', 'n50_realty_adv_tbl', 'n50_realty_adv', 'n50_realty_dec_tbl', 'n50_realty_dec'), justify = 'center')
            , dbc.Row(sector_tbl('FMCG', 'n50_fmcg_adv_tbl', 'n50_fmcg_adv', 'n50_fmcg_dec_tbl', 'n50_fmcg_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Cons. Durables', 'n50_consdur_adv_tbl', 'n50_consdur_adv', 'n50_consdur_dec_tbl', 'n50_consdur_dec'), justify = 'center')

    ], style={'overflow-y' : 'scroll', 'height':'700px'}, fluid = True)

def fnosectors():
    return dbc.Container([
              dbc.Row(sector_tbl('Banks', 'fno_bank_adv_tbl', 'fno_bank_adv', 'fno_bank_dec_tbl', 'fno_bank_dec'), justify = 'center')
            , dbc.Row(sector_tbl('IT', 'fno_it_adv_tbl', 'fno_it_adv', 'fno_it_dec_tbl', 'fno_it_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Pharma', 'fno_pharma_adv_tbl', 'fno_pharma_adv', 'fno_pharma_dec_tbl', 'fno_pharma_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Auto', 'fno_auto_adv_tbl', 'fno_auto_adv', 'fno_auto_dec_tbl', 'fno_auto_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Auto Ancillaries', 'fno_autoanc_adv_tbl', 'fno_autoanc_adv', 'fno_autoanc_dec_tbl', 'fno_autoanc_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Metal', 'fno_metal_adv_tbl', 'fno_metal_adv', 'fno_metal_dec_tbl', 'fno_metal_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Oil & Gas', 'fno_oilgas_adv_tbl', 'fno_oilgas_adv', 'fno_oilgas_dec_tbl', 'fno_oilgas_dec'), justify = 'center')
            , dbc.Row(sector_tbl('FinServ', 'fno_finserv_adv_tbl', 'fno_finserv_adv', 'fno_finserv_dec_tbl', 'fno_finserv_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Power', 'fno_power_adv_tbl', 'fno_power_adv', 'fno_power_dec_tbl', 'fno_power_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Media', 'fno_media_adv_tbl', 'fno_media_adv', 'fno_media_dec_tbl', 'fno_media_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Chemicals', 'fno_chemi_adv_tbl', 'fno_chemi_adv', 'fno_chemi_dec_tbl', 'fno_chemi_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Cement', 'fno_cement_adv_tbl', 'fno_cement_adv', 'fno_cement_dec_tbl', 'fno_cement_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Telecom', 'fno_telecom_adv_tbl', 'fno_telecom_adv', 'fno_telecom_dec_tbl', 'fno_telecom_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Transportation', 'fno_trans_adv_tbl', 'fno_trans_adv', 'fno_trans_dec_tbl', 'fno_trans_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Realty', 'fno_realty_adv_tbl', 'fno_realty_adv', 'fno_realty_dec_tbl', 'fno_realty_dec'), justify = 'center')
            , dbc.Row(sector_tbl('FMCG', 'fno_fmcg_adv_tbl', 'fno_fmcg_adv', 'fno_fmcg_dec_tbl', 'fno_fmcg_dec'), justify = 'center')
            , dbc.Row(sector_tbl('Cons. Durables', 'fno_consdur_adv_tbl', 'fno_consdur_adv', 'fno_consdur_dec_tbl', 'fno_consdur_dec'), justify = 'center')

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
                            dcc.Tab(label='Nifty 50', style=tab_style, selected_style=tab_selected_style, children = [nifty50symbols()])
                          , dcc.Tab(label='FNO', style=tab_style, selected_style=tab_selected_style, children = [fnosymbols()])
                          , dcc.Tab(label='Nifty 50 - By Sector', style=tab_style, selected_style=tab_selected_style, children = [n50sectors()])
                          , dcc.Tab(label='FNO - By Sector', style=tab_style, selected_style=tab_selected_style,  children = [fnosectors()])
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
    , Output('fno_adv', 'children')
    , Output('fno_dec', 'children')

    , Output('n50_bank_adv', 'children')
    , Output('n50_it_adv', 'children')
    , Output('n50_pharma_adv', 'children')
    , Output('n50_auto_adv', 'children')
    , Output('n50_autoanc_adv', 'children')
    , Output('n50_metal_adv', 'children')
    , Output('n50_oilgas_adv', 'children')
    , Output('n50_finserv_adv', 'children')
    , Output('n50_power_adv', 'children')
    , Output('n50_media_adv', 'children')
    , Output('n50_chemi_adv', 'children')
    , Output('n50_cement_adv', 'children')
    , Output('n50_telecom_adv', 'children')
    , Output('n50_trans_adv', 'children')
    , Output('n50_realty_adv', 'children')
    , Output('n50_fmcg_adv', 'children')
    , Output('n50_consdur_adv', 'children')

    , Output('n50_bank_dec', 'children')
    , Output('n50_it_dec', 'children')
    , Output('n50_pharma_dec', 'children')
    , Output('n50_auto_dec', 'children')
    , Output('n50_autoanc_dec', 'children')
    , Output('n50_metal_dec', 'children')
    , Output('n50_oilgas_dec', 'children')
    , Output('n50_finserv_dec', 'children')
    , Output('n50_power_dec', 'children')
    , Output('n50_media_dec', 'children')
    , Output('n50_chemi_dec', 'children')
    , Output('n50_cement_dec', 'children')
    , Output('n50_telecom_dec', 'children')
    , Output('n50_trans_dec', 'children')
    , Output('n50_realty_dec', 'children')
    , Output('n50_fmcg_dec', 'children')
    , Output('n50_consdur_dec', 'children')

    , Output('fno_bank_adv', 'children')
    , Output('fno_it_adv', 'children')
    , Output('fno_pharma_adv', 'children')
    , Output('fno_auto_adv', 'children')
    , Output('fno_autoanc_adv', 'children')
    , Output('fno_metal_adv', 'children')
    , Output('fno_oilgas_adv', 'children')
    , Output('fno_finserv_adv', 'children')
    , Output('fno_power_adv', 'children')
    , Output('fno_media_adv', 'children')
    , Output('fno_chemi_adv', 'children')
    , Output('fno_cement_adv', 'children')
    , Output('fno_telecom_adv', 'children')
    , Output('fno_trans_adv', 'children')
    , Output('fno_realty_adv', 'children')
    , Output('fno_fmcg_adv', 'children')
    , Output('fno_consdur_adv', 'children')

    , Output('fno_bank_dec', 'children')
    , Output('fno_it_dec', 'children')
    , Output('fno_pharma_dec', 'children')
    , Output('fno_auto_dec', 'children')
    , Output('fno_autoanc_dec', 'children')
    , Output('fno_metal_dec', 'children')
    , Output('fno_oilgas_dec', 'children')
    , Output('fno_finserv_dec', 'children')
    , Output('fno_power_dec', 'children')
    , Output('fno_media_dec', 'children')
    , Output('fno_chemi_dec', 'children')
    , Output('fno_cement_dec', 'children')
    , Output('fno_telecom_dec', 'children')
    , Output('fno_trans_dec', 'children')
    , Output('fno_realty_dec', 'children')
    , Output('fno_fmcg_dec', 'children')
    , Output('fno_consdur_dec', 'children')

], [Input('interval-component', 'n_intervals')])
def update_table(x):
    df = getprice()
    return_list = [
          indicestbl('nifty50_tbl', df['nifty50'])
        , indicestbl('indices_adv_tbl', df['indices_adv'])
        , indicestbl('indices_dec_tbl', df['indices_dec'])
        , pricetbl('nifty_adv_tbl', df['nifty_adv'])
        , pricetbl('nifty_dec_tbl', df['nifty_dec'])
        , pricetbl('fno_adv_tbl', df['fno_adv'])
        , pricetbl('fno_dec_tbl', df['fno_dec'])

        , pricetbl('n50_bank_adv_tbl', df['bank']['n50']['adv'])
        , pricetbl('n50_it_adv_tbl', df['it']['n50']['adv'])
        , pricetbl('n50_pharma_adv_tbl', df['pharma']['n50']['adv'])
        , pricetbl('n50_auto_adv_tbl', df['auto']['n50']['adv'])
        , pricetbl('n50_autoanc_adv_tbl', df['autoanc']['n50']['adv'])
        , pricetbl('n50_metal_adv_tbl', df['metal']['n50']['adv'])
        , pricetbl('n50_oilgas_adv_tbl', df['oilgas']['n50']['adv'])
        , pricetbl('n50_finserv_adv_tbl', df['finserv']['n50']['adv'])
        , pricetbl('n50_power_adv_tbl', df['power']['n50']['adv'])
        , pricetbl('n50_media_adv_tbl', df['media']['n50']['adv'])
        , pricetbl('n50_chemi_adv_tbl', df['chemi']['n50']['adv'])
        , pricetbl('n50_cement_adv_tbl', df['cement']['n50']['adv'])
        , pricetbl('n50_telecom_adv_tbl', df['telecom']['n50']['adv'])
        , pricetbl('n50_trans_adv_tbl', df['trans']['n50']['adv'])
        , pricetbl('n50_realty_adv_tbl', df['realty']['n50']['adv'])
        , pricetbl('n50_fmcg_adv_tbl', df['fmcg']['n50']['adv'])
        , pricetbl('n50_consdur_adv_tbl', df['consdur']['n50']['adv'])

        , pricetbl('n50_bank_dec_tbl', df['bank']['n50']['dec'])
        , pricetbl('n50_it_dec_tbl', df['it']['n50']['dec'])
        , pricetbl('n50_pharma_dec_tbl', df['pharma']['n50']['dec'])
        , pricetbl('n50_auto_dec_tbl', df['auto']['n50']['dec'])
        , pricetbl('n50_autoanc_dec_tbl', df['autoanc']['n50']['dec'])
        , pricetbl('n50_metal_dec_tbl', df['metal']['n50']['dec'])
        , pricetbl('n50_oilgas_dec_tbl', df['oilgas']['n50']['dec'])
        , pricetbl('n50_finserv_dec_tbl', df['finserv']['n50']['dec'])
        , pricetbl('n50_power_dec_tbl', df['power']['n50']['dec'])
        , pricetbl('n50_media_dec_tbl', df['media']['n50']['dec'])
        , pricetbl('n50_chemi_dec_tbl', df['chemi']['n50']['dec'])
        , pricetbl('n50_cement_dec_tbl', df['cement']['n50']['dec'])
        , pricetbl('n50_telecom_dec_tbl', df['telecom']['n50']['dec'])
        , pricetbl('n50_trans_dec_tbl', df['trans']['n50']['dec'])
        , pricetbl('n50_realty_dec_tbl', df['realty']['n50']['dec'])
        , pricetbl('n50_fmcg_dec_tbl', df['fmcg']['n50']['dec'])
        , pricetbl('n50_consdur_dec_tbl', df['consdur']['n50']['dec'])


        , pricetbl('fno_bank_adv_tbl', df['bank']['fno']['adv'])
        , pricetbl('fno_it_adv_tbl', df['it']['fno']['adv'])
        , pricetbl('fno_pharma_adv_tbl', df['pharma']['fno']['adv'])
        , pricetbl('fno_auto_adv_tbl', df['auto']['fno']['adv'])
        , pricetbl('fno_autoanc_adv_tbl', df['autoanc']['fno']['adv'])
        , pricetbl('fno_metal_adv_tbl', df['metal']['fno']['adv'])
        , pricetbl('fno_oilgas_adv_tbl', df['oilgas']['fno']['adv'])
        , pricetbl('fno_finserv_adv_tbl', df['finserv']['fno']['adv'])
        , pricetbl('fno_power_adv_tbl', df['power']['fno']['adv'])
        , pricetbl('fno_media_adv_tbl', df['media']['fno']['adv'])
        , pricetbl('fno_chemi_adv_tbl', df['chemi']['fno']['adv'])
        , pricetbl('fno_cement_adv_tbl', df['cement']['fno']['adv'])
        , pricetbl('fno_telecom_adv_tbl', df['telecom']['fno']['adv'])
        , pricetbl('fno_trans_adv_tbl', df['trans']['fno']['adv'])
        , pricetbl('fno_realty_adv_tbl', df['realty']['fno']['adv'])
        , pricetbl('fno_fmcg_adv_tbl', df['fmcg']['fno']['adv'])
        , pricetbl('fno_consdur_adv_tbl', df['consdur']['fno']['adv'])


        , pricetbl('fno_bank_dec_tbl', df['bank']['fno']['dec'])
        , pricetbl('fno_it_dec_tbl', df['it']['fno']['dec'])
        , pricetbl('fno_pharma_dec_tbl', df['pharma']['fno']['dec'])
        , pricetbl('fno_auto_dec_tbl', df['auto']['fno']['dec'])
        , pricetbl('fno_autoanc_dec_tbl', df['autoanc']['fno']['dec'])
        , pricetbl('fno_metal_dec_tbl', df['metal']['fno']['dec'])
        , pricetbl('fno_oilgas_dec_tbl', df['oilgas']['fno']['dec'])
        , pricetbl('fno_finserv_dec_tbl', df['finserv']['fno']['dec'])
        , pricetbl('fno_power_dec_tbl', df['power']['fno']['dec'])
        , pricetbl('fno_media_dec_tbl', df['media']['fno']['dec'])
        , pricetbl('fno_chemi_dec_tbl', df['chemi']['fno']['dec'])
        , pricetbl('fno_cement_dec_tbl', df['cement']['fno']['dec'])
        , pricetbl('fno_telecom_dec_tbl', df['telecom']['fno']['dec'])
        , pricetbl('fno_trans_dec_tbl', df['trans']['fno']['dec'])
        , pricetbl('fno_realty_dec_tbl', df['realty']['fno']['dec'])
        , pricetbl('fno_fmcg_dec_tbl', df['fmcg']['fno']['dec'])
        , pricetbl('fno_consdur_dec_tbl', df['consdur']['fno']['dec'])

    ]
    return return_list


if __name__ == '__main__':
    app.run_server(debug=True)
