# coding=utf-8


# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import flask
import dash
# from users import users_info
import dash_bootstrap_components as dbc
from users import users_info, new_user
import psycopg2
from app import app
from apps import page_1, page_2, login, page_end, buttons, forgot_passw, restore, portfolio
import os  # Importing OS functions


if app.database_url == 'Local':
    url_data = os.popen("heroku config:get DATABASE_URL -a emga").read().strip()  # When local machine

if app.database_url == 'Server':
    url_data = os.environ.get('DATABASE_URL')  # When Server


DATABASE_URL = (url_data)

users_info()
server = app.server

# Simple dash component login form.
login_form = html.Div([

    dbc.Container([
        html.Div([
            dbc.Row(
                [
                    dbc.Col([
                        html.Div([
                            html.Img(
                                src="https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/icon_2.svg",
                                style={
                                    'height': '15%',
                                    'width': '15%',
                                    # 'float': 'right',
                                    # 'position': 'relative',
                                    'margin-top': '5%',
                                },
                            ),
                        ], style={'textAlign': 'center'}),
                    ]),
                ]),

            dbc.Row(
                [
                    dbc.Col(
                        html.Div([
                            html.Form([
                                dcc.Input(placeholder='username', name='username', type='text',
                                          style={'borderWidth': '0.1vw'}),
                                dcc.Input(placeholder='password', name='password', type='password',
                                          style={'borderWidth': '0.1vw'}),
                                # dbc.Button('Login', size="lg", outline=True, color="success", className="mr-1", style={'color': app.color_4, 'borderColor': app.color_4}),
                                html.Button('Login', type='submit', className='button-primary',
                                            style={'font-size': '1.0vw', 'height': '2vw'})
                            ], action='/login', method='post', style={'marginTop': '2vw',
                                                                      'textAlign': 'center'})
                        ], style={'backgroundColor': app.color_1, 'textAlign': 'center', 'font-size': '1.0vw'}
                        ),
                        width=12, lg=12, md=12, sm=12)
                ], justify="center",
            ),

            html.Br(),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div([

                                new_user(),
                            ], style={'backgroundColor': app.color_1, 'textAlign': 'center', 'font-size': '1.0vw',
                                      'display': 'inline-block'}
                            ),
                        ], width=12, lg=12, md=12, sm=12
                    ),

                    # dbc.Col([
                    #     html.Div([
                    #
                    #         forg_pass(),
                    #     ], style={'backgroundColor': app.color_1, 'textAlign': 'left', 'font-size': '1.0vw',
                    #               'display': 'inline-block'}
                    #     ),
                    # ],width=6, lg=6, md=6, sm=6
                    # ),
                ], justify="center",
            )

        ], style={'height': '50vw', 'textAlign': 'center', 'vertical-align': 'bottom'}),
    ], fluid=True),

], style={'backgroundColor': app.color_1}
),

#############################################################
#############################################################

#  Layouts

# Favicon https://www.favicon.cc/ (icon in tab)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),

])


################################################################################
################################################################################
################################################################################


# --------------------------------------------------------------------

##################### - CALLBACKS - ############################


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/login':
        return login.layout
    # if pathname == '/Page_1':
    #     return page_1.layout
    if pathname == '/Page_2':
        session_cookie = flask.request.cookies.get('custom-auth-session')
        if not session_cookie:
            return login.layout
        else:
            user_active = session_cookie

            conn = psycopg2.connect(DATABASE_URL, sslmode='require')

            cur = conn.cursor()

            cur.execute("SELECT days FROM Leader_board WHERE Player = (%s);", (user_active,))
            # print(players)
            days = cur.fetchone()
            cur.close()
            conn.close()

            # if len(days):
            # print('OK')

            day = days[0]
            # print(day)
            # print(len(app.WF_real_power) / 96)

            if day >= len(app.WF_real_power) / 96:
                return page_end.layout

            return page_2.layout

    if pathname == '/portfolio':
        session_cookie = flask.request.cookies.get('custom-auth-session')
        if not session_cookie:
            return login.layout
        else:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')

            cur = conn.cursor()

            cur.execute("SELECT thermic FROM portfolio WHERE player = (%s);", (session_cookie,))
            # print(players)
            id = cur.fetchone()
            cur.close()
            conn.close()

            # if len(days):
            # print(id[0])

            # day = days[0]
            if not id:
                return portfolio.layout
            else:
                return login.layout

    if pathname == '/Page_end':
        session_cookie = flask.request.cookies.get('custom-auth-session')

        if not session_cookie:
            return login.layout

        else:

            conn = psycopg2.connect(DATABASE_URL, sslmode='require')

            cur = conn.cursor()

            cur.execute("SELECT days FROM Leader_board WHERE Player = (%s);", (session_cookie,))
            # print(players)
            days = cur.fetchone()
            cur.close()
            conn.close()

            # if len(days):
            # print('OK')

            day = days[0]
            if day >= app.play_days:#len(app.play_days) / 96:
                return page_end.layout
            else:
                return login.layout

    if pathname == '/restore':
        return restore.layout
    else:
        return login.layout




