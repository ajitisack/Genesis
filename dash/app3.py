import stockdata as sd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()

app.layout = html.Div(children=[
    html.Div(children='''
        Symbol to graph:
    '''),
    dcc.Input(id='input', value='', type='text'),
    html.Div(id='output-graph'),
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)

def update_value(input_data):
    df = sd.getnsehistprice(input_data)
    plt = df.close.plot.area(template='plotly_white', title=f'NSE Chart', y='close')
    return dcc.Graph('example-graph', figure = plt)

if __name__ == '__main__':
    app.run_server(debug=True)
