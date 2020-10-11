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
from zipfile import ZipFile

import pandas as pd

from app import app
from apps.opticsparser import ConvertOptics
from accessdata import *
from experimenttree import experimenttree
from template import tem

#get data
test = Experiment()



def get_experiments():
    options = []
    for experiment in os.scandir("apps/converted"):
        options.append({'label': experiment.name.split('.')[0], 'value': experiment.name.split('.')[0]})
    return options




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

selectexperiment = html.Div([
    html.H2("Select Experiment", style={'text-align': 'center'}),
    dcc.Dropdown(
        id='selectexperiment',
        options=get_experiments(),
        placeholder="Experiment",
        style={'width':'70%', 'box-sizing':'border-box', 'background-color':'#DDDDDD', 'text-color':'black'},
    ),
    html.Div(id='experiment-output'),
    html.Br(),
    

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})







current = ConvertOptics() 

layout = html.Div([
    html.Div([
        uploadarea,
        selectexperiment,
        html.H1('tem'),
    ], style= SIDEBAR_STYLE),
    
    
    html.Div([
        html.Div([
            html.H2("Prepare Data"),
            #html.Div(id='current-exp', style={'text-indent': '1.5%'}),
            html.Div(children=[
                html.P('Segment', style={'float':'left'}),
                dcc.Checklist(
                options=[
                    {'label': 'Forward', 'value': 'NYC'},
                    {'label': 'Backward', 'value': 'MTL'},
                ],
                value=[],
                labelStyle={'display': 'inline-block', 'float':'left', 'width':'35%'},
                )], style={'width': '49%', 'display': 'inline-block', 'border': '1px solid black', 'margin-left': '1%', 'padding':'0%'}),
            
            html.Div([
                dcc.Dropdown(
                id='backward',
                options=[{'label':'Seg1', 'value':'Seg1'}, {'label':'Seg2', 'value':'Seg2'}, {'label':'Seg3', 'value':'Seg3'}, {'label':'Seg4', 'value':'Seg4'}, {'label':'Seg5', 'value':'Seg5'}],
                placeholder="Backward",
                style={}
            )], style={'width': '22%', 'display': 'inline-block', 'float':'right', 'border': '1px solid black'}),
            html.Div([
            dcc.Dropdown(
                id='forward',
                options=[{'label':'Seg1', 'value':'Seg1'}, {'label':'Seg2', 'value':'Seg2'}, {'label':'Seg3', 'value':'Seg3'}, {'label':'Seg4', 'value':'Seg4'}, {'label':'Seg5', 'value':'Seg5'}],
                placeholder="Forward",
                style={}
            )], style={'width': '22%', 'display': 'inline-block', 'float':'right', 'border': '1px solid black'}),
           
           
            html.Div([
                html.Div([dcc.Slider(id='slider',vertical=True)], style={'float':'left'}),
                dcc.Graph(id='overviewgraph', style={'float':'left', 'width':'65%', 'padding':'1%', 'bgcolor': 'black'}, config={'displayModeBar':False}),
                dcc.Graph(id='comparsiongraph',style={'float':'left', 'width': '30%', 'padding': '1%'}, config={'displayModeBar':False}),
            ],style={'padding':'0%'}),
            html.Button('Convert', id='submit-val', n_clicks=0, style={'float':'left', 'box-sizing':'border-box', 'margin-right':'2%'}),
            html.Button('Convert', id='submit-val', n_clicks=0, style={'float':'right', 'box-sizing':'border-box', 'margin-right':'2%'}),
            html.H1('test'),
            html.Pre(id='click-data'),
            html.P(id='one'),
            html.P(id='two'),
            dcc.Checklist(
                options= [{'label': 'Forward', 'value': 'NYC'},
                    {'label': 'Backward', 'value': 'MTL'},]
            )

            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'}),
        
    ], style=MAIN_STYLE),
])


'''
@app.callback(
    Output('forward', 'children'),
    [Input('forward', 'value')]
)
def forward(value):
    #assign forward segment

@app.callback(
    Output('backward', 'children'),
    [Input('backward', 'value')]
)
def backward(value):
    #assign backward segment
'''
@app.callback(
    Output("current-exp", 'children'),
    [Input("selectexperiment", "value")]
)
def exp(value):
    if value is not None:
        test.assignname(value)
        test.assignfilepath('apps/converted/' + test.name)
        test.loadexperiment()
        message = u'Experiment Name: {}'.format(value)
    else:
        message = u'Select an Experiment'
    return message

@app.callback(
    Output("experiment-output", 'children'),
    [Input("selectexperiment", "value")]
)
def exp(value):
    if value is not None:
        return tem

@app.callback(
    Output("comparsiongraph", 'figure'),
    [Input('slider', 'value')]
)
def return_comparsion(value):
    info = []
    for sample in test.samples.values():
        print(test.samples.values())
        if value is not None:
            if sample == 'Glass':
                sample.color = dict(color="#BB2CD9")
            else:
                sample.color = dict(color="#3498DB")
            for sets in sample.sets:
                print(sets.segments)
                for indent in sets.indents:
                    xtemp = indent.piezo[500:2500]
                    ytemp = indent.load[500:2500]
                    xtempback = indent.piezo[3500:5500]
                    ytempback = indent.load[3500:5500]
                    for i, loadvalue in enumerate(ytemp):
                        if loadvalue < value/150:
                            lasti = xtemp [i]
                            lasty = ytemp[i]
                            xtemp[i] = 0
                            ytemp[i] = 0
                    
                    for i, loadvalue in enumerate(ytempback):
                        if loadvalue < value/150:
                            lastxback = xtempback[i]
                            lastyback = ytempback[i]
                            xtempback[i] = 0
                            ytempback[i] = 0  
                    
                    for i in range(len(xtemp)):
                        xtemp[i] = xtemp[i] - lasti
                        xtempback[i] = xtempback[i] - lastxback
                        if xtemp[i] < 0:
                            xtemp[i] = 0
                        if xtempback[i] < 0:
                            xtempback[i] = 0
                            
                    for i in range(len(ytemp)):                      
                        ytemp[i] = ytemp[i] - lasty
                        ytempback[i] = ytempback[i] - lastyback
                        if ytemp[i] < 0:
                            ytemp[i] = 0
                        if ytempback[i] < 0:
                            ytempback[i] = 0

                        
                                        
                    info.append(go.Scatter(x=xtemp, y=ytemp, showlegend=False, line=sample.color))
                    info.append(go.Scatter(x=xtempback, y=ytempback, showlegend=False, line=sample.color))

    fig = go.Figure(data=info)
    fig.update_layout(
        title="Indentation Comparison",
        xaxis_title='Indentation',
        yaxis_title='Load',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD',
        clickmode='event+select'
    )
    return fig

@app.callback(
    Output("overviewgraph", 'figure'),
    [Input("slider", 'value'),
    Input("selectexperiment", "value2")]
)
def return_graph(value, value2):
    info = []
    print(value2)
    if test.name is not None or value2 is not None:
        print(test.samples.values())
        for sample in test.samples.values():
            if sample.name == 'Glass':
                sample.color = dict(color="#BB2CD9")
            else:
                sample.color = dict(color="#3498DB")
            for set1 in sample.sets:
                for indent in set1.indents:
                    #info.append(go.Scatter(x=indent.piezo[500:2500], y=indent.load[500:2500], name=indent.name, line=sample.color, showlegend=False))
                    info.append(go.Scatter(x=indent.piezo[3500:5500], y=indent.load[3500:5500], name=indent.name, line=sample.color, showlegend=False))
                    

        if value is not None:
            info.append(go.Scatter(x=list(range(0,10000)), y=np.full(10001, value/150), name='Threshold', showlegend=False))

    fig = go.Figure(data=info)
    fig.update_layout(
        title="Experiment Overview",
        xaxis_title='Displacement',
        yaxis_title='Load',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD'
    )
    return fig

@app.callback(
    Output('click-data', 'children'),
    [Input('overviewgraph', 'clickData')])
def display_click_data(clickData):
    print('2')

    return json.dumps(clickData, indent=2)

@app.callback(
    Output('one', 'children'),
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
    Output('two', 'children'),
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
        if list_of_names[0].split('.')[-1] == 'zip':
            
            for content, name, date in zip(list_of_contents, list_of_names, list_of_dates):
                # the content needs to be split. It contains the type and the real content
                content_type, content_string = content.split(',')
                # Decode the base64 string
                content_decoded = base64.b64decode(content_string)
                # Use BytesIO to handle the decoded content
                zip_str = io.BytesIO(content_decoded)
                # Now you can use ZipFile to take the BytesIO output
                zip_obj = ZipFile(zip_str, 'r')
                
                test.assignname(name.split('.')[0])
                out = ConvertOptics()
                for name in zip_obj.namelist():
                    if name.split('.')[-1] == 'txt':
                        if name.split('/')[0] != '__MACOSX' and name.split('/')[2] != '' and name.split('/')[2] != '.DS_Store':
                            if name.split('/')[1] not in test.data:
                                test.addsample(name.split('/')[1])
                            if name.split('/')[2] not in test.data[name.split('/')[1]]:
                                test.addset(name.split('/')[1], name.split('/')[2])
                            if name.split('/')[3] not in test.data[name.split('/')[1]][name.split('/')[2]]:
                                test.addindent(name.split('/')[1], name.split('/')[2], name.split('/')[3], zip_obj, name)
            print(test.data)

        else:
            children = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)] 
            return children
    
    
    

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    print(decoded[0:110])
    current.assignfilename(filename)
    current.loaddata(decoded)
    current.loadheader(decoded)
    current.createfile()

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        html.Hr(),  # horizontal line
    ])



