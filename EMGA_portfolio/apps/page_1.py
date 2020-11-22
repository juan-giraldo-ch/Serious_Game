# coding=utf-8
# -*- coding: utf-8 -*-
import base64
import io
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os  # Importing OS functions
import datetime
import pickle
import copy
import pathlib
import json
from bson import json_util
import dash_table as dt
import time
from users import users_info
import dash_bootstrap_components as dbc
import flask
from six.moves.urllib.parse import quote
from app import app
from apps import tue_header, user_data, buttons, messages, score_info, leader_board
import psycopg2

# from sqlalchemy import create_engine

#

if app.database_url == 'Local':
    url_data = os.popen("heroku config:get DATABASE_URL -a emga").read().strip()  # When local machine

if app.database_url == 'Server':
    url_data = os.environ.get('DATABASE_URL')  # When Server

DATABASE_URL = (url_data)

user_pwd, user_names = users_info()

# log = login.route_login()
#
# print(log)

play_days = app.play_days

button1 = html.Div([
    html.Div([
        html.Img(src='https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/wind_tu1.svg',
                 alt="Avatar", className="image",
                 title='Download Historical Wind Data',
                 # style={'height': '70%','width': '70%'}
                 ),
        html.Div([
            html.Img(
                src='https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/wind_tu_2.svg',
                alt="Avatar", className="image",
                title='Download Historical Wind Data',
                # style={'height': '70%', 'width': '70%'}
            ),
        ], className="overlay"),
    ], className="container", ),

])

button2 = html.Div([
    html.Div([
        html.Img(src='https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/stocks1.svg',
                 alt="Avatar", className="image",
                 title='Download Day Ahead Data',
                 # style={'height': '10vw','width': '10vw'}
                 ),
        html.Div([
            html.Img(
                src='https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/stocks_2.svg',
                alt="Avatar", className="image",
                title='Download Day Ahead Data',
                # style={'height': '10vw','width': '10vw'}
            ),
        ], className="overlay"),
    ], className="container", ),

])

button3 = html.Div([
    html.Div([
        html.Img(src='https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/solar_tu.svg',
                 alt="Avatar", className="image",
                 title='Download Historical Irradiation',
                 # style={'height': '10vw','width': '10vw'}
                 ),
        html.Div([
            html.Img(
                src='https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/solar_tu2.svg',
                alt="Avatar", className="image",
                title='Download Historical Irradiation',
                # style={'height': '10vw','width': '10vw'}
            ),
        ], className="overlay"),
    ], className="container", ),

])


button4 = html.Div([
    html.Div([
        html.Img(src='https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/portfolio_1.svg',
                 alt="Avatar", className="image",
                 title='Portfolio',
                 style={'height': '7vw','width': '7vw'}
                 ),
        html.Div([
            html.Img(
                src='https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/portfolio.svg',
                alt="Avatar", className="image",
                title='Portfolio',
                style={'height': '7vw','width': '7vw'}
            ),
        ], className="overlay"),
    ], className="container", ),

])

# ##################### - FIRST PAGE - ############################
layout = html.Div([

    # ----------------------------------------------------------------------

    html.Div([

        # ---------- SCORE BOARD ----------- #
        dbc.Container([

            # First row

            dbc.Row(
                [
                    dbc.Col([

                    ], width=2, lg=2, md=2, sm=2, style={'backgroundColor': app.color_3, 'textAlign': 'center'}),

                    dbc.Col([
                    ], width=10, lg=10, md=10, sm=10),
                ], style={'height': '1vw'},
            ),

            dbc.Row(
                [
                    dbc.Col([
                        score_info.position_lead(),

                    ], width=2, lg=2, md=2, sm=2, style={'backgroundColor': app.color_3, 'textAlign': 'center'}),

                    dbc.Col([
                        tue_header.curr_date(),
                    ], width=10, lg=10, md=10, sm=10),
                ], style={'height': '5vw'},
            ),

            # Second row

            dbc.Row(
                [
                    dbc.Col([
                        score_info.self_score(),

                    ], width=2, lg=2, md=2, sm=2, style={'backgroundColor': app.color_3}),

                    dbc.Col([

                        html.Div([
                            buttons.download_irrad(),
                        ], style={'textAlign': 'center'}),
                    ], width=3, lg=3, md=3, sm=3),

                    dbc.Col([

                        html.Div([
                            buttons.download_data(),
                        ], style={'textAlign': 'center'}),
                    ], width=3, lg=3, md=3, sm=3),

                    # dbc.Col([
                    #
                    #     html.Div([
                    #         # buttons.download_data(),
                    #     ], style={'textAlign': 'center'}),
                    # ], width=1, lg=1, md=1, sm=1),

                    dbc.Col([
                        html.Div([
                            buttons.download_DAP()
                        ], style={'textAlign': 'center'}),
                    ], width=3, lg=3, md=3, sm=3),

                    # dbc.Col([
                    #
                    #     html.Div([
                    #         buttons.download_irrad(),
                    #     ], style={'textAlign': 'center'}),
                    # ], width=2, lg=2, md=2, sm=2),

                ], style={'height': '10vw'}, justify="between"
            ),

            dbc.Row(
                [
                    dbc.Col([
                        html.Div([
                            leader_board.L_table()
                        ], style={'marginTop': '7vw'}, )

                    ], width=2, lg=2, md=2, sm=2, style={'backgroundColor': app.color_3, 'textAlign': 'center'}),

                    dbc.Col([


                        # html.Div([
                        #     buttons.port_info(),
                        # ]),

                    ], width=3, lg=3, md=3, sm=3),

                    dbc.Col([
                        html.Div([
                            user_data.nominal_P(),
                        ], style={'display': 'none', 'marginTop': '7vw'}),



                        html.Div([
                            user_data.drag_file(),
                        ], style={'marginTop': '7vw'}
                            # style={'marginTop': '7vw', 'marginLeft': '28vw'}
                        ),  #

                    ], width=4, lg=4, md=4, sm=4, style={'textAlign': 'center'}),

                    dbc.Col([
                        html.Div([
                            # dcc.Loading([
                                html.Div([
                                    buttons.port_info(),
                                ], style={'height': '1vw'},),
                            # ],id='loading_port', color=app.color_3, type='default'),

                        ], style={'marginTop': '7vw'})
                    ], width=3, lg=3, md=3, sm=3, style={'textAlign': 'center'}),

                ], style={'height': '20vw'},
            ),

            dbc.Row([

                dbc.Col([
                    # dbc.Alert([
                    html.Div([
                        buttons.submit_b(),
                    ], style={'textAlign': 'center', 'height': '100%'}),
                    # ], color="info"),

                ], width=2, lg=2, md=2, sm=2, style={'backgroundColor': app.color_3, 'textAlign': 'center'}),

                dbc.Col([
                    html.Div([
                        user_data.table_data(),
                    ], style={'backgroundColor': app.color_1, 'height': '100%'}),
                ], width=3, lg=3, md=3, sm=3),

                dbc.Col([
                    html.Div([
                        score_info.fig_rev(),
                    ], style={'backgroundColor': app.color_1, 'textAlign': 'right', 'height': '100%'}),
                ], width=7, lg=7, md=7, sm=7),

            ], style={'height': '100%'}, ),

        ], fluid=True),

    ], style={'height': '100%', 'backgroundColor': app.color_1}),

    ##################### - ERROR MESSAGES - ############################

    # # ---------- FILE HAS WRONG SIZE ----------- #
    messages.mesag_size(),

    # ##############################################

    # ---------- BID > THAN NOMINAL P ----------- #
    messages.mesag_nom(),

    ##############################################

    ################### - STORE HIST DATA - ###########################

    # dcc.Store(id='wind_hist', storage_type='session'),
    # dcc.Store(id='irrad_hist', storage_type='memory'),

    # --------------------------------------------------------------------

], id='Page_1', style={'height': '100%', 'backgroundColor': app.color_1}

)


