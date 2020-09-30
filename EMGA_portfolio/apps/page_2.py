# coding=utf-8
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
# from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
# import dash_daq as daq
import flask
import dash_bootstrap_components as dbc
import json
import psycopg2
import os  # Importing OS functions

# import os  # Importing OS functions

from app import app

from apps import tue_header, fig_day, buttons, score_info, login

################################################################################

#################### - SECOND PAGE - ############################

if app.database_url == 'Local':
    url_data = os.popen("heroku config:get DATABASE_URL -a emga").read().strip()  # When local machine

if app.database_url == 'Server':
    url_data = os.environ.get('DATABASE_URL')  # When Server


DATABASE_URL = (url_data)
layout = html.Div([

    # ----------------------------------------------------------------------

    html.Div([

        # ---------- SCORE BOARD ----------- #
        dbc.Container([
            dbc.Row(
                [
                    dbc.Col([

                        tue_header.header(),
                    ], width=12, lg=12, md=12, style={'backgroundColor': app.color_3}
                    ),
                ], ),

            dbc.Row(
                [
                    dbc.Col([

                    ], width=2, lg=2, md=2, sm=2, style={'backgroundColor': app.color_3, 'textAlign': 'center'}),

                    dbc.Col([
                        tue_header.curr_date(),
                    ], width=9, lg=9, md=9),
                ],
            ),

            # Figs. Top!
            dbc.Row(
                [
                    dbc.Col([
                        html.Div([
                            buttons.next_day(),
                        ], style={'backgroundColor': app.color_3}),
                    ], width=2, lg=2, md=2, sm=2, style={'backgroundColor': app.color_3, 'textAlign': 'center'}),

                    dbc.Col([
                        # Fig. Top-Left
                        html.Div([
                            dcc.Loading(fig_day.fig_bid(), color=app.color_3, type='circle'),

                        ], style={'width': '95%', 'height': '95%'}),
                    ], width=5, lg=5, md=5),

                    dbc.Col([
                        # Fig. Top-Right
                        html.Div([
                            dcc.Loading(fig_day.fig_unbal(), color=app.color_3, type='circle'),
                        ], style={'width': '95%', 'height': '95%'}),
                    ], width=5, lg=5, md=5),
                ], style={'height': '25vw'}, justify="around"
            ),

            dbc.Row(
                [
                    dbc.Col([

                    ], width=2, lg=2, md=2, sm=2, style={'backgroundColor': app.color_3, 'textAlign': 'center'}),

                    dbc.Col([

                    ], width=10, lg=10, md=10, sm=10, style={'backgroundColor': app.color_1, 'textAlign': 'center'}),

                ], style={'height': '1vw'},
            ),

            dbc.Row(
                [
                    dbc.Col([

                    ], width=2, lg=2, md=2, sm=2, style={'backgroundColor': app.color_3, 'textAlign': 'center'}),

                    dbc.Col([
                        html.Div([
                            dcc.Loading(fig_day.fig_ahead(), color=app.color_3, type='circle'),
                        ], style={'width': '95%', 'height': '95%'}),
                    ], width=5, lg=5, md=5),

                    dbc.Col([
                        html.Div([
                            dcc.Loading(fig_day.fig_accum(), color=app.color_3, type='circle'),

                        ], style={'width': '95%', 'height': '95%'}),
                    ], width=5, lg=5, md=5),
                ], style={'height': '25vw'}, justify="around",
            ),

        ], fluid=True),
    ]),
], id='Page_2', style={'height': '100%', 'backgroundColor': app.color_1})


##############################################################################


################################################

# ----------  UPDATES THE FIGURE ""Day Ahead Bid Information"" ----------- #
@app.callback([Output('graph_data', 'figure'),
               Output('datatable_graph_data', 'style')],
              [Input('Page_2', 'id')])
