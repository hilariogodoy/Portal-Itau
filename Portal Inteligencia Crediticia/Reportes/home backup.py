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
        # dbc.Row([
        #     dbc.Col(html.H5(children='This app marks my very first attempt at using Plotly, Dash and Bootstrap! '
        #                              )
        #             , className="mb-4")
        #     ]),

        # dbc.Row([
        #     dbc.Col(html.H5(children='It consists of two main pages: Global, which gives an overview of the COVID-19 cases and deaths around the world, '
        #                              'Singapore, which gives an overview of the situation in Singapore after different measures have been implemented by the local government.')
        #             , className="mb-5")
        # ]),

        dbc.Row([
            dbc.Col(dbc.Card(children=[html.H3(children='Info mercado CENDEU',
                                               className="text-center"),
                                       dbc.Row([dbc.Col(dbc.Button("Mercado", href=link+"Cendeu-Total",
                                                                   color="primary"),
                                                        className="mt-3"),
                                                dbc.Col(dbc.Button("ITAU", href=link+"Cendeu-Itau",
                                                                   color="primary"),
                                                        className="mt-3")], justify="center")
                                       ],
                             body=True, color="dark", outline=True)
                    , width=4, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='Indices de principalidad por banco',
                                               className="text-center"),
                                       dbc.Button("Principalidad",
                                                  href=link+"Principalidad",
                                                  color="primary",
                                                  className="mt-3"),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=4, className="mb-4"),
        ], className="mb-5"),
    ])

])

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)