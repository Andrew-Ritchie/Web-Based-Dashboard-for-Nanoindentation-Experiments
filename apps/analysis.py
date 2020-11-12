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
from apps.kaggle2 import DataProcessor

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
    html.Div(id='currentusername', style={'display': 'none'}),
    html.H2('')


], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})

@app.callback(
    dash.dependencies.Output('currentusername', 'children'),
    [dash.dependencies.Input("loginbutton", "n_clicks"),
     dash.dependencies.Input("username", "value")]
)
def saveusername(clicks, name):
    if clicks != 0 and name is not None:
        return name
    


@app.callback(
    dash.dependencies.Output('availabledatasets', 'options'),
    [dash.dependencies.Input("loginbutton", "n_clicks"),
    dash.dependencies.Input("username", "value"),
    dash.dependencies.Input("key", "value")],
)
def getdata(button, name, key):
    print('do we get here')
    if button != 0 and name is not None:
        print('ahhh')
        opts = []
        datasets.assign_details(name, key)
        
        for element in datasets.available_datasets:
            opts.append({'label': element[1], 'value': '*'.join(element)})

        return opts
    return []

@app.callback(
    dash.dependencies.Output('info', 'children'),
    [dash.dependencies.Input("availabledatasets", "value")]
)
def outputinfo(value):
    print('we got here')
    if value is not None:
        value = value.split('*')
        return html.Div([

            html.Div([
                html.H4('Title: ' + value[1]),
                html.H4('Size: ' + value[2]),
                html.H4('Usability Rating:' + value[7]),

            ], style={'padding-left':'10%', 'display': 'inline-block'}),

            html.Div([
                html.H4('Author: ' + value[0].split('/')[0]),
                html.H4('Download Count: ' + value[5]),
                html.H4('Vote Count: ' + value[6]),
        
            ], style = {'float':'right', 'margin-right':'10%'}),
            
            html.Div(id='line', style={ 'width': '80%', 'height': '47px', 'border-bottom': '1px solid black', 'position': 'relative', 'margin-left': '10%', 'margin-right':'10%'}),
            html.H4('Last Updated', style={'padding-left':'20%', 'display': 'inline-block'}),
            html.H4('Day: ' + value[3], style={'padding-left':'10%', 'display': 'inline-block'}),
            html.H4('Time: ' + value[4], style={'padding-left':'10%', 'display': 'inline-block'}),
        





        ], style = {'text-indent':'0px', 'box-sizing':'border-box'})
    else:
        return html.Div(children = [
            html.P('Please sign in and select an available dataset to utlise this feature.')
        ], style = {'clear':'both', 'float':'left', 'text-indent':'0px'})
        




#---------------------------------------------------------------------------------------------------------------------------------------


availbledata = html.Div(children = [
    html.H2("Available Experiments", style={'text-align': 'center'}),
    html.Div(id = 'availabledata', children = [
    
    dcc.RadioItems(
            id = 'availabledatasets',
            options=[],
            labelStyle={'display': 'block', 'margin':'0%'},
        )  

    ]),

    html.Button('Download', id='downloadbutton', n_clicks=0, style={'float':'right', 'box-sizing':'border-box', 'margin-right':'2%'}),
    html.Br(),
    html.Br()

    

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black'})

process = DataProcessor()

@app.callback(
    dash.dependencies.Output('availabledata', 'children'),
    [dash.dependencies.Input("downloadbutton", "n_clicks")],
     [dash.dependencies.State("availabledatasets", "value")]
)
def pushdataview(clicks, selecteddata):
    
    if clicks != 0:
        datasets.download_data(selecteddata.split('*')[0])
        overview = process.getsets('andrewritchie98')
        expname = list(overview.keys())[0]
        samples = overview[expname].keys()
        output = []
        index = 1
        for element in samples:
            opts = []
            for sets in overview[expname][element]:
                opts.append({'label': sets, 'value': sets})
            output.append(html.Details(children=[
                    html.Summary([
                        element
                    ]),
                    html.Div([
                        dcc.Checklist(
                            id = 'sample'+str(index),
                            options=opts,
                            labelStyle={'display': 'block', 'margin':'0%'},
                            value=[]
                        ),
                        html.Button('All', id='samplebutton'+str(index), n_clicks=0),
                    ], style={'padding-left':'10%'})
                ], style={'padding-left': '5%'}))
            index += 1

        return html.Div(id='dataoverview', children=output)
    else:
        return dcc.RadioItems(
            id = 'availabledatasets',
            options=[],
            labelStyle={'display': 'block', 'margin':'0%'},
        ) 

@app.callback(
    Output('sample1', 'value'),
    [Input('samplebutton1', 'n_clicks')],
    [State("sample1", "options")]
)
def sample1button(n_clicks, options):
    print('do we ever get here')
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
    return all_or_none

@app.callback(
    Output('sample2', 'value'),
    [Input('samplebutton2', 'n_clicks')],
    [State("sample2", "options")]
)
def sample1button(n_clicks, options):
    print('do we ever get here')
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
    return all_or_none



#---------------------------------------------------------------------------------------------------------------------------------------

workflow = html.Div(children = [
    html.H2("Workflow", style={'text-align': 'center'}),
    
    
], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black'})



#---------------------------------------------------------------------------------------------------------------------------------------

overview = html.Div([
            html.H2("Overview"),
            html.Div(id='info', style = {'margin':'0%', 'padding':'0%'}),

            html.Br(),
            html.H1(' '),



            
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
        features,
        workflow

    ], style= SIDEBAR_STYLE),


    html.Div(id='analysismainfeed',children=[], style=MAIN_STYLE),
])


