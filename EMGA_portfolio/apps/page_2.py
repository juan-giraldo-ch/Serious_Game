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
import power_renew_generators as pwg
import datetime

from pyomo.environ import *
import matplotlib.pyplot as plt
import pyutilib


# import os  # Importing OS functions

from app import app

from apps import tue_header, fig_day, buttons, score_info, login, feas_check

pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False #this is required to avoid the threading problem (Pyomo + solver signals)


################################################################################

#################### - SECOND PAGE - ############################

if app.database_url == 'Local':
    url_data = os.popen("heroku config:get DATABASE_URL -a emga").read().strip()  # When local machine

if app.database_url == 'Server':
    url_data = os.environ.get('DATABASE_URL')  # When Server

play_days = app.play_days

port_param_num = pd.read_csv(
    'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/Portafolio_parameters.csv',
    # r'C:\Users\20194851\Google Drive\Postdoc TUe\Project Serious Game\Dash_tests\EMGA_portfolio\apps\Portafolio_parameters.csv',
    header=0, squeeze=True)



# ############################################################################
# feas, tot_inf = feas_check.feasibility_check()
#
# ############################################################################

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
               Output('datatable_graph_data', 'style'),
               Output('graph_day_ahead', 'figure'),
               Output('datatable_graph_day_ahead', 'style'),
               Output('graph_accum_revenue', 'figure'),
               Output('datatable_graph_accum_revenue', 'style'),
               Output('graph_unbal', 'figure'),
               Output('datatable_graph_unbal', 'style')

               ],
              [Input('Page_2', 'id')],
              # [State('irrad_hist', 'data')]
              )