################################################################
################################################################

##################### - FUNCTION -- LOAD FILE - ############################

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if '.csv' in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))


        if (len(df.axes[1]) == 5) and (len(df.axes[0]) == 24):
            return df
        else:
            return None

    elif '.xls' in filename:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded))

        if (len(df.axes[1]) == 5) and (len(df.axes[0]) == 24):
            return df
        else:
            return None


#################################################################
#################################################################

# ---------- UPDATE CURRENT_DAY ----------- #
@app.callback(Output('Counter_day', 'children'),
              # Output('link_downl', 'href')],
              [Input('Counter_day', 'contents'),
                Input('Page_1', 'id')
               ])
def display_confirm(day,page):
    user_active = flask.request.cookies.get('custom-auth-session')

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    cur = conn.cursor()

    cur.execute("SELECT days FROM Leader_board WHERE Player = (%s);", (user_active,))

    # print(players)
    days = cur.fetchone()



    cur.close()
    conn.close()

    # if len(days):

    day = days[0]

    # if day == len(app.WF_real_power) / 96:

    dash.callback_context.response.set_cookie('b2', str(day), max_age=7200)
    accum_1 = float(flask.request.cookies.get('accum_1'))

    b2 = day

    #############################
    accum = float(flask.request.cookies.get('accum_val'))
    b2p = float(flask.request.cookies.get('b2p'))
    accufig1 = (json.loads((flask.request.cookies.get('accufig'))))
    rate_accum1 = (json.loads((flask.request.cookies.get('rate_accum'))))

    if (b2p) >= 1:
        A1 = ((datetime.datetime.now() + datetime.timedelta(days=b2 - 1)).strftime("%d/%m/%Y"))

        data1 = json.loads((flask.request.cookies.get('data_c')))
        data1.append(A1)
        data1 = list(dict.fromkeys(data1))
        x = json.dumps(data1)
        dash.callback_context.response.set_cookie('data_c', (x), max_age=7200)

        accufig1.append(accum)
        accufig1 = list(dict.fromkeys(accufig1))
        x = json.dumps(accufig1)
        dash.callback_context.response.set_cookie('accufig', (x), max_age=7200)

        bar_acum = (json.loads((flask.request.cookies.get('bar_acum'))))
        bar_acum.append(accum_1)
        bar_acum = list(dict.fromkeys(bar_acum))

        x = json.dumps(bar_acum)
        dash.callback_context.response.set_cookie('bar_acum', (x), max_age=7200)

        rate_accum1.append(accufig1[-1] / b2)
        rate_accum1 = list(dict.fromkeys(rate_accum1))

        x = json.dumps(rate_accum1)
        dash.callback_context.response.set_cookie('rate_accum', (x), max_age=7200)

    else:
        data1 = (json.loads((flask.request.cookies.get('data_c'))))
        if data1 == 0:
            data1 = [((datetime.datetime.now() + datetime.timedelta(days=b2 - 1)).strftime("%d/%m/%Y"))]
        if accufig1 == 0:
            accufig1 = [accum]

        bar_acum = (json.loads((flask.request.cookies.get('bar_acum'))))
        if bar_acum == 0:
            bar_acum = [accum_1]

        rate_accum1 = (json.loads((flask.request.cookies.get('rate_accum'))))
        if rate_accum1 == 0 and b2 > 0:
            rate_accum1 = [accum / b2]

        x = json.dumps(data1)
        dash.callback_context.response.set_cookie('data_c', (x), max_age=7200)

        # accufig1 = (json.loads((flask.request.cookies.get('accufig'))))
        x = json.dumps(accufig1)
        dash.callback_context.response.set_cookie('accufig', (x), max_age=7200)

        x = json.dumps(bar_acum)
        dash.callback_context.response.set_cookie('bar_acum', (x), max_age=7200)

        x = json.dumps(rate_accum1)
        dash.callback_context.response.set_cookie('rate_accum', (x), max_age=7200)
    #############################

    # rate_accum1.append(accufig1[-1] / b2)
    # rate_accum1 = list(dict.fromkeys(rate_accum1))

    day = '''*Current trading day: {}*'''.format(
        (datetime.datetime.now() + datetime.timedelta(days=b2)).strftime("%d/%m/%Y"))
    return day


