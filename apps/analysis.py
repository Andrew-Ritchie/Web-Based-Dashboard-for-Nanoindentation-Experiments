import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import json
import plotly.express as px


from dash.dependencies import Input, Output


x = [1,2,3,4,5,6,7,8,9,10]
y = [1,2,3,4,5,6,7,8,9,10]
z = [1,2,3,4,5,2,3,8,9,10]
plot = []
with open('apps/converted/Experiment_1.txt') as json_file:
    data = json.load(json_file)
    for element in data['Experiment_1'].keys():
        plot.append(data['Experiment_1'][element]['results']['Indentation'][0:6287])
    

fig = px.line(x=data['Experiment_1']['2NapFF 16mgmL GdL S-1 X-1 Y-1 I-1.txt']['results']['Time'][0:6287], y=plot, title='Example Analysis Graph')
fig.update_xaxes(title_text='Time')
fig.update_yaxes(title_text='Indentation')
layout = html.Div(children=[
    dcc.Graph(figure=fig)
],style={'float': 'right'})