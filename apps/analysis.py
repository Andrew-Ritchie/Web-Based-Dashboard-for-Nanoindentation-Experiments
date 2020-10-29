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
from apps.kaggle2 import KaggleAPI

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
datasets = KaggleAPI()

login = html.Div([
    html.H2("Log In", style={'text-align': 'center'}),
    dcc.Input(id="username", type="text", placeholder="User Name", debounce=True),
    dcc.Input(id="key", type="password", placeholder="Key", debounce=True),
    html.Button('Login', id='loginbutton', n_clicks=0, style={'float':'right', 'box-sizing':'border-box', 'margin-right':'2%'}),
    html.Br(),
    html.H2('')


], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})

@app.callback(
    dash.dependencies.Output('availabledatasets', 'options'),
    [dash.dependencies.Input("loginbutton", "n_clicks"),
    dash.dependencies.Input("username", "value"),
    dash.dependencies.Input("key", "value")],
)
def getdata(button, name, key):

    if button != 0 and name is not None:
        print('ahhh')
        opts = []
        datasets.assign_details(name, key)
        
        for element in datasets.available_datasets:
            opts.append({'label': element[1], 'value': element[1]})

        return opts
    return []

@app.callback(
    dash.dependencies.Output('availbledata', 'children'),
    [dash.dependencies.Input("availabledatasets", "value")]
)
def outputinfo(value):
    print('we got here')
    return html.H2("Available Experiments", style={'text-align': 'center'})




#---------------------------------------------------------------------------------------------------------------------------------------


availbledata = html.Div(children = [
    html.H2("Available Experiments", style={'text-align': 'center'}),
    html.Div(id = 'availabledata', children = [
    
    dcc.RadioItems(
            id = 'availabledatasets',
            options=[],
            labelStyle={'display': 'block', 'margin':'0%'},
        )  

    ])
    

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})



#---------------------------------------------------------------------------------------------------------------------------------------

overview = html.Div([
            html.H2("Overview"),
            
            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})


filter1 = html.Div([
            html.H2("Filter One"),
            
            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})


accessfeatures = { 'overview':overview, 'filter1':filter1 }


#---------------------------------------------------------------------------------------------------------------------------------------




features = html.Div([
    html.H2("Features", style={'text-align': 'center'}),
    dcc.Checklist(
                id = 'selectedfeatures',
                options=[{'label': 'Overview', 'value': 'overview'},
                         {'label': 'Filter1', 'value': 'filter1'}],
                labelStyle={'display': 'block', 'margin':'0%'},
    ),
    html.Br()
    


], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})

@app.callback(
    dash.dependencies.Output('analysismainfeed', 'children'),
    [dash.dependencies.Input("selectedfeatures", "value")]
)
def displayfeature(value):
    output = []
    if value is not None:
        for item in value:
            output.append(accessfeatures[item])
    return output


        


      



layout = html.Div([
    html.Div([
        login,
        availbledata,
        features

    ], style= SIDEBAR_STYLE),


    html.Div(id='analysismainfeed',children=[], style=MAIN_STYLE),
])


