import dash
import dash_core_components as dcc
import dash_html_components as html
import os  # Importing OS functions
import dash_bootstrap_components as dbc
from apps import tue_header, messages
from app import app
from dash.dependencies import Input, Output, State
import psycopg2
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
import dash_daq as daq
from matplotlib import cm
import math
import flask


import pandas as pd

cmap_name = 'RdYlGn'
cmap = cm.get_cmap(cmap_name)  # cm.colors.LinearSegmentedColormap.from_list("", ["green","yellow","red"])
reversed_color_map = cmap.reversed()
cmap_name2 = 'cool'
cmap2 = cm.get_cmap(cmap_name2)  # cm.colors.LinearSegmentedColormap.from_list("", ["green","yellow","red"])

night_colors = ['darkblue', 'royalblue', 'cyan',
                'lightcyan']

if app.database_url == 'Local':
    url_data = os.popen("heroku config:get DATABASE_URL -a emga").read().strip()  # When local machine

if app.database_url == 'Server':
    url_data = os.environ.get('DATABASE_URL')  # When Server

DATABASE_URL = (url_data)

# user_pwd, user_names = users_info()

port_param = pd.read_csv('https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/Portafolio_parameters.csv',
    #r'C:\Users\20194851\Google Drive\Postdoc TUe\Project Serious Game\Dash_tests\EMGA_portfolio\apps\Portafolio_parameters.csv',
    header=0, squeeze=True)

port_param_num = port_param.replace({'High': 3 / 3, 'Medium': 2 / 3, 'Low': 1 / 3})

