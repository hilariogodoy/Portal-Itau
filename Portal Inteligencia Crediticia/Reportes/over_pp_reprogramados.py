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

previsiones = pd.read_sql("""
SELECT a.clinum,
       NROOPERACION,
       codprod,
       ppdesc,
       ppcges,
       b.atraso_cliente,
       b.deuda_cliente,
       CASE
           WHEN c.NRO_ACUERDO IS NOT NULL THEN 'Reprogramado'
           ELSE 'Normal'
       END AS repro,
       CASE
           WHEN b.atraso_cliente > 30 THEN b.deuda_cliente
           ELSE 0
       END AS over_30,
       CASE
           WHEN b.atraso_cliente > 90 THEN b.deuda_cliente
           ELSE 0
       END AS over_90,
       CASE
           WHEN b.atraso_cliente BETWEEN 90 AND 360 THEN b.deuda_cliente
           ELSE 0
       END AS over_90_360
FROM previsiones_bcapers AS a
LEFT JOIN
  (SELECT clinum,
          MAX(diasatraso) AS atraso_cliente,
          SUM(importe_deuda + intereses) AS deuda_cliente
   FROM previsiones_bcapers
   WHERE tipo_oper = 'PRE'
   GROUP BY clinum) AS b ON a.clinum = b.clinum
LEFT JOIN
  (SELECT DISTINCT cliente,
                   NRO_ACUERDO
   FROM interfaces..PXTBPPRO
   WHERE SEGMENTO IN ('4000',
                      '5000')
     AND COBRADA = 'N'
     OR (COBRADA = 'S'
         AND FECHA_DE_PAGO_CUOTA >
           (SELECT top 1 fechaproceso
            FROM previsiones_bcapers))) AS c ON a.clinum = c.cliente
AND CAST(a.nrooperacion AS numeric) = c.nro_acuerdo
INNER JOIN
  (SELECT DISTINCT PPCODI,
                   PPDESC,
                   ppcges
   FROM Interfaces..PXMTOP) AS d ON a.CODPROD = d.ppcodi
WHERE tipo_oper = 'PRE'
""" , conn)

df = pd.read_sql("""
select dateadd(MONTH, datediff(MONTH, 0, cast(cast(fecha_vto as char) as date)), 0) as mes_vto	, CAST(SUM(CAPITAL_DE_LA_CUOTA + INTERES_DE_LA_CUOTA + AJUSTE_DE_LA_CUOTA)/1000000 AS DECIMAL(18,1)) as total_cuotas
from interfaces..PXTBPPRO
where (cobrada = 'N'
or (COBRADA = 'S' and FECHA_DE_PAGO_CUOTA > (select top 1 fechaproceso from previsiones_bcapers)))
and cast(cast(fecha_vto as char) as date) >= dateadd(MONTH, datediff(MONTH, 0, DATEADD(MONTH, 0, getdate())), 0)
and segmento in ('4000','5000')
group by dateadd(MONTH, datediff(MONTH, 0, cast(cast(fecha_vto as char) as date)), 0)
order by mes_vto
""" , conn)





#%% Dataframes

over_repro = previsiones.groupby("repro")[
    "over_30", "over_90", "over_90_360", "deuda_cliente"
].sum()

over_repro["over 30"] = over_repro["over_30"] / over_repro["deuda_cliente"]
over_repro["over 90"] = over_repro["over_90"] / over_repro["deuda_cliente"]
over_repro["over 90-360"] = over_repro["over_90_360"] / over_repro["deuda_cliente"]

over_repro = (
    over_repro.loc[:, ["over 30", "over 90", "over 90-360"]]
    .stack()
    .reset_index()
    .rename(columns={"level_1": "over", 0: "indicador"})
)

over_30_repro_producto = (
    previsiones[
        (previsiones["repro"] == "Reprogramado")
        & (previsiones["atraso_cliente"] < 91)
        & (previsiones["over_30"] > 0)
    ]
    .groupby(["ppdesc", "ppcges"])["over_30", "NROOPERACION"]
    .agg(over_30=("over_30", "sum"), cantidad=("NROOPERACION", "count"))
    .sort_values("over_30", ascending=False)
    .reset_index()
)

df_trunc = df[df["mes_vto"] < '20250101']  #trunco el dataset para que el grafico no sea demasiado extenso

#%% Graficos


fig = px.bar(over_repro, 
             x="over", 
             y="indicador", 
             color="repro",
             text_auto=True,
             height=300,
             width=600,
             template="plotly_white",
             color_discrete_sequence=["#E9C46A","#E76F51"])

fig.update_layout(barmode="group",
                  yaxis_title="",
                  xaxis_title="",
                  yaxis_tickformat=",.01%",   #formato porcentaje con 1 decimal
                  yaxis_nticks=3,
                  yaxis_showgrid=False,
                  legend=dict(title="Préstamo", 
                              orientation="h",
                              y=1.2,
                              x=0.15))


fig2 = px.scatter(over_30_repro_producto,
                 x="over_30",
                 y="cantidad",
                 color="ppcges",
                 size="over_30",
                 size_max=50,
                 template="plotly_white",
                 width=1000)

fig2.update_layout(xaxis=dict(showgrid=False, title="over 30-90"),
                  yaxis=dict(showgrid=False),
                  legend=dict(title="Tipo de préstamo")
                 )



fig3 = px.bar(df_trunc, 
             x=pd.to_datetime(df_trunc["mes_vto"]),
             y="total_cuotas",
             template="plotly_white",
             text_auto=True,
             height=300,
             color_discrete_sequence = ["#F4A261"])

fig3.update_layout(xaxis_tickformat= '%m-%Y',
                  yaxis_tickprefix= "$",
                  yaxis_ticksuffix= "MM",
                  xaxis_showgrid=False,
                  yaxis_showgrid=False,
                  xaxis_title="",
                  yaxis_title="",
                  yaxis_nticks= 3
                 )


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
                            html.H3("Write Off Ultimo Año"),
                            html.Div(dcc.Graph(figure=fig)),
                            #html.P("Población: Totalidad de Personas fisicas registradas en CENDEU segmentadas por entidad de la que son clientes y si ya son clientes ITAU o no")
                        ],
                    ),
                    width=12,
                )
                
                
            ],
        ),       
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        className="uno mx-2",
                        children=[
                            html.H3("Write Off Ultimo Año"),
                            html.Div(dcc.Graph(figure=fig2)),
                            #html.P("Población: Totalidad de Personas fisicas registradas en CENDEU segmentadas por entidad de la que son clientes y si ya son clientes ITAU o no")
                        ],
                    ),
                    width=12,
                )
                
                
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        className="uno mx-2",
                        children=[
                            html.H3("Write Off Ultimo Año"),
                            html.Div(dcc.Graph(figure=fig3)),
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







