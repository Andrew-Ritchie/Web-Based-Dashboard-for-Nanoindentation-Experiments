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
from apps.opticsparser import ConvertRangeAFM
from accessdata import *
from template import out
import uuid
from dash.exceptions import PreventUpdate
from apps.kaggle2 import KaggleAPI
import shutil
import dash_core_components as dcc
import time
import plotly.io as pio
pio.renderers.default = 'iframe'




#Set up the Preparation data structure and the database functionality
db = Data()
kaggle = KaggleAPI()






@app.callback(
    dash.dependencies.Output('sessionid', 'children'),
    [dash.dependencies.Input("sessionid", "value")]
)
def update_forward_dro(click):
    """
    Returns session ID to create a separate space in memory for the active user


    :type sessionid: string
    :param sessionid: this parameter is used to fire the callback once when the user loads the page
    
    """
    sesid = str(uuid.uuid4())
    db.add_exp(sesid, Experiment())
    return sesid
    


#Create a styling theme to be used throughout the prepare page
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


#Set up the HTML for the upload functionality
uploadarea = html.Div([

    html.H2("Upload Experiment", style={'text-align': 'center'}),
    html.Div([
    dcc.RadioItems(
    id='filetype',
    options=[
        {'label': 'Optics11', 'value': 'Optics11'},
        {'label': 'JPK Instruments', 'value': 'JPK Instruments'},
        #{'label': 'AFM workshop', 'value': 'AFM workshop'},
        #{'label': 'Asylum Research', 'value': 'Asylum Research'},
    ],
    labelStyle={'display': 'block', 'margin':'0%'},
    value='Optics11',
    
    )], style={'width': '100%', 'margin-left': '1%', 'padding':'0%', "maxHeight": "100px", "overflow": "scroll"}),

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
    ),


], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})


#Set up the HTML for the automatic filter
thresholdfilter = html.Div([
    html.H2("Automatic Filter", style={'text-align': 'center'}),
    html.Div([
        dcc.Input(
            id="filtervalue", type="number",
            debounce=True, placeholder="Debounce True", value= 1,
            style={'float':'left',  }
    ),
    html.P('nN', style={'float':'left'})
    ]),
    html.Br(),
    html.Div([]),

    html.Br(),
    

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})


