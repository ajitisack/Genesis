import stockdata as sd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

prods = ['Aaaa', 'Bbbb', 'Cccc', 'Dddd', 'Eeee', 'Ffff']
vals = [-1.2, 2.3, 4.5, -2.5, 3.2, -0.5]
font_color = ['rgb(40,40,40)', ['rgb(255,0,0)' if v <= 0 else 'rgb(10,10,10)' for v in vals]]

table_trace = go.Table(
                 columnwidth= [15]+[15],
                 columnorder=[0, 1],
                 header = dict(height = 50,
                               values = [['<b>Product</b>'], ['<b>Quantity</b>']],
                               line = dict(color='rgb(50,50,50)'),
                               align = ['left']*2,
                               font = dict(color=['rgb(45,45,45)']*2, size=14),

                              ),
                 cells = dict(values = [prods, vals],
                              line = dict(color='#506784'),
                              align = ['left']*5,

                              font = dict(family="Arial", size=14, color=font_color),
                              format = [None, ",.2f"],

                              height = 30,
                              fill = dict(color='rgb(245,245,245)'))
                             )


layout = go.Layout(width=400, height=415, autosize=False,
              title_text='Table title',
                   title_x=0.5, showlegend=False)
fig = go.Figure(data=[table_trace], layout=layout)

app = dash.Dash()

app.layout = html.Div(children=[
    html.Div(children='''
        Symbol to graph:
    '''),
    dcc.Graph('example-graph', figure = fig),
])

if __name__ == '__main__':
    app.run_server(debug=True)
