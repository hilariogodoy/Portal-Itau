#!/usr/bin/env python
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import pyodbc 
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

#%% Conexion SQL


conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server}; SERVER=SQLNONITPROD; DATABASE=aig;Trusted_Connection=yes')

cendeu_x_cliente = pd.read_sql("""select noment,categoria,cliente_itau, clientes 
                                from vw_mercado_total_cendeu
                                order by 3 desc""", conn)

cendeu_x_deuda = pd.read_sql("""select noment,categoria, cliente_itau, deuda 
                                from vw_mercado_total_cendeu
                                order by 3 desc""", conn)

deuda_categoria = pd.read_sql("""select categoria, cliente_itau, sum(deuda) as deuda
                                from vw_mercado_total_cendeu
                                group by categoria, cliente_itau
                                order by 3 desc""", conn)
clientes_categoria = pd.read_sql("""select categoria, cliente_itau, sum(clientes) as clientes
                                from vw_mercado_total_cendeu
                                group by categoria, cliente_itau
                                order by 3 desc""", conn)

#%%Graficos

fig_clientes = px.treemap(cendeu_x_cliente, path=[px.Constant("Mercado Argentino Total por Personas"),'categoria', 'noment', 'cliente_itau'], values = 'clientes')

fig_deuda = px.treemap(cendeu_x_deuda, path=[px.Constant("Mercado Argentino Total por Deuda"),'categoria', 'noment', 'cliente_itau'], values = 'deuda')

fig_bar = px.bar(deuda_categoria, x = 'categoria', y='deuda', color = 'cliente_itau')

fig_bar2 = px.bar(clientes_categoria, x = 'categoria', y='clientes', color = 'cliente_itau')

fig_clientes2 = px.treemap(cendeu_x_cliente[cendeu_x_cliente['cliente_itau']=='No cliente ITAU'], path=[px.Constant("Mercado Argentino Total por Personas"),'categoria', 'noment'], values = 'clientes')

fig_deuda2 = px.treemap(cendeu_x_deuda[cendeu_x_deuda['cliente_itau']=='No cliente ITAU'], path=[px.Constant("Mercado Argentino Total por deuda"),'categoria', 'noment'], values = 'deuda')

#%% Layout

layout = dbc.Container(
    [
        html.Div(className="separador1"),
#        html.H1("Banca Personal | Información de Mercado |" + mes["mes"].astype("string")),
        html.Div(className="separador2"),
        
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        className="uno mx-2",
                        children=[
                            html.H3("Clientes por Entidad"),
                            html.Div(dcc.Graph(figure=fig_clientes)),
                            html.P("Población: Totalidad de Personas fisicas registradas en CENDEU segmentadas por entidad de la que son clientes y si ya son clientes ITAU o no")
                        ],
                    ),
                    width=12,
                )
            ],
        ),
        html.Div(className="separador2"),

        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        className="uno mx-2",
                        children=[
                            html.H3("Deuda por Entidad"),
                            html.Div(dcc.Graph(figure=fig_deuda)),
                            html.P("Población: Totalidad de deuda de personas fisicas registradas en CENDEU segmentada por entidad y si ésta corresponde a ITAU o no")
                        ],
                    ),
                    width=12,
                )
            ],
        ),
        html.Div(className="separador2"),

                dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        className="uno mx-2",
                        children=[
                            html.H3("Clientes por categoria"),
                            html.Div(dcc.Graph(figure=fig_bar2)),
                            html.P("Total de clientes agrupados por categoria")
                        ],
                    ),
                    width=12,
                )
            ],
        ),
        html.Div(className="separador2"),
        
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        className="uno mx-2",
                        children=[
                            html.H3("Deuda por categoria"),
                            html.Div(dcc.Graph(figure=fig_bar)),
                            html.P("Total de deuda agrupada por categoria")
                        ],
                    ),
                    width=12,
                )
            ],
        ),
        html.Div(className="separador2"),
    ]
)


