import dash
import dash_core_components as dcc
import dash_html_components as html
import os
from app import app
from dash.dependencies import Input, Output, State



#html for experiments
def getexperiments():
    exp = []
    for experiment in os.scandir('apps/converted'):
        if experiment.name.split('.')[-1] != 'txt':
            exp.append(experiment.name)
    return exp

test = getexperiments()


def template(expname, samname):
    opts = []
    for element in os.scandir('apps/converted/' + expname + '/' + samname):
        opts.append({'label': element.name, 'value': element.name})
    print(opts)
    return html.Div([
        html.Details(id='in', children=[
            html.Summary([
                samname,
            ]),
            html.Div(id='list', style={'padding-left':'10%'})]),
    ], style = {'padding-left':'5%'})

def populatesamples(name):
    temp = []
    for element in os.scandir('apps/converted/' + name):
        temp.append(template(name, element.name))
    return html.Div([
        html.Details([
            html.Summary([
                name,
            ], style={'background-color': 'blue'}),
            
        ] + temp),
    ])

def run(test):
    temp = []
    for element in test:
        temp.append(populatesamples(element))
    return temp


def test12(test, test2):
    return html.Details(id= 'my-input',children=[
            html.Summary([
                'Exp',
            ]),
            html.Div(id=test2,children=[
                html.Details([
                    html.Summary([
                        'Samp',
                    ]),
                dcc.Checklist(
                id = test,
                options=[{'label': 'Forward', 'value': test},
                        {'label': 'Backward', 'value': 'MT11L'}],
                labelStyle={'display': 'block', 'margin':'0%'},
            ),
            
            
            ]),
            ]),
            
        ])

def second():
    return html.Div([test12('checklist2', 'in2'), test12('check', 'in2')])

experimenttree = html.Div([
    second()
    ])

info = [Input('checklist2', 'value')]
out = []


def one():
    def checklist2(*input_values):
        print('value from template', input_values)
    checklist2()

@app.callback(
    Output('checklist2', 'children'),
    info
)
def checklist2(v):
        print('value from template', v)

@app.callback(
    Output('check', 'children'),
    [Input('check', 'value')]
)
def checklists3(v):
        print('value from template', v)

'''

@app.callback(
    Output('check', 'children'),
    [Input('check', 'value'),
    Input('checklist2', 'value')]
)
def check(value, v):
    print('value from template', value)


'''


