import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
from app import app
from dash.exceptions import PreventUpdate
import json
import os
import sys



from dash.dependencies import Input, Output, State

comments = [] 
arguments = []
outputs = []
states = []

indexglob = 0



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
    print('HELLOOOOOOOOOOOO')
    mainfeed = []   
    index2 = 0
    with open('postdb/data.json', 'r') as db:
        data = json.load(db)
        print(data)
    for element in data.keys():
        for value in data[element].keys(): 
            print(element, 'here we arererererererere')
            mainfeed.append(generatepost(element, value, list(data[element][value].keys())[0], index2, list(data[element][value].values())[0]))
            print(index2, 'indexx222')
            #comments.append(Input('commentarea' + str(index), 'children'))
            #print(comments)
            index2 += 1

    return mainfeed





@app.callback(
    Output('user', 'value'),
    [Input("post", "n_clicks")]
)
def update_username(click):
    output = 'Username'
    try:
        output = os.environ['KAGGLE_USERNAME']
    except: # catch *all* exceptions
        output = 'Username'

    return output


@app.callback(
    Output('output2', 'children'),
    [Input('post', 'n_clicks')],
    State('title', 'value'),
    State('user', 'value'),
    State('textarea', 'value')
)
def update_postdb(clicks, title, user, text):
    print('DO we do this 123')
    if clicks != 0:
        print('hellomoto')
        dic = {'user54': {'Hello Everyone!':{'This is the post I have sent to the platfrom.' : ['andrewritchie98', 'Welcome!']}}}
        
        with open('postdb/data.json', 'r') as db:
            data = json.load(db)
            print(data)
            print(type(data))
            if user not in data.keys():
                data.update({user: {title: {text : {}}}})
            else:
                data[user].update({title: {text: {}}})
        post = {user: {title: {text : []}}}
        with open('postdb/data.json', 'w') as outfile:
            json.dump(data, outfile) 
        os.execv(sys.executable, ['python'] + sys.argv)

        '''
        global indexglob
        global comments
        global arguments
        global states
        global run
        comments.append(Input('commentbutton' + str(indexglob), 'n_clicks'))
        comments.append(Input('commenttext' + str(indexglob), 'value'))
        arguments.append('click' + str(indexglob))
        arguments.append('commenttext' + str(indexglob))
        arguments.append('posttitle' + str(indexglob))
        outputs.append(Output('commentarea' + str(indexglob), 'children'))
        states.append(State('posttitle' + str(indexglob), 'children'))
        states.append(State('commenttext' + str(indexglob), 'value'))
        print('this is the index value used', indexglob)
        print(outputs, 'check this')
        indexglob += 1 

        loop(outputs)

        with open('postdb/data.json', 'w') as outfile:
            json.dump(data, outfile) 
        
        y = 0 
        global comments
        global arguments
        global states

        comments = []
        arguments = []
        states = []

        comments.append(Input('commentbutton' + str(y), 'n_clicks'))
        comments.append(Input('commenttext' + str(y), 'value'))
        arguments.append('click' + str(y))
        arguments.append('commenttext' + str(y))
        arguments.append('posttitle' + str(y))
        outputs.append(Output('commentarea' + str(y), 'children'))
        states.append(State('posttitle' + str(y), 'children'))
        states.append(State('commenttext' + str(y), 'value'))
        print('this is the index value used', y)
        print(outputs, 'check this')
        print('this is y', y)
        y += 1
        with open('postdb/data.json', 'w') as outfile:
            json.dump(data, outfile) 
        ''
        '''
        
        
 





