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

def listelement(samplename, exp, num):
    """
    displays the sample list

    :type samplename: string
    :param samplename: name of the uploaded sample 

    :type exp: string
    :param exp: name of the experiment uploaded by the user

    :type num: int
    :param num: number of samples uploaded by the user
    """ 
    if num == 0:
        startvalue = 1
    else:
        startvalue = 3
    
    setlist = []
    for num, name in enumerate(exp.samples[samplename].sets.keys(), start=startvalue):
        setlist.append(generatesetlist(samplename, name, exp, num))
        print(num)

    return html.Details(id= 'my-input',children=[
            html.Summary([
                samplename,
            ]),
            
            
        ] + setlist, style={'padding-left':'5%'})

def generatesetlist(samplename, setname, exp, index):
    """
    displays the indentation files within a sample

    :type samplename: string
    :param samplename: name of the uploaded sample 

    :type setname: string
    :param setname: name of the set uplaoded by the user

    :type exp: string
    :param exp: name of the experiment uploaded by the user

    :type index: int
    :param index: number of samples already displayed
    """ 
    opts = []
    for element in exp.samples[samplename].sets[setname].indents.keys():
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



def generatelist(exp):
    """
    returns a list of uploaded samples

    :type exp: string
    :param exp: name of the experiment uploaded by the user
    """     
    samples = exp.samples.keys()
    experimentlist = []
    for num, element in enumerate(samples):
        experimentlist.append(listelement(element, exp, num))
    return experimentlist
        

def out(exp):
    """
    returns a list of indentation files

    :type exp: string
    :param exp: name of the experiment uploaded by the user
    """  
    x = html.Div(generatelist(exp))
    return html.Div([
        x
    ])

