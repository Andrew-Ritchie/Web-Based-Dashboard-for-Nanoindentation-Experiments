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
from dash.exceptions import PreventUpdate
from apps.anlysisfunctions import ContactPoint
from apps.anlysisfunctions import Filters
from apps.anlysisfunctions import YoungsModulus
import dash_table
import numpy as np
import scipy.signal
from scipy.optimize import curve_fit
from apps.prepare import current

"""
This script creates the analysis page.
"""

# setting up CSS for consistent style throuhout the page
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
  'padding-bottom': '100%',
  "maxHeight": "400px", 
  "overflow": "scroll"
}

opts = []
#------------------------------------------------------------------------------------------------------------------------------------
#Login section of sidebar
datasets = KaggleAPI()
process = DataProcessor()
cpfunctions = ContactPoint()
filters = Filters()



#HTML for the log in section of the Analysis page
login =  html.Div([
            html.H2("Log In", style={'text-align': 'center'}),
            dcc.Input(id="username", type="text", placeholder="User Name", debounce=True),
            dcc.Input(id="key", type="password", placeholder="Key", debounce=True),
            html.Button('Login', id='loginbutton', n_clicks=0, style={'float':'right', 'box-sizing':'border-box', 'margin-right':'2%'}),
            html.Br(),
            html.Div(id='currentusername', style={'display': 'none'}),
            #dcc.Store(id='rawdata'),
            html.Div(id='rawdata', style={'display': 'none'}),


            html.H2('')


        ], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})

@app.callback(
    dash.dependencies.Output('currentusername', 'value'),
    [dash.dependencies.Input("loginbutton", "n_clicks"),
     dash.dependencies.Input("username", "value")]
)
def saveusername(clicks, name):
    """
    Save the username inserted by the user

    :type clicks: int
    :param clicks: number of times the user has selected the log in button

    :type name: string
    :param name: the username inserted by the user
    
    """
    if clicks != 0 and name is not None:
        return name


'''
@app.callback(
    dash.dependencies.Output('rawdata', 'data'),
    [dash.dependencies.Input("downloadbutton", "n_clicks"),
    dash.dependencies.Input("currentusername", "value")]
)
def uploaddata(clicks, username):
    if clicks != 0:
        print('AHHHHHHH')
        print(username + 'test')
        data = process.uploadrawdata(username)
        return data
'''



@app.callback(
    dash.dependencies.Output('availabledatasets', 'options'),
    [dash.dependencies.Input("loginbutton", "n_clicks"),
    dash.dependencies.Input("username", "value"),
    dash.dependencies.Input("key", "value")],
)
def getdata(button, name, key):
    """
    load the sets of FD curves from Kaggle

    :type button: int
    :param button: number of times the user has selected the log in button

    :type name: string
    :param name: the username of the user performing the action
    
    :type key: string
    :param key: the user's Kaggle key
    """    
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
    """
    lets the user review datasets metadata before downloading it from Kaggle

    :type value: string
    :param value: the value of the dataset selected by the user
    """
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

#HTML to display the possible datasets the user can download from Kaggle
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


@app.callback(
    dash.dependencies.Output('availabledata', 'children'),
    [dash.dependencies.Input("downloadbutton", "n_clicks"),
     dash.dependencies.Input("username", "value")],
     [dash.dependencies.State("availabledatasets", "value"),
     dash.dependencies.State('rawdata', 'value')]
)
def pushdataview(clicks, username, selecteddata, rawdata):
    """
    load the sets of FD curves from Kaggle

    :type clicks: int
    :param clicks: number of times the user has selected the download button

    :type name: string
    :param name: the username of the user performing the action
    
    :type selecteddata: string
    :param selecteddata: the selected dataset to download from Kaggle

    :type rawdata: string
    :param rawdata: any data already download from Kaggle
    """
    if clicks != 0:
        datasets.download_data(selecteddata.split('*')[0], username) 
        overview = process.getsets(username)
        expname = list(overview.keys())[0]
        samples = overview[expname].keys()
        output = []
        index = 1
        for element in samples:
            opts = []
            for sets in overview[expname][element]:
                opts.append({'label': sets, 'value': expname + '/' + element + '/' + sets})
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
    """
    lets the user selected which sets to display from the first sample

    :type n_clicks: int
    :param n_clicks: number of times the user has selected the first sample button

    :type options: array
    :param options: list of sets within a sample
    """
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
def sample2button(n_clicks, options):
    """
    lets the user selected which sets to display from the second sample

    :type n_clicks: int
    :param n_clicks: number of times the user has selected the second sample button

    :type options: array
    :param options: list of sets within a sample
    """
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
    return all_or_none



