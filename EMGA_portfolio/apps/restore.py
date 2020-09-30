import dash
import dash_core_components as dcc
import dash_html_components as html
import os  # Importing OS functions
import dash_bootstrap_components as dbc
from apps import tue_header
from app import app
from dash.dependencies import Input, Output, State
import psycopg2
from dash.exceptions import PreventUpdate






if app.database_url == 'Local':
    url_data = os.popen("heroku config:get DATABASE_URL -a emga").read().strip()  # When local machine

if app.database_url == 'Server':
    url_data = os.environ.get('DATABASE_URL')  # When Server



DATABASE_URL = (url_data)

# user_pwd, user_names = users_info()

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
            [
                dbc.Col([
                    html.Div([

                    ]),

                ], width=4, lg=4, md=4, sm=4),

                dbc.Col([
                    html.Div([

                        html.P('Please type in your username and new password:', style={'font-size': '1.0vw'}),

                        html.Div(
                            [dcc.Input(id='us_name2', placeholder='Username', name='user_name', type='text',
                                       debounce=True,
                                       required=True, minLength=6,
                                       style={'borderWidth': '0.01vw'}),
                             dbc.Tooltip(
                                 "The username you registered.",
                                 target="us_name2", placement='right', style={'font-size': '0.7vw'}
                             ), ]),

                        html.Div(
                            [dcc.Input(id='email2', placeholder='E-mail', name='email', type='email',
                                       debounce=True,
                                       required=True,
                                       style={'borderWidth': '0.01vw'}),
                             dbc.Tooltip(
                                 "The E-mail address you registered.",
                                 target="us_name2", placement='right', style={'font-size': '0.7vw'}
                             ), ]),

                        html.Div([
                            dcc.Input(id='pswd2', placeholder='New password', name='pswd2', type='password',
                                      debounce=True,
                                      minLength=6,
                                      required=True,
                                      style={'borderWidth': '0.01vw'}),
                            dbc.Tooltip(
                                "New password must have at least 6 characters.",
                                target="pswd2", placement='right', style={'font-size': '0.7vw'},
                            ),
                        ]),

                        html.Br(),

                        html.Button('Register', id='reg3', type='submit',
                                    style={'font-size': '1.0vw', 'height': '2vw'}, disabled=True, className='disabled'),

                        dbc.Modal(
                            [
                                dbc.ModalHeader("", id='header_regis3'),
                                dbc.ModalBody(
                                    "", id='body_regis3'
                                ),
                                dbc.ModalFooter(
                                    html.A(html.Button(
                                        "Got it", id="close-backdrop3", className='button-primary'
                                    ), id='link4'),

                                ),
                            ],
                            id="modal-backdrop3", backdrop="static"
                        ),
                    ])
                ], width=4, lg=4, md=4, sm=4, style={'textAlign': 'center'}),

                dbc.Col([

                    html.Div([

                    ]),

                ], width=4, lg=4, md=4, sm=4),

            ], style={'height': '25vw'}, justify="center", align="center",
        ),


    ], fluid=True),

], id='restore', style={'height': '100%', 'backgroundColor': app.color_1}
)

#################################################################
#################################################################

@app.callback(
    [Output("reg3", "disabled"),
     Output("reg3", "className"), ],
    [Input('us_name2', 'value'),
     Input('pswd2', 'value'),
     Input('email2', 'value'),],
    [State("reg3", "n_clicks"), ]
)
def toggle_left(usname, pswd, email, n_left):
    if usname and pswd and email:
        if len(usname) >= 6 and len(pswd) >= 6:
            return False, 'button-primary'

    return True, 'disabled'


@app.callback(
    [Output("modal-backdrop3", "is_open"),
     Output('body_regis3', 'children'),
     Output("link4", "href"),],
    [Input("reg3", "n_clicks"),
     Input('us_name2', 'value'),
     Input('pswd2', 'value'),
     Input('email2', 'value'),
     Input("close-backdrop3", "n_clicks"), ],
    [State("modal-backdrop3", "is_open")],
)
def mensj_regist(n1, usname, pswd, email, n2, is_open):
    link = ''
    if n1:

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        cur = conn.cursor()

        cur.execute("""SELECT username, password FROM user_info WHERE username = (%s) AND email = (%s)""", (usname, email))
        # cur.execute("SELECT username, password, email FROM User_info;")
        players = cur.fetchall()


        if len(players) == 0:
            body = 'Please provide a valid Username/Email combination'

            link = """/restore"""

            cur.close()
            conn.close()

            return not is_open, body, link

        else:

            cur.execute(
                """UPDATE user_info SET password = crypt(%s, gen_salt('bf')) WHERE username = (%s);""", (pswd, usname))

            conn.commit()

            body = 'New password has been successfully updated'

            link = '\login'

            cur.close()
            conn.close()

            return not is_open, body, link

        # return not is_open, '', ''

    return is_open, '', ''