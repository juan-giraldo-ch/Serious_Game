import dash
import dash_core_components as dcc
import dash_html_components as html

from app import app



def fig_bid():
    A = html.Div([
        dcc.Graph(id='graph_data'),
    ],id='datatable_graph_data', style={'display': 'none'})
    return A


def fig_unbal():
    B = html.Div([
        dcc.Graph(id='graph_unbal'),
    ], id='datatable_graph_unbal', style={'display': 'none'})
    return B


def fig_ahead():
    C = html.Div([
        dcc.Graph(id='graph_day_ahead'),
    ], id='datatable_graph_day_ahead', style={'display': 'none'})
    return C


def fig_accum():
    D = html.Div([
        dcc.Graph(id='graph_accum_revenue'),
    ], id='datatable_graph_accum_revenue', style={'display': 'none'})
    return D
