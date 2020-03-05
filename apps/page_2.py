# coding=utf-8
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import dash_daq as daq
# import os  # Importing OS functions

from app import app

from apps import tue_header, fig_day, buttons, score_info

################################################################################

#################### - SECOND PAGE - ############################


layout = html.Div([

    #################### - HEADER - ############################

    tue_header.header(),

    # ----------------------------------------------------------------------
    html.Div([

            ## Include a link to previous days
            # dcc.Tabs(
            #         id="tabs",
            #         children=[
            #             dcc.Tab(label="Run #1", value="1")
            #         ],
            #         value="1",
            #     ),


        html.Div([
            ##################### - BUTTON FOR returnoing - ############################

            # -- Button for returning to bidding page
                buttons.next_day(),
        ], className='row'),

    ], className='three columns', style={'marginLeft':'-0px','backgroundColor': app.color_3}
    ),

    html.Div([
        html.Div([

            tue_header.curr_date(),

        ], className='nine columns'),

        html.Div([
html.Div([
            # ##########################################

            html.Div([
                # # ---------- TYPE IN NOMINAL POWER ----------- #
                fig_day.fig_bid(),
            ], className = 'row', style={'marginLeft':'30px'}),

            html.Div([
                # # ---------- TYPE IN NOMINAL POWER ----------- #
                fig_day.fig_ahead(),
            ], className='row', style = {'marginTop':'50px', 'marginLeft':'30px'}),

        ], className='four columns'),

        html.Div([
            # ##########################################

            html.Div([
                # # ---------- TYPE IN NOMINAL POWER ----------- #
                fig_day.fig_unbal(),
            ], className='row', style={'marginLeft':'80px'}),

            html.Div([
                # # ---------- TYPE IN NOMINAL POWER ----------- #
                fig_day.fig_accum(),
            ], className='row', style={'marginTop': '50px', 'marginLeft':'80px'}),

        ], className='four columns'),
        ], className = 'row'),
    ]),






    ##################### - FIGURES - ############################
    # html.Div([
    #     html.Div([
    #         fig_day.fig_bid(),
    #
    #         fig_day.fig_ahead(),
    #
    #     ], className='six columns'),
    #
    #
    #     html.Div([
    #         fig_day.fig_unbal(),
    #
    #             #
    #         fig_day.fig_accum(),
    #             #
    #         ],className='six columns'),
    #
    # ], className='row')

    # # --------------------------------------------------------------------

    # ---------------------------------------------------------------------------
], className='twelve columns', id='Page_2', style={'backgroundColor':app.color_1}
),


##############################################################################


################################################

# ----------  UPDATES THE FIGURE ""Day Ahead Bid Information"" ----------- #
@app.callback([Output('graph_data', 'figure'),
               Output('datatable_graph_data', 'style')],
              [Input('Page_2', 'id')])
def display_graph(nome):
    A = nome
    app.b2p = app.b2
    df = pd.DataFrame(app.ddf)
    P_value = app.Pvalue
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

        realp = fact[fact.columns[app.b2 + 1]] * float(P_value)
        df['Pnom'] = float(P_value) * np.ones(24)
        figure = {
            'data': [{'x': df[df.columns[0]], 'y': df[df.columns[1]], 'type': 'bar', 'name': 'Bid',
                      'marker': {'color': app.color_9}},
                     {'x': df[df.columns[0]], 'y': realp, 'type': 'bar', 'name': 'RealP',
                      'marker': {'color': app.color_10}},
                     {'x': df[df.columns[0]], 'y': pr[pr.columns[app.b2 + 1]], 'type': 'line', 'name': 'Price',
                      'marker': {'color': app.color_5}, 'yaxis': 'y2'},
                     ],
            'layout': go.Layout(title='Day Ahead Bid Information',
                                xaxis=dict(title='Time',automargin= True, gridcolor=app.color_3),
                                yaxis=dict(title='Energy [MWh]', titlefont=dict(color=app.color_9),automargin= True, gridcolor=app.color_3),
                                yaxis2=dict(title='Tariff [€/MWh]', titlefont=dict(color=app.color_5),
                                            tickfont=dict(color=app.color_5), overlaying='y', side='right',automargin= True),
                                margin=dict(l=50, r=50, b=60, t=40),
                                hovermode="closest",
                                paper_bgcolor=app.color_3,
                                plot_bgcolor=app.color_1,
                                width=650, height=400,
                                )
        }
        return figure, {'display': 'block'}


