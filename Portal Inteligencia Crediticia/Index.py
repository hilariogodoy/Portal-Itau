from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import server
from app import app #Comentar esta linea para correr en Jupyter

from Reportes import home_oficial, home_desarrollos, Mercado_Clientes_Cendeu, Mercado_Share, Mercado_Total_Cendeu, Woff, Motivos_Exclusion, over_pp_reprogramados #Comentar esta linea para correr en Jupyter

#APP
#server = flask.Flask(__name__) #Descomentar esta linea para correr en Jupyter
#app = dash.Dash(__name__, server=server) #Descomentar esta linea para correr en Jupyter

##Indexer
#dropdown = dbc.DropdownMenu(
#    children=[
#	dbc.DropdownMenuItem("Home", href="/home"),
#    dbc.DropdownMenuItem(divider=True),
#	dbc.DropdownMenuItem("Historico", href="/page-Historico")
#	dbc.DropdownMenuItem("AC BPM Hoy", href="http://IBA8112.sis.ad.bia.itau:8051",target='_blank')
#	],
#    nav = True,
#    in_navbar = True,
#    label = "Navegar Sitio"
#)

navbar = dbc.Navbar(
    dbc.Container([
        html.A(
            dbc.Row([
                dbc.Col(html.Img(src='/assets/logo.png', height="60px")),
                dbc.Col(dbc.NavbarBrand("Banco ITAU | Inteligencia Crediticia", className="ml-1"))],
                align="center",
                #no_gutters=True
                ),
            href="/home"),
        #dbc.NavbarToggler(id="navbar-toggler2"),
#        dbc.Collapse(
#            dbc.Nav([dropdown], className="ml-auto", navbar=True),
#            id="navbar-collapse2",
#            navbar=True,
#        ),
    ],style={'height': '50px'}),
    color="#F99417",
    dark=True,
    sticky="top"
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

#Layout Pagina
#layout = dbc.Container([ #Comentar esta linea para correr en Jupyter
#app.layout = dbc.Container([ #Descomentar esta linea para correr en Jupyter

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
],style={'backgroundColor': 'dark'})


app.title="Dash - Información de Mercado" 

# Callback de carga de contenidos
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/Cendeu-Itau':
        return Mercado_Clientes_Cendeu.layout
    elif pathname == '/Principalidad':
        return Mercado_Share.layout	
    elif pathname == '/Cendeu-Total':
        return Mercado_Total_Cendeu.layout
    elif pathname == '/Write-Off':
        return Woff.layout
    elif pathname == '/Motivos-Exclusion':
        return Motivos_Exclusion.layout
    elif pathname == '/over_pp_reprogramados':
        return over_pp_reprogramados.layout
    elif pathname == '/home':
        return home_oficial.layout
    elif pathname == '/home_desarrollos':
        return home_desarrollos.layout
    else:
        return home_oficial.layout

if __name__ == '__main__':
    app.run_server(debug=True)
        
