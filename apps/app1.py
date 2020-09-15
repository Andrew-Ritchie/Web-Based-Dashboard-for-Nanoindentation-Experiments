import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output


layout = html.Div([
    html.H1('App 1'),
    dcc.Link('Go to App 2', href='/apps/app2'),
    dbc.Button("Primary", color="primary", className="mr-1")
])