#Set up the area on the Prep page to let users select experiments
selectexperiment = html.Div([
    html.Button(html.H2('Data Overview'), id='dataoverview', n_clicks=0, style={'box-sizing':'border-box', 'align':'center'}),
    html.Div(id='select-experiment'),
    html.Br(),
    

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black', "maxHeight": "400px", "overflow": "scroll"})

#Set up area in Prep page for the user to include any missing metadata from uploaded files
metadata = html.Div([
    html.H2("Metadata", style={'text-align': 'center'}),
    html.Div(id='metaoutput'),

    html.Br(),
    

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})


@app.callback(
    dash.dependencies.Output('metaoutput', 'children'),
    [dash.dependencies.Input("filetype", "value")]
)
def getmetadatavalues(filetype):
    """
    Returns custom HTML, tailored for the specific file type uploaded by the user. 
    This lets the user insert any metadata values that are not included in the uploaded files.


    :type filetype: string
    :param filetype: outlines the filetype uploaded by the user
    
    """

    if filetype != 'Optics11':
        return html.Div([
            html.P('Please enter the following metadata values, as these are not provided by JPK files.'),
            html.P('Tip Radius'),
            html.Div([
                dcc.Input(
                    id="tiprad", type="number",
                    debounce=True, placeholder="Debounce True", value= 10,
                    style={'float':'left',  }
                ),
                html.P('um', style={'float':'left'})
            ]),
            html.Div([
                html.P('Cantilever K', style={"clear":"both"}),
            ]),
            html.Div([
                dcc.Input(
                    id="cantiliver", type="number",
                    debounce=True, placeholder="Debounce True", value= 0.51,
                    style={'float':'left',  }
                ),
                html.P('Nm', style={'float':'left'})
            ]),
            html.Br(),
            html.Div(id='update')
            ])
    else:
        return html.P('No metadata values required as these are all provided by Optics11.')

@app.callback(
    dash.dependencies.Output('update', 'children'),
    [dash.dependencies.Input("tiprad", "value"),
    dash.dependencies.Input("cantiliver", "value"),
    dash.dependencies.Input('sessionid', 'children'),
    dash.dependencies.Input("dataoverview", "n_clicks")]
)
def updatemetavalues(tiprad, cantileverk, sesid, clicks):
    """
    Update the metadata values in the applications data structure with the values outlined by the user. 


    :type tiprad: float
    :param tiprad: value outlined by user fro the tip radius

    :type sesid: float
    :param sesid: the session value of the user interacting with the page

    :type clicks: int
    :param clicks: triggers callback when the dataoverview button
    
    """
    if clicks != 0:
        exp = db.exps[sesid]
        for sample in exp.samples.values():
                for sets in sample.sets.values():
                    for indent in sets.indents.values():
                        indent.tipradius = tiprad
                        indent.cantileverk = cantileverk


'''
@app.callback(Output("progress", "value"), [Input("interval", "n_intervals")])
def advance_progress(n):
    return min(n % 110, 100)
'''

#HTML used to let the user select to use reduced or full resolution of FD curves
selectfeature = html.Div([
    html.H2("Resolution", style={'text-align': 'center'}),
    dcc.RadioItems(
    id='res',
    options=[
        {'label': 'Full', 'value': 'full'},
        {'label': 'Reduced', 'value': 'reduced'},
    ],
    labelStyle={'display': 'block', 'margin':'0%'},
    value='reduced', 
    style={'width': '100%', 'margin-left': '1%', 'padding':'0%'}),

    html.Br(),
    

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})



#integrate parser functionality
current = ConvertOptics() 
multipleAFM = ConvertRangeAFM()


#Set up the HTML for the entire Prep page
layout = html.Div([
    #set up the order of the sidebar in the Prep page
    html.Div([
        uploadarea,
        selectexperiment,
        metadata,
        thresholdfilter,
        selectfeature,
    ], style= SIDEBAR_STYLE),
    
    
    #The HTML used for the main area of the Prep page
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
                html.Div(id='slidervalue', style={'display': 'none'}),
                dcc.Graph(id='overviewgraph', style={'float':'left', 'width':'65%', 'padding':'1%', 'bgcolor': 'black'}, config={'displayModeBar':False}),
                dcc.Graph(id='comparsiongraph',style={'float':'left', 'width': '30%', 'padding': '1%'}, config={'displayModeBar':False}),
            ],style={'padding':'0%'}),
            html.Div(children=[
                html.Div(id='testdiv', style={'display': 'none'}),
                html.Div(id='selectedcurve', style={'display': 'none'}),
                html.Div(id='nameofselectedcurve', style={'foat':'left', 'margin':'0%'}),
                dcc.RadioItems(
                id='filteredselector',
                options=[
                    {'label': 'Keep', 'value': 'True'},
                    {'label': 'Remove', 'value': 'False'},
                ],
                value='Keep',
                labelStyle={'display': 'inline-block', 'float':'left', 'width':'35%', 'color':'red', 'margin-left':'1%', 'margin-right':'1%'},
                )], style={'width': '90%', 'display': 'inline-block', 'margin-left': '1%', 'padding':'0%'}),
            
            html.Button('Convert', id='submit-to-kaggle', n_clicks=0, style={'float':'right', 'box-sizing':'border-box', 'margin-right':'2%'}),
            html.Br(),
            html.Div([
                html.Pre(id='click-data'),
                html.Br(),

            ]),
            html.Br(),

            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'}),
        
    ], style=MAIN_STYLE),
])