def display_graph(nome):
    A = nome
    b2 = int(flask.request.cookies.get('b2'))
    dash.callback_context.response.set_cookie('b2p', str(b2), max_age=7200)

    b2p = int(flask.request.cookies.get('b2p'))

    P_value = (json.loads((flask.request.cookies.get('P_value'))))

    # df = pd.DataFrame(app.ddf)

    aa = (flask.request.cookies.get('ddf'))

    # s1 = json.dumps(df)
    df = json.loads(aa)

    df = pd.DataFrame.from_dict(df, orient='columns')
    # P_value = app.Pvalue
    clicks = 1
    if (df.empty or len(df.columns) < 1 or clicks is None or P_value == 0):
        figure = {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
        return figure, {'display': 'none'}
    else:
        pr = pd.DataFrame(app.prices)
        fact = pd.DataFrame(app.real_P)

        realp = (fact[fact.columns[b2 + 1]])  # * float(P_value)
        df['Pnom'] = float(P_value) * np.ones(24)
        figure = {
            'data': [{'x': df[df.columns[0]], 'y': df[df.columns[1]], 'type': 'bar', 'name': 'Bid',
                      'marker': {'color': app.color_3}},
                     {'x': df[df.columns[0]], 'y': realp, 'type': 'bar', 'name': 'RealP',
                      'marker': {'color': app.color_bar2}},
                     {'x': df[df.columns[0]], 'y': pr[pr.columns[b2 + 1]], 'type': 'line', 'name': 'Price',
                      'marker': {'color': app.color_line}, 'yaxis': 'y2'},
                     ],
            'layout': go.Layout(title='Day Ahead Information', titlefont=dict(color=app.color_3),
                                xaxis=dict(title='Time', automargin=True, gridcolor=app.color_3,
                                           titlefont=dict(color=app.color_3), tickfont=dict(color=app.color_3)),
                                yaxis=dict(title='Energy [MWh]', titlefont=dict(color=app.color_3),
                                           tickfont=dict(color=app.color_3), automargin=True, gridcolor=app.color_3),
                                yaxis2=dict(title='Day ahead price [€/MWh]', titlefont=dict(color=app.color_line),
                                            tickfont=dict(color=app.color_line), overlaying='y', side='right',
                                            automargin=True),
                                margin=dict(l=50, r=50, b=60, t=40),
                                hovermode="closest",
                                paper_bgcolor=app.color_bfig,  # 'app.color_6,
                                plot_bgcolor=app.color_1,
                                # width=650, height=400,
                                legend_orientation="h",
                                legend=dict(x=-.1, y=1.1, font=dict(color=app.color_3)),
                                )
        }
        return figure, {'display': 'inline-block', 'width': '95%', 'height': '95%'}


# #################################################

# ----------  UPDATES THE FIGURE "Revenue per Period" ----------- #
@app.callback([Output('graph_day_ahead', 'figure'),
               Output('datatable_graph_day_ahead', 'style')],
              [Input('Page_2', 'id')])
def display_graph_day_ahead(nome):
    A = nome
    # df = pd.DataFrame(app.ddf)
    aa = (flask.request.cookies.get('ddf'))

    # s1 = json.dumps(df)
    df = json.loads(aa)

    df = pd.DataFrame.from_dict(df, orient='columns')

    P_value = (json.loads((flask.request.cookies.get('P_value'))))

    # P_value = app.Pvalue
    clicks = 1
    b2 = int(flask.request.cookies.get('b2'))

    if (df.empty or len(df.columns) < 1 or clicks is None or P_value == 0):
        figure = {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
        return figure, {'display': 'none'}
    else:
        pr = pd.DataFrame(app.prices)
        fact = pd.DataFrame(app.real_P)
        ubpr_pos = pd.DataFrame(app.UB_prices_pos)
        ubpr_neg = pd.DataFrame(app.UB_prices_neg)

        realp = (fact[fact.columns[b2 + 1]]).array
        unb = realp - df[df.columns[1]]
        act_prices = np.zeros((len(realp), 1))
        for i in range(len(realp)):
            if unb[i] >= 0.0:
                act_prices[i] = unb[i] * pr.iloc[i, b2 + 1] * (ubpr_pos.iloc[i, b2 + 1])
            else:
                act_prices[i] = unb[i] * pr.iloc[i, b2 + 1] * (ubpr_neg.iloc[i, b2 + 1])
        act_prices = pd.DataFrame(act_prices)
        df['Pnom'] = float(P_value) * np.ones(24)

        figure = dict(
            data=[dict(x=df[df.columns[0]], y=df[df.columns[1]] * pr[pr.columns[b2 + 1]].array, type='bar',
                       name='Expected',
                       marker=dict(color=app.color_3)),
                  dict(x=df[df.columns[0]], y=(act_prices[act_prices.columns[0]]), type='bar', name='Inb. Income',
                       marker=dict(color=app.color_bar2),
                       textfont_color=app.color_3,
                       ),
                  dict(x=df[df.columns[0]], y=(act_prices[act_prices.columns[0]].values + (df[df.columns[1]] * pr[pr.columns[b2 + 1]].array)),
                       type='line', name='Total Rev.',
                       marker=dict(color=app.color_line),
                       textfont_color=app.color_3,
                       ),

                  ],
            layout=go.Layout(dict(title='Revenue per Period', titlefont=dict(color=app.color_3),
                                  xaxis=dict(title='Time', automargin=True, gridcolor=app.color_3,
                                             titlefont=dict(color=app.color_3), tickfont=dict(color=app.color_3)),
                                  yaxis=dict(title='Revenue [€]', automargin=True, gridcolor=app.color_3,
                                             titlefont=dict(color=app.color_3), tickfont=dict(color=app.color_3))),
                             margin=dict(l=50, r=50, b=60, t=40),
                             hovermode="closest",
                             paper_bgcolor=app.color_bfig,
                             plot_bgcolor=app.color_1,
                             # width=650, height=400,
                             legend_orientation="h",
                             legend=dict(x=-.1, y=1.06, font=dict(color=app.color_3)),
                             barmode='relative'
                             ),
        )
        return figure, {'display': 'inline-block', 'width': '95%', 'height': '95%'}


#
#
# #################################################


# ----------  UPDATES THE FIGURE "Day Accumulated Revenue" ----------- #
@app.callback([Output('graph_accum_revenue', 'figure'),
               Output('datatable_graph_accum_revenue', 'style')],
              [Input('Page_2', 'id')])
def display_graph_accum_revenue(nome):
    A = nome
    # df = pd.DataFrame(app.ddf)

    aa = (flask.request.cookies.get('ddf'))

    # s1 = json.dumps(df)
    df = json.loads(aa)

    df = pd.DataFrame.from_dict(df, orient='columns')

    P_value = (json.loads((flask.request.cookies.get('P_value'))))

    # P_value = app.Pvalue
    clicks = 1
    accum = [0]
    accumA = float(flask.request.cookies.get('accum_val'))
    b2 = int(flask.request.cookies.get('b2'))

    if (df.empty or len(df.columns) < 1 or clicks is None or P_value == 0):
        figure = {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
        return figure, {'display': 'none'}
    else:
        pr = pd.DataFrame(app.prices)

        fact = pd.DataFrame(app.real_P)
        ubpr_pos = pd.DataFrame(app.UB_prices_pos)
        ubpr_neg = pd.DataFrame(app.UB_prices_neg)
        realp = (fact[fact.columns[b2 + 1]]).array
        unb = realp - df[df.columns[1]]
        act_prices = np.zeros((len(realp), 1))
        for i in range(len(realp)):
            if unb[i] >= 0.0:
                act_prices[i] = unb[i] * pr.iloc[i, b2 + 1] * (ubpr_pos.iloc[i, b2 + 1])
            else:
                act_prices[i] = unb[i] * pr.iloc[i, b2 + 1] * (ubpr_neg.iloc[i, b2 + 1])

        act_prices = pd.DataFrame(act_prices)
        AA = (df[df.columns[1]] * (pr[pr.columns[b2 + 1]]).array + (act_prices[act_prices.columns[0]]).array)
        A = accum
        accum = np.cumsum(AA)
        exp_accum = np.cumsum(realp * pr[pr.columns[b2 + 1]])
        dash.callback_context.response.set_cookie('accum_1', str(accum.iloc[-1]), max_age=7200)

        if abs(accum.iloc[-1] - A[-1]) > 0:
            accumA = accumA + accum.iloc[-1]
            cookie_exp = float(flask.request.cookies.get('exp_accum'))

            cookie_exp = cookie_exp + exp_accum.iloc[-1]

            dash.callback_context.response.set_cookie('exp_accum', str(cookie_exp), max_age=7200)

        else:
            accumA = accumA
            # cookie_exp = cookie_exp

        # co = set_cookie('acc_cookie', app.accum) # colocar en return

        df['Pnom'] = float(P_value) * np.ones(24)
        figure = dict(
            data=[dict(x=df[df.columns[0]], y=np.cumsum(realp * pr[pr.columns[b2 + 1]]), type='line',
                       name='Expected', marker=dict(color=app.color_3)),
                  dict(x=df[df.columns[0]],
                       y=accum,
                       type='line', name='Actual', marker=dict(color=app.color_line)),
                  ],


            layout=go.Layout(dict(title='Day Accumulated Revenue', titlefont=dict(color=app.color_3),
                                  xaxis=dict(title='Time', automargin=True, gridcolor=app.color_3,
                                             titlefont=dict(color=app.color_3), tickfont=dict(color=app.color_3)),
                                  yaxis=dict(title='Revenue [€]', automargin=True, gridcolor=app.color_3,
                                             titlefont=dict(color=app.color_3), tickfont=dict(color=app.color_3))),
                             margin=dict(l=50, r=50, b=60, t=40),
                             hovermode="closest",
                             paper_bgcolor=app.color_bfig,
                             plot_bgcolor=app.color_1,
                             # width=650, height=400,
                             legend_orientation="h",
                             legend=dict(x=-.1, y=1.1, font=dict(color=app.color_3)),
                             barmode='relative'
                             ),
        )

        dash.callback_context.response.set_cookie('accum_val', str(accumA), max_age=7200)

        return figure, {'display': 'inline-block', 'width': '95%', 'height': '95%'}


#
# #################################################
#
# ----------  UPDATES THE FIGURE "Power inbalance & Inbalance tariffs" ----------- #
@app.callback([Output('graph_unbal', 'figure'),
               Output('datatable_graph_unbal', 'style')],
              [Input('Page_2', 'id')])
def display_graph_unbal(nome):
    A = nome
    # df = pd.DataFrame(app.ddf)
    aa = (flask.request.cookies.get('ddf'))

    # s1 = json.dumps(df)
    df = json.loads(aa)

    df = pd.DataFrame.from_dict(df, orient='columns')

    # test = pd.Series(df[df.columns[1]])

    P_value = (json.loads((flask.request.cookies.get('P_value'))))

    # P_value = app.Pvalue
    clicks = 1
    b2 = int(flask.request.cookies.get('b2'))

    if (df.empty or len(df.columns) < 1 or clicks is None or P_value == 0):
        figure = {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
        return figure, {'display': 'none'}
    else:
        pr = pd.DataFrame(app.prices)
        fact = pd.DataFrame(app.real_P)
        ubpr_pos = pd.DataFrame(app.UB_prices_pos)
        ubpr_neg = pd.DataFrame(app.UB_prices_neg)
        realp = (fact[fact.columns[b2 + 1]]).array
        # realp = realp.rename('Power_[MWh]')
        unb = realp - df[df.columns[1]]

        figure = {
            'data': [{'x': df[df.columns[0]], 'y': unb, 'type': 'bar', 'name': 'Imbalance',
                      'marker': {'color': app.color_3}},
                     {'x': df[df.columns[0]], 'y': (ubpr_pos[ubpr_pos.columns[b2 + 1]]) * pr[pr.columns[b2 + 1]],
                      'type': 'line',
                      'name': 'Pos. Price',
                      'marker': {'color': app.color_bar2}, 'yaxis': 'y2'},
                     {'x': df[df.columns[0]], 'y': (ubpr_neg[ubpr_neg.columns[b2 + 1]]) * pr[pr.columns[b2 + 1]],
                      'type': 'line',
                      'name': 'Neg. Price',
                      'marker': {'color': app.color_line}, 'yaxis': 'y2'}
                     ],

            'layout': go.Layout(title='Imbalance & Prices', titlefont=dict(color=app.color_3),
                                xaxis=dict(title='Time', automargin=True, gridcolor=app.color_3,
                                           titlefont=dict(color=app.color_3), tickfont=dict(color=app.color_3)),
                                yaxis=dict(title='Imbalance [MWh]', titlefont=dict(color=app.color_3),
                                           tickfont=dict(color=app.color_3), automargin=True, gridcolor=app.color_3),
                                yaxis2=dict(title='Price [€/MWh]', titlefont=dict(color=app.color_line),
                                            tickfont=dict(color=app.color_line), overlaying='y', side='right',
                                            automargin=True),
                                margin=dict(l=50, r=50, b=60, t=40),
                                hovermode="closest",
                                paper_bgcolor=app.color_bfig,  # 'app.color_6,
                                plot_bgcolor=app.color_1,
                                # width=650, height=400,
                                legend_orientation="h",
                                legend=dict(x=-.1, y=1.1, font=dict(color=app.color_3)),
                                )

        }

        return figure, {'display': 'inline-block', 'width': '95%', 'height': '95%'}


################################################

# #################################################


# ----------  SENDS TO PAGE 1 ----------- #
@app.callback(Output('link_b2', 'disabled'),
              [Input('nextD_b', 'n_clicks')])
def button_2(clicks):
    accumA = float(flask.request.cookies.get('accum_val'))
    user_active = flask.request.cookies.get('custom-auth-session')

    if clicks is not None:
        b2 = int(flask.request.cookies.get('b2'))

        b2 = b2 + 1

        rate = float(accumA) / b2


        dash.callback_context.response.set_cookie('b2', str(b2), max_age=7200)
        dash.callback_context.response.set_cookie('b2p', str(b2 - 1), max_age=7200)
        dash.callback_context.response.set_cookie('accum_val', str(accumA), max_age=7200)

        ############################################################
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("""UPDATE Leader_board SET Days = (%s) WHERE Player = (%s);""", (b2, user_active,))
        cur.execute("""UPDATE Leader_board SET Revenue = (%s) WHERE Player = (%s);""", (accumA, user_active,))
        cur.execute("""UPDATE Leader_board SET Rate = (%s) WHERE Player = (%s);""", (rate, user_active,))

        conn.commit()

        cur.close()
        conn.close()
        ############################################################

        return False

# @app.callback(Output('url', 'pathname'),
#               [Input('graph_unbal', 'figure')])
# def day_limit(input):
#
#     b2p = float(flask.request.cookies.get('b2p'))
#
#     ############################
#     ############################
#
#     user_active = flask.request.cookies.get('custom-auth-session')
#
#     print(user_active)
#
#     conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#
#     cur = conn.cursor()
#
#     cur.execute("SELECT days FROM Leader_board WHERE Player = (%s);", (user_active,))
#     # print(players)
#     days = cur.fetchone()
#     cur.close()
#     conn.close()
#
#     # if len(days):
#     print('OK')
#
#     day = days[0]
#     print(day)
#     print(len(app.WF_real_power) / 96)
#
#     if day > len(app.WF_real_power) / 96:
#         return '/Page_end'
#
# ############################
# ############################
