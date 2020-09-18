import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import app
from apps import home, analysis, feed, about
from apps.feed import parse_contents

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/apps/home")),
        dbc.NavItem(dbc.NavLink("Analysis", href="/apps/analysis")),
        dbc.NavItem(dbc.NavLink("Feed", href="/apps/feed")),
        dbc.NavItem(dbc.NavLink("About", href="/apps/about"))
    ],
    horizontal=True,
    fill=True,
    pills=True
)
SIDEBAR_STYLE = {
    "position": "fixed",
    "padding": '10px',
    "padding-bottom": '100%',
    "background-color": "#EAF0F1",
}
sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        
    ],
    style=SIDEBAR_STYLE,
)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(children=[html.H1('Nanoindentation Application', style={'color': 'blue', 'fontSize': 50, 'font-family': 'verdana', 'textAlign': 'center', 'backgroundColor': '#EAF0F1'}), nav], style={'backgroundColor': '#EAF0F1', 'height': '87%'}),
    html.Div(children=[sidebar],style={'float':'left'}),    
    html.Div(id='page-content',style={"background-color": "#f8f9fa", 'textIndent':'50%'})
])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              State('upload-data', 'filename'),
               State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)] 
        return children

@app.callback(Output('page-content', 'children'),
                [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/home':
        return home.layout
    elif pathname == '/apps/analysis':
        return analysis.layout
    elif pathname == '/apps/feed':
        return feed.layout
    elif pathname == '/apps/about':
        return about.layout
    else:
        return home.layout



if __name__ == '__main__':
    app.run_server(debug=True)