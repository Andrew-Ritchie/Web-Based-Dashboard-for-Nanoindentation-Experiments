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
import timeit

import pandas as pd

from app import app
from apps.opticsparser import ConvertOptics
from accessdata import *
from experimenttree import experimenttree
from template import out
import uuid
from dash.exceptions import PreventUpdate
from apps.kaggle2 import KaggleAPI


#get data

db = Data()
kaggle = KaggleAPI()




import plotly.io as pio
pio.renderers.default = 'iframe'

@app.callback(
    dash.dependencies.Output('sessionid', 'children'),
    [dash.dependencies.Input("sessionid", "value")]
)
def update_forward_dro(click):
    print('testing testing 123')
    #return json.dumps(uuid.uuid4())
    sesid = str(uuid.uuid4())
    db.add_exp(sesid, Experiment())
    return sesid
    



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
    html.Div(id='sessionid', style={'display': 'none'}),
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
    

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black', "maxHeight": "400px", "overflow": "scroll"})


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
    
    
    html.Div(id='mainfeedprep',children=[
        html.Div([
            html.H2("Prepare Data"),
            #html.Div(id='current-exp', style={'text-indent': '1.5%'}),
            html.Div(children=[
                html.P('Segment', style={'float':'left'}),
                dcc.Checklist(
                id='segmentselector',
                options=[
                    {'label': 'Forward', 'value': 'forward'},
                    {'label': 'Backward', 'value': 'backward'},
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
                html.Div([dcc.Slider(id='slider',vertical=True, min = 0, max = 100)], style={'float':'left'}),
                dcc.Graph(id='overviewgraph', style={'float':'left', 'width':'65%', 'padding':'1%', 'bgcolor': 'black'}, config={'displayModeBar':False}),
                dcc.Graph(id='comparsiongraph',style={'float':'left', 'width': '30%', 'padding': '1%'}, config={'displayModeBar':False}),
            ],style={'padding':'0%'}),
            html.Button('Convert', id='submit-val', n_clicks=0, style={'float':'left', 'box-sizing':'border-box', 'margin-right':'2%'}),
            html.Button('Convert', id='submit-to-kaggle', n_clicks=0, style={'float':'right', 'box-sizing':'border-box', 'margin-right':'2%'}),
            html.Br(),
            html.Div([
                html.Pre(id='click-data'),
                html.Br(),

            ]),
            html.H1('-  '),
            html.Br(),

            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'}),
        
    ], style=MAIN_STYLE),
])

submit = html.Div(id='kagglepush', children=[
            html.H2("Upload Dataset"),
            html.Div([
                dcc.Input(id="kagglename", type="text", placeholder="Kaggle Username", debounce=True),
                dcc.Input(id="kagglekey", type="text", placeholder="Kaggle Key", debounce=True),
            ], style = {}),
            html.Div([
                dcc.Input(id="title", type="text", placeholder="Experiment name", debounce=True),
                dcc.Input(id="slugid", type="text", placeholder="Experiment name", debounce=True)
            ], style = {}),

            html.Button('Upload', id='dbpush', n_clicks=0, style={'float':'right', 'box-sizing':'border-box', 'margin-right':'2%'}),
            html.P('Please enter your experimental details, as well as Kaggle credentials.')

            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})

@app.callback(
    dash.dependencies.Output('mainfeedprep', 'children'),
    [dash.dependencies.Input("submit-to-kaggle", "n_clicks"),
     dash.dependencies.Input('sessionid', 'children')]
)
def submitdataset(click, sesid):
    if click != 0:

        db.exps[sesid].outputdata(sesid)
        return submit
    else:
        raise PreventUpdate

@app.callback(
    dash.dependencies.Output('kagglepush', 'children'),
    [dash.dependencies.Input("dbpush", "n_clicks")],
    [dash.dependencies.State("kagglename", "value"),
     dash.dependencies.State("kagglekey", "value"),
     dash.dependencies.State("title", "value"),
     dash.dependencies.State("slugid", "value"),
     dash.dependencies.State('sessionid', 'children')]
)
def submitdataset(click, username, key, title, slugid, sessionid):
    if click != 0:
        kaggle.assign_details(username, key)
        kaggle.upload_dataset(sessionid + '/', title, slugid, username)


        #+ os.listdir(sessionid + '/')[0]
        return html.P('You have submited this dataset to Kaggle')
    else:
        raise PreventUpdate


        

@app.callback(
    dash.dependencies.Output('forward', 'options'),
    [dash.dependencies.Input("dataoverview", "n_clicks"),
    dash.dependencies.Input("forward", "value"),
    dash.dependencies.Input("sessionid", "children")]
)
def update_forward_dropdown(click, selected, sesid):
    outputvalues = []
    test = db.exps[sesid]
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
    dash.dependencies.Input("backward", "value"),
    dash.dependencies.Input('sessionid', 'children')]
)
def update_backward_dropdown(click, selected, sesid):
    outputvalues = []
    test = db.exps[sesid]
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
    [Input("selectexperiment", "value"),
    Input('sessionid', 'children')]
)
def exp(value, sesid):
    test = db.exps[sesid]
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
    [Input("dataoverview", "n_clicks"),
    Input('sessionid', 'children')]
)
def exp1(value, sesid):
    test = db.exps[sesid]
    if value !=0:
       return out(test) 