layout = html.Div([

    # ---------- SCORE BOARD ----------- #
    dbc.Container([
        dbc.Row(
            [
                dbc.Col([
                    tue_header.header(),
                ], width=12, lg=12, md=12, style={'backgroundColor': app.color_3}
                ),
            ]
        ),

        dbc.Row([

        ], style={'height': '3vw'}, justify="start"),

        dbc.Row(
            # Characteristics generation technologies
            [
                dbc.Col(
                    [

                        html.Div(
                            [

                                html.Div(
                                    [
                                        dbc.Card(
                                            [
                                                # html.H4("Thermic Plant", className="card-title")
                                                dbc.CardImg(
                                                    src="https://bioenergyinternational.com/app/uploads/sites/3/2018/11/ENGIE_Rotterdam.jpg",
                                                    top=True,
                                                    style={'height': '10vw'}),
                                                dbc.CardBody(
                                                    [
                                                        html.Div(
                                                            dcc.Checklist(
                                                                options=[
                                                                    {"label": "Thermic Plant", "value": '1'},
                                                                ],
                                                                labelStyle={'color': 'black', 'font-size': '1.2vw', },
                                                                inputStyle={"width": "2vw"},
                                                                id="checklist",

                                                            ),
                                                            id="checklist_div",
                                                            style={"margin": "1vw", },
                                                        ),

                                                        html.Div(
                                                            [

                                                                html.Div([
                                                                    dcc.Slider(
                                                                        id='slider_th',
                                                                        min=port_param.iloc[0][7] * 0.2,
                                                                        max=port_param.iloc[0][7],
                                                                        step=port_param.iloc[0][7] * 0.2,
                                                                        value=0.0,
                                                                        marks={
                                                                            2: {'label': str(
                                                                                port_param.iloc[0][7] * 0.2)},
                                                                            str(port_param.iloc[0][7]): {
                                                                                'label': str(port_param.iloc[0][7])}},
                                                                        updatemode='drag',
                                                                        disabled=True,

                                                                    ),
                                                                    html.Div(id='slider_th_container')
                                                                ], style={'font-size': '1.0vw', 'width': '100%',
                                                                          'display': 'inline-block'}),
                                                                html.Div(id='slider_th_container',
                                                                         style={'font-size': '1.0vw',
                                                                                'display': 'inline-block', }),

                                                            ], style={'width': '100%'}
                                                        ),

                                                        html.Div(
                                                            [
                                                                html.Div(
                                                                    [
                                                                        html.P('Capacity Factor ',
                                                                               style={'font-size': '1.0vw'}),
                                                                    ], style={'textAlign': 'left',
                                                                              'display': 'inline-block',
                                                                              'width': '2 vw'}
                                                                ),

                                                                html.Div(
                                                                    [
                                                                        html.P('{} '.format(port_param.iloc[0][1]),
                                                                               style={'textAlign': 'right',
                                                                                      'font-size': '1.0vw',
                                                                                      'width': '2 vw'
                                                                                      }),
                                                                    ],
                                                                    style={"margin": "1vw", 'display': 'inline-block',
                                                                           'textAlign': 'center', 'width': '2 vw'}
                                                                ),

                                                            ], style={'height': '2.0vw'}
                                                        ),

                                                        html.Div(
                                                            [
                                                                html.Div(
                                                                    [
                                                                        html.P('Dispatchability ',
                                                                               style={'font-size': '1.0vw'}),
                                                                    ], style={'textAlign': 'left',
                                                                              'display': 'inline-block',
                                                                              'width': '2 vw'}
                                                                ),

                                                                html.Div(
                                                                    [
                                                                        html.P('{} '.format(port_param.iloc[0][2]),
                                                                               style={'textAlign': 'right',
                                                                                      'font-size': '1.0vw',
                                                                                      'width': '2 vw'
                                                                                      }),
                                                                    ],
                                                                    style={"margin": "1vw", 'display': 'inline-block',
                                                                           'textAlign': 'center', 'width': '2 vw'}
                                                                ),

                                                            ], style={'height': '2.0vw'}
                                                        ),

                                                        html.Div(
                                                            [
                                                                html.Div(
                                                                    [
                                                                        html.P('Variability ',
                                                                               style={'font-size': '1.0vw'}),
                                                                    ], style={'textAlign': 'left',
                                                                              'display': 'inline-block',
                                                                              'width': '2 vw'}
                                                                ),

                                                                html.Div(
                                                                    [
                                                                        html.P('{} '.format(port_param.iloc[0][3]),
                                                                               style={'textAlign': 'right',
                                                                                      'font-size': '1.0vw',
                                                                                      'width': '2 vw'
                                                                                      }),
                                                                    ],
                                                                    style={"margin": "1vw", 'display': 'inline-block',
                                                                           'textAlign': 'center', 'width': '2 vw'}
                                                                ),

                                                            ], style={'height': '2.0vw'}
                                                        ),

                                                        html.Div(
                                                            [
                                                                html.Div(
                                                                    [
                                                                        html.P('Direct Emissions ',
                                                                               style={'font-size': '1.0vw'}),
                                                                    ],
                                                                    style={'textAlign': 'left',
                                                                           'display': 'inline-block',
                                                                           'width': '2 vw'}
                                                                ),

                                                                html.Div(
                                                                    [
                                                                        html.P('{} '.format(port_param.iloc[0][4]),
                                                                               style={'textAlign': 'right',
                                                                                      'font-size': '1.0vw',
                                                                                      'width': '2 vw'
                                                                                      }),
                                                                    ],
                                                                    style={"margin": "1vw", 'display': 'inline-block',
                                                                           'textAlign': 'center', 'width': '2 vw'}
                                                                ),

                                                            ], style={'height': '2.0vw'}
                                                        ),

                                                        html.Div(
                                                            [
                                                                html.Div(
                                                                    [
                                                                        html.P('Indirect Emissions ',
                                                                               style={'font-size': '1.0vw'}),
                                                                    ],
                                                                    style={'textAlign': 'left',
                                                                           'display': 'inline-block',
                                                                           'width': '2 vw'}
                                                                ),

                                                                html.Div(
                                                                    [
                                                                        html.P('{} '.format(port_param.iloc[0][5]),
                                                                               style={'textAlign': 'right',
                                                                                      'font-size': '1.0vw',
                                                                                      'width': '2 vw'
                                                                                      }),
                                                                    ],
                                                                    style={"margin": "1vw", 'display': 'inline-block',
                                                                           'textAlign': 'center', 'width': '2 vw'}
                                                                ),

                                                            ], style={'height': '2.0vw'}
                                                        ),

                                                        html.Div(
                                                            [
                                                                html.Div(
                                                                    [
                                                                        html.P('Construction Cost ',
                                                                               style={'font-size': '1.0vw'}),
                                                                    ],
                                                                    style={'textAlign': 'left',
                                                                           'display': 'inline-block',
                                                                           'width': '2 vw'}
                                                                ),

                                                                html.Div(
                                                                    [
                                                                        html.P('{} $/MW'.format(port_param.iloc[0][6]),
                                                                               style={'textAlign': 'right',
                                                                                      'font-size': '1.0vw',
                                                                                      'width': '2 vw'
                                                                                      }),
                                                                    ],
                                                                    style={"margin": "1vw", 'display': 'inline-block',
                                                                           'textAlign': 'center', 'width': '2 vw'}
                                                                ),

                                                            ], style={'height': '2.0vw'}
                                                        ),
                                                    ]
                                                ),
                                            ], style={'height': '100%', "width": "22vw", 'textAlign': 'center', },
                                        ),
                                    ]
                                ),

                            ], style={'textAlign': 'center',
                                      'display': 'inline-block', 'height': '100%'}
                        ),

                    ], width=3, lg=3, md=3, sm=3, style={'height': '100%', }
                ),

                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Card(
                                    [
                                        # html.H4("Thermic Plant", className="card-title")
                                        dbc.CardImg(
                                            src="https://etap.com/images/default-source/product/wind-turbine-generator/wind-turbine-generator-icon4c89d3450c286c028629ff0c005ae2384d86fc450c286c028629ff00005ae238.jpg?sfvrsn=afa3b87f_62",
                                            top=True,
                                            style={'height': '10vw'}),
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    dcc.Checklist(
                                                        options=[
                                                            {"label": "Wind Farm", "value": '2'},
                                                        ],
                                                        labelStyle={'color': 'black', 'font-size': '1.2vw', },
                                                        inputStyle={"width": "5vw"},
                                                        id="checklist2",

                                                    ),
                                                    id="checklist2_div",
                                                    style={"margin": "1vw", },
                                                ),

                                                html.Div(
                                                    [

                                                        html.Div([
                                                            dcc.Slider(
                                                                id='slider_wt',
                                                                min=port_param.iloc[1][7] * 0.1,
                                                                max=port_param.iloc[1][7],
                                                                step=port_param.iloc[1][7] * 0.1,
                                                                value=0.0,
                                                                marks={
                                                                    2: {'label': str(port_param.iloc[1][7] * 0.1)},
                                                                    str(port_param.iloc[1][7]): {
                                                                        'label': str(port_param.iloc[1][7])}},
                                                                updatemode='drag',
                                                                disabled=True,

                                                            ),
                                                            html.Div(id='slider_wt_container')
                                                        ], style={'font-size': '1.0vw', 'width': '100%',
                                                                  'display': 'inline-block'}),
                                                        html.Div(id='slider_wt_container', style={'font-size': '1.0vw',
                                                                                                  'display': 'inline-block', }),

                                                    ], style={'width': '100%'}
                                                ),

                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.P('Capacity Factor ',
                                                                       style={'font-size': '1.0vw'}),
                                                            ], style={'textAlign': 'left', 'display': 'inline-block',
                                                                      'width': '2 vw'}
                                                        ),

                                                        html.Div(
                                                            [
                                                                html.P('{} '.format(port_param.iloc[1][1]),
                                                                       style={'textAlign': 'right',
                                                                              'font-size': '1.0vw',
                                                                              'width': '2 vw'
                                                                              }),
                                                            ], style={"margin": "1vw", 'display': 'inline-block',
                                                                      'textAlign': 'center', 'width': '2 vw'}
                                                        ),

                                                    ], style={'height': '2.0vw'}
                                                ),

                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.P('Dispatchability ',
                                                                       style={'font-size': '1.0vw'}),
                                                            ], style={'textAlign': 'left', 'display': 'inline-block',
                                                                      'width': '2 vw'}
                                                        ),

                                                        html.Div(
                                                            [
                                                                html.P('{} '.format(port_param.iloc[1][2]),
                                                                       style={'textAlign': 'right',
                                                                              'font-size': '1.0vw',
                                                                              'width': '2 vw'
                                                                              }),
                                                            ], style={"margin": "1vw", 'display': 'inline-block',
                                                                      'textAlign': 'center', 'width': '2 vw'}
                                                        ),

                                                    ], style={'height': '2.0vw'}
                                                ),

                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.P('Variability ',
                                                                       style={'font-size': '1.0vw'}),
                                                            ], style={'textAlign': 'left', 'display': 'inline-block',
                                                                      'width': '2 vw'}
                                                        ),

                                                        html.Div(
                                                            [
                                                                html.P('{} '.format(port_param.iloc[1][3]),
                                                                       style={'textAlign': 'right',
                                                                              'font-size': '1.0vw',
                                                                              'width': '2 vw'
                                                                              }),
                                                            ], style={"margin": "1vw", 'display': 'inline-block',
                                                                      'textAlign': 'center', 'width': '2 vw'}
                                                        ),

                                                    ], style={'height': '2.0vw'}
                                                ),

                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.P('Direct Emissions ',
                                                                       style={'font-size': '1.0vw'}),
                                                            ],
                                                            style={'textAlign': 'left', 'display': 'inline-block',
                                                                   'width': '2 vw'}
                                                        ),

                                                        html.Div(
                                                            [
                                                                html.P('{} '.format(port_param.iloc[1][4]),
                                                                       style={'textAlign': 'right',
                                                                              'font-size': '1.0vw',
                                                                              'width': '2 vw'
                                                                              }),
                                                            ], style={"margin": "1vw", 'display': 'inline-block',
                                                                      'textAlign': 'center', 'width': '2 vw'}
                                                        ),

                                                    ], style={'height': '2.0vw'}
                                                ),

                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.P('Indirect Emissions ',
                                                                       style={'font-size': '1.0vw'}),
                                                            ],
                                                            style={'textAlign': 'left', 'display': 'inline-block',
                                                                   'width': '2 vw'}
                                                        ),

                                                        html.Div(
                                                            [
                                                                html.P('{} '.format(port_param.iloc[1][5]),
                                                                       style={'textAlign': 'right',
                                                                              'font-size': '1.0vw',
                                                                              'width': '2 vw'
                                                                              }),
                                                            ], style={"margin": "1vw", 'display': 'inline-block',
                                                                      'textAlign': 'center', 'width': '2 vw'}
                                                        ),

                                                    ], style={'height': '2.0vw'}
                                                ),

                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.P('Construction Cost ',
                                                                       style={'font-size': '1.0vw'}),
                                                            ],
                                                            style={'textAlign': 'left', 'display': 'inline-block',
                                                                   'width': '2 vw'}
                                                        ),

                                                        html.Div(
                                                            [
                                                                html.P('{} $/MW'.format(port_param.iloc[1][6]),
                                                                       style={'textAlign': 'right',
                                                                              'font-size': '1.0vw',
                                                                              'width': '2 vw'
                                                                              }),
                                                            ], style={"margin": "1vw", 'display': 'inline-block',
                                                                      'textAlign': 'center', 'width': '2 vw'}
                                                        ),

                                                    ], style={'height': '2.0vw'}
                                                ),
                                            ]
                                        ),
                                    ], style={'height': '100%', "width": "22vw", 'textAlign': 'center', },
                                ),
                            ]
                        ),

                    ], width=3, lg=3, md=3, sm=3, style={'height': '100%', }
                ),

                dbc.Col([
                    html.Div(
                        [
                            dbc.Card(
                                [
                                    # html.H4("Thermic Plant", className="card-title")
                                    dbc.CardImg(
                                        src="https://www.azocleantech.com/image.axd?src=%2fimages%2fArticle_Images%2fImageForArticle_980(1).jpg&ts=20191111052332&ri=750",
                                        top=True,
                                        style={'height': '10vw'}),
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                dcc.Checklist(
                                                    options=[
                                                        {"label": "Solar Farm", "value": '3'},
                                                    ],
                                                    labelStyle={'color': 'black', 'font-size': '1.2vw', },
                                                    inputStyle={"width": "5vw"},
                                                    id="checklist3",
                                                ),
                                                id="checklist3_div",
                                                style={"margin": "1vw", },
                                            ),

                                            html.Div(
                                                [

                                                    html.Div([
                                                        dcc.Slider(
                                                            id='slider_pv',
                                                            min=port_param.iloc[2][7] * 0.1,
                                                            max=port_param.iloc[2][7],
                                                            step=1.0,
                                                            value=0.0,
                                                            marks={
                                                                2: {'label': str(port_param.iloc[2][7] * 0.1)},
                                                                str(port_param.iloc[2][7]): {
                                                                    'label': str(port_param.iloc[2][7])}},
                                                            updatemode='drag',
                                                            disabled=True,

                                                        ),
                                                        html.Div(id='slider_pv_container')
                                                    ], style={'font-size': '1.0vw', 'width': '100%',
                                                              'display': 'inline-block'}),
                                                    html.Div(id='slider_pv_container',
                                                             style={'font-size': '1.0vw', 'display': 'inline-block', }),

                                                ], style={'width': '100%'}
                                            ),

                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.P('Capacity Factor ',
                                                                   style={'font-size': '1.0vw'}),
                                                        ],
                                                        style={'textAlign': 'left', 'display': 'inline-block',
                                                               'width': '2 vw'}
                                                    ),

                                                    html.Div(
                                                        [
                                                            html.P('{} '.format(port_param.iloc[2][1]),
                                                                   style={'textAlign': 'right',
                                                                          'font-size': '1.0vw',
                                                                          'width': '2 vw'
                                                                          }),
                                                        ], style={"margin": "1vw", 'display': 'inline-block',
                                                                  'textAlign': 'center', 'width': '2 vw'}
                                                    ),

                                                ], style={'height': '2.0vw'}
                                            ),

                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.P('Dispatchability ',
                                                                   style={'font-size': '1.0vw'}),
                                                        ],
                                                        style={'textAlign': 'left', 'display': 'inline-block',
                                                               'width': '2 vw'}
                                                    ),

                                                    html.Div(
                                                        [
                                                            html.P('{} '.format(port_param.iloc[2][2]),
                                                                   style={'textAlign': 'right',
                                                                          'font-size': '1.0vw',
                                                                          'width': '2 vw'
                                                                          }),
                                                        ], style={"margin": "1vw", 'display': 'inline-block',
                                                                  'textAlign': 'center', 'width': '2 vw'}
                                                    ),

                                                ], style={'height': '2.0vw'}
                                            ),

                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.P('Variability ',
                                                                   style={'font-size': '1.0vw'}),
                                                        ],
                                                        style={'textAlign': 'left', 'display': 'inline-block',
                                                               'width': '2 vw'}
                                                    ),

                                                    html.Div(
                                                        [
                                                            html.P('{} '.format(port_param.iloc[2][3]),
                                                                   style={'textAlign': 'right',
                                                                          'font-size': '1.0vw',
                                                                          'width': '2 vw'
                                                                          }),
                                                        ], style={"margin": "1vw", 'display': 'inline-block',
                                                                  'textAlign': 'center', 'width': '2 vw'}
                                                    ),

                                                ], style={'height': '2.0vw'}
                                            ),

                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.P('Direct Emissions ',
                                                                   style={'font-size': '1.0vw'}),
                                                        ],
                                                        style={'textAlign': 'left', 'display': 'inline-block',
                                                               'width': '2 vw'}
                                                    ),

                                                    html.Div(
                                                        [
                                                            html.P('{} '.format(port_param.iloc[2][4]),
                                                                   style={'textAlign': 'right',
                                                                          'font-size': '1.0vw',
                                                                          'width': '2 vw'
                                                                          }),
                                                        ], style={"margin": "1vw", 'display': 'inline-block',
                                                                  'textAlign': 'center', 'width': '2 vw'}
                                                    ),

                                                ], style={'height': '2.0vw'}
                                            ),

                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.P('Indirect Emissions ',
                                                                   style={'font-size': '1.0vw'}),
                                                        ],
                                                        style={'textAlign': 'left', 'display': 'inline-block',
                                                               'width': '2 vw'}
                                                    ),

                                                    html.Div(
                                                        [
                                                            html.P('{} '.format(port_param.iloc[2][5]),
                                                                   style={'textAlign': 'right',
                                                                          'font-size': '1.0vw',
                                                                          'width': '2 vw'
                                                                          }),
                                                        ], style={"margin": "1vw", 'display': 'inline-block',
                                                                  'textAlign': 'center', 'width': '2 vw'}
                                                    ),

                                                ], style={'height': '2.0vw'}
                                            ),

                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.P('Construction Cost ',
                                                                   style={'font-size': '1.0vw'}),
                                                        ],
                                                        style={'textAlign': 'left', 'display': 'inline-block',
                                                               'width': '2 vw'}
                                                    ),

                                                    html.Div(
                                                        [
                                                            html.P('{} $/MW'.format(port_param.iloc[2][6]),
                                                                   style={'textAlign': 'right',
                                                                          'font-size': '1.0vw',
                                                                          'width': '2 vw'
                                                                          }),
                                                        ], style={"margin": "1vw", 'display': 'inline-block',
                                                                  'textAlign': 'center', 'width': '2 vw'}
                                                    ),

                                                ], style={'height': '2.0vw'}
                                            ),
                                        ]
                                    ),
                                ], style={'height': '100%', "width": "22vw", 'textAlign': 'center', },
                            ),
                        ], style={"width": "100%", }
                    ),

                ], width=3, lg=3, md=3, sm=3, style={'height': '100%', }
                ),

                dbc.Col([
                    html.Div(
                        [
                            dbc.Card(
                                [
                                    # html.H4("Thermic Plant", className="card-title")
                                    dbc.CardImg(
                                        src="https://www.energy-pool.eu/wp-content/uploads/2019/01/batterie-1.jpg",
                                        top=True,
                                        style={'height': '10vw'}),
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                dcc.Checklist(
                                                    options=[
                                                        {"label": "Energy Storage", "value": 'ess'},
                                                    ],
                                                    labelStyle={'color': 'black', 'font-size': '1.2vw', },
                                                    inputStyle={"width": "5vw"},
                                                    id="checklist4",
                                                ),
                                                id="checklist4_div",
                                                style={"margin": "1vw", },
                                            ),

                                            html.Div(
                                                [

                                                    html.Div([
                                                        dcc.Slider(
                                                            id='slider_ess',
                                                            min=port_param.iloc[3][7] * 0.1,
                                                            max=port_param.iloc[3][7],
                                                            step=2.0,
                                                            value=0.0,
                                                            marks={
                                                                2: {'label': str(port_param.iloc[3][7] * 0.1)},
                                                                str(port_param.iloc[3][7]): {
                                                                    'label': str(port_param.iloc[3][7])}},
                                                            updatemode='drag',
                                                            disabled=True,

                                                        ),
                                                        html.Div(id='slider_ess_container')
                                                    ], style={'font-size': '1.0vw', 'width': '100%',
                                                              'display': 'inline-block'}),
                                                    html.Div(id='slider_ess_container',
                                                             style={'font-size': '1.0vw', 'display': 'inline-block', }),

                                                ], style={'width': '100%'}
                                            ),

                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.P('Capacity Factor ',
                                                                   style={'font-size': '1.0vw'}),
                                                        ],
                                                        style={'textAlign': 'left', 'display': 'inline-block',
                                                               'width': '2 vw'}
                                                    ),

                                                    html.Div(
                                                        [

                                                            html.P('{} '.format(port_param.iloc[3][1]),
                                                                   style={'textAlign': 'right',
                                                                          'font-size': '1.0vw',
                                                                          'width': '2 vw'
                                                                          }),

                                                        ], style={"margin": "1vw", 'display': 'inline-block',
                                                                  'textAlign': 'center', 'width': '2 vw'}
                                                    ),

                                                ], style={'height': '2.0vw'}
                                            ),

                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.P('Dispatchability ',
                                                                   style={'font-size': '1.0vw'}),
                                                        ],
                                                        style={'textAlign': 'left', 'display': 'inline-block',
                                                               'width': '2 vw'}
                                                    ),

                                                    html.Div(
                                                        [
                                                            html.P('{} '.format(port_param.iloc[3][2]),
                                                                   style={'textAlign': 'right',
                                                                          'font-size': '1.0vw',
                                                                          'width': '2 vw'
                                                                          }),
                                                        ], style={"margin": "1vw", 'display': 'inline-block',
                                                                  'textAlign': 'center', 'width': '2 vw'}
                                                    ),

                                                ], style={'height': '2.0vw'}
                                            ),

                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.P('Variability ',
                                                                   style={'font-size': '1.0vw'}),
                                                        ],
                                                        style={'textAlign': 'left', 'display': 'inline-block',
                                                               'width': '2 vw'}
                                                    ),

                                                    html.Div(
                                                        [
                                                            html.P('{} '.format(port_param.iloc[3][3]),
                                                                   style={'textAlign': 'right',
                                                                          'font-size': '1.0vw',
                                                                          'width': '2 vw'
                                                                          }),
                                                        ], style={"margin": "1vw", 'display': 'inline-block',
                                                                  'textAlign': 'center', 'width': '2 vw'}
                                                    ),

                                                ], style={'height': '2.0vw'}
                                            ),

                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.P('Direct Emissions ',
                                                                   style={'font-size': '1.0vw'}),
                                                        ],
                                                        style={'textAlign': 'left', 'display': 'inline-block',
                                                               'width': '2 vw'}
                                                    ),

                                                    html.Div(
                                                        [
                                                            html.P('{} '.format(port_param.iloc[3][4]),
                                                                   style={'textAlign': 'right',
                                                                          'font-size': '1.0vw',
                                                                          'width': '2 vw'
                                                                          }),
                                                        ], style={"margin": "1vw", 'display': 'inline-block',
                                                                  'textAlign': 'center', 'width': '2 vw'}
                                                    ),

                                                ], style={'height': '2.0vw'}
                                            ),

                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.P('Indirect Emissions ',
                                                                   style={'font-size': '1.0vw'}),
                                                        ],
                                                        style={'textAlign': 'left', 'display': 'inline-block',
                                                               'width': '2 vw'}
                                                    ),

                                                    html.Div(
                                                        [
                                                            html.P('{} '.format(port_param.iloc[3][5]),
                                                                   style={'textAlign': 'right',
                                                                          'font-size': '1.0vw',
                                                                          'width': '2 vw'
                                                                          }),
                                                        ], style={"margin": "1vw", 'display': 'inline-block',
                                                                  'textAlign': 'center', 'width': '2 vw'}
                                                    ),

                                                ], style={'height': '2.0vw'}
                                            ),

                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.P('Construction Cost ',
                                                                   style={'font-size': '1.0vw'}),
                                                        ],
                                                        style={'textAlign': 'left', 'display': 'inline-block',
                                                               'width': '2 vw'}
                                                    ),

                                                    html.Div(
                                                        [
                                                            html.P('{} $/MW'.format(port_param.iloc[3][6]),
                                                                   style={'textAlign': 'right',
                                                                          'font-size': '1.0vw',
                                                                          'width': '2 vw'
                                                                          }),
                                                        ], style={"margin": "1vw", 'display': 'inline-block',
                                                                  'textAlign': 'center', 'width': '2 vw'}
                                                    ),

                                                ], style={'height': '2.0vw'}
                                            ),
                                        ]
                                    ),
                                ], style={'height': '100%', "width": "22vw", 'textAlign': 'center', },
                            ),
                        ], style={"width": "100%", }
                    ),

                ], width=3, lg=3, md=3, sm=3, style={'height': '100%', }
                ),

            ], justify="around", align="center", style={'height': '32vw'},
        ),

        dbc.Row(
            # Spider plot
            [

                dbc.Col(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='spider', style={'width': '30vw', 'height': '20vw'}, )

                            ], style={'height': '20vw'}
                        ),

                    ], align="start", width=4, lg=4, md=4, sm=4, style={'height': '20vw'}
                ),

                dbc.Col(
                    [
                        html.Div(
                            [

                                html.Div(
                                    [
                                        daq.GraduatedBar(
                                            id='budget_total',
                                            color={"gradient": True,
                                                   "ranges": {app.color_5 : [0, 4], app.color_line: [4, 7], app.color_3: [7, 10]}},
                                            showCurrentValue=True,
                                            style={'color':"cyan", 'font-size': '1.0vw'},
                                            value=0,
                                            max=10,
                                            step=0.5,
                                            vertical=False,
                                            label={'label':'Investment Cost', 'style':{'color':'black', 'font-size': '1.0vw'}},
                                            labelPosition='top',
                                        ),

                                    ], style={'margin': '1vw', }
                                ),

                                html.Div(
                                    [
                                        html.P(id='tot_budget', style={'font-size': '1.0vw'}),
                                        html.P(id='current_budget', style={'font-size': '1.0vw'}),
                                        html.P(id='remaining_budget', style={'font-size': '1.0vw'}),

                                    ], style={'textAlign': 'left', 'width': '2 vw'}
                                ),

                                html.Div([
                                    html.Div([

                                        dcc.Link(
                                            html.Button("Continue", id="portf_button", className='disabled',
                                                        style={'font-size': '1.0vw', 'height': '2vw', 'width': '10vw',
                                                               'textAlign': 'center'},
                                                        disabled=True,
                                                        ),
                                            id='link_port', href='/Page_1'),
                                    ]),
                                ], style={'textAlign': 'left', 'height': '100%'}
                                ),

                            ], style={'margin': '1vw', 'height': '20vw', 'width': '20vw', 'textAlign': 'center',
                                      'display': 'inline-block', }
                        ),

                    ], align="center", width=4, lg=4, md=4, sm=4,
                    style={'height': '20vw', 'textAlign': 'center', }
                ),

                dbc.Col(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='pie_mix', style={'width': '30vw', 'height': '20vw', }
                                          )

                            ]
                        ),

                    ], align="start", width=4, lg=4, md=4, sm=4, style={'height': '20vw'}
                ),

            ], justify="around", align="center", style={'height': '25vw'},
        ),

    ], fluid=True),

], id='portfolio', style={'height': '100%', 'backgroundColor': app.color_1}
)



