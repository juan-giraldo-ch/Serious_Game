import dash
import dash_core_components as dcc
import dash_html_components as html
from app import app
import dash_bootstrap_components as dbc


# BUTT = html.Div([
#     dbc.Button("Primary", color="primary", className="mr-1"),
# ]
# ),

def submit_b():
    A = html.Div([
        html.Div([
            # dcc.Link(html.Button('3. Submit', id='button', disabled=True, style={'color':app.color_4})),
            dcc.Link(
                dbc.Button(size='md', color="success", outline=True, children='Submit', id='button', disabled=True,
                           style={'font-size': '1.2vw'}), href='/Page_2'),
            html.Div(id='Button_data',
                     children='',
                     # style={'color': app.color_8, 'font-size': '22px', 'textAlign': 'center'}
                     )
        ]),

        # dbc.Container(
        #     html.Div(
        #     BUTT,
        #     ),
        # ),

    ])
    return A


def next_day():
    B = html.Div([
        html.Div([
            dcc.Link(
                dbc.Button(size='lg', color="success", outline=True, children='Go to Next Day\'s Bid', id='nextD_b',
                           disabled=False, style={
                        # 'marginTop':'165%',
                        'marginBottom': '5%', 'font-size': '0.7vw', }),
                id='link_b2', href='/Page_1'),
        ], style={'textAlign': 'center', 'width': '100%', 'height': '100%'}),

    ])
    return B


def download_data():
    C = html.Div([
        html.Div([

            html.A(
                dcc.Loading(id='loading_1', color=app.color_3, type='default'),
                   id='link_downl',
                   download="",
                   href="",
                   target="_blank",
                   ),
        ]),  #

    ])
    return C

def download_irrad():
    I = html.Div([
        html.Div([

            html.A(dcc.Loading(id='loading_3', color=app.color_3, type='default'),
                   id='link_downl3',
                   download="",
                   href="",
                   target="_blank",
                   ),
        ]),  #

    ])
    return I

def port_info():
    G = html.Div([

        html.A(dcc.Loading(id='loading_4', color=app.color_3, type='default'),
               id='port_dwnl',
               download="",
               href="",
               target="_blank"
               ),
        ])

    return G


def download_DAP():
    D = html.Div([
        html.Div([

            html.A(dcc.Loading(id='loading_2', color=app.color_3, type='default'),
                   id='link_downl_dap',
                   download="",
                   href="",
                   target="_blank"
                   ),
        ]),  #

    ])
    return D


def return_page1():
    E = html.Div([
        html.Div(dcc.LogoutButton(logout_url='/logout',
                                  className='button-logout',
                                  style={'font-size': '0.8vw',
                                         'vertical-align': 'middle',
                                         'height': '2vw'}, ),
                 style={'display': 'inline-block', 'height': '5vw'},
                 id='logout_but2', ),
        # html.Div([
        #     dcc.Link(
        #         dbc.Button(size='lg', color="success", outline=True, children='Return', id='return_b',
        #                    disabled=False, style={
        #                 # 'marginTop':'165%',
        #                 'marginBottom': '5%', 'font-size': '0.7vw', }),
        #         id='link_b2', href='/logout'),
        # ], style={'textAlign': 'center', 'width': '100%', 'height': '100%'}),

    ])
    return E


def help_drag():
    F = html.Div([

            html.Div([
                html.Button([

                    html.Div([
                        html.Div([html.H2('Help ',
                                          style={'font-size': '1.0vw', 'color': app.color_4, 'display': 'inline-block',
                                                 'text-transform': 'capitalize'}),
                                  html.Img(
                                      src='https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/question.svg',
                                      style={'display': 'inline-block', 'height': '1.5vw', 'width': '1.5vw'},
                                      title='Help',
                                  ),
                                  ],
                                 style={'display': 'inline-block'}),

                    ],
                        style={'display': 'inline-block', 'height': '100%'}
                    ),

                ], id='your_button', style={'height': '3vw', 'border': 'none', 'background': 'none'}
                ),

            ], style={'display': 'inline-block', 'textAlign': 'left'}
            ),

        dbc.Modal(
            [
                dbc.ModalHeader("Guidelines"),
                dbc.ModalBody([
                    html.P(
                      dcc.Markdown(
                          "***Game Instructions***:"
                      )
                    ),

                    html.P(
                        dcc.Markdown(
                            "**1)** Download past wind speed records by clicking on the `Download Historical Wind Data` "
                            " button. Also, get the day-ahead prices from the `Download Day Ahead Prices` button."
                        ),
                    ),
                    html.P(
                        dcc.Markdown(
                            "**2)** Generate a .csv file containing your expected hourly energy bids. The file structure "
                            " must have 24 rows and 2 columns."
                        )
                    ),

                    html.P(
                        dcc.Markdown(
                            ">***Obs.*** The **FIRST** column represents the time periods, i.e., \{t0, t1, ..., t23\},"
                            "   while the **SECOND** column should contain the energy bid."
                        )
                    ),

                    html.P(
                        dcc.Markdown(
                            "**3)** Check the uploaded data file in the table."
                        )
                    ),

                    html.P(
                        dcc.Markdown(
                            "**4)** In case your data is OK, click on the `SUBMIT` button to "
                            " continue and check the day's revenue."
                        ),
                    ),

                    html.P(
                        dcc.Markdown(
                            "**5)** Four figures will be displayed where you can compare your"
                            " uploaded bid with the actual energy production, check hourly energy mismatches, "
                            " your revenue per hour, and the day accumulated revenue."
                        )
                    ),

                    html.P(
                        dcc.Markdown(
                            "**6)** After checking your revenue, you can continue to the next trading day "
                            "by clicking on the button `Go to Next Day's Bid`."
                        )
                    ),

                    html.P(
                        dcc.Markdown(
                            "**7)** You must repeat steps **1)**--**6)** for a predefined number of days (time horizon). "
                            " You can leave your current session anytime by logging out clicking on the `LOGOUT` button."
                            " Don't worry, your process **will not be lost**."
                        )
                    ),

                    html.P(
                        dcc.Markdown(
                            "**8)** Once you have completed the time horizon, you will not be able to make any other bid. "
                            " You can always re-enter using your username/password and review your current position in the Leaderboard."
                        )
                    ),

                    html.P(
                        dcc.Markdown(
                            "---"
                        )
                    ),

                    html.P(
                        dcc.Markdown(
                            "***Leaderboard***:"
                        )
                    ),

                    html.P(
                        dcc.Markdown(
                            "**1)** You can check the **leaderboard** by clicking on the `LEADERBOARD` button."
                        )
                    ),

                  html.P(
                      dcc.Markdown(
                          "**2)** The **leaderboard** displays your accumulated revenue, "
                          " the number of days you have played, and your `Rate`."
                      )
                  ),

                html.P(
                    dcc.Markdown(
                        "**3)** The `Rate` is the ratio between your `Accumulated Revenue`/`Played days`. "
                        " The `Rate` is the measurement for the game's ranking... "
                        "**So keep it as high as possible!!**"
                    )
                )


            ]

                ),
                dbc.ModalFooter(
                    html.Button("Let's Play!", id="close", className='button-primary',)
                ),
            ], id="modal", backdrop="static", scrollable=True, centered=True,
        ),

    ], style={'display': 'inline-block'})

    return F