#HTML used for the convert section of the Prep page
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
            dcc.RadioItems(
                id='privatekaggle',
                options=[
                    {'label': 'Public', 'value': 'public'},
                    {'label': 'Private', 'value': 'private'},
                    
                ],
                value='public'
            ),  

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
     dash.dependencies.State('sessionid', 'children'),
     dash.dependencies.State('privatekaggle', 'value'),]
)
def submitdataset(click, username, key, title, slugid, sessionid, private):
    """
    Submits prepared dataset to Kaggle


    :type click: int
    :param click: click value of the submit button

    :type username: string
    :param username: name of the user submitting to Kaggle

    :type key: int
    :param key: Kaggle Key


    
    """
    if click != 0:
        kaggle.assign_details(username, key)
        kaggle.upload_dataset(sessionid + '/', title, slugid, username, private)


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
    """
    Update the forward dropdown menu with the segments used in the uploaded file.


    :type click: int
    :param click: dataoverview button value

    :type selected: string
    :param selected: the selected value from the forward dropdown menu

    :type sesid: string
    :param sesid: session ID of the active user
    
    """
    outputvalues = []
    test = db.exps[sesid]
    if test.segments is not None:
        for value in range(0,test.segments):
            name = u'Segment{}'.format(str(value))
            outputvalues.append({'label': name, 'value': value})
        if selected is not None:
            if selected != 'None':
                test.forwardseg = selected
                #print(test.forwardseg)
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
    """
    Update the backward dropdown menu with the segments used in the uploaded file.


    :type click: int
    :param click: dataoverview button value

    :type selected: string
    :param selected: the selected value from the backward dropdown menu

    :type sesid: string
    :param sesid: session ID of the active user
    
    """
    outputvalues = []
    test = db.exps[sesid]
    if test.segments is not None:
        for value in range(0,test.segments):
            name = u'Segment{}'.format(str(value))
            outputvalues.append({'label': name, 'value': value})
        if selected is not None:
            if selected != 'None':
                test.backwardseg = selected
                #print(test.backwardseg, 'BACKWARD SEG')
    else:
        outputvalues = [{'label': 'Upload Experiment', 'value': 'boo'}]
    return outputvalues

@app.callback(
    Output("current-exp", 'children'),
    [Input("selectexperiment", "value"),
    Input('sessionid', 'children')]
)
def exp(value, sesid):
    """
    Update the forward dropdown menu with the segments used in the uploaded file.


    :type click: int
    :param click: dataoverview button value

    :type selected: string
    :param selected: the selected value from the forward dropdown menu

    :type sesid: string
    :param sesid: session ID of the active user
    
    """
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
    [Input('slidervalue', 'value'),
    Input('segmentselector', 'value'),
    Input('sessionid', 'children')]
)
def return_comparsion(value, segment, sesid):
    """
    Return the CP Comparison Graph


    :type value: int
    :param value: value selected by the slider

    :type segment: string
    :param segment: the segment being inspected

    :type sesid: string
    :param sesid: session ID of the active user
    
    """
    test = db.exps[sesid]
    info = []
    n = 0
    if segment != [] and value is not None:
        if value != 0:
            for displaypaths in test.displaypaths:
                if displaypaths != []:
                    samplename = displaypaths[0].split('/')[0]
                    setname = displaypaths[0].split('/')[1]
                    filenames = []
                    for element in displaypaths:
                        filenames.append(element.split('/')[2])

                    for indent in test.samples[samplename].sets[setname].indents.values():
                        if indent.name in filenames:

                            if indent.piezo[test.forwardseg][0] < indent.piezo[test.forwardseg][-1]:
                                xtemp = indent.piezo[test.forwardseg].copy()
                                ytemp = indent.load[test.forwardseg].copy()
                                xtempback = indent.piezo[test.backwardseg][::-1].copy()
                                ytempback = indent.load[test.backwardseg][::-1].copy()
                            else:
                                xtemp = indent.piezo[test.forwardseg][::-1].copy()
                                ytemp = indent.load[test.forwardseg].copy()
                                xtempback = indent.piezo[test.backwardseg].copy()
                                ytempback = indent.load[test.backwardseg][::-1].copy()
                                

                            
                            
                            
                            for i, loadvalue in enumerate(ytemp):
                                if loadvalue < value:
                                    lasti = xtemp [i]
                                    lasty = ytemp[i]
                                    xtemp[i] = 0
                                    ytemp[i] = 0
                            
                            for i, loadvalue in enumerate(ytempback):
                                if loadvalue < value:
                                    lastxback = xtempback[i]
                                    lastyback = ytempback[i]
                                    xtempback[i] = 0
                                    ytempback[i] = 0
                            
                            
                            for i in range(len(xtemp)):
                                xtemp[i] = xtemp[i] - lasti
                                if xtemp[i] < 0:
                                    xtemp[i] = 0
                            
                            for i in range(len(xtempback)):
                                xtempback[i] = xtempback[i] - lastxback
                                if xtempback[i] < 0:
                                    xtempback[i] = 0


                            
                                    
                            for i in range(len(ytemp)):                      
                                ytemp[i] = ytemp[i] - lasty
                                if ytemp[i] < 0:
                                    ytemp[i] = 0
                                
                                
                            for i in range(len(ytempback)):
                                ytempback[i] = ytempback[i] - lastyback
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
    [Output('nameofselectedcurve', 'children'),
    Output("filteredselector", "value")],
    [Input('overviewgraph', 'clickData'),
    Input('sessionid', 'children')],
    [State('overviewgraph', 'figure')])