#---------------------------------------------------------------------------------------------------------------------------------------
#HTML for the resolution section of the Analysis page
workflow = html.Div([
    html.H2("Resolution", style={'text-align': 'center'}),
    dcc.RadioItems(
    id='resolution',
    options=[
        {'label': 'Full', 'value': 'full'},
        {'label': 'Reduced', 'value': 'reduced'},
    ],
    labelStyle={'display': 'block', 'margin':'0%'},
    value='reduced', 
    style={'width': '100%', 'margin-left': '1%', 'padding':'0%'}),

    html.Br(),
    

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black'})



#---------------------------------------------------------------------------------------------------------------------------------------
#HTML for the overview feature on the Analysis page
overview = html.Div([
            html.H2("Overview"),
            html.Div(id='info', style = {'margin':'0%', 'padding':'0%'}),

            html.Br(),
            html.H1(' '),



            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})


#HTML for the indentation feature on the Analysis page
indentation = html.Div(id='indentationdiv', children=[
            html.H2("Calculated Indentation"),
            dcc.Graph(id='calindentation',
                  style={'float':'left', 'width':'65%', 'padding':'1%', 'bgcolor': 'black'}, 
                  config={'displayModeBar':False},
                  ),
            html.Div([     
            html.P('Indentation Fit Value', style={'text-indent':'0'}),
            dcc.Input(
                    id="indentationvalue", type="number",
                    debounce=True, placeholder="Debounce True", value= 1500,
                    style={'float':'left', 'indent':'0' }
                ),
            ]),
            html.Div(id='fitv', children=[
                html.Br(),
                html.H1(' '),
            ])
            
            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})

@app.callback(
    dash.dependencies.Output('calindentation', 'figure'),
    [dash.dependencies.Input("selectedfeatures", "value"),
     dash.dependencies.Input("currentusername", "value"),
     dash.dependencies.Input("indentationvalue", "value")],
    [dash.dependencies.State("cpindexes", "data"),
     dash.dependencies.State("savgoldata", "data"),
     dash.dependencies.State("resolution", "value")]
)
def indentationoutput(value, username, indentationvalue, cpindexes, data, resolution):
    """
    returns indentation data for the indentation feature of the analysis page

    :type value: string
    :param value: selected feature by the user

    :type username: string
    :param username: username of the active user

    :type indentationvalue: int
    :param indentationvalue: value that determines how far up the indentation curve will be analysised

    :type cpindexes: tuple
    :param cpindexes: the value of the detected CPs

    :type data: array
    :param data: any filtered data

    :type resolution: string
    :param resolution: the tye of resolution selected by the user
    """
    raw_data = process.uploadrawdata(username)
    cantileverk = raw_data['metadata']['cantileverk']
    tipradius = raw_data['metadata']['tipradius']
    info = []
    index = 0
    availablecolors = [dict(color='#E44236', width=1), dict(color='#3498DB',width=1), dict(color='#2ecc72',width=1), dict(color='#E74292',width=1), dict(color='#575E76', width=1), dict(color='#C7980A', width=1), dict(color='#F4651F', width=1), dict(color='#82D8A7', width=1), dict(color='#CC3A05', width=1)]
    #R is the tip radius
    R = tipradius
    def Hertz(x, E):
                x = np.abs(x)
                poisson = 0.5
                # Eeff = E*1.0e9 #to convert E in GPa to keep consistency with the units nm and nN
                return (4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)

    fit_indentation_value = indentationvalue
    indmax = float(fit_indentation_value)
    
    for element in data.keys():
        expname = element.split('/')[0]
        sample = element.split('/')[1]
        sets = element.split('/')[2]
        for indent in list(cpindexes[element].keys()):
            indentation_array = YM.calculate_indentation(data[element][indent], raw_data[expname][sample][sets][indent]['piezo'], cpindexes[element][indent], cantileverk)                
            print(len(indentation_array), len(data[element][indent]), 'TESTING THIS')
            print(data[element][indent][-2:])
            
            contactforce = np.array(data[element][indent][cpindexes[element][indent]:]) - data[element][indent][cpindexes[element][indent]]
            
            if resolution == 'reduced':
                info.append(go.Scattergl(x=indentation_array[0::10], y=contactforce[0::10], line = availablecolors[index], name = indent, showlegend=False))
            else:
                info.append(go.Scattergl(x=indentation_array, y=contactforce, line = availablecolors[index], name = indent, showlegend=False))

            ind = np.array(indentation_array)
            jj = np.argmin((ind-indmax)**2)
            popt, pcov = curve_fit(Hertz, ind[:jj], contactforce[:jj], p0=[1000.0 / 1e9], maxfev=100000)
            info.append(go.Scattergl(x=indentation_array[:jj], y=Hertz(indentation_array[:jj], *popt), line = dict(color='#01CBC6', width=1), name = indent, showlegend=False))

        index += 1
    
    fig = go.Figure(data=info)
    
    fig.update_layout(
        title="Indentation",
        xaxis_title='Indentation [nm]',
        yaxis_title='Load [nN]',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD',
        clickmode='event+select'
    )
    return fig


#HTML for the savgol filter feature
filter1 = html.Div(id='savgol', children=[
            html.H2("Savgol Filter"),
            dcc.Store(id='savgoldata', storage_type='session'),
            html.P('Displacement Window', style={'float':'left', 'text-indent':'0'}),
            dcc.Input(id="savgolzwin", type="number", value=21)

            
            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})



@app.callback(
    dash.dependencies.Output('savgoldata', 'data'),
    [dash.dependencies.Input("slotorder", "value"),
    dash.dependencies.Input("savgolzwin", "value"),
    dash.dependencies.Input("currentusername", "value"),
    dash.dependencies.Input("sample1", "value"),
    dash.dependencies.Input("sample2", "value")])
def savgol(order, win, username, sample1, sample2):
    """
    returns filter FD data

    :type value: array
    :param value: order of selected features by the user

    :type win: int
    :param win: the window value of the filter

    :type username: string
    :param username: username of the active user


    :type sample1: string
    :param sample1: data from the first sample

    :type sample2: string
    :param sample2: data from the second sample

    """
    raw_data = process.uploadrawdata(username)
    #selected_data = sample1 + sample2
    if sample2 is not None:
        selected_data = sample1 + sample2
    else:
        selected_data = sample1
    data = {}
    for datapath in selected_data:
        print(datapath)
        expname = datapath.split('/')[0]
        sample = datapath.split('/')[1]
        sets = datapath.split('/')[2]
        for indent in list(raw_data[expname][sample][sets].keys()):
            force = filters.savgol(raw_data[expname][sample][sets][indent]['load'], raw_data[expname][sample][sets][indent]['piezo'] )
            if datapath in data.keys():
                print('is this ture')
                data[datapath][indent] = force
            else:
                data[datapath] = {}
                data[datapath][indent] = force
    print(data, 'this is our filtered data')
    return data


#HTML for the YM feature in the analysis page
elasticmod = html.Div(id='elasticmod', children=[
            html.H2("Elastic Modulus"),
            #dcc.Input(id="savgolzwin", type="number", value=0),
            dcc.Graph(id='elasticmodgraph',
                  style={'float':'left', 'width':'65%', 'padding':'1%', 'bgcolor': 'black'}, 
                  config={'displayModeBar':False},
                  ),
            html.Div([
                dash_table.DataTable(
                id='table',
                style_header={'backgroundColor': '#AFAFAF'},
                style_cell={
                    'textAlign': 'left',
                    'backgroundColor': '#DDDDDD',
                    'color': 'black'
                },
                style_cell_conditional=[
                        {
                            'if': {'column_id': 'Region'},
                            'textAlign': 'left'
                        }
                ]
                )
            ], style={'float':'left', 'width':'65%', 'padding':'1%', 'bgcolor': 'black'}),
            
            html.Div([
                html.Br()
            ])
            
            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})

YM = YoungsModulus()

@app.callback(
    [dash.dependencies.Output('elasticmodgraph', 'figure'),
     dash.dependencies.Output('table', 'columns'),
     dash.dependencies.Output('table', 'data')],
    [dash.dependencies.Input("selectedfeatures", "value"),
     dash.dependencies.Input("currentusername", "value")],
    [dash.dependencies.State("cpindexes", "data"),
     dash.dependencies.State("savgoldata", "data")]
)
def youngs(value, username, cpindexes, data):
    """
    returns the calculated YM data

    :type value: array
    :param value: order of selected features by the user

    :type username: string
    :param username: username of the active user

    :type cpindexes: tuple
    :param cpindexes: the index of the calculated contact point

    :type data: string
    :param data: filtered FD data
    """
    raw_data = process.uploadrawdata(username)
    cantileverk = raw_data['metadata']['cantileverk']
    tipradius = raw_data['metadata']['tipradius']
    info = []
    x = []
    numberofindents = 0
    caldata = {}

    for element in data.keys():
        expname = element.split('/')[0]
        sample = element.split('/')[1]
        sets = element.split('/')[2]
        for indent in list(cpindexes[element].keys()):
            print(cpindexes[element][indent], 'cp indexesssss')
            print(cantileverk, 'this is k value')
            indentation_array = YM.calculate_indentation(data[element][indent], raw_data[expname][sample][sets][indent]['piezo'], cpindexes[element][indent], cantileverk)
            elasticity = YM.fitHertz(indentation_array, data[element][indent], cpindexes[element][indent], tipradius, fit_indentation_value=300)
            caldata[indent] = elasticity
            x.append(elasticity)
            print(elasticity, 'elasticity')
            numberofindents += 1
    if (numberofindents % 2) == 1:
        numberofindents += 1
    
    info.append(go.Histogram(x=x, nbinsx=int(numberofindents/2)))
    
    fig = go.Figure(data=info)
    
    fig.update_layout(
        title="Elastic Modulus Histogram",
        xaxis_title='Youngs Modulus [Pa]',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD',
        clickmode='event+select'
    )
    cols = [{"name": 'filename', "id": 'filename'}, {"name": 'Youngs Modulus [Pa]', "id": 'ym'}]
    out = []
    for element in list(caldata.keys()):
        out.append({'filename':element, 'ym':round(caldata[element], 3)})

    return fig, cols, out

# HTML for the overview CP feature
inspect = html.Div([
    html.Div(id='inspect', children=[
        dcc.Store(id='savgoldata', storage_type='session'),

        dcc.Store(id='cpindexes', storage_type='session'),
        dcc.Graph(id='inspectgraph',
                  style={'float':'left', 'width':'65%', 'padding':'1%', 'bgcolor': 'black'}, 
                  config={'displayModeBar':False},
                  ),
        html.Div(children=[
            html.H4('Athreshold', style={'text-indent':'0'}),
            dcc.Input(id="athreshold", type="number", value=10),
            html.H4('Fthreshold', style={'text-indent':'0'}),
            dcc.Input(id="fthreshold", type="number", value=100.0),
            html.H4('Deltax', style={'text-indent':'0'}),
            dcc.Input(id="deltax", type="number", value=2000.0),

        ], style = {'float':'left', 'padding-top':'10%'}),
        


        html.Br()
    ], style = {'margin':'0%', 'padding':'0%'}),

], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})

@app.callback(
    [dash.dependencies.Output('inspectgraph', 'figure'),
     dash.dependencies.Output("cpindexes", "data")],
    [dash.dependencies.Input("selectedfeatures", "value"),
     dash.dependencies.Input("currentusername", "value"),
     dash.dependencies.Input("inspectgraph", "value"),
     dash.dependencies.Input("sample1", "value"),
     dash.dependencies.Input("sample2", "value"),
     dash.dependencies.Input("athreshold", "value"),
     dash.dependencies.Input("fthreshold", "value"),
     dash.dependencies.Input("deltax", "value"),
     dash.dependencies.Input("selectedfeatures", "value")],
    [dash.dependencies.State("savgoldata", "data"),
    dash.dependencies.State("resolution", "value")]
)
def data(value, username, graph, sample1, sample2, athreshold, fthreshold, deltax, order, filter1, resolution):
    """
    returns the calculated CP and displays them on the inspection graph

    :type value: array
    :param value: value selected feature by the user

    :type username: string
    :param username: username of the active user

    :type graph: dict
    :param graph: the data held currently by the inspect graph

    :type sample1: string
    :param sample1: name of the first sample being inspected

    :type sample2: string
    :param sample2: name of the second sample being inspected

    :type athreshold: int
    :param athreshold: CP value selected by the user

    :type fthreshold: int
    :param fthreshold: CP value selected by the user

    :type deltax: int
    :param deltax: CP value selected by the user

    :type order: array
    :param order: order of features selected by the user

    :type filter1: array
    :param filter1: filtered FD data

    :type resolution: string
    :param resolution: resolution option selected by the user
    """
    y = order.index('inspect')
    
    raw_data = process.uploadrawdata(username)
    info = []
    availablecolors = [dict(color='#E44236', width=1), dict(color='#3498DB',width=1), dict(color='#2ecc72',width=1), dict(color='#E74292',width=1), dict(color='#575E76', width=1), dict(color='#C7980A', width=1), dict(color='#F4651F', width=1), dict(color='#82D8A7', width=1), dict(color='#CC3A05', width=1)]
    index = 0
    cpindexes = {}
    if y > 0:
        outdata = vars()[order[y-1]]
        #print(outdata, 'this is outdata')
        for element in outdata.keys():
            expname = element.split('/')[0]
            sample = element.split('/')[1]
            sets = element.split('/')[2]
            cpindexes[element] = {}
            for indent in list(outdata[element].keys()):
                print('fired!!!!')
                if resolution == 'reduced':
                    info.append(go.Scattergl(x=raw_data[expname][sample][sets][indent]['piezo'][0::10], y=outdata[element][indent][0::10], line = availablecolors[index], name = indent, showlegend=False))
                else:
                    info.append(go.Scattergl(x=raw_data[expname][sample][sets][indent]['piezo'], y=outdata[element][indent], line = availablecolors[index], name = indent, showlegend=False))

                cp = cpfunctions.calculate(outdata[element][indent], raw_data[expname][sample][sets][indent]['piezo'], athreshold, fthreshold, deltax)
                if cp is not None: 
                    info.append(go.Scattergl(mode='markers', x=[cp[0]], y=[cp[1]], showlegend=False, marker=dict(color='black', size=10)))
                    cpindexes[element][indent] = cp[2]
                    print(cp[0], cp[1], 'indexes')
                else:
                    print(indent, 'FAILEEDD')
                
            index += 1
    else:
        print('hellooooooo')
        raw_data = process.uploadrawdata(username)
        availablecolors = [dict(color='#E44236', width=1), dict(color='#3498DB',width=1), dict(color='#2ecc72',width=1), dict(color='#E74292',width=1), dict(color='#575E76', width=1), dict(color='#C7980A', width=1), dict(color='#F4651F', width=1), dict(color='#82D8A7', width=1), dict(color='#CC3A05', width=1)]
        index = 0
        info = []

        selected_data = sample1
        for datapath in selected_data:
            expname = datapath.split('/')[0]
            sample = datapath.split('/')[1]
            sets = datapath.split('/')[2]
            for indent in list(raw_data[expname][sample][sets].keys()):
                if resolution == 'reduced':                
                    info.append(go.Scattergl(x=raw_data[expname][sample][sets][indent]['piezo'][0::10], y=raw_data[expname][sample][sets][indent]['load'][0::10], line = availablecolors[index], name = indent, showlegend=False))
                else:
                    info.append(go.Scattergl(x=raw_data[expname][sample][sets][indent]['piezo'], y=raw_data[expname][sample][sets][indent]['load'], line = availablecolors[index], name = indent, showlegend=False))

                cp = cpfunctions.calculate(raw_data[expname][sample][sets][indent]['load'], raw_data[expname][sample][sets][indent]['piezo'], athreshold, fthreshold, deltax)
                info.append(go.Scattergl(mode='markers', x=[cp[0]], y=[cp[1]], showlegend=False, marker=dict(color='black', size=10)))
            index += 1
        
        print('DONE AND DUSTED')

    

    fig = go.Figure(data=info)
    
    fig.update_layout(
        title="Experimental Overview: Threshold Contact Point",
        xaxis_title='Displacement [nm]',
        yaxis_title='Load [nN]',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD',
        clickmode='event+select'
    )
    print(cpindexes)
    return fig, cpindexes

# stand alone overview contact point feature
overcp = html.Div([
    html.Div(id='inspect', children=[
        
        dcc.Graph(id='overcurves',
                  style={'float':'left', 'width':'65%', 'padding':'1%', 'bgcolor': 'black'}, 
                  config={'displayModeBar':False},
        ),
        dcc.Graph(id='cpgraph',style={'float':'left', 'width': '30%', 'padding': '1%'}, config={'displayModeBar':False}),
        html.Br(),
        
        html.Br(),
        dcc.Input(id='athresh', value=10, style={'float':'right'}),
        html.P('Athreshold', style={'text-indent':'0', 'float':'right'}),
        dcc.Input(id='fthresh', value=100, style={'float':'right'}),
        html.P('Fthreshold', style={'text-indent':'0', 'float':'right'}),
        dcc.Input(id='delta', value=2000, style={'float':'right', 'padding-right':'0'}),
        html.P('Delta', style={'text-indent':'0', 'float':'right'}),
        html.Br(),
        html.Br()
    ], style = {'margin':'0%', 'padding':'0%'}),

], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})