@app.callback(
    Output("comparsiongraph", 'figure'),
    [Input('slider', 'value'),
    Input('segmentselector', 'value'),
    Input('sessionid', 'children')]
)
def return_comparsion(value, segment, sesid):
    test = db.exps[sesid]
    print(segment)
    info = []
    n = 0
    if segment != []:
        for displaypaths in test.displaypaths:
            if displaypaths != []:
                samplename = displaypaths[0].split('/')[0]
                setname = displaypaths[0].split('/')[1]
                filenames = []
                for element in displaypaths:
                    filenames.append(element.split('/')[2])
                
                for indent in test.samples[samplename].sets[setname].indents.values():
                    if indent.name in filenames:
                        xtemp = indent.piezo[500:2500]
                        ytemp = indent.load[500:2500]
                        xtempback = indent.piezo[3500:5500][::-1]
                        ytempback = indent.load[3500:5500][::-1]
                        for i, loadvalue in enumerate(ytemp):
                            if loadvalue < value:
                                #if loadvalue < (value*1000)/(150):
                                lasti = xtemp [i]
                                lasty = ytemp[i]
                                xtemp[i] = 0
                                ytemp[i] = 0
                        
                        for i, loadvalue in enumerate(ytempback):
                            if loadvalue < value:
                                #if loadvalue < (value*1000)/(150):
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

                    
                        if 'forward' in segment:
                            info.append(go.Scatter(x=xtemp, y=ytemp, showlegend=False, line=test.availablecolors[n]))
                        if 'backward' in segment:
                            info.append(go.Scatter(x=xtempback, y=ytempback, showlegend=False, line=test.availablecolors[n]))
                n += 1
                    
      

    fig = go.Figure(data=info)
    fig.update_layout(
        title="CP Displacement Comparison",
        xaxis_title='Displacement [nm]',
        yaxis_title='Load [nN]',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD',
        clickmode='event+select'
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

dispaycurves = [ ]

@app.callback(
    Output("output", "children"),
    [Input("input2", "value")],
)
def update_output2(input2):
    #create the experiment object
    return u'Experiment Name: {}'.format(input2)

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
              Input('sessionid', 'children')],
              State('upload-data', 'filename'),
               State('upload-data', 'last_modified'))
def update_output(list_of_contents, sesid, list_of_names, list_of_dates):
    test = db.exps[sesid]
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
                x = 0
                for name in zip_obj.namelist():
                    x+= 1
                    print(x)
                    if name.split('.')[-1] == 'txt':
                        if name.split('/')[0] != '__MACOSX' and name.split('/')[2] != '' and name.split('/')[2] != '.DS_Store':
                            #do same thing but with objects and 2 lists
                            print(name.split('/')[1])
                            print(name, 'full name')
                            if name.split('/')[1] not in test.samples.keys():
                                test.addsample(name.split('/')[1])
                            
                            if name.split('/')[2] not in test.samples[name.split('/')[1]].sets.keys():
                                test.samples[name.split('/')[1]].addset(name.split('/')[2])

                            if name.split('/')[3] not in test.samples[name.split('/')[1]].sets[name.split('/')[2]].indents.keys():
                                test.samples[name.split('/')[1]].sets[name.split('/')[2]].addindent(name.split('/')[3], zip_obj, name)
                                test.segments = test.samples[name.split('/')[1]].sets[name.split('/')[2]].indents[name.split('/')[3]].segments
            
            print(test.samples)
            #print(test.samples['Rubber'], test.samples['Rubber'].sets['Day2'].indents )
            #test.outputdata()

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
    print(filename)
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
    [Input('button1', 'n_clicks'),
    Input('sessionid', 'children')],
    [State("test1", "options")]
)
def first(n_clicks, sesid, options):
    print('do we ever get here')
    test = db.exps[sesid]
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
    test.displaypaths[0] = all_or_none
    return all_or_none

@app.callback(
    Output('test1', 'children'),
    [Input('select-experiment', 'n_clicks'), Input('test1', 'value'), Input('sessionid', 'children')]
)
def tes(val, value, sesid):
    test = db.exps[sesid]
    #displayfunction(value)
    test.displaypaths[0] = value
    test.flag = True
    print('value from template First', value)




@app.callback(
    Output('test2', 'value'),
    [Input('button2', 'n_clicks'),
    Input('sessionid', 'children')],
    [State("test2", "options")]
)
def test2a(n_clicks, sesid, options):
    test = db.exps[sesid]
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
    test.displaypaths[1] = all_or_none
    return all_or_none

