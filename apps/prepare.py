import base64
import datetime
import io
import re 
import codecs
import numpy as np


import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go


import pandas as pd

from app import app
from apps.opticsparser import ConvertOptics
from accessdata import *

#get data
test = Experiment("apps/converted/exp1", "test")
test.loadexperiment()

SIDEBAR_STYLE = {
    'box-sizing':'border-box',
    'width': '20%',
    'border': '1px solid black',
    'float': 'left',
    'text-indent': '5%',
    'padding-bottom': '100%',
    "background-color": "#EAF0F1"
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
    dcc.Input(id="expname", type="text", placeholder="Experiment name", debounce=True),
    dcc.Input(id="samname", type="text", placeholder="Sample name", debounce=True),
    dcc.Input(id="setname", type="text", placeholder="Set name", debounce=True),
    html.Div(id="output", style= {"text-indent": '0%'}),
    html.Div(id='output-data-upload'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'text-align': 'center'
            
        },
        # Allow multiple files to be uploaded
        multiple=True
    )

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})







current = ConvertOptics() 

layout = html.Div([
    html.Div([
        uploadarea
    ], style= SIDEBAR_STYLE),
    
    
    html.Div([
        html.Div([
            html.H2("Prepare Data"),
            html.Div(id='current-exp', style={'text-indent': '1.5%'}),
            html.Div([
                html.Div([dcc.Slider(id='slider',vertical=True)], style={'float':'left'}),
            
            dcc.Graph(id='overviewgraph', style={'float':'left', 'width':'60%', 'padding':'1%', 'bgcolor': 'black'}),
            dcc.Graph(id='comparsiongraph',style={'float':'left', 'width': '30%', 'padding': '1%'}),
            ],style={'padding':'1%'}),
            html.Br(),
            dcc.Input(id="input2", type="text", placeholder="", debounce=True),
            html.Div(id="output", style= {"text-indent": '0%'}),
            html.Div(id='output-data-upload'),
            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'}),
        
    ], style=MAIN_STYLE),
])

@app.callback(
    Output("comparsiongraph", 'figure'),
    [Input('slider', 'value')]
)
def return_comparsion(value):
    info = []
    for i in test.samples:
        print(i.name)
        for x in i.sets:
            print(x.name)
            for y in x.indents:
                info.append(go.Scatter(x=y.indentation[500:2500], y=y.load[500:2500], showlegend=False))

    if value is not None:
        info.append(go.Scatter(x=list(range(0,2000)), y=np.full(2001, value/150), showlegend=False))
        print(value)

    fig = go.Figure(data=info)
    fig.update_layout(
        title="Experiment Overview",
        xaxis_title='Indentation',
        yaxis_title='Load',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD'
    )
    return fig

@app.callback(
    Output("overviewgraph", 'figure'),
    [Input("slider", 'value')]
)
def return_graph(value):
    info = []
    for i in test.samples:
        print(i.name)
        for x in i.sets:
            print(x.name)
            for y in x.indents:
                info.append(go.Scatter(x=y.indentation[500:2500], y=y.load[500:2500], name=x.name))

    if value is not None:
        info.append(go.Scatter(x=list(range(0,2000)), y=np.full(2001, value/150), name='Threshold'))
        print(value)

    fig = go.Figure(data=info)
    fig.update_layout(
        title="Experiment Overview",
        xaxis_title='Indentation',
        yaxis_title='Load',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD'
    )
    return fig

@app.callback(
    Output("current-exp", 'children'),
    [Input("expname", "value")]
)
def experiment_name(value):
    print(value)
    current.assignexperiment(value)
    return u'Experiment Name: {}'.format(value)


@app.callback(
    Output("samname", 'children'),
    [Input("samname", "value")]
)
def sample_name(value):
    print(value)
    current.assignsampname(value)



@app.callback(
    Output("input2", 'children'),
    [Input("setname", "value")]
)
def set_name(value):
    print(value)
    current.assignsetname(value)



@app.callback(
    Output("output", "children"),
    [Input("input2", "value")],
)
def update_output2(input2):
    #create the experiment object
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