@app.callback(
    dash.dependencies.Output('overcurves', 'figure'),
     [dash.dependencies.Input("currentusername", "value"),
     dash.dependencies.Input("sample1", "value"),
     dash.dependencies.Input("sample2", "value")],
     dash.dependencies.State("resolution", "value"),
     )
def overviewgraph(username, sample1, sample2, resolution):
    """
    returns the stand alone overview contact point feature

    :type username: string
    :param username: username of the active user

    :type sample1: string
    :param sample1: name of the first sample being inspected

    :type sample2: string
    :param sample2: name of the second sample being inspected

    :type resolution: string
    :param resolution: resolution option selected by the user
    """
    raw_data = process.uploadrawdata(username)
    selected_data = sample1
    info = []
    availablecolors = [dict(color='#E44236', width=1), dict(color='#3498DB',width=1), dict(color='#2ecc72',width=1), dict(color='#E74292',width=1), dict(color='#575E76', width=1), dict(color='#C7980A', width=1), dict(color='#F4651F', width=1), dict(color='#82D8A7', width=1), dict(color='#CC3A05', width=1)]
    index = 0
    for datapath in selected_data:
        expname = datapath.split('/')[0]
        sample = datapath.split('/')[1]
        sets = datapath.split('/')[2]
        for indent in list(raw_data[expname][sample][sets].keys()):       
            if resolution == 'reduced':         
                info.append(go.Scattergl(x=raw_data[expname][sample][sets][indent]['piezo'][0::10], y=raw_data[expname][sample][sets][indent]['load'][0::10], line = availablecolors[index], name = indent, showlegend=False))            
            else:
                info.append(go.Scattergl(x=raw_data[expname][sample][sets][indent]['piezo'], y=raw_data[expname][sample][sets][indent]['load'], line = availablecolors[index], name = indent, showlegend=False))            
        
        index += 1

    fig = go.Figure(data=info)
    
    fig.update_layout(
        title="Experimental Overview",
        xaxis_title='Displacement [nm]',
        yaxis_title='Load [nN]',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD',
        clickmode='event+select'
    )
    return fig

