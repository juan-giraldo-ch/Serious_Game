import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
import plotly.graph_objs as go
from apps import tue_header, page_1
import flask
from users import users_info
import time
import os  # Importing OS functions
import psycopg2

_app_route = '/Page_1'

if app.database_url == 'Local':
    url_data = os.popen("heroku config:get DATABASE_URL -a emga").read().strip()  # When local machine

if app.database_url == 'Server':
    url_data = os.environ.get('DATABASE_URL')  # When Server



DATABASE_URL = (url_data)


# Create a login route
@app.server.route('/login', methods=['POST'])
def route_login():
    user_pwd, user_names = users_info()

    data = flask.request.form
    username = data.get('username')
    password = data.get('password')

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    cur = conn.cursor()

    cur.execute("SELECT username, password FROM User_info WHERE username = (%s) AND password = crypt(%s, password);", (username, password)) # crypt(%s, gen_salt('bf'))
    players = cur.fetchall()

    #print(players)

    cur.close()
    conn.close()

    if len(players) == 0:
    #if username not in user_pwd.keys() or user_pwd[username] != password:
        return flask.redirect('/login')
    else:
        #############################################################

        session_cookie = username

        user_active = session_cookie

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        cur = conn.cursor()

        cur.execute("SELECT days FROM Leader_board WHERE Player = (%s);", (user_active,))
        # print(players)
        days = cur.fetchone()
        cur.close()
        conn.close()

        # if len(days):
        #print('OK')

        if days:
            day = days[0]
            #print(day)
            #print(len(app.WF_real_power) / 96)

            if day >= len(app.WF_real_power) / 96:
                rep = flask.redirect('/Page_end')

                rep.set_cookie('custom-auth-session', username, max_age=7200)  # expires in 2 hours

                return rep


            # Return a redirect with
            rep = flask.redirect(_app_route)

            # Here we just store the given username in a cookie.
            # Actual session cookies should be signed or use a JWT token.

            rep.set_cookie('custom-auth-session', username, max_age=7200)  # expires in 2 hours

            return rep
        #############################################################

        elif not days:
            rep = flask.redirect('/portfolio')
            rep.set_cookie('custom-auth-session', username, max_age=7200)  # expires in 2 hours

            return rep

        # Return a redirect with
        rep = flask.redirect(_app_route)

        # Here we just store the given username in a cookie.
        # Actual session cookies should be signed or use a JWT token.

        rep.set_cookie('custom-auth-session', username, max_age=7200)  # expires in 2 hours

        return rep



# create a logout route
@app.server.route('/logout', methods=['POST'])
def route_logout():
    # Redirect back to the index and remove the session cookie.
    rep = flask.redirect('/login')
    rep.set_cookie('custom-auth-session', '', expires=0)
    rep.set_cookie('accum_val', '', expires=0)
    rep.set_cookie('accum_1', '', expires=0)
    rep.set_cookie('bar_acum', '', expires=0)
    rep.set_cookie('b2', '', expires=0)
    rep.set_cookie('b2p', '', expires=0)
    rep.set_cookie('wf_power', '', expires=0)
    rep.set_cookie('ddf', '', expires=0)

    return rep


###########################################################


########### Set up the layout
layout = html.Div([

    tue_header.header(),

    html.Div(id='custom-auth-frame'),
    html.Div(
        html.Div(
            id='custom-auth-frame-1',
            style={
                'textAlign': 'right',
                "background": app.color_3,
            },
        ),
    )

    # html.Form([
    #     dcc.Input(id='age_b', value='Age', type='number'),
    #     html.Button('Age', id='age', type='submit')
    # ], action='', method='get'),

], id='login', style={'backgroundColor': app.color_1},
)
