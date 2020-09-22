import base64
import datetime
import io
import re 
import codecs


import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd

from app import app
from apps.opticsparser import ConvertOptics


layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    dcc.Input(id="input2", type="text", placeholder="", debounce=True),
    html.Div(id="output"),
    html.Div(id='output-data-upload'),
], style= {'padding-left': '30%', 'padding-right': '10%'})

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    experiment_name = "Experiment_1" #This will be user defined
    test = ConvertOptics(filename, experiment_name)
    test.loaddata(decoded)
    test.loadheader(decoded)
    test.createfile()
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        html.Hr(),  # horizontal line
    ])