@app.callback(
    dash.dependencies.Output('cpgraph', 'figure'),
     [dash.dependencies.Input("overcurves", "clickData"),
     dash.dependencies.Input("currentusername", "value"),
     dash.dependencies.Input('delta', 'value'),
     dash.dependencies.Input('athresh', 'value'),
     dash.dependencies.Input('fthresh', 'value')],
     [dash.dependencies.State('overcurves', 'figure'),
     dash.dependencies.State('resolution', 'value')])
def cpgraph(click_data, username, delta, athresh, fthresh, figure, resolution):
    """
    returns the cp graph for the CP overview feature feature

    :type click_data: dict
    :param click_data: information regarding the selected FD curve

    :type username: string
    :param username: username of the active user

    :type delta: int
    :param delta: CP value selected by the user

    :type athreshold: int
    :param athreshold: CP value selected by the user

    :type fthreshold: int
    :param fthreshold: CP value selected by the user

    :type deltax: int
    :param deltax: CP value selected by the user

    :type figure: dict
    :param figure: data displayed on the overview graph

    :type resolution: string
    :param resolution: resolution option selected by the user
    """
    raw_data = process.uploadrawdata(username)
    info = []
    if click_data is not None:
        #country_name = data['points'][0]['customdata']
        curve_number = click_data['points'][0]['curveNumber']
        trace_name = figure['data'][curve_number]['name']
        print(trace_name)
        if resolution == 'reduced':
            info.append(go.Scattergl(x=figure['data'][curve_number]['x'][0::10], y=figure['data'][curve_number]['y'][0::10], line = dict(color='#2ecc72',width=1), name = trace_name, showlegend=False))
        else:
            info.append(go.Scattergl(x=figure['data'][curve_number]['x'], y=figure['data'][curve_number]['y'], line = dict(color='#2ecc72',width=1), name = trace_name, showlegend=False))

        cp = cpfunctions.calculate(figure['data'][curve_number]['y'], figure['data'][curve_number]['x'], float(athresh), float(fthresh), float(delta))
        print(cp, 'this is CP')
        info.append(go.Scattergl(mode='markers', x=[cp[0]], y=[cp[1]], showlegend=False, marker=dict(color='black', size=10)))
        

    fig = go.Figure(data=info)
    
    fig.update_layout(
        title="Threshold Contact Point",
        xaxis_title='Displacement [nm]',
        yaxis_title='Load [nN]',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD',
        clickmode='event+select'
    )
    return fig

