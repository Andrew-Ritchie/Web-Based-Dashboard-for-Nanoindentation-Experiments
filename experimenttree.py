import dash
import dash_core_components as dcc
import dash_html_components as html
import os


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
    return html.Div([
        html.Details([
            html.Summary([
                samname,
            ]),
            html.Div([
            dcc.Checklist(
                options=opts,
                labelStyle={'display': 'block', 'margin':'0%'}
                
            )
        ], style={'padding-left':'10%'})]),
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



#html for samples




experimenttree = html.Div([
    html.Div(run(test)),
    html.Br()
])




'''
 html.Details([
                html.Summary([
                    html.Div([
                    dcc.Checklist(
                        options=[
                    {'label': 'Forward', 'value': 'NYC'},
                    ],
                    value=[],
                    labelStyle={ 'margin-bottom': '0%'},
                        )
                    ], style={'display': 'inline-block', 'float':'left'}),
                
                ], style={'width': '49%', 'display': 'inline-block', 'border': '1px solid black', 'margin-left': '1%', 'padding':'0%', 'float':'left'}),

                html.Details([
                    html.Summary('Label of the item'),
                    html.Div('Contents'),
                    dcc.Checklist(
                        options=[
                    {'label': 'Forward', 'value': 'NYC'},
                    {'label': 'Backward', 'value': 'MTL'},
                ],
                value=[],
                labelStyle={'display': 'inline-block', 'float':'left', 'width':'35%'},
                    )
                ]),
                html.Div('Contents')

            ]),
'''