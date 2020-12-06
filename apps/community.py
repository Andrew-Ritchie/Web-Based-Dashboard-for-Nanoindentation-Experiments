import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
from app import app


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
  'padding-bottom': '100%'
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
    html.Button('Post', id='post', n_clicks=0, style={'float':'left', 'box-sizing':'border-box', 'margin-right':'2%'}),
    dcc.Input(),
    html.Br(),
    html.Br()

], style={"background-color": "#DDDDDD", 'margin': '5%', 'margin-top':'4%', 'border-radius': '10px', 'border': '1px solid black',})

@app.callback(
    Output('mainfeed', 'children'),
    [Input("post", "n_clicks")]
)
def update_forward_dropdown(click):
    if click != 0:
        mainfeed.append(post)
        return mainfeed

    




layout = html.Div([
    html.Div([
        selectfeature,
    ], style= SIDEBAR_STYLE),
    
    
    html.Div(id='mainfeed',children= [], style=MAIN_STYLE),
])   