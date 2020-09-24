import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import json
import plotly.express as px
import os

from dash.dependencies import Input, Output


plot = []

def getdirectories():
    result = []
    for root, dirs, files in os.walk("/Users/andrew/Documents/Web-Based-Dashboard-for-Nanoindentation-Experiments/apps/converted/"):
        return files
test = getdirectories()
with open('apps/converted/Experiment_1.txt') as json_file:
    data = json.load(json_file)
    for element in data['Experiment_1'].keys():
        plot.append(data['Experiment_1'][element]['results']['Load'][500:2500])
    

fig = px.line(x=data['Experiment_1']['2NapFF 16mgmL GdL S-1 X-1 Y-1 I-1.txt']['results']['Indentation'][500:2500], y=plot, title='Example Analysis Graph')
fig.update_xaxes(title_text='Indentation')
fig.update_yaxes(title_text='Load')
layout = html.Div(children=[
    dcc.Graph(figure=fig, style={'float': 'right'}),
    html.H3(children=["Converted Files"], style={ 'textIndent': '15%'}),
    html.Ul([html.Li(x) for x in test], style={ 'textIndent': '15%'})
])

