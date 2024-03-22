import pandas as pd
import numpy as np
import plotly.express as px
import warnings as ws
import dash_bootstrap_components as  dbc

from graph1 import *
from graph2 import *
from graph3 import *
from graph4 import *
from controllers import *
from dash import Dash, html, dash_table
from dash.dependencies import Input, Output

pd.set_option('Display.max_columns', None)
ws.filterwarnings('ignore')


df = pd.read_excel('data/dados.xlsx', 
                   usecols=['ID_Pedido', 'Data_Pedido', 'ID_Representante',
        'Nome_Representante', 'Regional', 'ID_Produto', 'Nome_Produto',
        'Valor_Produto', 'Quantidade_Vendida', 'Valor_Total_Venda',
        'Nome_Cliente', 'Cidade_Cliente', 'Estado_Cliente'])


app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

df_product = html.Div([
    html.H6('Total Sales per Product (Month)', style={'font-style': 'normal',
                                                'font-weight': '500',
                                                'color': 'white',
                                                'font-style': 'bold',
                                                'letter-spacing': '2px',
                                                'margin-bottom': '10px',
                                                'margin-top': '30px',
                                                'text-align': 'center'}),
    dash_table.DataTable(
        id='df_prod',
        columns=[
            {'name': 'Product', 'id': 'Nome_Produto'},
            {'name': 'Total Sales', 'id': 'Valor_Total_Venda'}
        ],
        style_header={'backgroundColor': 'rgb(6, 6, 6)', 'fontWeight': 'bold', 'text-transform':'uppercase'},
        style_cell={'backgroundColor': 'rgb(6, 6, 6)', 'color': 'white'}
    )
])

app.layout = dbc.Container(
    children=[
        dbc.Row([
            html.H1('Interactive Sales Dashboard', style = {'text-align': 'center', 
                                                               'font-size': '40px', 
                                                               'font-style': 'italic',
                                                               'margin-top': '20px',
                                                               'letter-spacing': '2px',
                                                               'text-transform': 'uppercase'}),
            controllers
        ], style={'box-shadow': '0px 4px 6px rgba(255, 255, 255, 0.5)'}),

        dbc.Row([
            graph1,
    ]),

        dbc.Row([
            dbc.Col([
                graph2
            ], width=6),
            dbc.Col([
                graph3
            ], width=6, style = {'margin-top': '20px'})
        ]),

        dbc.Row([
            dbc.Col([graph4]),
            dbc.Col([df_product], style = {'margin-right': '50px'}),
        ])
    ],
    fluid=True
)


@app.callback([Output('graph1', 'figure'), Output('graph2', 'figure'), 
               Output('graph3', 'figure'), Output('graph4', 'figure'),
               Output('df_prod', 'data')],
              [Input('monthselection', 'value')])


def update_hist(months):

    df_months = df[df['Data_Pedido'].dt.month == months]
    df_months['day'] = df_months['Data_Pedido'].dt.day
    df_grouped = df_months.groupby('day')['Valor_Total_Venda'].sum().reset_index()
    hist = px.line(df_grouped, x='day', y='Valor_Total_Venda', width=1500,
                      height=600, title='Sales per Month',
                      color_discrete_sequence= ['#4292c6'])
   
    hist.update_layout(
        xaxis_title='Month Day',
        yaxis_title='Total Sales',
        showlegend=False,
        plot_bgcolor='#000',
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color='white')
    )

    df_grouped = df_months.groupby('Regional')['Valor_Total_Venda'].sum().reset_index()
    hist2 = px.bar(df_grouped, x='Regional', y='Valor_Total_Venda', width=800,
                      height=600, title='Sales per Region', color = 'Regional',
                      color_discrete_sequence= ['#f7fbff', '#2171b5'])
   
    hist2.update_layout(
        xaxis_title='Region',
        yaxis_title='Total Sales',
        showlegend=False,
        plot_bgcolor='#000',
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color='white')
    )

    pie = px.pie(df_months, names='Nome_Representante', 
                 values='Valor_Total_Venda', width=600, height=600,
                 color_discrete_sequence=px.colors.sequential.Reds)
   

    pie.update_traces(
        hoverinfo='label+percent',
        textinfo='value',
        textfont=dict(color='black'),
        marker=dict(line=dict(color='#000', width=2))
    )

    pie.update_layout(
        showlegend=True,
        legend=dict(font=dict(color='white')),
        plot_bgcolor='#000',
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color='white'),
        title=dict(text='Sales by Representative', font=dict(color='white'))
    )



    df_grouped = df_months.groupby('Estado_Cliente')['Valor_Total_Venda'].sum().reset_index().sort_values(by = ['Valor_Total_Venda'])
    hist4 = px.bar(df_grouped, y='Estado_Cliente', x='Valor_Total_Venda', width=800,
                      height=600, title='Sales per State', color = 'Estado_Cliente',
                      color_discrete_sequence= px.colors.sequential.Reds)
   
    hist4.update_layout(
        xaxis_title='State',
        yaxis_title='Total Sales',
        showlegend=False,
        plot_bgcolor='#000',
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color='white')
    )

    df_product = df_months.groupby('Nome_Produto')['Valor_Total_Venda'].sum().reset_index().sort_values(by = ['Valor_Total_Venda'], ascending = False)

    return hist, hist2, pie, hist4, df_product.to_dict('records')
    


if __name__ == '__main__':
    app.run(debug=False)