# ---------- TABLE FROM DATA FILE ----------- #
@app.callback([Output('table_data', 'data'),
               Output('table_data', 'columns'),
               Output('datatable-container', 'style')],
              [Input('Drag_file', 'contents')],
              [State('Drag_file', 'filename')])
def display_confirm(contents, filename):
    if contents is None:
        return [{}], [], {'display': 'block'}
    else:
        df = parse_contents(contents, filename)

        if df is not None:

            df_1 = df.to_json()
            dash.callback_context.response.set_cookie('ddf', str(df_1), max_age=7200)

            if (len(df.axes[1]) == 5) and (len(df.axes[0]) == 24):
                return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {'display': 'block'}
            else:
                return [{}], [], {'display': 'block', }
        else:
            return [{}], [], {'display': 'block', }


# ---------- CHANGING STYLE OF DRAG/DROP SELECT BID FILE ----------- #
@app.callback([Output('Drag_file', 'children'),
               Output('Drag_file', 'disabled'),
               Output('Drag_file', 'style')],
              [Input('Drag_file', 'contents'),
               Input('Pnom', 'value'),
               Input('button', 'n_clicks'),
               Input('table_size', 'submit_n_clicks'),
               Input('compare_p', 'submit_n_clicks')],
              [State('Drag_file', 'filename'),
               State('Drag_file', 'children')])
def update_drag_bar(contents, P_value, clicks, ok_button, ok_P, filename, existing_state):
    tab = False
    if (contents == None) and P_value == 0:
        raise PreventUpdate
    if (contents == None) and P_value > 0 and clicks is None:
        col = {
            'width': '25vw', 'height': '3vw', 'lineHeight': '2.5vw',
            'borderWidth': '0.15vw', 'borderStyle': 'outset',
            'borderRadius': '1.5vw', 'textAlign': 'center', 'border-color': app.color_3,
            'backgroundColor': app.color_1, 'font-size': '1.2vw',
        }
        disab = False
        return existing_state, disab, col
    if (P_value == 0 and contents is not None and clicks is None):
        df = parse_contents(contents, filename)
        if (len(df.axes[1]) == 5) and (len(df.axes[0]) == 24):
            col = {
                'width': '25vw', 'height': '3vw', 'lineHeight': '2.5vw',
                'borderWidth': '0.15vw', 'borderStyle': 'dashed',
                'borderRadius': '1.5vw', 'textAlign': 'center', 'border-color': app.color_3,
                'font-size': '1.2vw',
                'color': app.color_3, 'backgroundColor': app.color_green,
            }
            name = filename
        else:
            if not ok_button:
                col = {
                    'width': '25vw', 'height': '3vw', 'lineHeight': '2.5vw',
                    'borderWidth': '0.15vw', 'borderStyle': 'dashed',
                    'borderRadius': '1.5vw', 'textAlign': 'center', 'border-color': app.color_3,
                    'font-size': '1.2vw',
                    'color': app.color_3, 'backgroundColor': app.color_red,
                }
            else:
                col = {
                    'width': '25vw', 'height': '3vw', 'lineHeight': '2.5vw',
                    'borderWidth': '0.15vw', 'borderStyle': 'dashed',
                    'borderRadius': '1.5vw', 'textAlign': 'center',
                    'border-color': app.color_7, 'font-size': '1.2vw',
                    'color': app.color_3, 'backgroundColor': app.color_green,
                }
            name = existing_state
        disab = False
        return name, disab, col
    if P_value > 0 and contents is not None and clicks is None:
        df = parse_contents(contents, filename)

        if df is not None:

            if (len(df.axes[1]) == 5) and (len(df.axes[0]) == 24):
                col = {
                    'width': '25vw', 'height': '3vw', 'lineHeight': '2.5vw',
                    'borderWidth': '0.15vw', 'borderStyle': 'dashed',
                    'borderRadius': '1.5vw', 'textAlign': 'center',
                    'border-color': app.color_3,
                    'backgroundColor': app.color_green, 'font-size': '1.2vw', 'color': app.color_3
                }
                if ok_P:
                    col = {
                        'width': '25vw', 'height': '3vw', 'lineHeight': '2.5vw',
                        'borderWidth': '0.15vw', 'borderStyle': 'dashed',
                        'borderRadius': '1.5vw', 'textAlign': 'center',
                        'border-color': app.color_3, 'font-size': '1.2vw',
                        'backgroundColor': app.color_green,
                        # 'backgroundColor':'green',
                    }
                name = filename
                disab = True

            else:
                col = {
                    'width': '25vw', 'height': '3vw', 'lineHeight': '2.5vw',
                    'borderWidth': '0.15vw', 'borderStyle': 'dashed',
                    'borderRadius': '1.5vw', 'textAlign': 'center',
                    'border-color': app.color_7, 'font-size': '1.2vw',
                    'backgroundColor': app.color_red
                }
                disab = False
                name = existing_state


        else:
            col = {
                'width': '25vw', 'height': '3vw', 'lineHeight': '2.5vw',
                'borderWidth': '0.15vw', 'borderStyle': 'dashed',
                'borderRadius': '1.5vw', 'textAlign': 'center',
                'border-color': app.color_7, 'font-size': '1.2vw',
                'backgroundColor': app.color_red
            }
            name = existing_state
            disab = False

        return name, disab, col

    if (P_value > 0 and contents is not None and clicks is not None):
        df = parse_contents(contents, filename)
        if (len(df.axes[1]) == 5) and (len(df.axes[0]) == 24):
            col = {
                'width': '25vw', 'height': '3vw', 'lineHeight': '2.5vw',
                'borderWidth': '0.15vw', 'borderStyle': 'dashed',
                'borderRadius': '1.5vw', 'textAlign': 'center',
                'border-color': app.color_8, 'font-size': '1.2vw',
                'backgroundColor': app.color_green,
            }
            name = filename
            disab = False

        else:
            col = {
                'width': '25vw', 'height': '3vw', 'lineHeight': '2.5vw',
                'borderWidth': '0.15vw', 'borderStyle': 'dashed',
                'borderRadius': '1.5vw', 'textAlign': 'center',
                'border-color': app.color_7, 'font-size': '1.2vw',
                'backgroundColor': app.color_red,

            }
            name = existing_state
            disab = True
        return name, disab, col