#################################################################
#################################################################


@app.callback(
    [Output("spider", "figure"),
     Output('budget_total', 'value'),
     Output('pie_mix', 'figure'),
     Output('tot_budget', 'children'),
     Output('current_budget', 'children'),
     Output('remaining_budget', 'children'),
     Output("portf_button", "disabled"),
     Output("portf_button", "className"),
     ],
    [
        # Input('portfolio', 'id'),
     Input('slider_ess', 'value'),
     Input('slider_pv', 'value'),
     Input('slider_wt', 'value'),
     Input('slider_th', 'value'),
     Input('slider_ess', 'disabled'),
     Input('slider_pv', 'disabled'),
     Input('slider_wt', 'disabled'),
     Input('slider_th', 'disabled'),
     Input('portf_button', 'n_clicks')],
)
def spider_fig(ess, pv, wt, th, ess_dis, pv_dis, wt_dis, th_dis, nclick):
    total = ess * (not ess_dis) + pv * (not pv_dis) + wt * (not wt_dis) + th * (not th_dis) + 0.00001
    budget = ess * (not ess_dis) * port_param_num.iloc[3][6] + pv * (not pv_dis) * port_param_num.iloc[2][6] \
             + wt * (not wt_dis) * port_param_num.iloc[1][6] + th * (not th_dis) * port_param_num.iloc[0][6]

    if total > 0:
        cap = ess * (not ess_dis) * port_param_num.iloc[3][1] * 1 / total + pv * (not pv_dis) * port_param_num.iloc[2][
            1] * 1 / total + wt * (not wt_dis) * port_param_num.iloc[1][1] * 1 / total + th * (not th_dis) * \
              port_param_num.iloc[0][1] * 1 / total
        disp = ess * (not ess_dis) * port_param_num.iloc[3][2] * 1 / total + pv * (not pv_dis) * port_param_num.iloc[2][
            2] * 0 / total + wt * (not wt_dis) * port_param_num.iloc[1][2] * 0 / total + th * (not th_dis) * \
               port_param_num.iloc[0][2] * 1 / total
        vari = ess * (not ess_dis) * port_param_num.iloc[3][3] * 1 / total + pv * (not pv_dis) * port_param_num.iloc[2][
            3] * 1 / total + wt * (not wt_dis) * port_param_num.iloc[1][3] * 1 / total + th * (not th_dis) * \
               port_param_num.iloc[0][3] * 1 / total
        emi1 = ess * (not ess_dis) * port_param_num.iloc[3][4] * 1 / total + pv * (not pv_dis) * port_param_num.iloc[2][
            4] * 1 / total + wt * (not wt_dis) * port_param_num.iloc[1][4] * 1 / total + th * (not th_dis) * \
               port_param_num.iloc[0][4] * 1 / total
        emi2 = ess * (not ess_dis) * port_param_num.iloc[3][5] * 1 / total + pv * (not pv_dis) * port_param_num.iloc[2][
            5] * 1 / total + wt * (not wt_dis) * port_param_num.iloc[1][5] * 1 / total + th * (not th_dis) * \
               port_param_num.iloc[0][5] * 1 / total

    else:
        cap = 0.0
        disp = 0.0
        vari = 0.0
        emi1 = 0.0
        emi2 = 0.0

    # dash.callback_context.response.set_cookie('flex_therm', str(port_param_num.iloc[0][9]), max_age=7200)
    # dash.callback_context.response.set_cookie('flex_storage', str(port_param_num.iloc[3][9]), max_age=7200)


    fig = go.Figure(data=go.Scatterpolar(
        r=[cap, disp, vari, emi1, emi2],
        theta=list(port_param.columns.values[1:6]),
        fill='toself',
        fillcolor='rgba' + str(cmap2(0.5 / total * (pv * (not pv_dis) + wt * (not wt_dis)) + 0.25 / total * (
                ess * (not ess_dis) + th * (not th_dis)))),
        opacity=0.7,
        marker=dict(
            cmin=0,
            cmax=1,
            size=12
        ),
        mode='markers',
        showlegend=False,
        marker_color=['rgba' + str((cmap(cap))), 'rgba' + str(cmap(disp)), 'rgba' + str((reversed_color_map(vari))),
                      'rgba' + str(reversed_color_map(emi1)), 'rgba' + str(reversed_color_map(emi2))],
    ),
    )

    fig.update_layout(
        title='Energy mix Characteristics',
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=True,
        autosize=False,

    )

    fig.update_yaxes(automargin=True)

    labels = list(port_param['Technology'])
    values = [th * (not th_dis) / total, wt * (not wt_dis) / total, pv * (not pv_dis) / total,
              ess * (not ess_dis) / total]

    pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3,
                                 marker_colors=night_colors)],
                    )

    pie.update_layout(
        title="Participation of Energy Sources",
    )

    if 0.98 <= budget / (0.6 * sum(port_param_num['Budg_tot'])) <= 1.0:
        dis_but = False
        but_sty = 'button-primary'
    else:
        dis_but = True
        but_sty = 'disabled'

    user_active = flask.request.cookies.get('custom-auth-session')

    if nclick:
        ############################################################
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("""INSERT INTO portfolio (player, thermic, wind, solar, storage, flexibility) VALUES (%s, %s, %s, %s, %s, %s)""",
        (user_active, th * (not th_dis), wt * (not wt_dis), pv * (not pv_dis), ess * (not ess_dis), disp))
        # cur.execute("""UPDATE portfolio SET thermic = (%s) WHERE Player = (%s);""", (th * (not th_dis), user_active,))
        # cur.execute("""UPDATE Leader_board SET Revenue = (%s) WHERE Player = (%s);""", (accumA, user_active,))
        # cur.execute("""UPDATE Leader_board SET Rate = (%s) WHERE Player = (%s);""", (rate, user_active,))

        conn.commit()

        cur.close()
        conn.close()
        ############################################################

    return fig, 10 * budget / (0.6 * sum(port_param_num['Budg_tot'])), pie, \
           'Total Budget $ {}'.format(math.floor(0.6 * sum(port_param_num['Budg_tot']) / 100) * 100), \
           'Current Investment $ {}'.format(budget), \
           'Remaining Budget $ {}'.format(math.floor(0.6 * sum(port_param_num['Budg_tot']) / 100) * 100 - budget), \
           dis_but, but_sty


