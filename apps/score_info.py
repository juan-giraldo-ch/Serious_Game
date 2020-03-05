# coding=utf-8
import dash
import dash_core_components as dcc
import dash_html_components as html
from app import app


def self_score():
    A = html.Div([
        html.Div(id='scb_text', children='Global Accumulated Revenue:',
                 style={'font-size': '20px', 'margin-left': '5%','color':app.color_4, 'marginTop': '5%'}),
        dcc.Textarea(id='score_board1', readOnly='readOnly', value='€ ' + f'{app.accum:.2f}',
                     style={'width': '30%', 'height': '1%', 'margin-left': '5%', 'resize': 'none',
                            'textAlign': 'center','backgroundColor':app.color_3, 'color':app.color_4,
                            'borderColor': app.color_3},
                     rows=0),
    ], id='score_board_h')
    print(app.accum)

    return A


def fig_rev():
    B = html.Div([
        html.Div([
            dcc.Graph(id='graph_reve'),
        ],),
    ], id='datatable_graph_reve')
    return B
