#!/usr/bin/env python
# coding: utf-8

# In[13]:

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import numpy as np
import pandas as pd
import pyodbc 
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go

import flask
import dash
#import dash_bootstrap_components as dbc


#%% Conexion a SQL:
conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server}; SERVER=SQLNONITPROD; DATABASE=aig;Trusted_Connection=yes') 

woff = pd.read_sql("""
select fecha , pad_segmento2 as segmento, sum(ope_saldo_cont) deuda from (
select *, format(ope_fec_cla, 'yyyyMM') as fecha
from operaciones_castigadas_con_saldo) a
group by fecha, pad_segmento2
order by fecha 
""", conn)
stock = pd.read_sql("""
select format(mes, 'yyyyMM') as mes, J_Woff+XJ_Woff+[Pre-legal_Woff] as stock from cartera_recuperos_por_gestion
--group  by mes
order by mes
""", conn)
#%% Datasets

fechas = woff['fecha'].unique()[-13:]
woff = woff[woff['fecha'].isin(fechas)]
stock = stock[stock['mes'].isin(fechas)]

#%% Graficos


bar_trace = go.Bar(
    x=fechas,
    y=woff[woff['segmento']=='4000']['deuda'],
    name='Segmento 4000',
    marker=dict(color='#FFB84C'),
    yaxis='y',
    text=woff[woff['segmento']=='4000']['deuda']
)

stacked_bar_trace = go.Bar(
    x=woff[woff['segmento']=='8000']['fecha'],
    y=woff[woff['segmento']=='8000']['deuda'],
    name='Segmento 8000',
    marker=dict(color='#A459D1'),
    yaxis='y',
    text=woff[woff['segmento']=='8000']['deuda']
)

line_trace = go.Scatter(
    x=fechas,
    y=stock['stock'],
    name='Stock',
    line=dict(color='#F16767'),
    yaxis='y2',
    text = stock['stock']
)

layout = go.Layout(
    #title='Stacked Bar Line Chart with 2 Axes',
    #yaxis=dict(title='Bar and Stacked Bar Y Axis'),
    yaxis2=dict(overlaying='y', side='right')
)

fig = go.Figure(data=[bar_trace, stacked_bar_trace, line_trace], layout=layout)

fig.update_layout(barmode = 'stack')
fig.update_yaxes(showgrid=False)

#%% Layout

layout = layout = dbc.Container(
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
                            html.H3("Write Off Ultimo Año"),
                            html.Div(dcc.Graph(figure=fig)),
                            #html.P("Población: Totalidad de Personas fisicas registradas en CENDEU segmentadas por entidad de la que son clientes y si ya son clientes ITAU o no")
                        ],
                    ),
                    width=12,
                )
            ],
        ),
        html.Div(className="separador2"),
    ]
)







