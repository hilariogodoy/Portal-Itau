# %%
import dash
from dash import dash_table
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pyodbc 

# %%
#Conexion SQL
conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=SQLNONITPROD; DATABASE=aig;Trusted_Connection=yes') 

exclusiones_x_cliente = pd.read_sql("""SELECT * FROM vw_motivos_exclusion_cantidad order by cast(cantidad_motivos as int)""", conn)

motivos_exclusion = pd.read_sql( """SELECT * FROM vw_motivos_exclusion ORDER BY 3 """, conn)

excluidos1motivo = pd.read_sql( """select * from
dbo.vw_excluidos_1_motivo order by 2 desc """, conn)

#codigos = pd.read_sql("""select codigo, descripcion from tbcodigos""",conn)


conn.close


#%% Gráficos

fig_exclusiones=px.bar(exclusiones_x_cliente, y='total_clientes',x='cantidad_motivos', orientation = 'v', text_auto = True)

## -------------------------------------------------------------------

fig_excluidos_motivo = px.bar(motivos_exclusion, x='cantidad', y='Descripcion', orientation = 'h', text_auto = True)
fig_excluidos_motivo.update_layout(height=2000)
## -------------------------------------------------------------------


fig1motivo = go.Figure(data=[go.Pie(labels = list(excluidos1motivo['Descripcion']), values = list(excluidos1motivo['cantidad']), textinfo='label+percent',insidetextorientation='radial', hole = .5, textfont_size=14)])
fig1motivo.update_layout(height=1125, width = 1125)
fig1motivo.update(layout_showlegend=False)


#%% Layout Pagina


#app.layout = dbc.Container(#linea comentada para .py
layout = dbc.Container(
    [
        html.Div(className="separador1"),
        html.H1("Análisis Motivos de Exclusión de Oferta Crediticia"),
        html.Div(className="separador2"),
                dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        className="uno mx-2",
                        children=[
                            html.H3("Motivos de exclusion"),
                            html.Div(dcc.Graph(figure=fig_excluidos_motivo)),
                            html.P("Total de clientes excluidos agrupados por motivo")
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
                            html.H3("Cuenta de cantidad de motivos por cliente"),
                            html.Div(dcc.Graph(figure=fig_exclusiones)),
                            html.P("Total de clientes excluidos agrupados por cantidad de motivos por los que fueron rechazados")
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
                            html.H3("Excluidos por un solo Filtro"),
                            html.Div(dcc.Graph(figure=fig1motivo)),
                            html.P("Clientes que fueron excluidos por un solo motivo")
                        ],
                    ),
                    width=12,
                )
            ],
        ),
        html.Div(className="separador2"),


    ]
)


# if __name__ == '__main__':
#     app.run_server(debug=True, use_reloader=False)