import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
# external_stylesheets = [dbc.themes.LUX]

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead

link = "http://localhost:8052/"

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Dashboard Inteligencia Crediticia", className="text-center")
                    , className="mb-5 mt-5")
        ]),
       
        dbc.Row([            
            dbc.Col(dbc.Card(children=[html.H3(children='Info mercado ITAU CENDEU',
                                               className="text-center", style = {'color':'white'}),
                                       dbc.Row([dbc.Button("Ingresar", href=link+"Cendeu-Itau",
                                                                   color="primary"),
                                                        
                                                ], justify="center")
                                       ],
                             body=True, color="#F99417", outline=True)
                    , width=4, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='Principalidad por banco',
                                               className="text-center", style = {'color':'white'}),
                                       dbc.Row([dbc.Button("Ingresar", href=link+"Principalidad",
                                                                   color="primary"),
                                                        
                                                ], justify="center")
                                       ],
                             body=True, color="#F99417", outline=True)
                    , width=4, className="mb-4"),
            dbc.Col(dbc.Card(children=[html.H3(children='Motivos de Exclusión',
                                                className="text-center", style = {'color':'white'}),
                                        dbc.Row([dbc.Button("Ingresar", href=link+"Motivos-Exclusion",
                                                                    color="primary"),
                                                        
                                                ], justify="center")
                                        ],
                              body=True, color="#F99417", outline=True)
                    , width=4, className="mb-4"),          
        ], className="mb-5"),
 
    ])

])

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)