#################################################
@app.callback(Output('custom-auth-frame-1', 'children'),
              [Input('custom-auth-frame', 'children'),
               # Input('age', 'n_clicks'),
               # Input('age_b', 'value')
               ])
def render_content(data):
    session_cookie = flask.request.cookies.get('custom-auth-session')

    if not session_cookie:
        # If there's no cookie we need to login.
        dash.callback_context.response.set_cookie('accum_val', '0')
        dash.callback_context.response.set_cookie('accum_1', '0')
        dash.callback_context.response.set_cookie('bar_acum', '0')
        dash.callback_context.response.set_cookie('b2', '0')
        dash.callback_context.response.set_cookie('b2p', '0')
        dash.callback_context.response.set_cookie('exp_accum', '0')
        dash.callback_context.response.set_cookie('accufig', '0')
        dash.callback_context.response.set_cookie('lin_exp_accum', '0')
        dash.callback_context.response.set_cookie('rate_accum', '0')
        dash.callback_context.response.set_cookie('data_c', '0')
        dash.callback_context.response.set_cookie('dff', '0')

        return login_form  # html.Div(html.H2("Charts will be displayed here after user's authentication."),
        #       style={'textAlign': 'center',
        #             'color': 'red'})

    else:

        user_active = flask.request.cookies.get('custom-auth-session')
        b2 = (flask.request.cookies.get('b2'))
        accum = float(flask.request.cookies.get('accum_val'))

        # user_pos = app.lead_board[app.lead_board['index'] == user_active].index
        #
        if accum == 0:

            conn = psycopg2.connect(DATABASE_URL, sslmode='require')

            cur = conn.cursor()

            cur.execute("SELECT Player FROM Leader_board WHERE Player = (%s);", (user_active,))
            players = cur.fetchall()
            # print(players)
            day = b2
            if len(players):
                print('OK')
            else:
                # print('NOT')
                cur.execute("""INSERT INTO Leader_board (Player, Days, Revenue, Rate) VALUES (%s, %s, %s, %s)""",
                            (user_active, day, 0, 0,))

            conn.commit()

            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute("SELECT Revenue FROM Leader_board WHERE Player = (%s);", (user_active,))
            accum = cur.fetchone()
            accum = accum[0]
            conn.close()
            cur.close()

            dash.callback_context.response.set_cookie('accum_val', str(accum), max_age=7200)
        #
        if b2 == 0:

            cur.execute("SELECT days FROM Leader_board WHERE Player = (%s);", (user_active,))
            # print(players)
            days = cur.fetchone()

            if len(days):
                # print('OK')
                day = days[0]
                # print(days[0])
                dash.callback_context.response.set_cookie('b2', str(day), max_age=7200)
                dash.callback_context.response.set_cookie('b2p', str(day), max_age=7200)
                b2 = int(day)
                cur.close()
                conn.close()

        logout_output = dbc.Container([
            dbc.Row([

                dbc.Col(
                    [
                        html.Div([

                            buttons.help_drag(),
                        ], style={'display': 'inline-block', 'textAlign': 'left', 'margin': 'auto'}),

                    ], width=2, lg=2, md=2, sm=2, align='center'
                ),

                dbc.Col(
                    [

                    ], width=3, lg=3, md=3, sm=3
                ),

                dbc.Col(
                    [

                        html.Div(children=[html.Div(html.H6('Welcome {}! '.format(session_cookie),
                                                            style={'font-size': '1.4vw', 'color': app.color_4}),
                                                    style={'display': 'inline-block'}),
                                           ],
                                 style={'height': '3vw'}
                                 ),

                    ], width=4, lg=4, md=4, sm=4, ),
                dbc.Col(
                    [
                        html.Div(dcc.LogoutButton(logout_url='/logout',
                                                  className='button-logout',
                                                  style={'font-size': '0.8vw',
                                                         'height': '3vw'}, ),
                                 style={'height': '3vw', 'display': 'inline-block'},
                                 id='logout_but', ),
                    ]
                    , width=3, lg=3, md=3, sm=3)
            ], style={'backgroundColor': app.color_6, }, justify="center", ),

            dbc.Row([
                dbc.Col(
                    [
                        page_1.layout,
                    ],  # width=12, lg=12, md=12, sm=12
                ),
            ]),
        ], fluid=True),

        return logout_output


@app.callback(Output('href', 'children'),
              [Input('Submit', 'n_clicks'),
               ])
def render_content(data):
    session_cookie = flask.request.cookies.get('custom-auth-session')


#######################################################################

