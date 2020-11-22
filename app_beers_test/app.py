import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


import flask

from users import users_info






########### Define your variables
beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 4.3]
color1='lightblue'
color2='darkgreen'
mytitle='Beer Comparison'
tabtitle='beer!'
myheading='Flying Dog Beers'
label1='IBU'
label2='ABV'
githublink='https://github.com/austinlasseter/flying-dog-beers'
sourceurl='https://www.flyingdog.com/beers/'

########### Set up the chart
bitterness = go.Bar(
    x=beers,
    y=ibu_values,
    name=label1,
    marker={'color':color1}
)
alcohol = go.Bar(
    x=beers,
    y=abv_values,
    name=label2,
    marker={'color':color2}
)

beer_data = [bitterness, alcohol]
beer_layout = go.Layout(
    barmode='group',
    title = mytitle
)

#beer_fig = go.Figure(data=beer_data, layout=beer_layout)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

##########################################################
##########################################################
user_pwd, user_names = users_info()

_app_route = '/'

# Create a login route
@app.server.route('/login', methods=['POST'])
def route_login():
    data = flask.request.form
    username = data.get('username')
    password = data.get('password')

    if username not in user_pwd.keys() or  user_pwd[username] != password:
        return flask.redirect('/login')
    else:

        # Return a redirect with
        rep = flask.redirect(_app_route)

        # Here we just store the given username in a cookie.
        # Actual session cookies should be signed or use a JWT token.
        rep.set_cookie('custom-auth-session', username)
        return rep


# Simple dash component login form.
login_form = html.Div([
    html.Form([
        dcc.Input(placeholder='username', name='username', type='text'),
        dcc.Input(placeholder='password', name='password', type='password'),
        html.Button('Login', type='submit')
    ], action='/login', method='post')
])



# create a logout route
@app.server.route('/logout', methods=['POST'])
def route_logout():
    # Redirect back to the index and remove the session cookie.
    rep = flask.redirect('/login')
    rep.set_cookie('custom-auth-session', '', expires=0)
    return rep
    
    



###########################################################



########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    
    #login_form,
    
    html.Div(id='custom-auth-frame'),
    html.Div(id='custom-auth-frame-1',
           style={
                  'textAlign': 'right',
                  "background": "black",
           }
           ),
    
    dcc.Graph(
        id='flyingdog',
        #figure=beer_fig
    ),
    
    html.Form([
        dcc.Input(id = 'age_b', value = 'Age', type='number'),
        html.Button('Age', id = 'age', type='submit')
    ], action='', method='get'),
    
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A('Data Source', href=sourceurl),
    ]
)


@app.callback([Output('flyingdog', 'figure'),
               Output('custom-auth-frame-1', 'children')],
              [Input('custom-auth-frame', 'children'),
               Input('age', 'n_clicks'),
               Input('age_b','value')])
def render_content(data, nc, val):
    session_cookie = flask.request.cookies.get('custom-auth-session')
    

    if not session_cookie:
        # If there's no cookie we need to login.
        return go.Figure(data=[]), login_form#html.Div(html.H2("Charts will be displayed here after user's authentication."),
                  #       style={'textAlign': 'center',
                   #             'color': 'red'})
                                
    else:
    
        logout_output = html.Div(children=[html.Div(html.H3('Hello {} !'.format(user_names[session_cookie])),
                                            style={'display': 'inline-block'}),
                                   html.Div(dcc.LogoutButton(logout_url='/logout'),
                                            style={'display': 'inline-block'})],
                         style={
                             'color': 'green',
                             'height': '50px'
                         }
                         )
        if nc is not None:
            with open('result.csv', 'a+') as f:
                print(session_cookie)
                f.write('{},'.format(session_cookie) + '{} \n'.format(val))
            f.close()

        return go.Figure(data=beer_data, layout=beer_layout), logout_output
        


if __name__ == '__main__':
    app.run_server(debug=True)