#################################################

# ----------  UPDATES THE APPEARANCE OF BUTTON "SUBMIT" ----------- #
# %%% Updates the text of the Button
@app.callback([Output('Button_data', 'children'),
               Output('Button_data', 'style'),
               Output('Pnom', 'style'),
               Output('Pnom', 'disabled'),
               Output('table_data', 'editable')],
              [Input('Drag_file', 'contents'),
               Input('Pnom', 'value'),
               Input('button', 'n_clicks'),
               Input('table_size', 'submit_n_clicks')],
              [State('Drag_file', 'filename')])
def update_texts(contents, P_value, clicks, ok_button, filename):
    if (contents == None) and P_value == 0:
        raise PreventUpdate
    if (contents == None) and P_value > 0 and clicks is None and not ok_button:
        x = json.dumps(P_value)
        dash.callback_context.response.set_cookie('P_value', (x), max_age=7200)
        # app.Pvalue = P_value
        prompt = 'Bid file missing'
        col = {'color': app.color_7, 'font-size': '1.2vw', 'textAlign': 'center'}
        bord = {'borderColor': app.color_8, 'borderWidth': '2.0px',
                'backgroundColor': app.color_6}  # style={'marginLeft':130}
        disab = True
        tab_disab = True
        return prompt, col, bord, disab, tab_disab
    if (P_value == 0 and contents is not None and clicks is None):
        df = parse_contents(contents, filename)
        if (len(df.axes[1]) == 5) and (len(df.axes[0]) == 24):
            prompt = 'Nominal power missing'
            col = {'font-size': '1.2vw', 'textAlign': 'center'}
            bord = {'borderColor': app.color_7, 'borderWidth': '2.0px',
                    'backgroundColor': app.color_6}
            tab_disab = True
            disab = True
            return prompt, col, bord, disab, tab_disab
        else:
            prompt = 'Error in Data file - Upload correct file'
            col = {'font-size': '1.2vw', 'textAlign': 'center'}
            bord = {'borderColor': app.color_7, 'borderWidth': '2.0px',
                    'backgroundColor': app.color_6}
            tab_disab = True
            disab = True
            return prompt, col, bord, disab, tab_disab

    if (P_value > 0 and contents is not None and clicks is None):
        df = parse_contents(contents, filename)
        x = json.dumps(P_value)
        dash.callback_context.response.set_cookie('P_value', (x), max_age=7200)
        # app.Pvalue = P_value

        if df is not None:

            if (len(df.axes[1]) == 5) and (len(df.axes[0]) == 24):
                prompt = 'Click SUBMIT to Continue'
                col = {'color': app.color_line, 'font-size': '1.2vw', 'textAlign': 'center'}
                bord = {'borderColor': app.color_3, 'borderWidth': '2.0px',
                        'backgroundColor': app.color_6}
                disab = True
                tab_disab = True
                return prompt, col, bord, disab, tab_disab
        else:
            prompt = 'Error in Data file - Upload correct file'
            col = {'color': app.color_red, 'font-size': '1.2vw', 'textAlign': 'center'}
            bord = {'borderColor': app.color_3, 'borderWidth': '2.0px',
                    'backgroundColor': app.color_6}
            disab = True
            tab_disab = True
            return prompt, col, bord, disab, tab_disab

    if (P_value > 0 and contents is not None and clicks is not None):
        x = json.dumps(P_value)
        dash.callback_context.response.set_cookie('P_value', (x), max_age=7200)
        # app.Pvalue = P_value
        prompt = 'Bid Successfully Submitted!'
        col = {'font-size': '1.2vw', 'textAlign': 'center'}
        bord = {'borderColor': app.color_3, 'borderWidth': '2.0px',
                'backgroundColor': app.color_6}
        disab = True
        tab_disab = True
        tab = True
        return prompt, col, bord, disab, tab_disab


#################################################

# ----------  UPDATES THE AVAILABILITY OF BUTTON "SUBMIT" ----------- #
@app.callback(Output('button', 'disabled'),
              [Input('Drag_file', 'contents'),
               Input('Pnom', 'value')],
              [State('Drag_file', 'filename')])
def update_filename(contents, P_value, filename):
    if contents is None or P_value == 0:
        raise PreventUpdate
    if P_value > 0 and contents is not None:
        df = parse_contents(contents, filename)

        if df is not None:
            max_P = df[df.columns[1]].max()
            # if max_P > float(P_value):
            #     raise PreventUpdate
        else:
            raise PreventUpdate

    else:
        return False


#################################################

# ----------  DISPLAYS MESSAGE OF CAUTION ABOUT NOMINAL POWER  ----------- #
@app.callback(Output('compare_p', 'displayed'),
              [Input('Drag_file', 'contents'),
               Input('Pnom', 'value'),
               Input('button', 'n_clicks'), ],
              [State('Drag_file', 'filename')])