# #################################################

# ----------  UPDATES THE FIGURE "Revenue per Period" ----------- #
@app.callback([Output('graph_day_ahead', 'figure'),
               Output('datatable_graph_day_ahead', 'style')],
              [Input('Page_2', 'id')])
def display_graph_day_ahead(nome):
    A = nome
    df = pd.DataFrame(app.ddf)
    P_value = app.Pvalue
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
        ubpr_pos = pd.DataFrame(app.UB_prices_pos)
        ubpr_neg = pd.DataFrame(app.UB_prices_pos)

        realp = fact[fact.columns[app.b2 + 1]] * float(P_value)
        unb = realp - df[df.columns[1]]
        act_prices = np.zeros((len(realp), 1))
        for i in range(len(realp)):
            if unb[i] >= 0.0:
                act_prices[i] = -unb[i] * ubpr_pos.iloc[i, app.b2 + 1]
            else:
                act_prices[i] = unb[i] * ubpr_neg.iloc[i, app.b2 + 1]
        act_prices = pd.DataFrame(act_prices)
        df['Pnom'] = float(P_value) * np.ones(24)
        figure = dict(
            data=[dict(x=df[df.columns[0]], y=df[df.columns[1]] * pr[pr.columns[app.b2 + 1]], type='bar', name='Expeted',
                       marker=dict(color=app.color_9)),
                  dict(x=df[df.columns[0]], y=act_prices[act_prices.columns[0]], type='bar', name='Inbalance discount',
                       marker=dict(color=app.color_5)),
                  dict(x=df[df.columns[0]],
                       y=(df[df.columns[1]] * pr[pr.columns[app.b2 + 1]]) + act_prices[act_prices.columns[0]], type='bar',
                       name='Actual', marker=dict(color=app.color_10))
                  ],
            layout=go.Layout(dict(title='Revenue per Period', xaxis=dict(title='Time',automargin= True, gridcolor=app.color_3),
                                  yaxis=dict(title='Euros [€]',automargin= True, gridcolor=app.color_3)),
                             margin=dict(l=50, r=50, b=60, t=40),
                             hovermode="closest",
                             paper_bgcolor=app.color_3,
                             plot_bgcolor=app.color_1,
                             width=650, height=400,
                             ),
        )
        return figure, {'display': 'block'}


#
#
# #################################################


# ----------  UPDATES THE FIGURE "Day Accumulated Revenue" ----------- #
@app.callback([Output('graph_accum_revenue', 'figure'),
               Output('datatable_graph_accum_revenue', 'style')],
              [Input('Page_2', 'id')])
def display_graph_accum_revenue(nome):
    A = nome
    df = pd.DataFrame(app.ddf)
    P_value = app.Pvalue
    clicks = 1
    accum = [0]

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
        realp = fact[fact.columns[app.b2 + 1]] * float(P_value)
        unb = realp - df[df.columns[1]]
        act_prices = np.zeros((len(realp), 1))
        for i in range(len(realp)):
            if unb[i] >= 0.0:
                act_prices[i] = -unb[i] * ubpr_pos.iloc[i, app.b2+1]
            else:
                act_prices[i] = unb[i] * ubpr_neg.iloc[i, app.b2+1]

        act_prices = pd.DataFrame(act_prices)
        A = accum
        accum = np.cumsum((df[df.columns[1]] * pr[pr.columns[app.b2 + 1]]) + act_prices[act_prices.columns[0]])
        exp_accum = np.cumsum(df[df.columns[1]] * pr[pr.columns[app.b2 + 1]])

        if abs(accum.iloc[-1] - A[-1]) > 0:
            app.accum = app.accum + accum.iloc[-1]
            app.exp_accum = app.exp_accum + exp_accum.iloc[-1]
        else:
            app.accum = app.accum
            app.exp_accum = app.exp_accum



        df['Pnom'] = float(P_value) * np.ones(24)
        figure = dict(
            data=[dict(x=df[df.columns[0]], y=np.cumsum(df[df.columns[1]] * pr[pr.columns[app.b2 + 1]]), type='line',
                       name='Expeted', marker=dict(color=app.color_9)),
                  dict(x=df[df.columns[0]],
                       y=accum,
                       type='line', name='Actual', marker=dict(color=app.color_10)),
                  ],
            layout=dict(title='Day Accumulated Revenue', xaxis=dict(title='Time', gridcolor=app.color_3),
                        yaxis=dict(title='Euros [€]', gridcolor=app.color_3),
                        margin=dict(l=50, r=50, b=90, t=40),
                        paper_bgcolor=app.color_3,
                        plot_bgcolor=app.color_1,
                        width=650, height=400,
                        ),
        )

        return figure, {'display': 'block'}