def display_graph(nome):
    A = nome
    b2 = int(flask.request.cookies.get('b2'))
    dash.callback_context.response.set_cookie('b2p', str(b2), max_age=7200)

    b2p = int(flask.request.cookies.get('b2p'))

    user_active = flask.request.cookies.get('custom-auth-session')



    # feas, tot_inf = feas_check.feasibility_check(user_active)

    # print(irrad_stored)

    PV_irradiation = app.PV_irradiation

    PV_irradiation['DateTime'] = pd.to_datetime(PV_irradiation['DateTime'], format="%d/%m/%Y %H:%M")

    time_mask = PV_irradiation['DateTime'] <= PV_irradiation['DateTime'].iloc[-1] - datetime.timedelta(
        days=play_days - b2)

    dates_irrad = PV_irradiation['DateTime'][time_mask]

    #
    #
    delta2 = (datetime.datetime.now() - datetime.datetime.strptime(str(dates_irrad.iloc[-1]),
                                                                   "%Y-%m-%d %H:%M:%S")).days

    PV_irradiation['DateTime'] = PV_irradiation['DateTime'] + datetime.timedelta(delta2)

    # PV_irradiation_hist = PV_irradiation[time_mask]
    PV_irradiation_play = PV_irradiation[~time_mask]

    PV_irradiation_play = PV_irradiation_play[96 * 0:96 * (0 + 1)]

    #
    A_i = PV_irradiation_play.resample('H', on='DateTime').mean()
    # print(A_i)
    # p_pv = pd.DataFrame(data=p_pv, index=A.index)
    days_play1_i = 1  # only for one day


    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM portfolio WHERE Player = (%s);", (user_active,))
    accum = cur.fetchall()
    thermic_p_nom = accum[0][2]
    wind_p_nom = accum[0][3]
    pv_p_nom = accum[0][4]
    storage_p_nom = accum[0][5]

    conn.close()
    cur.close()

    portf = accum

    p_pv = pwg.power_solar(A_i, pv_p_nom)

    p_pv = pd.DataFrame(data=p_pv, index=range(24))

    a1 = np.zeros((24, days_play1_i))

    flex_th = port_param_num.iloc[0][9]
    flex_storage = port_param_num.iloc[3][9]

    # for h in range(24):
    #     for d in range(days_play1_i):
    #         a1[h, d] = a_i.iloc[d * h, 0]
    # # print(pd.DataFrame(a_i).iloc[:, 0])

    ##########################################
    ###########################################

    P_value = (json.loads((flask.request.cookies.get('P_value'))))

    # df = pd.DataFrame(app.ddf)

    aa = (flask.request.cookies.get('ddf'))

    # s1 = json.dumps(df)
    df = json.loads(aa)

    df = pd.DataFrame.from_dict(df, orient='columns')
    # P_value = app.Pvalue
    clicks = 1
    accum = [0]
    accumA = float(flask.request.cookies.get('accum_val'))

    if (df.empty or len(df.columns) < 1 or clicks is None or P_value == 0):
        figure = {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
        return figure, {'display': 'none'}, figure2, {'display': 'none'}, figure3, {'display': 'none'}, figure4, {
            'display': 'none'}


    else:
        pr = pd.DataFrame(app.prices)
        fact = pd.DataFrame(app.real_P) * wind_p_nom

        realp_pv = (((p_pv[p_pv.columns[0]])))  # * float(P_value)
        # df['Pnom'] = float(P_value) * np.ones(24)

        ##################
        feas, tot_inf, phi_plus, phi_minus, zeta_plus, zeta_minus, rho_plus, rho_minus = feas_check.feasibility_check(user_active, portf, df)


        ##################


        total_bid = (df.iloc[:, 1:5].sum(axis=1) - (phi_plus.iloc[:, 0] + zeta_plus.iloc[:,0] + rho_plus.iloc[:,0])[0] +
                     (phi_minus.iloc[:, 0] + zeta_minus.iloc[:,0] + rho_minus.iloc[:,0])[0])
        therm_bid = (df.iloc[:, 1])
        storage_bid = (df.iloc[:, 4])




        # print((-(phi_plus.iloc[:, 0] + zeta_plus.iloc[:,0] + rho_plus.iloc[:,0]) + (phi_minus.iloc[:, 0] + zeta_minus.iloc[:,0] + rho_minus.iloc[:,0]))[0])
        # print((df.iloc[:, 1:5].sum(axis=1)))

        realp = (fact[fact.columns[b2 + 1]]) + realp_pv.array + therm_bid.array + storage_bid.array # * float(P_value)

        flexibility = therm_bid * flex_th / 100 + storage_bid * flex_storage / 100

        figure = go.Figure()
        figure.add_trace(go.Bar(
            name='Bid',
            x=df[df.columns[0]], y=total_bid,
            marker={'color': app.color_3}
        ))
        figure.add_trace(go.Bar(
            name='Actual',
            x=df[df.columns[0]], y=realp,
            error_y=dict(type='data', array=flexibility,
                         color=app.color_10),
            marker={'color': app.color_bar2}
            # error_y=dict(type='data', array=[0.5, 1, 2])
        ))
        figure.add_trace(go.Scatter(
            name='Price',
            x=df[df.columns[0]], y=pr[pr.columns[b2 + 1]],
            marker={'color': app.color_line}, yaxis='y2'
            # error_y=dict(type='data', array=[0.5, 1, 2])
        ))
        figure.update_layout(barmode='group')


        figure.update_layout(title='Day Ahead Information', titlefont=dict(color=app.color_3),
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
        # }

        #########################################################################
        pr = pd.DataFrame(app.prices)
        fact = pd.DataFrame(app.real_P) * wind_p_nom
        ubpr_pos = pd.DataFrame(app.UB_prices_pos)
        ubpr_neg = pd.DataFrame(app.UB_prices_neg)

        # realp = (fact[fact.columns[b2 + 1]]).array + realp_pv.array

        unb_no_flex = realp.array - total_bid
        unb = unb_no_flex
        # if -flexibility <= unb <= flexibility:
        #     unb = 0.0

        # print(unb)
        act_prices = np.zeros((len(realp), 1))
        act_prices_feas = np.zeros((len(realp), 1))

        imb_1 = unb.array - tot_inf.iloc[:, 0]

        flexib = np.zeros((len(realp),1))

        #########################
        for t in range(24):
            a = feas_check.redispatch(portf, imb_1, ubpr_pos[ubpr_pos.columns[b2 + 1]] * pr[pr.columns[b2 + 1]], ubpr_neg[ubpr_neg.columns[b2 + 1]] * pr[pr.columns[b2 + 1]], t, df)

            flexib[t] = a.flex[0, t].value

            # print(a.flex[0,t].value)
            #
            # print(a.cost[0,t].value)
            # if (a.Imbalance[t]) >= 0:
            #     print('pos')
            #     print(sum(a.cost[i,t].value for i in a.S) + a.price_plus[t].value*(a.Imbalance[t] - a.flex[0,t].value) )
            #     print(a.price_plus[t].value * (a.Imbalance[t]))
            # if (a.Imbalance[t]) < 0:
            #     print('neg')
            #     print(sum(a.cost[i,t].value for i in a.S) + a.price_neg[t].value*(-a.Imbalance[t] - a.flex[0,t].value) )
            #     print(a.price_neg[t].value * (-a.Imbalance[t]))





        #########################



        for i in range(len(realp)):


            if -flexibility.iloc[i] <= unb_no_flex[i] <= flexibility.iloc[i]:
                unb[i] = 0.0
            elif unb_no_flex[i] < -flexibility.iloc[i]:
                unb[i] = (realp.iloc[i] + a.flex[0,i].value) - total_bid.iloc[i]
            elif unb_no_flex[i] > flexibility.iloc[i]:
                unb[i] = realp.iloc[i] - a.flex[0,i].value - total_bid.iloc[i]


            if unb[i] >= 0.0:
                act_prices[i] = (unb[i]) * pr.iloc[i, b2 + 1] * (ubpr_pos.iloc[i, b2 + 1])
                act_prices_feas[i] = (unb.array[i] - tot_inf.iloc[i,0]) * pr.iloc[i, b2 + 1] * (ubpr_pos.iloc[i, b2 + 1])

            else:
                act_prices[i] = unb[i] * pr.iloc[i, b2 + 1] * (ubpr_neg.iloc[i, b2 + 1])
                act_prices_feas[i] = (unb.array[i] - tot_inf.iloc[i,0]) * pr.iloc[i, b2 + 1] * (ubpr_neg.iloc[i, b2 + 1])

            act_prices = pd.DataFrame(act_prices)
            act_prices_feas = pd.DataFrame(act_prices_feas)



            # if unb_no_flex[i] >= 0.0:
            #     act_prices_no_flex[i] = unb_no_flex[i] * pr.iloc[i, b2 + 1] * (ubpr_pos.iloc[i, b2 + 1])
            # else:
            #     act_prices_no_flex[i] = unb_no_flex[i] * pr.iloc[i, b2 + 1] * (ubpr_neg.iloc[i, b2 + 1])
            # act_prices = pd.DataFrame(act_prices)
        # df['Pnom'] = float(P_value) * np.ones(24)

        figure2 = dict(
            data=[dict(x=df[df.columns[0]], y=total_bid * pr[pr.columns[b2 + 1]].array, type='bar',
                       name='Expected',
                       marker=dict(color=app.color_3)),
                  dict(x=df[df.columns[0]], y=(act_prices.iloc[0,:]), type='bar', name='Inb. Income',
                       marker=dict(color=app.color_bar2),
                       textfont_color=app.color_3,
                       ),
                  dict(x=df[df.columns[0]], y=(act_prices_feas.iloc[0,:].values + (
                          total_bid * pr[pr.columns[b2 + 1]].array)), type='line', name='Feasible Rev.',
                       marker=dict(color=app.color_10),
                       textfont_color=app.color_3,
                       ),
                  dict(x=df[df.columns[0]], y=(act_prices.iloc[0,:].values + (
                          total_bid * pr[pr.columns[b2 + 1]].array)),
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
        #########################################################################
        pr = pd.DataFrame(app.prices)

        fact = pd.DataFrame(app.real_P)
        ubpr_pos = pd.DataFrame(app.UB_prices_pos)
        ubpr_neg = pd.DataFrame(app.UB_prices_neg)
        # realp = (fact[fact.columns[b2 + 1]]).array + realp_pv.array
        # unb = realp - total_bid
        # act_prices = np.zeros((len(realp), 1))
        # for i in range(len(realp)):
        #     if unb[i] >= 0.0:
        #         act_prices[i] = unb[i] * pr.iloc[i, b2 + 1] * (ubpr_pos.iloc[i, b2 + 1])
        #     else:
        #         act_prices[i] = unb[i] * pr.iloc[i, b2 + 1] * (ubpr_neg.iloc[i, b2 + 1])
        #
        # act_prices = pd.DataFrame(act_prices)
        # print(act_prices)
        AA = act_prices.iloc[0,:].values + (
                total_bid * pr[pr.columns[
            b2 + 1]].array)  # (total_bid * (pr[pr.columns[b2 + 1]]).array + (act_prices[act_prices.columns[0]]).array)

        A = accum
        accum = np.cumsum(AA)
        exp_accum = np.cumsum(realp * pr[pr.columns[b2 + 1]])
        dash.callback_context.response.set_cookie('accum_1', str(accum.iloc[-1]), max_age=7200)

        BB = act_prices_feas.iloc[0,:].values + (
                          total_bid * pr[pr.columns[b2 + 1]].array)
        accum_feas = np.cumsum(BB)

        if abs(accum.iloc[-1] - A[-1]) > 0:
            accumA = accumA + accum.iloc[-1]
            cookie_exp = float(flask.request.cookies.get('exp_accum'))

            cookie_exp = cookie_exp + exp_accum.iloc[-1]

            dash.callback_context.response.set_cookie('exp_accum', str(cookie_exp), max_age=7200)

        else:
            accumA = accumA
            # cookie_exp = cookie_exp

        # co = set_cookie('acc_cookie', app.accum) # colocar en return

        # df['Pnom'] = float(P_value) * np.ones(24)
        figure3 = dict(
            data=[dict(x=df[df.columns[0]], y=np.cumsum(realp * pr[pr.columns[b2 + 1]].array), type='line',
                       name='Perfect forecast', marker=dict(color=app.color_3)),
                  dict(x=df[df.columns[0]],
                       y=accum,
                       type='line', name='Actual Infeasible', marker=dict(color=app.color_line)),
                  dict(x=df[df.columns[0]],
                       y=accum_feas,
                       type='line', name='Actual Feasible', marker=dict(color=app.color_10)),

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

        ########################################################################
        pr = pd.DataFrame(app.prices)
        fact = pd.DataFrame(app.real_P)
        ubpr_pos = pd.DataFrame(app.UB_prices_pos)
        ubpr_neg = pd.DataFrame(app.UB_prices_neg)
        # realp = (fact[fact.columns[b2 + 1]]).array + realp_pv.array
        # realp = realp.rename('Power_[MWh]')
        # unb = realp.array - total_bid

        # imb_1 = unb.array - tot_inf.iloc[:, 0]

        flexib = pd.DataFrame(flexib)

        figure4 = {
            'data': [{'x': df[df.columns[0]], 'y': unb, 'type': 'bar', 'name': 'Imbalance',
                      'marker': {'color': app.color_3}}, #
                     {'x': df[df.columns[0]], 'y': unb.array - abs(tot_inf.iloc[:,0]), 'type': 'bar', 'name': 'Imbalance Feasible',
                      'marker': {'color': app.color_10}},
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

        ########################################################################

        return figure, {'display': 'inline-block', 'width': '95%', 'height': '95%'}, \
               figure2, {'display': 'inline-block', 'width': '95%', 'height': '95%'}, \
               figure3, {'display': 'inline-block', 'width': '95%', 'height': '95%'}, \
               figure4, {'display': 'inline-block', 'width': '95%', 'height': '95%'}




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