def bid_bigger_nominal(contents, P_value, clicks, filename):




    if (P_value > 0 and contents is not None and clicks is None):
        df = parse_contents(contents, filename)

        user_active = flask.request.cookies.get('custom-auth-session')

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("SELECT * FROM portfolio WHERE Player = (%s);", (user_active,))
        accum = cur.fetchall()
        total = accum[0][2] + accum[0][3] + accum[0][4] + accum[0][5]

        conn.close()
        cur.close()

        if df is not None:
            max_P = df[df.columns[1]].max()

            if max_P > float(total):
                return True
            else:
                return False


#################################################

# ----------  DISPLAYS MESSAGE OF CAUTION ABOUT FORMAT OF FILE ----------- #
@app.callback(Output('table_size', 'displayed'),
              [Input('Drag_file', 'contents')],
              [State('Drag_file', 'filename')])
def table_format(contents, filename):
    if contents is None:
        return False
    else:
        df = parse_contents(contents, filename)
        if df is not None:
            if (len(df.axes[1]) == 5) and (len(df.axes[0]) == 24):
                return False
            else:
                return True
        else:
            return True




## UPDATE SCORE FIGURE

@app.callback([Output('graph_reve', 'figure'),
               Output('datatable_graph_reve', 'style')],
              [Input("popover-target", "n_clicks")])
def score_fig(nome):
    b2 = int(flask.request.cookies.get('b2'))
    b2p = int(flask.request.cookies.get('b2p'))
    accufig1 = (json.loads((flask.request.cookies.get('accufig'))))
    data1 = (json.loads((flask.request.cookies.get('data_c'))))
    bar_acum = (json.loads((flask.request.cookies.get('bar_acum'))))
    rate_accum1 = json.loads((flask.request.cookies.get('rate_accum')))

    if b2p == 0:
        b2p = b2
        dash.callback_context.response.set_cookie('b2p', str(b2p), max_age=7200)

    # data1 = 1
    # accufig1 = 100

    accum = float(flask.request.cookies.get('accum_val'))
    accum_1 = float(flask.request.cookies.get('accum_1'))

    if b2 >= 1:

        sho = {'display': 'block', 'width': '100%', 'height': '20vw'}

        figure = make_subplots(specs=[[{"secondary_y": True}]])
        figure.add_trace(go.Bar(x=data1, y=bar_acum, name="Day Revenue", marker=dict(color=app.color_3)),
                         secondary_y=False, )

        figure.add_trace(go.Scatter(x=data1, y=rate_accum1, name="Rate", marker=dict(color=app.color_bar2)),
                         secondary_y=False, )

        figure.add_trace(go.Scatter(x=data1, y=accufig1, name="Accumulated", marker=dict(color=app.color_line)),
                         secondary_y=True, )

        figure.update_layout(title='Accumulated revenue & Accuracy rate', titlefont=dict(color=app.color_3),
                             xaxis=dict(title='Day', gridcolor=app.color_3, titlefont=dict(color=app.color_3),
                                        tickfont=dict(color=app.color_3)),
                             yaxis=dict(title='Revenue [€] -- Rate [€/day]', titlefont=dict(color=app.color_3),
                                        tickfont=dict(color=app.color_3), automargin=True, gridcolor=app.color_3, ),
                             yaxis2=dict(title='Acc. Revenue [€]', titlefont=dict(color=app.color_line),
                                         tickfont=dict(color=app.color_line), overlaying='y', side='right',
                                         automargin=True),
                             paper_bgcolor=app.color_bfig,
                             plot_bgcolor=app.color_1,
                             # height=350,
                             # width='100%', height=300,
                             legend_orientation="h",
                             legend=dict(x=-.1, y=1.1, font=dict(color=app.color_3)),
                             ),
        figure.update_yaxes(automargin=True)
        return figure, sho


    else:
        figure = {
            'data': [{
                'x': [],
                'y': [],
                'type': 'line'
            }]
        }

        sho = {'display': 'none'}

    return figure, sho


## DOWNLOAD DATA BUTTONS

@app.callback([Output('link_downl', 'href'),
               Output('downl_data', 'children'),
               # Output('wind_hist', 'data'),
               # Output('irrad_hist', 'data'),
               Output('link_downl', 'download'),
               Output('link_downl_dap', 'download'),
               Output('link_downl_dap', 'href'),
               Output('link_downl3', 'download'),
               Output('link_downl3', 'href'),
               Output('downl_data', 'disabled'),
               Output('downl_dap', 'disabled'),
               Output('downl_dap', 'children'),
               Output('loading_1', 'children'),
               Output('loading_2', 'children'),
               Output('loading_3', 'children'), ],
              [Input('Page_1', 'id')],
              # [State('wind_hist', 'data'),
              #  # State('irrad_hist', 'data')
              #  ]
              )
