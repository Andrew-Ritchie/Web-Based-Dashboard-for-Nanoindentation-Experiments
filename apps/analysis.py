import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import json
import plotly.express as px
import os
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from app import app
from apps.kaggle2 import get_datasets

from apps.prepare import current



SIDEBAR_STYLE = {
    'box-sizing':'border-box',
    'width': '20%',
    'border-bottom': '5px solid grey',
    'float': 'left',
    'text-indent': '5%',
    'padding-bottom': '100%',
    "background-color": "#EAF0F1",
}
MAIN_STYLE = {
  'box-sizing':'border-box',
  'width': '80%',
  'float': 'left',
  'background-color': '#AFAFAF',
  'marign': '20%',
  'padding-bottom': '100%'
}
opts = []
#------------------------------------------------------------------------------------------------------------------------------------
#Login section of sidebar

login = html.Div([
    html.H2("Log In", style={'text-align': 'center'}),
    dcc.Input(id="username", type="text", placeholder="User Name", debounce=True),
    dcc.Input(id="key", type="password", placeholder="Key", debounce=True),
    html.Button('Login', id='loginbutton', n_clicks=0, style={'float':'right', 'box-sizing':'border-box', 'margin-right':'2%'}),
    html.Br(),
    html.H2('')


], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})

@app.callback(
    dash.dependencies.Output('availabledata', 'children'),
    [dash.dependencies.Input("loginbutton", "n_clicks"),
    dash.dependencies.Input("username", "value"),
    dash.dependencies.Input("key", "value")]
)
def getdata(button, name, key):
    if button != 0:
        get_datasets(name, key)
        return dcc.Checklist(
                options=[{'label': 'New York City', 'value': 'NYC'}],
                labelStyle={'display': 'block', 'margin':'0%'},
            )  

#---------------------------------------------------------------------------------------------------------------------------------------


availbledata = html.Div(children = [
    html.H2("Available Experiments", style={'text-align': 'center'}),
    html.Div(id = 'availabledata', children = [

    ])
    

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})



#---------------------------------------------------------------------------------------------------------------------------------------



features = html.Div([
    html.H2("Features", style={'text-align': 'center'}),
    


], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})






layout = html.Div([
    html.Div([
        login,
        availbledata,
        features

    ], style= SIDEBAR_STYLE),


    html.Div(id='mainfeed',children=[
        
    ], style=MAIN_STYLE),
])


