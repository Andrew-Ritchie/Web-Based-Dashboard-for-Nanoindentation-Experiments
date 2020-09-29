import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import json
import plotly.express as px
import os
from plotly.subplots import make_subplots
import plotly.graph_objs as go



from dash.dependencies import Input, Output
from app import app


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
  'border': '5px solid grey',
  'float': 'left',
}

plot = []
outdata = [
    {'x': [], 'y': [], }
]
def getdirectories():
    result = []
    for root, dirs, files in os.walk("/Users/andrew/Documents/Web-Based-Dashboard-for-Nanoindentation-Experiments/apps/converted/"):
        return files
test = getdirectories()

info = []
with open('apps/converted/Experiment_1.txt') as json_file:
    data = json.load(json_file)
    for element in data['Experiment_1'].keys():
        plot.append(data['Experiment_1'][element]['results']['Load'][500:2500])
        info.append(go.Scatter(x=data['Experiment_1'][element]['results']['Indentation'][500:2500], y=data['Experiment_1'][element]['results']['Load'][500:2500] , name=element))
    select = data['Experiment_1']['2NapFF 16mgmL GdL S-1 X-1 Y-1 I-1.txt']['results'].keys()


options = []
for i in select:
    options.append({'label':i, 'value':i})

df = [
    {'x':data['Experiment_1']['2NapFF 16mgmL GdL S-1 X-1 Y-1 I-1.txt']['results']['Indentation'][500:2500], 'y': data['Experiment_1']['2NapFF 16mgmL GdL S-1 X-1 Y-1 I-1.txt']['results']['Load'][500:2500], 'name':'Test'}
]


fig = go.Figure(data=info)
fig.update_layout(
    title="Experiment Overview",
    xaxis_title='Indentation',
    yaxis_title='Load'
)





layout = html.Div(children=[
    html.Div([
        html.H2("Sidebar"),
        html.H3(children=["Converted Files"], style={ 'textIndent': '15%'}),
        html.Ul([html.Li(x) for x in test], style={ 'textIndent': '15%'})
        ], 
        style=SIDEBAR_STYLE
    ),

    html.Div([
        dcc.Graph(figure=fig),
    ], style=MAIN_STYLE),
    html.Div([
        html.H2("Custom Plotting"),
        dcc.Graph(id='output-container'),
        dcc.Dropdown(
            id='dropdown',
            options= options,
            value="Indentation",
            style={'width':'50%', 'box-sizing':'border-box', 'float':'left'}
        ),
        dcc.Dropdown(
            id='dropdown2',
            options= options,
            value='Load',
            style={'width':'50%', 'box-sizing':'border-box', 'float':'left'}
        )
    ], style=MAIN_STYLE)

])

@app.callback(
    dash.dependencies.Output('output-container', 'figure'),
    [dash.dependencies.Input('dropdown', 'value'),
    dash.dependencies.Input('dropdown2', 'value')])
def update_output(dropdown_output, dropdown2_output):
    x_data = data['Experiment_1']['2NapFF 16mgmL GdL S-1 X-1 Y-1 I-1.txt']['results'][dropdown_output][500:2500]
    y_data = data['Experiment_1']['2NapFF 16mgmL GdL S-1 X-1 Y-1 I-1.txt']['results'][dropdown2_output][500:2500]
    fig2 = px.line(x=x_data, y=y_data)
    fig2.update_xaxes(title=dropdown_output)
    fig2.update_yaxes(title=dropdown2_output)
    return fig2