def display_click_data(click_data, sesid, figure):
    """
    Return the curve that the user has selected


    :type click_data: dict
    :param value: data regarding the displayed FD curves

    :type sesid: string
    :param sesid: the session value of the active user

    :type figure: string
    :param figure: the displayed FD curves
    
    """
    if click_data is not None:
        curve_number = click_data['points'][0]['curveNumber']
        trace_name = figure['data'][curve_number]['name']

        dataset = db.exps[sesid]
        pathfound = False
        while pathfound == False:
            for element in dataset.displaypaths:
                if element != []:
                    for value in element:
                        path = value.split('/')
                        if path[-1] == trace_name:
                            sample_name = path[0]
                            set_name = path[1]
                            curve_name = path[2]
                            pathfound = True
        outvalue = str(dataset.samples[sample_name].sets[set_name].indents[curve_name].filtered)
        print(outvalue, 'this is out value ')
        return html.P(trace_name), outvalue
    return None, None

@app.callback(
    Output('testdiv', 'children'),
    [Input("filteredselector", "value"),
    Input('sessionid', 'children')],
    [State('nameofselectedcurve', 'children'),
    State('overviewgraph', 'figure')]
)
def filtercurve(selectedvalue, sesid, curveinput, figure):
    """
    Removes bogus FD curves selected by the user


    :type selectedvalue: string
    :param selectedvalue: curve selected by the user

    :type sesid: string
    :param sesid: session ID of the active user

    :type curveinput: string
    :param curveinput: name of the selected FD curve

    :type figure: string
    :param figure: data from the currently displayed curves
    
    """
    if curveinput is not None:
        dataset = db.exps[sesid]
        curvename = curveinput['props']['children']
        pathfound = False
        while pathfound == False:
            for element in dataset.displaypaths:
                if element != []:
                    for value in element:
                        path = value.split('/')
                        if path[-1] == curvename:
                            sample_name = path[0]
                            set_name = path[1]
                            curve_name = path[2]
                            pathfound = True
        
        if selectedvalue == 'True':
            dataset.samples[sample_name].sets[set_name].indents[curve_name].filtered = True
            print('made true')
        else:
            dataset.samples[sample_name].sets[set_name].indents[curve_name].filtered = False
            print('made false')
    




'''
def display_click_data(clickData):
    print('2')

    return json.dumps(clickData, indent=2)
'''
'''
@app.callback(
    Output('one', 'children'),
    [Input("expname", "value")]
)
def experiment_name(value):
    print(value)
    current.assignexperiment(value)
    return u'Experiment Name: {}'.format(value)
'''

