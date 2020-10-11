import dash
import dash_core_components as dcc
import dash_html_components as html
import os
from app import app
from dash.dependencies import Input, Output, State


def test12(test):
    return html.Details(id= 'my-input',children=[
            html.Summary([
                'Sample',
            ]),
            html.Div([
            dcc.Checklist(
                id = test,
                options=[{'label': 'Forward', 'value': test},
                        {'label': 'Backward', 'value': 'MT11L'}],
                labelStyle={'display': 'block', 'margin':'0%'},
            ),
            ], style={'padding-left':'10%'}),
            
        ], style={'padding-left':'5%'})


x = test12('third')


tem = html.Div([
    test12('first'),
    test12('second'),
    x
])

@app.callback(
    Output('first', 'children'),
    Input('first', 'value')
)
def first(value):
        print('value from template', value)

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
    Input('fouth', 'value')
)
def fouth(value):
        print('value from template SECOND', value)