#################################################

# # ----------  UPDATE SCOREBOARD ----------- #
# @app.callback(Output('score_board1', 'value'),
#               [State('score_board1', 'value')])
# def score_1(nome):
#     A = nome
#     df = app.ddf
#
#     col = {'width': '30%', 'height': '1%', 'textAlign': 'center','verticalAlign': "middle",
#            'margin-left': '5%', 'resize':'none', 'backgroundColor':app.color_3, 'color':app.color_10,
#                         'borderColor': app.color_3}
#
#     return '€ ' + f'{app.accum:.2f}'

##################################################
#
# #################################################
#
# ----------  UPDATES THE FIGURE "Power inbalance & Inbalance tariffs" ----------- #
@app.callback([Output('graph_unbal', 'figure'),
               Output('datatable_graph_unbal', 'style')],
              [Input('Page_2', 'id')])
def display_graph_unbal(nome):
    A = nome
    df = pd.DataFrame(app.ddf)
    P_value = app.Pvalue
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
        ubpr_pos = pd.DataFrame(app.UB_prices_pos)
        ubpr_neg = pd.DataFrame(app.UB_prices_neg)
        realp = fact[fact.columns[app.b2 + 1]] * float(P_value)
        unb = realp - df[df.columns[1]]

        figure = {
            'data': [{'x': df[df.columns[0]], 'y': unb, 'type': 'bar', 'name': 'Inbalance',
                      'marker': {'color': app.color_9}},
                     {'x': df[df.columns[0]], 'y': ubpr_pos.iloc[:, app.b2 + 1], 'type': 'line',
                      'name': 'Positive inbalance tariff',
                      'marker': {'color': app.color_5}, 'yaxis': 'y2'},
                     {'x': df[df.columns[0]], 'y': ubpr_neg.iloc[:, app.b2 + 1], 'type': 'line',
                      'name': 'Negative inbalance tariff',
                      'marker': {'color': app.color_10}, 'yaxis': 'y2'}
                     ],
            'layout': go.Layout(title='Power inbalance & Inbalance tariffs',
                                xaxis=dict(title='Time', gridcolor=app.color_3),
                                yaxis=dict(title='Inbalance [MWh]', titlefont=dict(color=app.color_9), gridcolor=app.color_3),
                                yaxis2=dict(title='Tariff [€/MWh]', titlefont=dict(color='#8b8b8b'),
                                            tickfont=dict(color='#8b8b8b'), overlaying='y', side='right'),
                                margin=dict(l=50, r=50, b=90, t=40),
                                paper_bgcolor=app.color_3,
                                plot_bgcolor=app.color_1,
                                width=650, height=400,
                                )
        }

        return figure, {'display': 'block'}


# # Callback for adding tabs
# @app.callback(
#     Output("tabs", "children"),
#     [Input('nextD_b', 'n_clicks')],
# )
# def update_total_tab_number(n_clicks):
#     if n_clicks is not None:
#         B = str(n_clicks + 1),
#         A = list(
#             dcc.Tab(
#                 label="Run #{}".format(n_clicks),
#                 value="{}".format(n_clicks),
#                 selected_style={
#                     "color": app.color_4,
#                     "backgroundColor": app.color_3,
#                     "border": "none",
#                 },
#                 style={
#                     "color": app.color_4,
#                     "backgroundColor": app.color_3,
#                     "border": "none",
#                 },
#             )
#         )
#     else:
#         A = list(
#             dcc.Tab(
#                 label="Run #0",
#                 value="{}",
#                 selected_style={
#                     "color": app.color_4,
#                     "backgroundColor": app.color_3,
#                     "border": "none",
#                 },
#                 style={
#                     "color": app.color_4,
#                     "backgroundColor": app.color_3,
#                     "border": "none",
#                 },
#             )
#         ),
#     return A

################################################

# #################################################


# ----------  SENDS TO PAGE 1 ----------- #
@app.callback(Output('link_b2', 'disabled'),
              [Input('nextD_b', 'n_clicks')])
def button_2(clicks):
    if clicks is not None:
        app.b2 = app.b2 + 1

        return False
