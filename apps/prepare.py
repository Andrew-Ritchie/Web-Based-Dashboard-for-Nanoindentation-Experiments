import base64
import datetime
import io
import re 
import codecs
import numpy as np
import plotly.express as px

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
from template import out

#get data
test = Experiment()








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
    html.Button(html.H2('Data Overview'), id='dataoverview', n_clicks=0, style={'box-sizing':'border-box', 'align':'center'}),
    html.Div(id='select-experiment'),
    html.Br(),
    

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})


selectfeature = html.Div([
    html.H2("Features", style={'text-align': 'center'}),
    html.Br(),
    

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})






current = ConvertOptics() 

layout = html.Div([
    html.Div([
        uploadarea,
        selectexperiment,
        selectfeature,
    ], style= SIDEBAR_STYLE),
    
    
    html.Div(id='mainfeed',children=[
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
                placeholder="Backward",
                style={}
            )], style={'width': '22%', 'display': 'inline-block', 'float':'right', 'border': '1px solid black'}),
            html.Div([
            dcc.Dropdown(
                id='forward',
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

@app.callback(
    dash.dependencies.Output('forward', 'options'),
    [dash.dependencies.Input("dataoverview", "n_clicks"),
    dash.dependencies.Input("forward", "value")]
)
def update_forward_dropdown(click, selected):
    outputvalues = []
    if test.segments is not None:
        for value in range(1, len(test.segments)):
            name = u'Segment{}'.format(str(value))
            outputvalues.append({'label': name, 'value': value})
        if selected is not None:
            if selected != 'None':
                test.forwardseg = [selected-1, selected]
                print(test.forwardseg)
    else:
        outputvalues = [{'label': 'Upload Experiment', 'value': 'None'}]
    return outputvalues

@app.callback(
    dash.dependencies.Output('backward', 'options'),
    [dash.dependencies.Input("dataoverview", "n_clicks"),
    dash.dependencies.Input("backward", "value")]
)
def update_backward_dropdown(click, selected):
    outputvalues = []
    if test.segments is not None:
        for value in range(1, len(test.segments)):
            name = u'Segment{}'.format(str(value))
            outputvalues.append({'label': name, 'value': value})
        if selected is not None:
            if selected != 'None':
                test.backwardseg = [selected-1, selected]
                print(test.backwardseg)
    else:
        outputvalues = [{'label': 'Upload Experiment', 'value': 'boo'}]
    return outputvalues


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
    Output("select-experiment", 'children'),
    [Input("dataoverview", "n_clicks")]
)
def exp1(value):
    if value !=0:
       return out(test) 

@app.callback(
    Output("comparsiongraph", 'figure'),
    [Input('slider', 'value')]
)
def return_comparsion(value):
    info = []
    '''
    if value is not None:
        rub = test.samplenames.index('Rubber')
        setindex = test.samples[rub].setnames.index('Day1')
        for indent in test.samples[rub].sets[setindex].indents:
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

                
                                
            info.append(go.Scatter(x=xtemp, y=ytemp, showlegend=False))
            info.append(go.Scatter(x=xtempback, y=ytempback, showlegend=False))
    '''

    '''
    for sample in test.samples[0:1]:
        if value is not None:
            if sample == 'Glass':
                sample.color = dict(color="#BB2CD9")
            else:
                sample.color = dict(color="#3498DB")
            for sets in sample.sets[0:1]:
                print(sets.segments)
                for indent in sets.indents[0:1]:
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
    '''
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
    [Input("slider", 'value')]
)
def return_graph(value):
    '''
    for sam in test.samples:
            for sets in sam.sets:
                for indent in sets.indents:
                    print('new')
                    print(indent.time[0:100])
    '''
    info = []
    n = 0
    for displaypaths in test.displaypaths:
        if displaypaths != []:
            samplename = displaypaths[0].split('/')[0]
            setname = displaypaths[0].split('/')[1]
            filenames = []
            for element in displaypaths:
                filenames.append(element.split('/')[2])
            
            if value is not None:
                for indent in test.samples[samplename].sets[setname].indents.values():
                    if indent.name in filenames:
                        print('we did get here')
                        #info.append(go.Scatter(x=indent.piezo[500:2500], y=indent.load[500:2500], name=indent.name, line=sample.color, showlegend=False))
                        info.append(go.Scatter(x=indent.piezo[3500:5500], y=indent.load[3500:5500], name=indent.name, showlegend=False, line=test.availablecolors[n]))
            n+=1 

            
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
    '''
    info = []
    fig = go.Figure()
    print(value2)
    if test.name is not None or value2 is not None:
        for sample in test.samples:
            if sample.name == 'Glass':
                sample.color = dict(color="#BB2CD9")
            else:
                sample.color = dict(color="#3498DB")
            for set1 in sample.sets:
                for indent in set1.indents:
                    fig.add_trace(
                        go.Scattergl(
                            x = indent.piezo[3500:5500],
                            y = indent.load[3500:5500],
                            name = indent.name,
                            line = sample.color,
                            showlegend=False
                            
                        )
                    )
                    #info.append(go.Scatter(x=indent.piezo[500:2500], y=indent.load[500:2500], name=indent.name, line=sample.color, showlegend=False))
                    #info.append(go.Scatter(x=indent.piezo[3500:5500], y=indent.load[3500:5500], name=indent.name, line=sample.color, showlegend=False))
                    
        
        if value is not None:
            #info.append(go.Scatter(x=list(range(0,10000)), y=np.full(10001, value/150), name='Threshold', showlegend=False))
            fig.add_trace(
                        go.Scattergl(
                            x = list(range(0,10000)),
                            y = np.full(10001, value/150),
                            name = 'threshold',
                            showlegend=False
                            
                        )
                    )
        
            
        
    
    fig = go.Figure(data=info)
    fig.update_layout(
        title="Experiment Overview",
        xaxis_title='Displacement',
        yaxis_title='Load',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD'
    )
    
    '''
    
    
    

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

dispaycurves = [ ]

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
                            #do same thing but with objects and 2 lists
                            if name.split('/')[1] not in test.samples.keys():
                                test.addsample(name.split('/')[1])
                            
                            if name.split('/')[2] not in test.samples[name.split('/')[1]].sets.keys():
                                test.samples[name.split('/')[1]].addset(name.split('/')[2])

                            if name.split('/')[3] not in test.samples[name.split('/')[1]].sets[name.split('/')[2]].indents.keys():
                                test.samples[name.split('/')[1]].sets[name.split('/')[2]].addindent(name.split('/')[3], zip_obj, name)
                                test.segments = test.samples[name.split('/')[1]].sets[name.split('/')[2]].indents[name.split('/')[3]].segments
            
            print(test.samples)
            print(test.samples['Rubber'], test.samples['Rubber'].sets['Day2'].indents )

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

all_files = []

def displayfunction(displaypaths):
    if displaypaths != []:
        samplename = displaypaths[0].split('/')[0]
        setname = displaypaths[0].split('/')[1]
        filenames = []
        for element in displaypaths:
            filenames.append(element.split('/')[2])
        print(filenames)

        for indent in test.samples[samplename].sets[setname].indents.values():
            if indent.name in filenames:
                print(indent.name, 'helloooo')
                indent.displayflag = True
            else:
                print('turned flase')
                indent.displayflag = False




@app.callback(
    Output('test1', 'value'),
    [Input('button1', 'n_clicks')],
    [State("test1", "options")]
)
def first(n_clicks, options):
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
    return all_or_none

@app.callback(
    Output('test1', 'children'),
    Input('test1', 'value')
)
def tes(value):
    displayfunction(value)
    test.displaypaths[0] = value
    print('value from template First', value)




@app.callback(
    Output('test2', 'value'),
    [Input('button2', 'n_clicks')],
    [State("test2", "options")]
)
def test2a(n_clicks, options):
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
        print(all_or_none)
    return all_or_none

@app.callback(
    Output('test2', 'children'),
    Input('test2', 'value')
)
def test2b(value):
    test.displaypaths[1] = value
    print('value from template First', value)

@app.callback(
    Output('test3', 'value'),
    [Input('button3', 'n_clicks')],
    [State("test3", "options")]
)
def test3a(n_clicks, options):
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
        print(all_or_none)
    return all_or_none

@app.callback(
    Output('test3', 'children'),
    Input('test3', 'value')
)
def test3b(value):
    print('value from template First', value)
    test.displaypaths[2] = value





@app.callback(
    Output('test4', 'value'),
    [Input('button4', 'n_clicks')],
    [State("test4", "options")]
)
def test4a(n_clicks, options):
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
        print(all_or_none)
    return all_or_none

@app.callback(
    Output('test4', 'children'),
    Input('test4', 'value')
)
def test4b(value):
    print('value from template First', value)
    test.displaypaths[3] = value






@app.callback(
    Output('second', 'children'),
    Input('second', 'value')
)
def second(value):
        print('value from template SECOND', value)

@app.callback(
    Output('third', 'children'),
    Input('third', 'value')
)
def thrid(value):
    print('value from template THIIRD', value)

@app.callback(
    Output('fourth', 'children'),
    Input('fourth', 'value')
)
def fouth(value):
        print('oi oi fourth', value)