@app.callback(
    [Output("left-collapse", "is_open"),
     Output("left-collapse", "children")],
    [Input("regist", "value"), ],
    [State("left-collapse", "is_open")],
)
def toggle_left(n_left, is_open):
    if n_left == 1:
        regist = html.Div([

            html.Br(),

            html.P('Please fill in the following form:'),

            html.Div([
                dcc.Input(id='email', placeholder='E-mail', name='email', type='email', debounce=True,
                          required=True,
                          style={'borderWidth': '0.01vw'}),
            ]),

            html.Div([dcc.Input(id='us_name', placeholder='Username', name='user_name', type='text', debounce=True,
                                required=True, minLength=6,
                                style={'borderWidth': '0.01vw'}),
                      dbc.Tooltip(
                          "Username must have at least 6 characters.",
                          target="us_name", placement='right', style={'font-size': '0.7vw'}
                      ), ]),

            html.Div([
                dcc.Input(id='pswd', placeholder='Password', name='last_name', type='password', debounce=True,
                          minLength=6,
                          required=True,
                          style={'borderWidth': '0.01vw'}),
                dbc.Tooltip(
                    "Password must have at least 6 characters.",
                    target="pswd", placement='right', style={'font-size': '0.7vw'},
                ),
            ]),

            html.Br(),

            html.Button('Register', id='reg', type='submit',
                        style={'font-size': '1.0vw', 'height': '2vw'}, disabled=True, className='disabled')
            # ], method='post', style={'marginTop': '2%',
            #                          'textAlign': 'center'})  #,action='/login'

        ]
        ),
        return True, regist

    if n_left == 2:
        regist = html.Div([

            html.Br(),

            html.P('Provide your registered E-mail'),

            html.Div([
                dcc.Input(id='email2', placeholder='E-mail', name='email', type='email', debounce=True,
                          required=True,
                          style={'borderWidth': '0.01vw'}),
            ]),

            html.Br(),

            html.Button('Send E-mail', id='reg2', type='submit',
                        style={'font-size': '1.0vw', 'height': '2vw'}, disabled=True, className='disabled'),
            # ], method='post', style={'marginTop': '2%',
            #                          'textAlign': 'center'})  #,action='/login'

        ]
        )

        return True, regist
    return is_open, ''


@app.callback(
    [Output("reg", "disabled"),
     Output("reg", "className"), ],
    [Input('email', 'value'),
     Input('us_name', 'value'),
     Input('pswd', 'value'), ],
    [State("reg", "n_clicks"), ]
)
def toggle_left(email, usname, pswd, n_left):
    if usname and pswd and email:
        if len(usname) >= 6 and len(pswd) >= 6:
            return False, 'button-primary'

    return True, 'disabled'


@app.callback(
    [Output("reg2", "disabled"),
     Output("reg2", "className"), ],
    [Input('email2', 'value'), ],
    [State("reg2", "n_clicks"), ]
)
def toggle_left(email, n_left):
    if email:
        return False, 'button-primary'

    return True, 'disabled'


@app.callback(
    [Output("modal-backdrop", "is_open"),
     Output('body_regis', 'children')],
    [Input("reg", "n_clicks"),
     Input('email', 'value'),
     Input('us_name', 'value'),
     Input('pswd', 'value'),
     Input("close-backdrop", "n_clicks"), ],
    [State("modal-backdrop", "is_open")],
)
def mensj_regist(n1, email, usname, pswd, n2, is_open):
    if n1 or n2:

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        cur = conn.cursor()

        cur.execute("""SELECT * FROM user_info WHERE username = (%s) OR email = (%s)""", (usname, email,))
        # cur.execute("SELECT username, password, email FROM User_info;")
        players = cur.fetchall()

        if len(players) == 0:
            body = 'You have successfully registered'
            cur.execute(
                """INSERT INTO user_info (email, Username, Password) VALUES (%s, %s,  crypt(%s, gen_salt('bf')))""",
                (email, usname, pswd,))

            conn.commit()
        else:
            body = 'User and/or email already in use'

        cur.close()
        conn.close()

        return not is_open, body

    return is_open, ''


@app.callback(
    [Output("modal-backdrop2", "is_open"),
     Output('body_regis2', 'children')],
    [Input("reg2", "n_clicks"),
     Input('email2', 'value'),
     Input("close-backdrop2", "n_clicks"), ],
    [State("modal-backdrop2", "is_open")],
)
def mensj_regist(n1, email, n2, is_open):
    if n1 or n2:

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        cur = conn.cursor()

        cur.execute("""SELECT username FROM user_info WHERE email = (%s)""", (email,))
        # cur.execute("SELECT username, password, email FROM User_info;")
        players = cur.fetchall()

        cur.close()
        conn.close()


        if len(players) == 0:
            body = 'Provided E-mail is not in use'

        else:
            if not n2:
                forgot_passw.send_email(players,email)

            body = 'An E-mail has been sent to the provided address'

        return not is_open, body

    return is_open, ''


#######################################################################

if __name__ == '__main__':
    app.run_server(debug=True)
