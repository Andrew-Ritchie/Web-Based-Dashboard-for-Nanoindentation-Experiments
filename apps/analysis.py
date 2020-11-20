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
from app import app, cache
from apps.kaggle2 import KaggleAPI
from apps.kaggle2 import DataProcessor
from dash.exceptions import PreventUpdate
from apps.anlysisfunctions import ContactPoint
from apps.anlysisfunctions import Filters
from apps.anlysisfunctions import YoungsModulus

import numpy as np
import scipy.signal
from scipy.optimize import curve_fit

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



login = html.Div([
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
    print(name)
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


@app.callback(
    dash.dependencies.Output('availabledata', 'children'),
    [dash.dependencies.Input("downloadbutton", "n_clicks"),
     dash.dependencies.Input("username", "value")],
     [dash.dependencies.State("availabledatasets", "value"),
     dash.dependencies.State('rawdata', 'value')]
)
def pushdataview(clicks, username, selecteddata, rawdata):
    print(rawdata, 'rawdata')
    if clicks != 0:
        datasets.download_data(selecteddata.split('*')[0], username) 
        overview = process.getsets('andrewritchie98')
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
def sample2button(n_clicks, options):
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


indentation = html.Div(id='indentationdiv', children=[
            html.H2("Calculated Indentation"),
            dcc.Graph(id='calindentation',
                  style={'float':'left', 'width':'65%', 'padding':'1%', 'bgcolor': 'black'}, 
                  config={'displayModeBar':False},
                  ),
            
            html.Div([
                html.Br(),
                html.H1(' '),
            ])
            
            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})

@app.callback(
    dash.dependencies.Output('calindentation', 'figure'),
    [dash.dependencies.Input("selectedfeatures", "value"),
     dash.dependencies.Input("currentusername", "value")],
    [dash.dependencies.State("cpindexes", "data"),
     dash.dependencies.State("savgoldata", "data")]
)
def indentationoutput(value, username, cpindexes, data):
    print(data.keys(), 'this is data keys')
    print(cpindexes, 'this is indexes')
    raw_data = process.uploadrawdata(username)
    info = []
    index = 0
    availablecolors = [dict(color='#E44236', width=1), dict(color='#3498DB',width=1), dict(color='#2ecc72',width=1), dict(color='#E74292',width=1), dict(color='#575E76', width=1), dict(color='#C7980A', width=1), dict(color='#F4651F', width=1), dict(color='#82D8A7', width=1), dict(color='#CC3A05', width=1)]
    #R is the tip radius
    R = 10.0
    def Hertz(x, E):
                x = np.abs(x)
                poisson = 0.5
                # Eeff = E*1.0e9 #to convert E in GPa to keep consistency with the units nm and nN
                return (4.0 / 3.0) * (E / (1 - poisson ** 2)) * np.sqrt(R * x ** 3)

    fit_indentation_value = 1500.0
    indmax = float(fit_indentation_value)
    
    for element in data.keys():
        expname = element.split('/')[0]
        sample = element.split('/')[1]
        sets = element.split('/')[2]
        for indent in list(data[element].keys()):
            indentation_array = YM.calculate_indentation(data[element][indent], raw_data[expname][sample][sets][indent]['piezo'][500:2500], cpindexes[element][indent])                
            print(len(indentation_array), len(data[element][indent]), 'TESTING THIS')
            info.append(go.Scattergl(x=indentation_array, y=data[element][indent][cpindexes[element][indent]:], line = availablecolors[index], name = indent, showlegend=False))
            print(data[element][indent][-2:]) 
            contactforce = np.array(data[element][indent][cpindexes[element][indent]:])
            ind = np.array(indentation_array)
            jj = np.argmin((ind-indmax)**2)
            popt, pcov = curve_fit(Hertz, ind[:jj], contactforce[:jj], p0=[1000.0 / 1e9], maxfev=100000)
            info.append(go.Scattergl(x=indentation_array[:jj], y=Hertz(indentation_array[:jj], *popt), line = dict(color='#01CBC6', width=1), name = indent, showlegend=False))

        index += 1
    
    fig = go.Figure(data=info)
    
    fig.update_layout(
        title="Indentation",
        xaxis_title='EM',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD',
        clickmode='event+select'
    )
    return fig



filter1 = html.Div(id='savgol', children=[
            html.H2("Savgol Filter"),
            dcc.Store(id='savgoldata', storage_type='session'),
            dcc.Input(id="savgolzwin", type="number", value=0)

            
            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})



@app.callback(
    dash.dependencies.Output('savgoldata', 'data'),
    [dash.dependencies.Input("slotorder", "value"),
    dash.dependencies.Input("savgolzwin", "value"),
    dash.dependencies.Input("currentusername", "value"),
    dash.dependencies.Input("sample1", "value"),
    dash.dependencies.Input("sample2", "value")],)
def savgol(order, win, username, sample1, sample2):
    raw_data = process.uploadrawdata(username)
    selected_data = sample1 + sample2
    data = {}
    for datapath in selected_data:
        expname = datapath.split('/')[0]
        sample = datapath.split('/')[1]
        sets = datapath.split('/')[2]
        for indent in list(raw_data[expname][sample][sets].keys()):
            force = filters.savgol(raw_data[expname][sample][sets][indent]['load'][500:2500], raw_data[expname][sample][sets][indent]['piezo'][500:2500] )
            if datapath in data.keys():
                data[datapath][indent] = force
            else:
                data[datapath] = {}
    print(data)
    return data
    
elasticmod = html.Div(id='elasticmod', children=[
            html.H2("Elastic Modulus"),
            dcc.Input(id="savgolzwin", type="number", value=0),
            dcc.Graph(id='elasticmodgraph',
                  style={'float':'left', 'width':'65%', 'padding':'1%', 'bgcolor': 'black'}, 
                  config={'displayModeBar':False},
                  ),
            html.Div([
                html.Br()
            ])
            
            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})

YM = YoungsModulus()

@app.callback(
    dash.dependencies.Output('elasticmodgraph', 'figure'),
    [dash.dependencies.Input("selectedfeatures", "value"),
     dash.dependencies.Input("currentusername", "value")],
    [dash.dependencies.State("cpindexes", "data"),
     dash.dependencies.State("savgoldata", "data")]
)
def youngs(value, username, cpindexes, data):
    print(data.keys(), 'this is data keys')
    print(cpindexes, 'this is indexes')
    raw_data = process.uploadrawdata(username)
    info = []
    x = []
    numberofindents = 0

    for element in data.keys():
        expname = element.split('/')[0]
        sample = element.split('/')[1]
        sets = element.split('/')[2]
        for indent in list(data[element].keys()):
            indentation_array = YM.calculate_indentation(data[element][indent], raw_data[expname][sample][sets][indent]['piezo'][500:2500], cpindexes[element][indent])
            elasticity = YM.fitHertz(indentation_array, data[element][indent], cpindexes[element][indent], tipradius=10e-6, fit_indentation_value=800)
            x.append(elasticity)
            print(elasticity, 'elasticity')
            numberofindents += 1
    if (numberofindents % 2) == 1:
        numberofindents += 1
    
    info.append(go.Histogram(x=x, nbinsx=int(numberofindents/2)))
    
    fig = go.Figure(data=info)
    
    fig.update_layout(
        title="Elastic Modulus Histogram",
        xaxis_title='EM',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD',
        clickmode='event+select'
    )
    return fig


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
            dcc.Input(id="athreshold", type="number", value=0.1),
            html.H4('Fthreshold', style={'text-indent':'0'}),
            dcc.Input(id="fthreshold", type="number", value=10.0),
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
    [dash.dependencies.State("savgoldata", "data")]
)
def data(value, username, test, sample1, sample2, athreshold, fthreshold, deltax, order, filter1):
    #print(data)
    print(deltax, 'delta')
    print(order)
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
                info.append(go.Scattergl(x=raw_data[expname][sample][sets][indent]['piezo'][500:2500], y=outdata[element][indent], line = availablecolors[index], name = indent, showlegend=False))
                cp = cpfunctions.calculate(outdata[element][indent], raw_data[expname][sample][sets][indent]['piezo'][500:2500], athreshold, fthreshold, deltax)
                info.append(go.Scattergl(mode='markers', x=[cp[0]], y=[cp[1]], showlegend=False, marker=dict(color='black', size=10)))
                cpindexes[element][indent] = cp[2]
            index += 1
    else:
        raw_data = process.uploadrawdata(username)
        data = process.uploadrawdata(username)
        availablecolors = [dict(color='#E44236', width=1), dict(color='#3498DB',width=1), dict(color='#2ecc72',width=1), dict(color='#E74292',width=1), dict(color='#575E76', width=1), dict(color='#C7980A', width=1), dict(color='#F4651F', width=1), dict(color='#82D8A7', width=1), dict(color='#CC3A05', width=1)]
        index = 0
        info = []

        selected_data = sample1 + sample2
        for datapath in selected_data:
            expname = datapath.split('/')[0]
            sample = datapath.split('/')[1]
            sets = datapath.split('/')[2]
            for indent in list(raw_data[expname][sample][sets].keys()):                
                info.append(go.Scattergl(x=raw_data[expname][sample][sets][indent]['piezo'][500:2500], y=raw_data[expname][sample][sets][indent]['load'][500:2500], line = availablecolors[index], name = indent, showlegend=False))
                cp = cpfunctions.calculate(raw_data[expname][sample][sets][indent]['load'][500:2500], raw_data[expname][sample][sets][indent]['piezo'][500:2500], athreshold, fthreshold, deltax)
                info.append(go.Scattergl(mode='markers', x=[cp[0]], y=[cp[1]], showlegend=False, marker=dict(color='black', size=10)))
            index += 1
    

    fig = go.Figure(data=info)
    
    fig.update_layout(
        title="Experimental Overview: Threshold Contact Point",
        xaxis_title='Displacement',
        yaxis_title='Load',
        plot_bgcolor='#DDDDDD',
        paper_bgcolor='#DDDDDD',
        clickmode='event+select'
    )
    print(cpindexes)
    return fig, cpindexes


        


accessfeatures = { 'overview':overview, 'filter1':filter1, 'inspect':inspect, 'elasticmod': elasticmod, 'indentation':indentation }


#---------------------------------------------------------------------------------------------------------------------------------------






features = html.Div([
    html.H2("Features", style={'text-align': 'center'}),
    dcc.Checklist(
                id = 'selectedfeatures',
                options=[{'label': 'Overview', 'value': 'overview'},
                         {'label': 'Filter1', 'value': 'filter1'},
                         {'label': 'inspect', 'value': 'inspect'},
                         {'label': 'elasticmod', 'value': 'elasticmod'},
                        {'label': 'indentation', 'value': 'indentation'}],
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

        html.Div(id='slot1', children=[
        ]),
        html.Div(id='slot2', children=[
        ]),
        html.Div(id='slot3', children=[
        ])
    ], style=MAIN_STYLE),
])

