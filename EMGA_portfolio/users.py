import psycopg2
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import flask
import dash
# from users import users_info
import dash_bootstrap_components as dbc
import os  # Importing OS functions
import subprocess
from app import app



def users_info():

    if app.database_url == 'Local':

        url_data = os.popen("heroku config:get DATABASE_URL -a emga").read().strip() #When local machine

    if app.database_url == 'Server':
        url_data = os.environ.get('DATABASE_URL')   # When Server


    DATABASE_URL = (url_data)


    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    cur = conn.cursor()


    cur.execute("SELECT username, password FROM User_info;")
    players = cur.fetchall()

    #print(players)

    cur.close()
    conn.close()



    user_pwd = {players[i][0]: players[i][1] for i in range(len(players))}

    user_names = {'dash': 'User1, welcome to the crypto indicators dashboard',
                  'dash1': 'User1, welcome to the crypto indicators dashboard',
                  }



    return user_pwd, user_names


def new_user():
    collapses = html.Div(
        [

            dcc.RadioItems(
                options=[
                    {'label': ' First time playing?  ', 'value': 1},
                    {'label': ' Forgotten credentials?  ', 'value': 2},

                ], id="regist", style={'color': app.color_3},
                labelStyle={'display': 'inline-block'}
            ),
            # html.Button('New User?', id="regist", type='submit', className='button-primary',
            #             style={'font-size': '0.5vw', 'height': '1vw'}),
            # dbc.Button(
            #     "Register", color="info", outline=True,  className="mr-1"
            # ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Collapse(
                            dbc.Card([], body=True),
                            id="left-collapse",
                        )
                    ),
                ],
                # className="mt-3",
            ),

            dbc.Modal(
                [
                    dbc.ModalHeader("", id='header_regis'),
                    dbc.ModalBody(
                        "", id='body_regis'
                    ),
                    dbc.ModalFooter(
                        html.A(html.Button(
                            "Got it", id="close-backdrop", className='button-primary'
                        ), href="\login"),

                    ),
                ],
                id="modal-backdrop", backdrop="static"
            ),

            dbc.Modal(
                [
                    dbc.ModalHeader("", id='header_regis2'),
                    dbc.ModalBody(
                        "", id='body_regis2'
                    ),
                    dbc.ModalFooter(
                        html.A(html.Button(
                            "Got it", id="close-backdrop2", className='button-primary'
                        ), href="\login"),

                    ),
                ],
                id="modal-backdrop2", backdrop="static"
            ),

        ]
    )

    return collapses

#
# def forg_pass():
#     A = html.Div(
#         [
#
#             dcc.RadioItems(
#                 options=[
#                     {'label': 'Forgotten credentials?', 'value': '1'},
#                 ], id="forg_pass", labelStyle={'display': 'inline-block'}, style={'color': app.color_3}
#             ),
#
#
#             # dbc.Row(
#             #     [
#             #         dbc.Col(
#             #             dbc.Collapse(
#             #                 dbc.Card([], body=True),
#             #                 id="left-collapse",
#             #             )
#             #         ),
#             #     ],
#             #     # className="mt-3",
#             # ),
#             #
#             # dbc.Modal(
#             #     [
#             #         dbc.ModalHeader("", id='header_regis'),
#             #         dbc.ModalBody(
#             #             "", id='body_regis'
#             #         ),
#             #         dbc.ModalFooter(
#             #             html.A(html.Button(
#             #                 "Got it", id="close-backdrop", className='button-primary'
#             #             ), href="\login"),
#             #
#             #         ),
#             #     ],
#             #     id="modal-backdrop", backdrop="static"
#             # ),
#
#         ]
#     )
#     return A
