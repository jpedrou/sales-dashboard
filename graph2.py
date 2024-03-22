from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

fig = go.Figure()
fig.update_layout( plot_bgcolor='#000', paper_bgcolor = 'rgba(0,0,0,0)')

graph2 = dbc.Row([
    dcc.Graph(id = 'graph2', figure = fig) 
])