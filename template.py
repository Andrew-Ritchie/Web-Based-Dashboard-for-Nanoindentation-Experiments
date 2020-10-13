import dash
import dash_core_components as dcc
import dash_html_components as html
import os
from app import app
from dash.dependencies import Input, Output, State


samples = ['Glass', 'Rubber']
setsglass = ['Day1', 'Day2']
setsrubber = ['Day1', 'Day2']
filenames = ['S-1 X-9 Y-6 I-1.txt', 'S-1 X-9 Y-6 I-2.txt', 'S-1 X-9 Y-6 I-3.txt' ]

def listelement(samplename, sets, filenames, num):
    if num == 0:
        startvalue = 1
    else:
        startvalue = 3
    
    setlist = []
    for num, name in enumerate(sets, start=startvalue):
        setlist.append(generatesetlist(samplename, name, filenames, num))
        print(num)

    return html.Details(id= 'my-input',children=[
            html.Summary([
                samplename,
            ]),
            
            
        ] + setlist, style={'padding-left':'5%'})

def generatesetlist(samplename, setname, filenames, index):
    opts = []
    for element in filenames:
        opts.append({'label': element, 'value': samplename + '/' + setname + '/' + element})
    return html.Details(children=[
                html.Summary([
                    setname
                ]),
                 html.Div([
                    dcc.Checklist(
                        id = 'test'+str(index),
                        options=opts,
                        labelStyle={'display': 'block', 'margin':'0%'},
                        value=[]
                    ),
                    html.Button('All', id='button'+str(index), n_clicks=0),
                 ], style={'padding-left':'10%'})
            ], style={'padding-left': '5%'})



def generatelist(samples, sets, filenames):
    experimentlist = []
    for num, element in enumerate(samples):
        experimentlist.append(listelement(element, sets, filenames, num))
    return experimentlist
        



#x = html.Div([listelement(samples[0], setsglass[0], filenames, 0)])
x = html.Div(generatelist(samples, setsglass, filenames))

tem = html.Div([
    x
])

@app.callback(
    Output('test1', 'value'),
    [Input('button1', 'n_clicks')],
    [State("test1", "options")]
)
def first(n_clicks, options):
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
        print(all_or_none)
    return all_or_none

@app.callback(
    Output('test1', 'children'),
    Input('test1', 'value')
)
def tes(value):
        print('value from template First', value)




@app.callback(
    Output('test2', 'value'),
    [Input('button2', 'n_clicks')],
    [State("test2", "options")]
)
def test2a(n_clicks, options):
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
        print(all_or_none)
    return all_or_none

@app.callback(
    Output('test2', 'children'),
    Input('test2', 'value')
)
def test2b(value):
        print('value from template First', value)

@app.callback(
    Output('test3', 'value'),
    [Input('button3', 'n_clicks')],
    [State("test3", "options")]
)
def test3a(n_clicks, options):
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
        print(all_or_none)
    return all_or_none

@app.callback(
    Output('test3', 'children'),
    Input('test3', 'value')
)
def test3b(value):
        print('value from template First', value)




@app.callback(
    Output('test4', 'value'),
    [Input('button4', 'n_clicks')],
    [State("test4", "options")]
)
def test4a(n_clicks, options):
    if (n_clicks%2) == 0:
        all_or_none = []
    else:
        all_or_none = [option["value"] for option in options]
        print(all_or_none)
    return all_or_none

@app.callback(
    Output('test4', 'children'),
    Input('test4', 'value')
)
def test4b(value):
        print('value from template First', value)





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