def generatepost(user, title, text, index, comments2):
    

    x = [
        html.Div([
            html.H3(user,  style = {'text-indent': '1%', 'float': 'left'}),
            html.H1(title, id='posttitle' + str(index), style = {'text-indent': '0%', 'padding-left':'40%'}),

        ]),
        html.Div([
                html.P(text, style={'text-indent': '1%','margin': '0', 'float':'left', 'width':'65%', 'padding':'1%', 'bgcolor': 'black'}),
            ],style={'padding':'0%'}),
        html.Br(),
        html.Br(),
        html.Button('Comment', id='commentbutton' + str(index), n_clicks=0, style={'float':'right', 'box-sizing':'border-box', 'margin-right':'2%'}),
        dcc.Textarea(
        id='commenttext' + str(index),
        value='Please write your post here.',
        style={'width': '100%', 'height': 50},
        ),
        html.Div(id='commentarea' + str(index)),
        html.Br(),
        html.Br()

    ]
    '''
    for value in comments.keys():
        x.append(html.P(comments[value] + ': ' + value))
    '''
    '''
    comments.append(Input('commentbutton' + str(index), 'n_clicks'))
    comments.append(Input('commenttext' + str(index), 'value'))
    arguments.append('click' + str(index))
    arguments.append('commenttext' + str(index))
    arguments.append('posttitle' + str(index))
    outputs.append(Output('commentarea' + str(index), 'children'))
    states.append(State('posttitle' + str(index), 'children'))
    states.append(State('commenttext' + str(index), 'value'))
    print('this is the index value used', index)
    print(outputs, 'these are the outputs') 
    '''


    output = html.Div(x, style={'background-color': '#DDDDDD', 'margin': '1%', 'border': '1px solid black', 'border-radius': '10px'})


    return output

'''
@app.callback(
     dash.Output('co')
)
def postcomment(*arguments):
    print('did this happen'

'''
def loop(outn):
    @app.callback(
        outn,
        comments,
        states
    )
    def postcomment(*arguments):
        print('did this happen')
        print(arguments[:-1])
        with open('postdb/data.json', 'r') as db:
            data = json.load(db)
        trigger = dash.callback_context.triggered[0]
        print(trigger, 'this is trigger')
        print(trigger['prop_id'].split('.')[0])
        print(trigger['value'], 'this is trigger')
        if trigger['value'] is not None:
            #print(trigger['prop_id'].split('.')[0][:-1], 'this is the value mann')
            if trigger['prop_id'].split('.')[0][:-1] == 'commentbutton':
                num = trigger['prop_id'].split('.')[0][-1]
                title = dash.callback_context.states['posttitle' + num + '.children']
                print(dash.callback_context.states, 'these are the states')
                print(title, 'testing')
                output = []
                postnum = 0
                for value in data.keys():
                    for element in data[value].keys():
                        if element == title:
                            '''
                            print('found it!')
                            print(element)
                            print(data[value][element])
                            print(data[value][element].values())
                            foundvalue = data[value][element]
                            '''
                            coms = list(data[value][element].keys())[0]
                            text = dash.callback_context.states['commenttext' + num +'.value']
                            user = dash.callback_context.states['user.value']
                            data[value][element][coms][text] = user
                            
                            output = []
                            print(data[value][element][coms])
                            
                            for plaintext in data[value][element][coms].keys():
                                output.append(html.P(data[value][element][coms][plaintext] + ': ' + plaintext))
                #this is rewriting it for some reason
                print(data, 'this is data')
                with open('postdb/data.json', 'w') as outfile:
                    json.dump(data, outfile)         
                return [output]
            else:
                raise PreventUpdate            
        else:
            output = []
            for value in data.keys():
                for element in data[value].keys():
                    outhtml = []
                    coms = list(data[value][element].keys())[0]
                    for plaintext in data[value][element][coms].keys():
                        outhtml.append(html.P(data[value][element][coms][plaintext] + ': ' + plaintext))
                    output.append(outhtml)
                    print('value')
            print(len(output)) 
            print(dash.callback_context.inputs, 'these are the inputs')
            #print(len([output, output]), 'is it this')
            return output  
            


'''
if arguments[0] > 0:
    #add to the file and re-read it!
    return (None, None,  html.P('this is a test'))
else:
    return [None, None, None]
'''


    
with open('postdb/data.json', 'r') as db:
    data = json.load(db)
    for element in data.keys():
        for value in data[element].keys(): 
            comments.append(Input('commentbutton' + str(indexglob), 'n_clicks'))
            comments.append(Input('commenttext' + str(indexglob), 'value'))
            arguments.append('click' + str(indexglob))
            arguments.append('commenttext' + str(indexglob))
            arguments.append('posttitle' + str(indexglob))
            outputs.append(Output('commentarea' + str(indexglob), 'children'))
            states.append(State('posttitle' + str(indexglob), 'children'))
            states.append(State('commenttext' + str(indexglob), 'value'))
            print(states)
            print(indexglob)
            indexglob += 1

    arguments.append('username')
    states.append(State('user', 'value'))

run = loop(outputs)


layout = html.Div([
    html.Div([
        selectfeature,
    ], style= SIDEBAR_STYLE),
    
    
    html.Div(id='mainfeed',children= [], style=MAIN_STYLE),
])   