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

principalidad_historico = pd.read_sql("""
SELECT concat(rtrim(codent),cartera) as codigo,*
FROM principalidad_clientes_bcra
where cartera <> 'Mov'
order by fecinf asc, id_princ_cliente desc""", conn)

#%% Datasets

principalidad_historico['cartera']=principalidad_historico['cartera'].str.strip()
principalidad_historico['id_princ_cliente'] = principalidad_historico['id_princ_cliente']*100

ents_v = principalidad_historico['nom_ent']
ents = []
for ent in ents_v:
    if 'ITAU' in ent:
        ents.append('ITAU')
    elif 'MACRO' in ent:
        ents.append('MACRO')
    elif 'GALICIA' in ent:
        ents.append('GALICIA')
    elif 'INDUSTRIAL AND COMMERCIAL BANK OF CHINA ' in ent:
        ents.append('ICBC')
    elif 'SANTANDER' in ent:
        ents.append('SANTANDER')
    elif 'BBVA' in ent:
        ents.append('BBVA')
    elif 'HSBC' in ent:
        ents.append('HSBC')
    elif 'SUPERVIELLE' in ent:
        ents.append('SUPERVIELLE')
    elif 'CREDICOOP' in ent:
        ents.append('CREDICOOP')
    elif 'PATAGONIA' in ent:
        ents.append('PATAGONIA')
    elif 'COMAFI' in ent:
        ents.append('COMAFI')
        
principalidad_historico['entidad'] = ents

principalidad_historico['entidad'] = np.where((principalidad_historico['entidad']=='ITAU') &  (principalidad_historico['cartera']== 'Tot'), 'ITAU Total',principalidad_historico['entidad'] )
principalidad_historico['entidad'] = np.where((principalidad_historico['entidad']=='ITAU') &  (principalidad_historico['cartera']== 'Pbnk'), 'ITAU PBnk',principalidad_historico['entidad'] )
principalidad_historico['entidad'] = np.where((principalidad_historico['entidad']=='ITAU') &  (principalidad_historico['cartera']== 'Mov'), 'ITAU Movistar',principalidad_historico['entidad'] )
principalidad_historico['entidad'] = np.where((principalidad_historico['entidad']=='ITAU') &  (principalidad_historico['cartera']== 'Sign'), 'ITAU Signature',principalidad_historico['entidad'] )

#df.loc[principalidad_historico['cartera']='Pbnk', 'cartera'] = 'ITAU Personal Bank' #, entidad]='ITAU Personal Bank'


y = principalidad_historico[principalidad_historico.fecinf== max(principalidad_historico['fecinf'])]
y = y.sort_values('id_princ_cliente', ascending = False)

#%% Graficos

fig = px.bar(y, x='entidad', y='id_princ_cliente', text_auto = True)

fig.update_layout(yaxis_ticksuffix = "%")



y_data = []

x_data = []
colors = ['#0D6ABF','#9A1616','#FF5757','#118DFF','#FF0303','#B3B3B3','#C30E0E','#48A505','#AA6300','#D23800','#117302','#000000','#FF9200','#0DBB00',]
entidades = principalidad_historico['entidad'].unique()
line_size = [1, 1, 1, 1, 1, 1,1, 1, 4, 1, 1, 4, 4, 4]
dash_type = ['dash', 'dash', 'dash', 'dash', 'dash', 'dash', 'dash', 'dash', 'solid', 'dash', 'dash', 'solid', 'solid', 'solid']



for i in principalidad_historico['fecinf'].unique():
    x_data.append(i)


for ent in entidades:
    lista = []
    for y_values in principalidad_historico[principalidad_historico.entidad==ent]['id_princ_cliente']:
        lista.append(round(y_values))
    y_data.append(lista)


fig2= go.Figure()

for i in range(0, len(entidades)):
    fig2.add_trace(go.Scatter(x=x_data, y=y_data[i], mode='lines',
        name=entidades[i],
        line=dict(color=colors[i], width=line_size[i], dash = dash_type[i]),
        connectgaps=True,
    ))

    # endpoints
    fig2.add_trace(go.Scatter(
        x=[x_data[0], x_data[-1]],
        y=[y_data[i][0], y_data[i][-1]],
        mode='markers',
        marker=dict(color=colors[i])#, size=mode_size[i])
    ))

fig2.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=True,
    ),
    autosize=False,
    width=1150,
    height=800,
    margin=dict(
        autoexpand=False,
        l=100,
        r=150,
        t=110,
    ),
    showlegend=False,
    plot_bgcolor= 'white'#'#f3f6f4'
)




annotations=[]

y_etiquetas = []

for i in y_data:
    j = i[len(i)-1]
    while j in y_etiquetas:
        j-=1     
    y_etiquetas.append(j)



for y_trace,etiqueta ,ent in zip(y_data,y_etiquetas, entidades):
    
        annotations.append(dict(xref='paper', x=0.95, y=etiqueta,
                                  xanchor='left', yanchor='middle',
                                  text=ent + ' {}%'.format(y_trace[len(principalidad_historico['fecinf'].unique())-1]),
                                  font=dict(family='Arial',
                                            size=12),
                                  showarrow=False))
     
fig2.update_layout(annotations=annotations)

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
                            html.H3("Principalidad ultimo mes"),
                            html.Div(dcc.Graph(figure=fig)),
                            #html.P("Población: Totalidad de Personas fisicas registradas en CENDEU segmentadas por entidad de la que son clientes y si ya son clientes ITAU o no")
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
                            html.H3("Principalidad Mensual Historica"),
                            html.Div(dcc.Graph(figure=fig2)),
                            #html.P("Población: Totalidad de deuda de personas fisicas registradas en CENDEU segmentada por entidad y si ésta corresponde a ITAU o no")
                        ],
                    ),
                    width=12,
                )
            ],
        ),
        html.Div(className="separador2"),
    ]
)