'''
@app.callback(
    dash.dependencies.Output('cpgraph', 'figure'),
     [dash.dependencies.Input("overcurves", "clickData"),
     dash.dependencies.Input("currentusername", "value")])
def cpgraph(click_data, username):
    raw_data = process.uploadrawdata(username)
    info = []
    if click_data is not None:
        print(click_data)
        #country_name = data['points'][0]['customdata']
        curve_number = click_data['points'][0]['curveNumber']
        trace_name = figure['data'][curve_number]['name']
        info.append(go.Scattergl(x=figure['data'][curve_number]['x'], y=figure['data'][curve_number]['y'], line = dict(color='#2ecc72',width=1), name = trace_name, showlegend=False))
        
        #cp = cpfunctions.calculate(figure['data'][curve_number]['y'], figure['data'][curve_number]['x'])
        #print(cp, 'this is CP')
        #info.append(go.Scattergl(mode='markers', x=[cp[0]], y=[cp[1]], showlegend=False, marker=dict(color='black', size=10)))
        

    fig = go.Figure(data=info)
    
    fig.update_layout(
        title="Experimental Overview: Threshold Contact Point",
        xaxis_title='Displacement [nm]',
        yaxis_title='Load [nN]',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD',
        clickmode='event+select'
    )
    return fig
'''
accessfeatures = { 'overview':overview, 'filter1':filter1, 'inspect':inspect, 'elasticmod': elasticmod, 'indentation':indentation, 'overcp': overcp }


