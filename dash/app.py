import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from layout import printtitle, pricetbl, trendtbl, indicestbl
from data import getprice


def layout():
    body = dbc.Container([
          dbc.Row([
            dbc.Col(html.Div(pricetbl('nifty50_tbl', getprice()[2]), id='nifty50'), width=3),
            dbc.Col('', width=1),
            dbc.Col(html.Div(pricetbl('indices_tbl', getprice()[1]), id='indices'), width=3),
          ], justify="center")
        , dbc.Row([
            dbc.Col([printtitle('Banks'), html.Div(pricetbl('banks_tbl', getprice()[3]), id='banks')]),
            dbc.Col([printtitle('IT'), html.Div(pricetbl('it_tbl', getprice()[4]), id='it')]),
            dbc.Col([printtitle('Pharma'), html.Div(pricetbl('pharma_tbl', getprice()[6]), id='pharma')]),
          ], justify="center")
        , dbc.Row([
            dbc.Col([printtitle('Auto'), html.Div(pricetbl('auto_tbl', getprice()[5]), id='auto')], md=4),
            dbc.Col([printtitle('Metal'), html.Div(pricetbl('metal_tbl', getprice()[5]), id='metal')], md=4),
            dbc.Col([printtitle('Oil & Gas'), html.Div(pricetbl('oilgas_tbl', getprice()[6]), id='oilgas')], md=4)
          ], justify="center")
        # , dbc.Row([
        #     dbc.Col([printtitle('Metal'), html.Div(pricetbl('metal_tbl', getprice()[5]), id='metal')], width=6),
        #     dbc.Col([printtitle('Oil & Gas'), html.Div(pricetbl('oilgas_tbl', getprice()[6]), id='oilgas')], width=6),
        #   ])
        # , dbc.Row([
        #     dbc.Col([printtitle('Financial Services'), html.Div(pricetbl('finserv_tbl', getprice()[5]), id='finserv')], width=6),
        #     dbc.Col([printtitle('Others'), html.Div(pricetbl('others_tbl', getprice()[6]), id='others')], width=6),
        #   ])
        , dbc.Row([
            dbc.Col([printtitle('Above Open'), html.Div(trendtbl('up_tbl', getprice()[0]), id='uptrend')], width=5),
            dbc.Col('', width=1),
            dbc.Col([printtitle('Below Open'), html.Div(trendtbl('down_tbl', getprice()[0]), id='downtrend')], width=5)
          ], justify="center")
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
      Output('uptrend', 'children')
    , Output('downtrend', 'children')
    , Output('nifty50', 'children')
    , Output('indices', 'children')
    , Output('banks', 'children')
    , Output('it', 'children')
    , Output('auto', 'children')
    , Output('pharma', 'children')
    , Output('metal', 'children')
    , Output('oilgas', 'children')
    # , Output('finserv', 'children')
    # , Output('others', 'children')
], [Input('interval-component', 'n_intervals')])
def update_table(x):
    df, df_indices1, df_indices2, df_banks, df_it, df_auto, df_pharma, df_metal, df_oilgas, df_finserv, df_others = getprice()
    dfu = df[df.changepct >=0].sort_values(by='changepct', ascending=False)
    dfd = df[df.changepct < 0].sort_values(by='changepct', ascending=True)
    return trendtbl('up_tbl', dfu), trendtbl('down_tbl', dfd), indicestbl('nifty50_tbl', df_indices1), indicestbl('indices_tbl', df_indices2), pricetbl('banks_tbl', df_banks), pricetbl('it_tbl', df_it), pricetbl('auto_tbl', df_auto), pricetbl('pharma_tbl', df_pharma), pricetbl('metal_tbl', df_metal), pricetbl('oilgas_tbl', df_oilgas)#, pricetbl('finserv_tbl', df_finserv), pricetbl('others_tbl', df_others)


if __name__ == '__main__':
    app.run_server(debug=True)