@app.callback(
    Output("samname", 'children'),
    [Input("samname", "value")]
)
def sample_name(value):
    """
    Loads the uploaded sample name into the Prep data structure

    :type value: string
    :param value: name of the uploaded sample

    """
    current.assignsampname(value)



@app.callback(
    Output('two', 'children'),
    [Input("setname", "value")]
)
def set_name(value):
    """
    Loads the uploaded set name into the Prep data structure

    :type value: string
    :param value: name of the uploaded set

    """
    current.assignsetname(value)

'''
@app.callback(
    Output("output", "children"),
    [Input("input2", "value")],
)
def update_output2(input2):
    #create the experiment object
    return u'Experiment Name: {}'.format(input2)


@app.callback(Output("loading-output-1", "children"), [Input("upload-data", "contents")])
def input_triggers_spinner(value):
    time.sleep(1)
    return None

@app.callback(Output("loading-output-2", "children"), [Input("output-data-upload", "children")])
def input_triggers_spinner(value):
    time.sleep(1)
    return None
'''


dispaycurves = [ ]




@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
              Input('sessionid', 'children')],
              State('upload-data', 'filename'),
               State('upload-data', 'last_modified'),
               State('filetype', 'value'),)
def update_output(list_of_contents, sesid, list_of_names, list_of_dates, filetype):
    """
    returns the main FD curve graph

    :type list_of_contents: string
    :param list_of_contents: list of uploaded data by the user

    :type sesid: string
    :param sesid: ID of the active user

    :type list_of_names: string
    :param list_of_names: list of uploaded file names

    :type list_of_dates: string
    :param list_of_dates: list of dates from uploaded files

    :type filetype: string
    :param filetype: the type of AFM vendor file uploaded onto the prep page

    """
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

                
                zip_obj.extractall('apps/converted/' + sesid + '/')
                uploaded_folders = os.listdir('apps/converted/' + sesid + '/')
                for element in uploaded_folders:
                    if element != '__MACOSX':
                        test.assignname(element)
                        for root, dirs, files in os.walk('apps/converted/' + sesid + '/' + element, topdown=False):
                            for name in files:
                                #print(os.path.join(root, name))
                                name = os.path.join(root, name)
                                print(name, 'this is name')
                                if name.split('.')[-1] == 'txt' or name.split('.')[-1] == 'jpk-force':
                                    if  name.split('/')[2] != '' and name.split('/')[-1] != '.DS_Store':
                                        #do same thing but with objects and 2 lists
                                        #print(name.split('/')[-3])
                                        #print(name, 'full name')
                                        
                                        if name.split('/')[-3] not in test.samples.keys():
                                            test.addsample(name.split('/')[-3])
                                        
                                        if name.split('/')[-2] not in test.samples[name.split('/')[-3]].sets.keys():
                                            test.samples[name.split('/')[-3]].addset(name.split('/')[-2])
                                        if name.split('/')[-1] not in test.samples[name.split('/')[-3]].sets[name.split('/')[-2]].indents.keys():
                                            #print(filetype, 'this is filetype')
                                            test.samples[name.split('/')[-3]].sets[name.split('/')[-2]].addindent(name.split('/')[-1], None, name, filetype)
                                            test.segments = test.samples[name.split('/')[-3]].sets[name.split('/')[-2]].indents[name.split('/')[-1]].segments 
                                            #test.segments = test.samples[name.split('/')[-3]].sets[name.split('/')[-2]].indents[name.split('/')[-1]].segments              
                shutil.rmtree('apps/converted/' + sesid + '/')
                        
                #return html.P('hello')                           
                #test.assignname(name.split('.')[0])
                #print('testing HELLOOOO')
                '''
                test.assignname(name.split('.')[0])
                out = ConvertOptics()
                x = 0
                for name in zip_obj.namelist():
                    x+= 1
                    if name.split('.')[-1] == 'txt':
                        if name.split('/')[0] != '__MACOSX' and name.split('/')[2] != '' and name.split('/')[2] != '.DS_Store':
                            #do same thing but with objects and 2 lists
                            #print(name.split('/')[1])
                            #print(name, 'full name')
                            if name.split('/')[1] not in test.samples.keys():
                                test.addsample(name.split('/')[1])
                            
                            if name.split('/')[2] not in test.samples[name.split('/')[1]].sets.keys():
                                test.samples[name.split('/')[1]].addset(name.split('/')[2])

                            if name.split('/')[3] not in test.samples[name.split('/')[1]].sets[name.split('/')[2]].indents.keys():
                                test.samples[name.split('/')[1]].sets[name.split('/')[2]].addindent(name.split('/')[3], zip_obj, name, filetype)
                                test.segments = test.samples[name.split('/')[1]].sets[name.split('/')[2]].indents[name.split('/')[3]].segments
                '''
            #print(test.samples)
            #print(test.samples['Rubber'], test.samples['Rubber'].sets['Day2'].indents )
            #test.outputdata()

            

        else:
            children = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)] 
            #return children
    #return None, None
    
    

