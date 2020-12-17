import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
from app import app
import json


from dash.dependencies import Input, Output, State




SIDEBAR_STYLE = {
    'box-sizing':'border-box',
    'width': '20%',
    'border': '1px solid black',
    'float': 'left',
    'text-indent': '5%',
    'padding-bottom': '100%',
    "background-color": "#EAF0F1"
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
sidebar = html.Div(
    [
        html.H2("Sidebar"),
        
    ]
)

post = html.Div([
            html.H2("Thread"),
            
            
        ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})
        


mainfeed = []



selectfeature = html.Div([
    html.H2("Search", style={'text-align': 'center'}),
    dcc.Input(id='title', value='Title'),
    dcc.Input(id='user', value='Username'),
    dcc.Textarea(
        id='textarea',
        value='Please write your post here.',
        style={'width': '100%', 'height': 300},
    ),
    html.Button('Post', id='post', n_clicks=0, style={'float':'left', 'box-sizing':'border-box', 'margin-right':'2%'}),

    html.Div(id='output2'),
    html.Br(),
    html.Br()

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})

@app.callback(
    Output('mainfeed', 'children'),
    [Input("post", "n_clicks"),
    Input('output2', 'children')]
)
def update_forward_dropdown(click, output2):
    mainfeed = []   
    with open('postdb/data.json', 'r') as db:
        data = json.load(db)
        print(data)
    for element in data.keys():
        for value in data[element].keys():
            mainfeed.append(generatepost(element, value, list(data[element][value].keys())[0]))

    return mainfeed

@app.callback(
    Output('output2', 'children'),
    [Input('post', 'n_clicks')],
    State('title', 'value'),
    State('user', 'value'),
    State('textarea', 'value')
)
def update_postdb(clicks, title, user, text):
    if clicks != 0:
        dic = {'user54': {'Hello Everyone!':{'This is the post I have sent to the platfrom.' : ['andrewritchie98', 'Welcome!']}}}
        
        with open('postdb/data.json', 'r') as db:
            data = json.load(db)
            print(data)
            print(type(data))
            if user not in data.keys():
                data.update({user: {title: {text : []}}})
            else:
                data[user].update({title: {text: []}})


        post = {user: {title: {text : []}}}
        print(data)

        
        
        with open('postdb/data.json', 'w') as outfile:
            json.dump(data, outfile)






def generatepost(user, title, text):

    return html.Div([
        html.Div([
            html.H3(user,  style = {'text-indent': '1%', 'float': 'left'}),
            html.H1(title, style = {'text-indent': '0%', 'padding-left':'40%'}),

        ]),
        html.Div([
                html.P(text, style={'text-indent': '1%','margin': '0', 'float':'left', 'width':'65%', 'padding':'1%', 'bgcolor': 'black'}),
            ],style={'padding':'0%'}),
        html.Br(),
        html.Br(),
        html.Button('Comment', id='commentbutton', n_clicks=0, style={'float':'right', 'box-sizing':'border-box', 'margin-right':'2%'}),
        html.Br(),
        html.Br()

    ], style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})
    

        


layout = html.Div([
    html.Div([
        selectfeature,
    ], style= SIDEBAR_STYLE),
    
    
    html.Div(id='mainfeed',children= [], style=MAIN_STYLE),
])   