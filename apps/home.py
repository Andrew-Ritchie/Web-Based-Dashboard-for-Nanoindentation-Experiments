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
    html.Button('button', id='but0', n_clicks=0),
    html.Div(children=[html.H2('Welcome!'),html.Br(),html.P('This platform serves as an initial concept, demonstrating basic preparation of data functionality.')], style={'textIndent':'15%'})
])