#---------------------------------------------------------------------------------------------------------------------------------------




#Provided analysis features the user can select 
features = html.Div([
    html.H2("Features", style={'text-align': 'center'}),
    dcc.Checklist(
                id = 'selectedfeatures',
                options=[{'label': 'Overview', 'value': 'overview'},
                         {'label': 'Filter1', 'value': 'filter1'},
                         {'label': 'inspect', 'value': 'inspect'},
                         {'label': 'elasticmod', 'value': 'elasticmod'},
                        {'label': 'indentation', 'value': 'indentation'},
                        {'label': 'overcp', 'value': 'overcp'}],
                labelStyle={'display': 'block', 'margin':'0%'},
    ),
    html.Br()
    


], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})




@app.callback(
    dash.dependencies.Output('slot1', 'children'),
    [dash.dependencies.Input("selectedfeatures", "value")],
     [dash.dependencies.State("slot1", "children"),
     dash.dependencies.State("slotorder", "children")]

)
def displayfeature(value, slot1, slot1name): 
    """
    returns the first selected feature into the first slot of the dynamic feed

    :type value: string
    :param value: name of selected feature

    :type slot1: string
    :param slot1: state of the first slot

    :type slot1name: array
    :param slot1name: list of seleted features
    """
    output = []
    deleted = None
    if value is not None:
        if slot1name is not None:
            for element in slot1name:
                if element not in value:
                    deleted = slot1name.index(element)

        if len(value) == 1 and slot1 is None:
            output = accessfeatures[value[0]]
            slot1name = value[0]
            return output
        elif len(value) == 0 or deleted == 0:
            slot1 = None
        else:
            raise PreventUpdate

