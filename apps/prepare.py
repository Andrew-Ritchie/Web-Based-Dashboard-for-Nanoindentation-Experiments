import base64
import datetime
import io
import re 
import codecs


import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd

from app import app
from apps.opticsparser import ConvertOptics


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
sidebar = html.Div(
    [
        html.H2("Sidebar"),
        
    ]
)


uploadarea = html.Div([
    html.H2("Upload Experiment", style={'text-align': 'center'}),
    dcc.Input(id="input2", type="text", placeholder="Experiment name", debounce=True),
    dcc.Input(id="input3", type="text", placeholder="Sample name", debounce=True),
    dcc.Input(id="input4", type="text", placeholder="Set name", debounce=True),
    html.Div(id="output", style= {"text-indent": '0%'}),
    html.Div(id='output-data-upload'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '70%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'text-align': 'center'
            
        },
        # Allow multiple files to be uploaded
        multiple=True
    )

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'0%'})







current = ConvertOptics() 
layout = html.Div([
    html.Div([
        uploadarea
    ], style= SIDEBAR_STYLE),
    
    
    html.Div([
        html.Div([
            html.H2("Upload Data"),
            dcc.Input(id="input2", type="text", placeholder="", debounce=True),
            html.Div(id="output", style= {"text-indent": '0%'}),
            html.Div(id='output-data-upload'),
            
        ], style={'background-color': '#DDDDDD', 'margin': '1%'}),
        
    ], style=MAIN_STYLE),
])

@app.callback(
    Output("output", "children"),
    [Input("input2", "value")],
)
def update_output2(input2):
    #create the experiment object
    current.assignexperiment(input2)
    return u'Experiment Name: {}'.format(input2)

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              State('upload-data', 'filename'),
               State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):  
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)] 
        return children
    

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    current.assignfilename(filename)
    current.loaddata(decoded)
    current.loadheader(decoded)
    current.createfile()

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        html.Hr(),  # horizontal line
    ])