def update_download_link(n_clicks):
    user_active = flask.request.cookies.get('custom-auth-session')

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    cur = conn.cursor()

    cur.execute("SELECT days FROM Leader_board WHERE Player = (%s);", (user_active,))
    # print(players)
    days = cur.fetchone()
    days = days[0]
    cur.close()
    conn.close()

    # b2 = int(flask.request.cookies.get('b2'))
    b2 = days



    # print(dff)

    if b2 >= 1:

        ################################
        ################################

        PV_irradiation = app.PV_irradiation


        PV_irradiation['DateTime'] = pd.to_datetime(PV_irradiation['DateTime'], format="%d/%m/%Y %H:%M")

        time_mask = PV_irradiation['DateTime'] <= PV_irradiation['DateTime'].iloc[-1] - datetime.timedelta(days=play_days - b2)

        dates_irrad = PV_irradiation['DateTime'][time_mask]

        #
        #
        delta2 = (datetime.datetime.now() - datetime.datetime.strptime(str(dates_irrad.iloc[-1]),
                                                                       "%Y-%m-%d %H:%M:%S")).days

        PV_irradiation['DateTime'] = PV_irradiation['DateTime'] + datetime.timedelta(delta2 + b2)

        PV_irradiation_hist = PV_irradiation[time_mask]
        PV_irradiation_play = PV_irradiation[~time_mask]
        PV_irradiation_play = PV_irradiation_play[0 + 96 * b2:96 * (b2 + 1)]

        ################################
        ################################

        ################################
        ################################

        WT_speed = app.wind_data


        WT_speed['DateTime'] = pd.to_datetime(WT_speed['DateTime'], format="%d/%m/%Y %H:%M")
        # WT_speed_dates_hist = WT_speed['DateTime']

        time_mask = WT_speed['DateTime'] <= WT_speed['DateTime'].iloc[-1] - datetime.timedelta(days=play_days - b2)


        dates_wind = WT_speed['DateTime'][time_mask]

        #
        #
        delta2 = (datetime.datetime.now() - datetime.datetime.strptime(str(dates_wind.iloc[-1]),
                                                                       "%Y-%m-%d %H:%M:%S")).days

        WT_speed['DateTime'] = WT_speed['DateTime'] + datetime.timedelta(delta2 + b2)

        WT_speed_hist = WT_speed[time_mask]
        # print(WT_speed_hist)
        WT_speed_play = WT_speed[~time_mask]
        WT_speed_play = WT_speed_play[0 + 144 * b2:144 * (b2 + 1)]
        ################################
        ################################



        wf_power = pd.DataFrame(WT_speed_hist, columns=['DateTime', 'Measured'])

        wf_power['DateTime'] = pd.to_datetime(wf_power['DateTime'])
        wf_power['DateTime'] = wf_power['DateTime'].dt.strftime('%Y-%m-%d %H:%M')

        irrad_power = pd.DataFrame(PV_irradiation_hist, columns=['DateTime', 'Irradiation [kW/m2]'])

        irrad_power['DateTime'] = pd.to_datetime(irrad_power['DateTime'])
        irrad_power['DateTime'] = irrad_power['DateTime'].dt.strftime('%Y-%m-%d %H:%M')


        # nd1 = (app.dates_nextday.iloc[(b2 - 1) * 144:144 * (b2 - 1) + 144]).to_frame()
        nd1 = WT_speed_play
        nd1_i = PV_irradiation_play

        # print((WT_speed_hist.iloc[-1, 0]))
        # print(type(datetime.timedelta(minutes=10)))
        nd1 = nd1.reset_index()
        nd1['DateTime'] = nd1['DateTime'].dt.strftime('%Y-%m-%d %H:%M')
        # print(nd1)
        nd1 = nd1.drop('index', 1)

        nd1_i = nd1_i.reset_index()
        nd1_i['DateTime'] = nd1_i['DateTime'].dt.strftime('%Y-%m-%d %H:%M')
        # print(nd1)
        nd1_i = nd1_i.drop('index', 1)


        idx = pd.date_range(
            datetime.datetime.strptime(str(WT_speed_hist.iloc[-1, 0]), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=10),
            periods=144, freq='10T')

        idx_i = pd.date_range(
            datetime.datetime.strptime(str(PV_irradiation_hist.iloc[-1, 0]), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=15),
            periods=96, freq='15T')

        ze = np.zeros((len(idx), 1))
        ndz = pd.DataFrame(ze, index=idx)
        ndz = ndz.reset_index()
        ndz = ndz.rename(columns={'index': 'DateTime', 0: 'Measured'})


        ze_i = np.zeros((len(idx_i), 1))
        ndz_i = pd.DataFrame(ze_i, index=idx_i)
        ndz_i = ndz_i.reset_index()
        ndz_i = ndz_i.rename(columns={'index': 'DateTime', 0: 'Irradiation [kW/m2]'})


        dff2 = wf_power.append((ndz), ignore_index=True)
        dff2 = dff2.rename(columns={'DateTime': 'date', 'Measured': 'speed'})

        dff1 = wf_power.append(nd1, ignore_index=True)

        # dff = dff.append(nd, ignore_index=False)

        a = dff1.to_numpy()
        b = a.tolist()
        wf_power = json.dumps(b, default=json_util.default)
        # print(wf_power)



        dff2_i = irrad_power.append((ndz_i), ignore_index=True)
        # dff2_i = dff2_i.rename(columns={'DateTime': 'date', 'Irradiation [kW/m2]': 'Irradiation'})

        dff1_i = irrad_power.append(nd1_i, ignore_index=True)

        # dff = dff.append(nd, ignore_index=False)

        # a_i = dff1_i.to_numpy()
        # b_i = a_i.tolist()
        # irrad_power = json.dumps(b_i, default=json_util.default)
        # print(wf_power)


        tn = pd.Series('t{}'.format(i) for i in range(1, 25))
        pr = pd.DataFrame(app.prices)
        aa = pd.Series(pr[pr.columns[b2 + 1]])
        aa = aa.reset_index()

        df_dap = pd.DataFrame({'': tn, 'DAP': aa.iloc[:, 1]})
        dap_file = 'DAP_{}.csv'.format((datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d"))

        csv_string_dap = df_dap.to_csv(index=False, header=True, encoding='utf-8')
        csv_string_dap = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string_dap)

        csv_string = dff2.to_csv(index=False, header=True, encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)

        csv_string_irrad = dff2_i.to_csv(index=False, header=True, encoding='utf-8')
        csv_string_irrad = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string_irrad)
        # print(dff)
        nfile = 'windSpeed_{}.csv'.format(
            (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d"))

        sifile = 'solarIrrad_{}.csv'.format(
            (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d"))

        return csv_string, ' Download Updated Historical Data', nfile, dap_file, csv_string_dap, sifile, csv_string_irrad, False, False, \
               ' Download Day Ahead Prices', button1, button2, button3


    else:


        ################################
        ################################

        PV_irradiation = app.PV_irradiation




        # PV_irradiation = pd.DataFrame(PV_irradiation)


        PV_irradiation['DateTime'] = pd.to_datetime(PV_irradiation['DateTime'], format="%d/%m/%Y %H:%M")
        # PV_irradiation_dates_hist = PV_irradiation['DateTime']

        time_mask = PV_irradiation['DateTime'] <= PV_irradiation['DateTime'].iloc[-1] - datetime.timedelta(days=play_days)

        dates_irrad = PV_irradiation['DateTime'][time_mask]

        #
        #
        delta2 = (datetime.datetime.now() - datetime.datetime.strptime(str(dates_irrad.iloc[-1]),
                                                                       "%Y-%m-%d %H:%M:%S")).days

        PV_irradiation['DateTime'] = PV_irradiation['DateTime'] + datetime.timedelta(delta2 + b2)

        PV_irradiation_hist = PV_irradiation[time_mask]
        # PV_irradiation_play = PV_irradiation[~time_mask]

        ################################
        ################################

        aa = PV_irradiation_hist

        a = aa.to_numpy()

        b = a.tolist()


        # a = PV_irradiation_hist
        #
        # b = a.tolist()

        idx = pd.date_range(
            (datetime.datetime.strptime(str(PV_irradiation_hist.iloc[-1, 0]), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=15)),
            periods=96, freq='15T')
        # print(idx)
        ze = np.zeros((len(idx), 1))
        ndz = pd.DataFrame(ze, index=idx)
        ndz = ndz.reset_index()

        ndz = ndz.rename(columns={'index': 'date', 0: 'irradiation'})
        irradiation = json.dumps(b, default=json_util.default)

        dff = PV_irradiation_hist#app.dates_irrad1
        dff = dff.reset_index()
        dff = dff.rename(columns={'DateTime': 'date', 'Irradiation [kW/m2]': 'irradiation'})
        dff_irrad = dff.append((ndz), ignore_index=True)
        dff_irrad= dff_irrad.drop('index', 1)

        # dff_irrad = dff_irrad.reset_index('date')



        ################################
        ################################

        WT_speed = app.wind_data


        WT_speed['DateTime'] = pd.to_datetime(WT_speed['DateTime'], format="%d/%m/%Y %H:%M")
        # WT_speed_dates_hist = WT_speed['DateTime']

        time_mask = WT_speed['DateTime'] <= WT_speed['DateTime'].iloc[-1] - datetime.timedelta(days=play_days)

        dates_irrad = WT_speed['DateTime'][time_mask]

        #
        #
        delta2 = (datetime.datetime.now() - datetime.datetime.strptime(str(dates_irrad.iloc[-1]),
                                                                       "%Y-%m-%d %H:%M:%S")).days

        WT_speed['DateTime'] = WT_speed['DateTime'] + datetime.timedelta(delta2 + b2)

        WT_speed_hist = WT_speed[time_mask]
        # WT_speed_play = WT_speed[~time_mask]

        ################################
        ################################


        p_wf_power = WT_speed_hist

        aa = WT_speed_hist


        a = aa.to_numpy()

        b = a.tolist()

        idx = pd.date_range(
            (datetime.datetime.strptime(str(aa.iloc[-1, 0]), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=10)),
            periods=144, freq='10T')
        ze = np.zeros((len(idx), 1))
        ndz = pd.DataFrame(ze, index=idx)
        ndz = ndz.reset_index()

        ndz = ndz.rename(columns={'index': 'date', 0: 'speed'})
        wf_power = json.dumps(b, default=json_util.default)

        dff = p_wf_power
        dff = dff.reset_index()
        dff = dff.rename(columns={'DateTime': 'date', 'Measured': 'speed'})
        dff = dff.drop('index', 1)

        dff1 = dff.append((ndz), ignore_index=True)

        tn = pd.Series('t{}'.format(i) for i in range(1, 25))
        pr = pd.DataFrame(app.prices)
        aa = pd.Series(pr[pr.columns[b2 + 1]])
        aa = aa.reset_index()

        df_dap = pd.DataFrame({'': tn, 'DAP': aa.iloc[:, 1]})
        dap_file = 'DAP_{}.csv'.format((datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d"))

        nfile = 'windSpeed_{}.csv'.format(
            (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d"))

        sifile = 'solarIrrad_{}.csv'.format(
            (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d"))

        ################################
        csv_string_dap = df_dap.to_csv(index=False, header=True, encoding='utf-8')
        csv_string_dap = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string_dap)

        csv_string = dff1.to_csv(index=False, header=True, encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)

        csv_string_irrad = dff_irrad.to_csv(index=False, header=True, encoding='utf-8')
        csv_string_irrad = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string_irrad)

        return csv_string, ' Download Historical Data', nfile, dap_file, csv_string_dap, sifile, csv_string_irrad, False, False, \
               ' Download Day Ahead Prices', button1, button2, button3


## Leaderboard popover

@app.callback(
    [Output("popover", "is_open"),
     Output('table-editing-simple', 'data'),
     Output('table-editing-simple', 'columns'),
     Output('position_lead1', 'value'),
     Output('table-editing-simple', 'style_data_conditional')],
    [Input("popover-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    ################
    # users = app.lead_board['index']
    # user_pos = app.lead_board[app.lead_board['index'] == user_active].index.values
    user_active = flask.request.cookies.get('custom-auth-session')

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    sql_command = "SELECT player, days, revenue, rate FROM Leader_board ORDER BY rate DESC;"

    df = pd.read_sql(sql_command, conn)

    df = df.reset_index()
    df = df.rename(columns={'index': 'position'})
    df['position'] = df['position'] + 1

    conn.close()

    user_pos2 = df.index[df['player'] == user_active]

    a = user_pos2 + 1

    # user_pos_sort = app.lead_board.sort_values(by=['rate'], ascending=False)
    # user_pos_sort = user_pos_sort.reset_index()

    # a = user_pos_sort[user_pos_sort['index'] == user_active].index.values

    style_data_conditional = [{
        "if": {"row_index": int(a[0] - 1)},
        "backgroundColor": app.color_line,
        'color': app.color_1,
    }]
    ################

    # columns = (
    #               [{'id': p, 'name': p} for p in app.lead_board.columns]
    #           )

    columns = (
        [{'id': p, 'name': p.capitalize()} for p in df.columns]
    )
    # data = flask.jsonify(df)
    # data = df.to_json()
    # columns = df.head()
    data = [
        {p: df.at[i, p] for p in df.columns}
        # dict(Model=i, **{param: app.lead_board[i]['index'] for param in params})

        # dict(Model=i, **{param: 0 for param in params})
        for i in range(len(df['player']))
    ]
    # data = df.to_dict()
    if n:
        return not is_open, data, columns, f'{int(int(a[0]))}', style_data_conditional
    return is_open, data, columns, f'{int(int(a[0]))}', style_data_conditional


# ----------  UPDATE SCOREBOARD ----------- #
@app.callback([Output('score_board1', 'value'),
               Output('score_board1', 'style')],
              [Input('Page_1', 'id')]
              )
def score_1(nome):
    A = nome

    # time.sleep(0.5)

    # df = app.ddf
    accum = float(flask.request.cookies.get('accum_val'))
    b2 = int(flask.request.cookies.get('b2'))
    b2p = int(flask.request.cookies.get('b2p'))
    user_active = flask.request.cookies.get('custom-auth-session')
    user = user_active

    if accum == 0:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("SELECT Revenue FROM Leader_board WHERE Player = (%s);", (user,))
        accum = cur.fetchone()
        accum = accum[0]
        conn.close()
        cur.close()

        # accum = float(app.lead_board.iloc[user_pos, 1])
        dash.callback_context.response.set_cookie('accum_val', str(accum), max_age=7200)

    # else:
    #     app.lead_board.at[user_pos, 'Accum'] = accum
    #
    # if b2 > 0:
    #     app.lead_board.at[user_pos, 'rate'] = app.lead_board.iloc[user_pos, 1] / int(b2)

    if (b2) > 0:
        # dash.callback_context.response.set_cookie('accum_1', str(accum), max_age=7200)
        accum_1 = float(flask.request.cookies.get('accum_1'))

        if accum - accum_1 >= 0:
            col = {'textAlign': 'center', 'verticalAlign': "middle", 'borderColor': app.color_3, 'borderWidth': '0.1vw',
                   'resize': 'none', 'height': '3vw', 'width': '100%',
                   'backgroundColor': app.color_3, 'color': app.color_8, 'font-size': '1.2vw'}
            accum_1 = accum
            # app.global_rev[b2 - 1] = accum
            dash.callback_context.response.set_cookie('accum_val', str(accum), max_age=7200)
            accum = flask.request.cookies.get('accum_val')
            # dash.callback_context.response.set_cookie('accum_1', str(accum), max_age=7200)

            day = b2

            return '€ ' + f'{float(accum):.2f}', col

        else:
            col = {'textAlign': 'center', 'verticalAlign': "middle", 'height': '3vw', 'width': '100%',
                   'borderColor': app.color_3, 'resize': 'none',
                   'backgroundColor': app.color_3, 'color': app.color_8, 'font-size': '1.2vw'}
            # app.global_rev[b2 - 1] = accum
            dash.callback_context.response.set_cookie('accum_val', str(accum), max_age=7200)
            accum = flask.request.cookies.get('accum_val')
            # dash.callback_context.response.set_cookie('accum_1', str(accum), max_age=7200)

            return '€ ' + f'{float(accum):.2f}', col



    else:
        col = {'textAlign': 'center', 'verticalAlign': "middle", 'height': '3vw', 'width': '100%',
               'resize': 'none', 'backgroundColor': app.color_3, 'color': app.color_8,
               'borderColor': app.color_3, 'font-size': '1.2vw'}
        dash.callback_context.response.set_cookie('accum_val', str(accum), max_age=7200)
        # accum = flask.request.cookies.get('accum_val')

        return '€ ' + f'{float(accum):.2f}', col


@app.callback(
    Output("modal", "is_open"),
    [Input("your_button", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    [Output("port_dwnl", "href"),
     Output("port_dwnl", "download"),
     Output('loading_4', 'children'),],
    [Input('Page_1', 'id')],
)
def toggle_modal(n2):


    user_active = flask.request.cookies.get('custom-auth-session')
    user = user_active

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM portfolio WHERE Player = (%s);", (user,))
    accum = cur.fetchall()
    conn.close()
    cur.close()

    constraints = {'Thermal':[accum[0][2],accum[0][2]*app.rampU_thermal,accum[0][2]*app.rampD_thermal, accum[0][2]*app.min_thermal,accum[0][2]*app.max_thermal,0,0,0],
                   'Wind':[accum[0][3],accum[0][3]*app.rampU_wind,accum[0][3]*app.rampD_wind, app.min_wind,accum[0][3]*app.max_wind,0,0,0],
                   'Solar':[accum[0][4],accum[0][4]*app.rampU_solar,accum[0][4]*app.rampD_solar, app.min_solar,accum[0][4]*app.max_solar,0,0,0],
                   'Storage':[accum[0][5],accum[0][5]*app.rampU_storage,accum[0][5]*app.rampD_storage, accum[0][5]*app.min_storage,accum[0][5]*app.max_storage,app.min_SOC_storage,app.max_SOC_storage,app.initial_SOC_storage]
                   }


    constraints = pd.DataFrame(constraints, index=['Nominal MWh','Ramp-up MWh', 'Ramp-down MWh', 'Min MWh', 'Max MWh', 'max_SOC %', 'min_SOC %','SOC_initial %'])




    # if n1:
    csv_string = constraints.to_csv(index=True, header=True, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)
    nfile = 'portfolio_{}.csv'.format(user)

    return csv_string, nfile, button4

    # else:
    #     raise PreventUpdate
