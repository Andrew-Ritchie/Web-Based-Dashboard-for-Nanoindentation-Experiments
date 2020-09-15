import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", active=True, href="/apps/home")),
        dbc.NavItem(dbc.NavLink("Analysis", href="/apps/analysis")),
        dbc.NavItem(dbc.NavLink("Feed", href="/apps/preparation")),
        dbc.NavItem(dbc.NavLink("About", href="/apps/about"))
    ],
    horizontal=True,
    fill=True
)
SIDEBAR_STYLE = {
    "position": "fixed",
    "height": '87%',
    "left": 0,
    "bottom": 0,
    "width": "18%",
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
    html.Div(sidebar),    
    html.Div(id='page-content',style={"background-color": "#f8f9fa", 'textIndent':'50%'}),
    html.H5('test test test')
])


@app.callback(Output('page-content', 'children'),
                [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)