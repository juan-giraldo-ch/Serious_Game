# coding=utf-8
import dash
import dash_core_components as dcc
import dash_html_components as html
from app import app
import flask

# accum = float(flask.request.cookies.get('accum_val'))


def self_score():

    A = html.Div([
        html.Div(id='scb_text', children='Accumulated Revenue:',
                 style={'font-size': '1.2vw','color':app.color_4, 'width': '100%', 'height':'1.5vw'}),
        dcc.Textarea(id='score_board1', readOnly='readOnly',# value='€ ' + '0.00',
                     style={'resize': 'none', #'width': '50%', 'height': '1%',
                            'borderColor': app.color_3,'textAlign': 'center','backgroundColor':app.color_3, 'color':app.color_8, 'font-size': '1.2vw','width': '100%',
                            'height':'3vw'},
                     rows=0),
    ], id='score_board_h')
    # print(accum)

    return A


def fig_rev():
    B = html.Div([
        html.Div([
            dcc.Graph(id='graph_reve',style={'height': '20vw'}),
        ],style={'height': '20vw'}),
    ], id='datatable_graph_reve', style={'display': 'none', 'height': '20vw'})
    return B


def position_lead():

    C = html.Div([
        html.Div(id='position_lead', children='Current Position:',
                 style={'font-size': '1.2vw','color':app.color_4, 'width': '100%', 'height':'1.5vw'}),
        dcc.Textarea(id='position_lead1', readOnly='readOnly', value='--',
                     style={'resize': 'none', #'width': '50%', 'height': '1%',
                            'borderColor': app.color_3,'textAlign': 'center','backgroundColor':app.color_3, 'color':app.color_8, 'font-size': '1.2vw','width': '100%',
                            'height':'3vw'},
                     rows=0),
    ], id='position_lead_h')
    # print(accum)

    return C