@app.callback(
    Output('test2', 'children'),
    [Input('select-experiment', 'n_clicks'), Input('test2', 'value'), Input('sessionid', 'children')]
)
def test2b(val, value, sesid):
    test = db.exps[sesid]
    test.displaypaths[1] = value
    print('value from template First', value)

@app.callback(
    Output('test3', 'value'),
    [Input('button3', 'n_clicks'),
    Input('sessionid', 'children')],
    [State("test3", "options")]
)
def test3a(n_clicks, sesid, options):
    test = db.exps[sesid]
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
    test.displaypaths[2] = all_or_none
    return all_or_none

@app.callback(
    Output('test3', 'children'),
    [Input('select-experiment', 'n_clicks'), Input('test3', 'value'), Input('sessionid', 'children')]
)
def test3b(val, value, sesid):
    test = db.exps[sesid]
    print('value from template First', value)
    test.displaypaths[2] = value





@app.callback(
    Output('test4', 'value'),
    [Input('button4', 'n_clicks'),
    Input('sessionid', 'children')],
    [State("test4", "options")]
)
def test4a(n_clicks, sesid, options):
    test = db.exps[sesid]
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
    test.displaypaths[3] = all_or_none
    return all_or_none

@app.callback(
    Output('test4', 'children'),
    [Input('select-experiment', 'n_clicks'), Input('test4', 'value'), Input('sessionid', 'children')]
)
def test4b(val, value, sesid):
    test = db.exps[sesid]
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

prev = None

@app.callback(
    [Output("overviewgraph", 'figure'),
     Output('slider', 'max')],
    [Input("slider", 'value'),
    Input('segmentselector', 'value'),
    Input('select-experiment', 'n_clicks'),
    Input('sessionid', 'children')]
)
def return_graph(value, segment, new, sesid):
    print('this is sesid', sesid)
    test = db.exps[sesid]
    print(new, 'test here')  
    info = []
    n = 0
    top = 100
    if segment != []:
        for displaypaths in test.displaypaths:
            if displaypaths != []:
                samplename = displaypaths[0].split('/')[0]
                setname = displaypaths[0].split('/')[1]
                filenames = []
                for element in displaypaths:
                    filenames.append(element.split('/')[2])
                
                for indent in test.samples[samplename].sets[setname].indents.values():
                    if indent.name in filenames:
                        if 'forward' in segment:
                            info.append(go.Scatter(x=indent.piezo[test.segments[test.forwardseg[0]]:test.segments[test.forwardseg[1]]][0::10], y=indent.load[test.segments[test.forwardseg[0]]:test.segments[test.forwardseg[1]]][0::10], name=indent.name, line=test.availablecolors[n], showlegend=False))
                            top = max(indent.load[test.segments[test.forwardseg[0]]:test.segments[test.forwardseg[1]]])
                            #info.append(indent.load[test.segments[test.forwardseg[0]]:test.segments[test.forwardseg[1]]])
                            #x = indent.piezo[test.segments[test.forwardseg[0]]:test.segments[test.forwardseg[1]]]

                        if 'backward' in segment:
                            top = max(indent.load[test.segments[test.backwardseg[0]]:test.segments[test.backwardseg[1]]])
                            info.append(go.Scatter(x=indent.piezo[test.segments[test.backwardseg[0]]:test.segments[test.backwardseg[1]]][0::10], y=indent.load[test.segments[test.backwardseg[0]]:test.segments[test.backwardseg[1]]][0::10], name=indent.name, showlegend=False, line=test.availablecolors[n]))
                            

                n+=1 

                if value is not None:
                    info.append(go.Scattergl(x=list(range(0,10000))[0::10], y=np.full(10001, value)[0::10], name='Threshold', showlegend=False, line = dict(color='#E44236')))
                    #info.append(go.Scattergl(x=list(range(0,10000))[0::10], y=np.full(10001, value/150)[0::10], name='Threshold', showlegend=False, line = dict(color='#E44236')))
                    
        print('oi, oi')
        #fig = px.line(x =info, y = list(range(0,2000)))
        print('done :-)')
    
    #fig = go.Figure(data=info)

    print('WE GOT HERE ******************')
    '''
    df = dict(x=[1,2,3,4,5],y=[1,2,3,4,5])
    fig = px.line(df, x='x', y="y", title='Life expectancy in Canada')
    N = 200
    x = np.random.randn(N)
    y = np.random.randn(N)
    tic=timeit.default_timer()
    info = []
    for i in range(0,100):
        df = dict(x=x,y=y)
        fig2 = px.line(df, x='x', y="y", title='La', render_mode='webgl')
        fig.add_trace(fig2.data[0])
    '''
    
    fig = go.Figure(data=info)
    

    fig.update_layout(
        title="Experiment Overview",
        xaxis_title='Displacement [nm]',
        yaxis_title='Load [nN]',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD',
    )
    #toc=timeit.default_timer()
    #print('Data Points: ', N, '/ TIME: ', toc - tic)
    return fig, top