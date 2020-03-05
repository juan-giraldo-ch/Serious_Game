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
import os  # Importing OS functions
import datetime
import pickle
import copy
import pathlib

from six.moves.urllib.parse import quote

from app import app

from apps import tue_header, user_data, buttons, messages, score_info





#
# ##################### - FIRST PAGE - ############################
layout = html.Div([

    ##################### - HEADER - ############################

    tue_header.header(),

    # ----------------------------------------------------------------------

    ##################### - DOWNLOAD HISTORICAL DATA - ############################

    # ----------------------------------------------------------------------

    html.Div([

        html.Div([
            # ---------- SCORE BOARD ----------- #
            html.Div([
                score_info.self_score(),
            ], className='row'),

            html.Div([
                ##################### - BUTTON FOR SUBMISSION - ############################

                # -- Button for submitting the info and plotting
                buttons.submit_b(),
            ], className='row'),

        ], className='three columns', style={'backgroundColor': app.color_3}
        ),

        ##################### - USER INFORMATION - ############################
        html.Div([
            html.Div([
                html.Div([
                    tue_header.curr_date(),
                    buttons.download_data(),

                ], className='nine columns'),
            ]),

            html.Div([
                # ##########################################

                # # ---------- TYPE IN NOMINAL POWER ----------- #
                user_data.nominal_P(),

                user_data.drag_file(),
            ], className='nine columns'),

            html.Div([
                html.Div([
                    # ----------------------------------------------------------------------
                    # ---------- BIDS TABLE ----------- #
                    html.Div([
                        user_data.table_data(),
                    ], className='two columns', style={'backgroundColor': app.color_1}),

                    html.Div([
                        score_info.fig_rev(),
                    ], className='seven columns', style={'marginLeft': '20%', 'backgroundColor': app.color_1}),

                    # ---------- SCORE FIGRURE ----------- #
                ], className='nine columns'),
            ], className='row'),

        ], className='row'),

    ], className='row'),
    # # ---------- LOAD BID_FILE ----------- #

    # ################################################

    ###########################################

    # ----------------------------------------------------------------------

    # html.Div(style={'padding': '10px'}),

    # ---------------------------------------------------------------------------

    ##################### - ERROR MESSAGES - ############################

    # # ---------- FILE HAS WRONG SIZE ----------- #
    messages.mesag_size(),

    # ##############################################

    # ---------- BID > THAN NOMINAL P ----------- #
    messages.mesag_nom(),

    ##############################################

    # --------------------------------------------------------------------

], className='twelve columns', id='Page_1', style={'backgroundColor': app.color_1}

)


################################################################
################################################################

##################### - FUNCTION -- LOAD FILE - ############################

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))


#################################################################
#################################################################

# ---------- UPDATE CURRENT_DAY ----------- #
@app.callback(Output('Counter_day', 'children'),
              [Input('Counter_day', 'contents')])
def display_confirm(day):
    day = '''*Current trading day: {}*'''.format(
        (datetime.datetime.now() + datetime.timedelta(days=app.b2)).strftime("%d/%m/%Y"))
    return day


# ---------- TABLE FROM DATA FILE ----------- #
@app.callback([Output('table_data', 'data'),
               Output('table_data', 'columns'),
               Output('datatable-container', 'style')],
              [Input('Drag_file', 'contents')],
              [State('Drag_file', 'filename')])