def parse_contents(contents, filename, date):
    """
    parses specific files and load them into the prep data structure

    :type contents: string
    :param contents: contents from uploaded file

    :type filename: string
    :param filename: name of file

    :type date: string
    :param date: date of uploaded file

    """

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    print(decoded[0:110])
    current.assignfilename(filename)
    current.loaddata(decoded)
    print(filename)
    current.loadheader(decoded)
    #current.createfile()

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        html.Hr(),  # horizontal line
    ])

all_files = []

def displayfunction(displaypaths):
    """
    Sets displayed flags in main prep data structure

    :type displaypaths: string
    :param displaypaths: exact path to the FD curve being displayed
    
    
    """
    if displaypaths != []:
        samplename = displaypaths[0].split('/')[0]
        setname = displaypaths[0].split('/')[1]
        filenames = []
        for element in displaypaths:
            filenames.append(element.split('/')[2])
        print(filenames)

        for indent in test.samples[samplename].sets[setname].indents.values():
            if indent.name in filenames:
                indent.displayflag = True
            else:
                indent.displayflag = False




@app.callback(
    Output('test1', 'value'),
    [Input('button1', 'n_clicks'),
    Input('sessionid', 'children')],
    [State("test1", "options")]
)
def first(n_clicks, sesid, options):
    """
    Selects all of the curves displayed in first section of the data overview feature.

    :type n_clicks: int
    :param n_clicks: number of times the button has been selected
    
    :type sesid: string
    :param sesid: the session ID of the active user

    :type options: array
    :param options: the possible FD curves that can be displayed

    """
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
    """
    Selects one of the curves displayed in first section of the data overview feature.

    :type val: int
    :param val: number of times the button has been selected

    :type value: string
    :param value: the value of the selected FD curve

    :type sesid: string
    :param sesid: the session ID of the active user

    """
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
    """
    Selects all of the curves displayed in second section of the data overview feature.

    :type n_clicks: int
    :param n_clicks: number of times the button has been selected
    
    :type sesid: string
    :param sesid: the session ID of the active user

    :type options: array
    :param options: the possible FD curves that can be displayed

    """
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
    """
    Selects one of the curves displayed in first section of the data overview feature.

    :type val: int
    :param val: number of times the button has been selected

    :type value: string
    :param value: the value of the selected FD curve

    :type sesid: string
    :param sesid: the session ID of the active user

    """
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
    """
    Selects all of the curves displayed in third section of the data overview feature.

    :type n_clicks: int
    :param n_clicks: number of times the button has been selected
    
    :type sesid: string
    :param sesid: the session ID of the active user

    :type options: array
    :param options: the possible FD curves that can be displayed

    """
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
    """
    Selects one of the curves displayed in first section of the data overview feature.

    :type val: int
    :param val: number of times the button has been selected

    :type value: string
    :param value: the value of the selected FD curve

    :type sesid: string
    :param sesid: the session ID of the active user

    """
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
    """
    Selects all of the curves displayed in fourth section of the data overview feature.

    :type n_clicks: int
    :param n_clicks: number of times the button has been selected
    
    :type sesid: string
    :param sesid: the session ID of the active user

    :type options: array
    :param options: the possible FD curves that can be displayed

    """
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
    """
    Selects one of the curves displayed in first section of the data overview feature.

    :type val: int
    :param val: number of times the button has been selected

    :type value: string
    :param value: the value of the selected FD curve

    :type sesid: string
    :param sesid: the session ID of the active user

    """
    test = db.exps[sesid]
    print('value from template First', value)
    test.displaypaths[3] = value



