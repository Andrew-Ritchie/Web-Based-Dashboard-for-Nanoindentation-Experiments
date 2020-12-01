import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output


layout = html.Div([
    html.H1('Home'),
    html.Div(children=[html.H2('Welcome!'),html.Br(),html.P('This platform serves as an initial concept, demonstrating basic preparation of data functionality.')], style={'textIndent':'15%'})
])