import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


layout = html.Div([
    html.H1('App2'),
    dcc.Link('Go to App 1', href='/apps/app1')
])