@app.callback(
    Output('slider_ess_container', 'children'),
    [Input('slider_ess', 'value'),
     Input('slider_ess', 'disabled')])
def update_output(value, dis):
    return 'Energy Capacity {} '.format(value * float(not dis)) + 'MWh'


@app.callback(
    Output('slider_ess', 'disabled'),
    [Input('checklist4', 'value')]
)
def energy_cap(value):
    if value == ['ess']:
        return False
    else:
        return True


@app.callback(
    Output('slider_pv_container', 'children'),
    [Input('slider_pv', 'value'),
     Input('slider_pv', 'disabled')])
def update_output_pv(value, dis):
    return 'Power Capacity {} '.format(value * float(not dis)) + 'MW'


@app.callback(
    Output('slider_pv', 'disabled'),
    [Input('checklist3', 'value')]
)
def energy_cap_pv(value):
    if value == ['3']:
        return False
    else:
        return True


@app.callback(
    Output('slider_wt_container', 'children'),
    [Input('slider_wt', 'value'),
     Input('slider_wt', 'disabled')])
def update_output_wt(value, dis):
    return 'Power Capacity {} '.format(value * float(not dis)) + 'MW'


@app.callback(
    Output('slider_wt', 'disabled'),
    [Input('checklist2', 'value')]
)
def energy_cap_wt(value):
    if value == ['2']:
        return False
    else:
        return True


@app.callback(
    Output('slider_th_container', 'children'),
    [Input('slider_th', 'value'),
     Input('slider_th', 'disabled'),])
def update_output_th(value, dis):
    return 'Power Capacity {} '.format(value * float(not dis)) + 'MW'


@app.callback(
    Output('slider_th', 'disabled'),
    [Input('checklist', 'value')]
)
def energy_cap_th(value):
    if value == ['1']:
        return False
    else:
        return True

