import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from app import app
import time 



from dash.dependencies import Input, Output


random_y = np.random.randn(20000)
random_x = np.random.randn(20000)


layout = html.Div([
    html.H1('Home'),
    dcc.Graph(
        id='testgraph233',
        

    ),
    html.Button('button', id='but0', n_clicks=0),
    html.Div(children=[html.H2('Welcome!'),html.Br(),html.P('This platform serves as an initial concept, demonstrating basic preparation of data functionality.')], style={'textIndent':'15%'})
])


@app.callback(
    Output("testgraph233", 'figure'),
    [Input('but0', 'n_clicks')]
)
def return_graph(clicks):
    info = []
    if clicks != 0: 
        N = 20000
        info.append(
            go.Scatter(
                x = np.random.randn(N),
                y = np.random.randn(N),
                mode = 'lines',
                marker = dict(
                    line = dict(
                        width = 1,
                        color = 'DarkSlateGrey')
                )
            )
        )
    fig = go.Figure(data=info)

    return fig