'''

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
'''
prev = None

@app.callback(
    [Output("overviewgraph", 'figure'),
    Output('slidervalue', 'value')],
    [Input("slider", 'value'),
    Input('segmentselector', 'value'),
    Input('select-experiment', 'n_clicks'),
    Input('sessionid', 'children'),
    Input('res', 'value'),
    Input('filtervalue', 'value')]
)
def return_graph(value, segment, new, sesid, resolution, filtervalue):
    """
    Returns the main graphical component of the Prep page

    :type value: int
    :param value: value selected by the user through the slider

    :type segment: string
    :param segment: selected segments

    :type new: int
    :param new: triggers update if new segment selected

    :type sesid: string
    :param sesid: the session ID of the active user

    :type resolution: string
    :param resolution: selected resolution by the user

    :type filtervalue: int
    :param filtervalue: value of the automatic threshold filter

    """
    test = db.exps[sesid]
    print(new, 'test here')  
    info = []
    n = 0
    top = 100
    yaxismax = 1
    tic1 = time.process_time()
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
                            if resolution == 'reduced':
                                info.append(go.Scattergl(x=indent.piezo[test.forwardseg][0::10], y=indent.load[test.forwardseg][0::10], name=indent.name, line=test.availablecolors[n], showlegend=False))
                                print('reduced reg is up')
                            else:
                                info.append(go.Scattergl(x=indent.piezo[test.forwardseg], y=indent.load[test.forwardseg], name=indent.name, line=test.availablecolors[n], showlegend=False))
                            
                            yaxismax = max(indent.load[test.forwardseg])
                            yaxismin = min(indent.load[test.forwardseg])
                            xaxismax = max(indent.piezo[test.forwardseg])
                            xaxismin = min(indent.piezo[test.forwardseg])
                            
                            print(filtervalue, 'filtered value ')
                            print(yaxismax, 'max')

                            if filtervalue > yaxismax:
                                indent.filtered = False
                            else:
                                indent.filtered = True

                            
                            

                        if 'backward' in segment:
                            
                            yaxismax = max(indent.load[test.backwardseg])
                            yaxismin = min(indent.load[test.backwardseg])
                            xaxismin = min(indent.piezo[test.backwardseg])
                            xaxismax = max(indent.piezo[test.backwardseg])
                            
                            if resolution == 'reduced':
                                info.append(go.Scatter(x=indent.piezo[test.backwardseg][0::10], y=indent.load[test.backwardseg][0::10], name=indent.name, showlegend=False, line=test.availablecolors[n]))
                            else:
                                info.append(go.Scatter(x=indent.piezo[test.backwardseg], y=indent.load[test.backwardseg], name=indent.name, showlegend=False, line=test.availablecolors[n]))
                            
                            if filtervalue > yaxismax:
                                indent.filtered = False
                            else:
                                indent.filtered = True

                n+=1 

                if value is not None:                    
                    info.append(go.Scattergl(x=list(range(int(xaxismin),int(xaxismax)))[0::10], y=np.full(int(xaxismax), (yaxismax/100)*value)[0::10], name='Threshold', showlegend=False, line = dict(color='#E44236')))
                                        

    fig = go.Figure(data=info)
    

    fig.update_layout(
        title="Experiment Overview",
        xaxis_title='Displacement [nm]',
        yaxis_title='Load [nN]',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD',
    )

    if value is None:
        out = 0
    else:
        out = ((yaxismax/100)*value)


    return fig, out