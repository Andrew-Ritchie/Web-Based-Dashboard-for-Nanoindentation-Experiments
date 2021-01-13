import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import app
from apps import home, analysis, prepare, about, community
from apps.prepare import parse_contents



nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/apps/home")),
        dbc.NavItem(dbc.NavLink("Analysis", href="/apps/analysis")),
        dbc.NavItem(dbc.NavLink("Prepare", href="/apps/prepare")),
        dbc.NavItem(dbc.NavLink("Community", href="/apps/community")),
        dbc.NavItem(dbc.NavLink("About", href="/apps/about"))
    ],
    horizontal=True,
    fill=True,
    pills=True,
    style={"padding-bottom":"10px", 'border': '1px solid black'}
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(children=[html.H1('Nanoindentation Application', style={'color': 'blue', 'fontSize': 50, 'font-family': 'verdana', 'textAlign': 'center', 'backgroundColor': '#AFAFAF'}), nav], style={'backgroundColor': '#EAF0F1', 'height': '87%', 'border': '1px solid black'}),   
    html.Div(id='page-content',style={"background-color": "#f8f9fa", 'textIndent':'50%'})
])



@app.callback(Output('page-content', 'children'),
                [Input('url', 'pathname')])
def display_page(pathname):
    print('index callback')
    if pathname == '/apps/home':
        return home.layout
    elif pathname == '/apps/analysis':
        return analysis.layout
    elif pathname == '/apps/prepare':
        return prepare.layout
    elif pathname == '/apps/about':
        return about.layout
    elif pathname == '/apps/community':
        return community.layout
    else:
        return home.layout



if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)