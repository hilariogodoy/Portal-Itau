# %%
import dash
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pyodbc 
from app import app

# %%
#Conexion SQL
conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=SQLNONITPROD; DATABASE=aig;Trusted_Connection=yes') 

df_treemap_categoria_principal = pd.read_sql("""
SELECT * FROM vw_cendeu_treemap_por_cliente_principal order by cantidad desc
""" , conn)
df_treemap_categoria_principal = df_treemap_categoria_principal.fillna(value='N/A')

#codigos = pd.read_sql("""select codigo, descripcion from tbcodigos""",conn)

mes= pd.read_sql("""
select max(fecha) as mes
from dbo.clientes_itau_mercado_cendeu
""" , conn)

conn.close


# %% Mes y Titulos
mes_corriente = mes["mes"].astype("string")
mes["mes"].astype("string")
title1 = "Total clientes - Por tipo de negocio"
title_pbnk = title1 #+ mes["mes"].astype("string")
title2 = "Total clientes - Apertura PSI"
title_psi =  title2 #+ mes["mes"].astype("string")



#%% Layout Pagina


#app.layout = dbc.Container(#linea comentada para .py
layout = dbc.Container(
    [
        html.Div(className="separador1"),
        html.H1("Banca Personal | Información de Mercado |" + mes["mes"].astype("string")),
        html.Div(className="separador2"),
        
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        className="uno mx-2",
                        children=[
                            html.H3(title_pbnk),
                            dcc.Dropdown(
                                id='dropdown',
                                style={'color': 'black'},
                                options=[
                                    {'label': 'Cuenta Chat', 'value': 'CUENTA CHAT'},
                                    {'label': 'No Cuenta Chat', 'value': 'NO CUENTA CHAT'},
                                ],
                                value= 'cuenta_chat',
                               # multi=True
                            ),
                            html.Div(dcc.Graph(id = 'x_categ')),
                            html.P("Población: Totalidad de clientes con y sin info en CENDEU, clasificados por entidad y motivo de rechazo crediticio en ITAU si corresponde")
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
                            html.H3(title_psi),
                            html.Div(dcc.Graph(id='x_categ_psi')),
                            html.P("Población: Totalidad de clientes con y sin info en CENDEU, clasificados por entidad y motivo de rechazo crediticio en ITAU si corresponde y clasificacion PSI")
                        ],
                    ),
                    width=12,
                )
            ],
        ),
        html.Div(className="separador2"),
    ]
)


#%% Gráficos


@app.callback([Output('x_categ', 'figure'),
               Output('x_categ_psi', 'figure')],
              [Input('dropdown', 'value')])

def update_graph(cuenta_chat):
    
    fig_treemap_x_categ = px.treemap(    	
        df_treemap_categoria_principal[df_treemap_categoria_principal['cuenta_chat'] == cuenta_chat],
        path=[px.Constant("Total clientes (Excluye Empleados y Asignación Universal)"), 'riesgo_sf','situacion','tipo_cliente','deuda_itau','oferta','pbnk','categoria','entidad','tiny_motivo_exclusion'],
        values="cantidad",
        color="categoria",
        color_discrete_map={
            "(?)": "#fff2cc",
    	"Sin riesgo en SF": "black",
            "5 - Fintech/Digital": "#f4cccc",
            "1 - Bancos 1er Orden": "#fe7f2d",
            "2 - Bancos 2do Orden": "#fcca46",
            "3 - Bancos 3er Orden": "#a1c181",
            "4 - Financieras": "#619b8a",
            "6 - Otros": "grey",
        },
        height=550
    )
    
    fig_treemap_x_categ.update_traces(root_color="grey")
    fig_treemap_x_categ.update_layout(
        margin=dict(t=20, l=0, r=0, b=0), uniformtext=dict(minsize=9, mode="hide")
    )
    
    fig_treemap_x_categ.data[0]["textfont"]["color"] = "black"
    
    ## -------------------------------------------------------------------
    
    fig_treemap_x_categ_psi = px.treemap(    	
        df_treemap_categoria_principal[df_treemap_categoria_principal['cuenta_chat'] == cuenta_chat],
        path=[px.Constant("Total clientes (Excluye Empleados y Asignación Universal)"), 'riesgo_sf','tipo_cliente','deuda_itau','oferta','cliente_psi','categoria','entidad','tiny_motivo_exclusion'],
        values="cantidad",
        color="categoria",
        color_discrete_map={
            "(?)": "#fff2cc",
    	"Sin riesgo en SF": "black",
            "5 - Fintech/Digital": "#f4cccc",
            "1 - Bancos 1er Orden": "#fe7f2d",
            "2 - Bancos 2do Orden": "#fcca46",
            "3 - Bancos 3er Orden": "#a1c181",
            "4 - Financieras": "#619b8a",
            "6 - Otros": "grey",
        },
        height=550
    )
    
    fig_treemap_x_categ_psi.update_traces(root_color="grey")
    fig_treemap_x_categ_psi.update_layout(
        margin=dict(t=20, l=0, r=0, b=0), uniformtext=dict(minsize=9, mode="hide")
    )
    
    fig_treemap_x_categ_psi.data[0]["textfont"]["color"] = "black"
    
    return fig_treemap_x_categ, fig_treemap_x_categ_psi

# if __name__ == '__main__':
#     app.run_server(debug=True, use_reloader=False)