@app.callback(
    dash.dependencies.Output('slot2', 'children'),
    [dash.dependencies.Input("selectedfeatures", "value")],
    [dash.dependencies.State("slot2", "children"),
     dash.dependencies.State("slotorder", "children")]
)
def displayslot2(value, slot2, slot1name):
    """
    returns the second selected feature into the second slot of the dynamic feed

    :type value: string
    :param value: name of selected feature

    :type slot2: string
    :param slot2: state of the second slot

    :type slot2name: array
    :param slot2name: list of seleted features
    """
    output = []
    deleted = None
    if value is not None:
        if slot1name is not None:
            for element in slot1name:
                if element not in value:
                    deleted = slot1name.index(element)
        if len(value) == 2 and slot2 is None:
            output = accessfeatures[value[1]]
            slot1name = value[1]
            return output
        elif len(value) == 0 or deleted == 1:
            print('did we do this')
            slot2 = None
        else:
            raise PreventUpdate

@app.callback(
    dash.dependencies.Output('slot3', 'children'),
    [dash.dependencies.Input("selectedfeatures", "value")],
    [dash.dependencies.State("slot3", "children"),
    dash.dependencies.State("slotorder", "children")]
)
def displayslot3(value, slot3, slot1name):
    """
    returns the third selected feature into the third slot of the dynamic feed

    :type value: string
    :param value: name of selected feature

    :type slot3: string
    :param slot3: state of the first slot

    :type slot3name: array
    :param slot3name: list of seleted features
    """
    deleted = None
    if value is not None:
        if slot1name is not None:
            for element in slot1name:
                if element not in value:
                    deleted = slot1name.index(element)
        if len(value) == 3 and slot3 is None:
            output = accessfeatures[value[2]]
            slot1name = value[2]
            return output
        elif len(value) == 0 or deleted == 2:
            slot3 = None
        else:
            raise PreventUpdate


        
@app.callback(
    dash.dependencies.Output('slotorder', 'children'),
    [dash.dependencies.Input("selectedfeatures", "value")]

)
def updatepreval(value):
    """
    returns the selected features

    :type value: string
    :param value: name of selected feature
    """
    return value

      
   
layout = html.Div([
    html.Div([
        login,
        availbledata,
        features,
        workflow,
        

    ], style= SIDEBAR_STYLE),


    html.Div(id='analysismainfeed',children=[
        html.Div(id='slotorder', style={'display': 'none'}),
        html.Div(id='filtereddata', style={'display': 'none'}),
        html.Div(id='sample2', style={'display': 'none'}),
        html.Div(id='cantieverk', style={'display': 'none'}),
        html.Div(id='tipradius', style={'display': 'none'}),

        html.Div(id='slot1', children=[
        ]),
        html.Div(id='slot2', children=[
        ]),
        html.Div(id='slot3', children=[
        ])
    ], style=MAIN_STYLE),
])