def display_confirm(contents, filename):
    if contents is None:
        return [{}], [], {'display': 'block', 'marginLeft': '20%'}
    else:
        df = parse_contents(contents, filename)
        app.ddf = df
        if (len(df.axes[1]) == 2) and (len(df.axes[0]) == 24):
            return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], {'display': 'block',
                                                                                       'marginLeft': '20%'}
        else:
            return [{}], [], {'display': 'block', 'marginLeft': '20%'}


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
            'width': '50%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '2.5px', 'borderStyle': 'ridge',
            'borderRadius': '50px', 'textAlign': 'center', 'margin': '80px',
            'marginLeft': '20%', 'border-color': app.color_7,
            'backgroundColor': app.color_1, 'font-size': '20px'
        }
        disab = False
        return existing_state, disab, col
    if (P_value == 0 and contents is not None and clicks is None):
        df = parse_contents(contents, filename)
        if (len(df.axes[1]) == 2) and (len(df.axes[0]) == 24):
            col = {
                'width': '50%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '2.5px', 'borderStyle': 'dashed',
                'borderRadius': '50px', 'textAlign': 'center', 'margin': '80px',
                'marginLeft': '20%', 'border-color': app.color_8, 'font-size': '20px'
            }
            name = filename
        else:
            if not ok_button:
                col = {
                    'width': '50%', 'height': '60px', 'lineHeight': '60px',
                    'borderWidth': '2.5px', 'borderStyle': 'dashed',
                    'borderRadius': '50px', 'textAlign': 'center', 'margin': '80px',
                    'marginLeft': '20%', 'border-color': app.color_7, 'font-size': '20px'
                }
            else:
                col = {
                    'width': '50%', 'height': '60px', 'lineHeight': '60px',
                    'borderWidth': '1.2px', 'borderStyle': 'dashed',
                    'borderRadius': '50px', 'textAlign': 'center', 'margin': '80px',
                    'marginLeft': '20%', 'border-color': app.color_7, 'font-size': '20px'
                }
            name = existing_state
        disab = False
        return name, disab, col
    if P_value > 0 and contents is not None and clicks is None:
        df = parse_contents(contents, filename)
        if (len(df.axes[1]) == 2) and (len(df.axes[0]) == 24):
            col = {
                'width': '50%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '2.5px', 'borderStyle': 'dashed',
                'borderRadius': '50px', 'textAlign': 'center', 'margin': '80px',
                'marginLeft': '20%', 'border-color': app.color_3,
                'backgroundColor': app.color_8, 'font-size': '20px'
            }
            if ok_P:
                col = {
                    'width': '50%', 'height': '60px', 'lineHeight': '60px',
                    'borderWidth': '2.5px', 'borderStyle': 'dashed',
                    'borderRadius': '50px', 'textAlign': 'center', 'margin': '80px',
                    'marginLeft': '20%', 'border-color': app.color_7, 'font-size': '20px'
                }
            name = filename
        else:
            col = {
                'width': '50%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1.2px', 'borderStyle': 'dashed',
                'borderRadius': '50px', 'textAlign': 'center', 'margin': '80px',
                'marginLeft': '20%', 'border-color': app.color_7, 'font-size': '20px'
            }
            name = existing_state
        disab = False
        return name, disab, col
    if (P_value > 0 and contents is not None and clicks is not None):
        df = parse_contents(contents, filename)
        if (len(df.axes[1]) == 2) and (len(df.axes[0]) == 24):
            col = {
                'width': '50%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '2.5px', 'borderStyle': 'dashed',
                'borderRadius': '50px', 'textAlign': 'center', 'margin': '80px',
                'marginLeft': '20%', 'border-color': app.color_8, 'font-size': '20px'
            }
            name = filename
        else:
            col = {
                'width': '50%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '2.5px', 'borderStyle': 'dashed',
                'borderRadius': '50px', 'textAlign': 'center', 'margin': '80px',
                'marginLeft': '20%', 'border-color': app.color_7, 'font-size': '20px'
            }
            name = existing_state
        disab = False
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
        app.Pvalue = P_value
        prompt = 'Bid file missing'
        col = {'color': app.color_7, 'font-size': '18px', 'marginLeft': '38%'}
        bord = {'borderColor': app.color_8, 'borderWidth': '2.0px', 'marginLeft': '35%',
                'backgroundColor': app.color_6}  # style={'marginLeft':130}
        disab = True
        tab_disab = True
        return prompt, col, bord, disab, tab_disab
    if (P_value == 0 and contents is not None and clicks is None):
        df = parse_contents(contents, filename)
        if (len(df.axes[1]) == 2) and (len(df.axes[0]) == 24):
            prompt = 'Nominal power missing'
            col = {'color': app.color_7, 'font-size': '18px', 'marginLeft': '10%'}
            bord = {'borderColor': app.color_7, 'borderWidth': '2.0px', 'marginLeft': '35%',
                    'backgroundColor': app.color_6}
            tab_disab = True
            disab = True
            return prompt, col, bord, disab, tab_disab
        else:
            prompt = 'Error in Data file - Upload correct file'
            col = {'color': app.color_7, 'font-size': '18px', 'marginLeft': '10%'}
            bord = {'borderColor': app.color_7, 'borderWidth': '2.0px', 'marginLeft': '35%',
                    'backgroundColor': app.color_6}
            tab_disab = True
            disab = True
            return prompt, col, bord, disab, tab_disab

    if (P_value > 0 and contents is not None and clicks is None):
        df = parse_contents(contents, filename)
        app.Pvalue = P_value
        if (len(df.axes[1]) == 2) and (len(df.axes[0]) == 24):
            prompt = 'Click SUBMIT to Continue'
            col = {'color': app.color_8, 'font-size': '18px', 'marginLeft': '30%'}
            bord = {'borderColor': app.color_8, 'borderWidth': '2.0px', 'marginLeft': '35%',
                    'backgroundColor': app.color_6}
            disab = True
            tab_disab = True
            return prompt, col, bord, disab, tab_disab
        else:
            prompt = 'Error in Data file - Upload correct file'
            col = {'color': app.color_7, 'font-size': '18px', 'marginLeft': '10%'}
            bord = {'borderColor': app.color_8, 'borderWidth': '2.0px', 'marginLeft': '35%',
                    'backgroundColor': app.color_6}
            disab = True
            tab_disab = True
            return prompt, col, bord, disab, tab_disab
    if (P_value > 0 and contents is not None and clicks is not None):
        app.Pvalue = P_value
        prompt = 'Bid Successfully Submitted!'
        col = {'color': app.color_8, 'font-size': '18px', 'marginLeft': '10%'}
        bord = {'borderColor': app.color_8, 'borderWidth': '2.0px', 'marginLeft': '35%',
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
        max_P = df[df.columns[1]].max()
        if max_P > float(P_value):
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
        max_P = df[df.columns[1]].max()
        if max_P > float(P_value):
            return True


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
        if (len(df.axes[1]) == 2) and (len(df.axes[0]) == 24):
            return False
        else:
            return True


# #################################################


# ----------  SENDS TO PAGE 2 ----------- #
@app.callback(Output('url', 'pathname'),
              [Input('button', 'n_clicks')])
def table_format(clicks):
    if clicks is not None:
        return '/Page_2'


# #################################################


# ----------  UPDATE SCOREBOARD ----------- #
@app.callback([Output('score_board1', 'value'),
               Output('score_board1', 'style')],
              [Input('Page_1', 'id'),
               Input('Counter_day', 'contents')]
               )
def score_1(nome, ncl):
    A = nome
    print(A)
    df = app.ddf
    if (app.b2 - app.b2p) >= 1:
        if app.accum - app.acc1 >= 0:
            col = {'width': '30%', 'height': '1%', 'textAlign': 'center', 'verticalAlign': "middle",
                   'margin-left': '5%', 'borderColor': app.color_8, 'borderWidth': '4.0px', 'resize': 'none',
                   'backgroundColor': app.color_3, 'color': app.color_4}
            app.acc1 = app.accum
            app.global_rev[app.b2 - 1] = app.accum

            return '€ ' + f'{app.accum:.2f}', col

        else:
            col = {'width': '30%', 'height': '1%', 'textAlign': 'center', 'verticalAlign': "middle",
                   'margin-left': '5%', 'borderColor': app.color_7, 'borderWidth': '4.0px', 'resize': 'none',
                   'backgroundColor': app.color_3, 'color': app.color_4}
            app.acc1 = app.accum
            app.global_rev[app.b2 - 1] = app.accum

            return '€ ' + f'{app.accum:.2f}', col



    else:
        col = {'width': '30%', 'height': '1%', 'textAlign': 'center', 'verticalAlign': "middle",
               'margin-left': '5%', 'resize': 'none', 'backgroundColor': app.color_3, 'color': app.color_4,
               'borderColor': app.color_3}

        return '€ ' + f'{app.accum:.2f}', col



## UPDATE SCORE FIGURE

@app.callback([Output('graph_reve', 'figure'),
               Output('datatable_graph_reve', 'style')],
              [Input('Page_1', 'id')])
def score_fig(nome):
    if (app.b2 - app.b2p) >= 1:
        app.accufig.append(app.accum)
        app.bar_acum.append(app.accum - app.acc1)
        app.lin_exp_accum.append(app.exp_accum)
        app.rate_accum.append(100 * app.accufig[-1] / app.lin_exp_accum[-1])
        app.A = ((datetime.datetime.now() + datetime.timedelta(days=app.b2 - 1)).strftime("%d/%m/%Y"))
        app.data.append(app.A)

        figure = {
            'data': [
                {
                    'x': app.data,
                    'y': app.accufig,
                    'type': 'line',
                    'name': 'Accumulated',
                    'marker': {'color': app.color_10}
                },
                {
                    'x': app.data,
                    'y': app.bar_acum,
                    'type': 'bar',
                    'name': 'Day\'s Revenue',
                    'marker': {'color': app.color_9}
                },
                {
                    'x': app.data,
                    'y': app.rate_accum,
                    'type': 'line',
                    'name': 'Rate',
                    'marker': {'color': app.color_5}, 'yaxis': 'y2'
                },
            ],
            'layout': go.Layout(title='Accumulated revenue & Accuracy rate', titlefont=dict(color=app.color_4),
                                xaxis=dict(title='Day', gridcolor=app.color_3, titlefont=dict(color=app.color_4),
                                           tickfont=dict(color=app.color_4)),
                                yaxis=dict(title='Revenue [€]', titlefont=dict(color=app.color_9),
                                           tickfont=dict(color=app.color_9), automargin=True, gridcolor=app.color_3, ),
                                yaxis2=dict(title='Acc. rate [%]', titlefont=dict(color=app.color_5),
                                            tickfont=dict(color=app.color_5), overlaying='y', side='right',
                                            automargin=True),
                                paper_bgcolor=app.color_3,
                                plot_bgcolor=app.color_1,
                                width=900, height=400,

                                ),
        }
        sho = {'display': 'block'}
    else:
        figure = {
            'data': [{
                'x': [],
                'y': [],
                'type': 'line'
            }]
        }
        if app.A != ((datetime.datetime.now() + datetime.timedelta(days=app.b2 - 1)).strftime("%d/%m/%Y")):
            app.A = ((datetime.datetime.now() + datetime.timedelta(days=app.b2 - 1)).strftime("%d/%m/%Y"))
            app.data.append(app.A)
        sho = {'display': 'none'}
        app.accufig = app.accufig
    return figure, sho


@app.callback([Output('link_downl', 'href'),
               Output('downl_data', 'children')],
              [Input('Page_1', 'id')])
def update_download_link(n_clicks):
    dff = app.wf_power
    csv_string = dff.to_csv(index=True, header=True, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)

    if app.b2 >= 1:
        nd = app.dates_nextday.iloc[(app.b2 - 1) * 96:96 * (app.b2 - 1) + 96, 0]
        dff = dff.append(nd, ignore_index=False)
        csv_string = dff.to_csv(index=True, header=True, encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)

        return csv_string, '1. Download Updated Historical Data'
    else:
        return csv_string, '1. Download Historical Data'

# #################################################
