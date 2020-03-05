import dash
import dash_core_components as dcc
import dash_html_components as html
from app import app


def submit_b():
    A = html.Div([
        html.Div([
            dcc.Link(html.Button('3. Submit', id='button', disabled=True, style={'color':app.color_4,'marginLeft': '38%',
                                                                              'marginTop':'180%'})),
            html.Div(id='Button_data',
                     children='',
                     style={'color': app.color_8, 'font-size': '22px'})
        ], style={'verticalAlign': "middle"}),

    ])
    return A


def next_day():
    B = html.Div([
        html.Div([
            dcc.Link(html.Button('Go to Next Day`s Bid', id='nextD_b', disabled=False, style={'color':app.color_4,
                                                                                              'marginTop':'230%'}),
                     id='link_b2', href='/Page_1'),
            html.Div(id='Button_nextday',
                     style={'color': 'black', 'font-size': '22px'})
        ], style={'marginLeft':'20%'}),

    ])
    return B


def download_data():
    C = html.Div([
        html.Div([

            html.A(html.Button(children='1. Download Historical Data', id='downl_data', style={'borderWidth': '1.0px',
                                                                                               'borderColor': app.color_6,
                                                                                                'color': app.color_4,
                                                                                                'marginTop': '10%',
                                                                                                'marginLeft':'-15%',
                                                                                                'font-size': '16px'}),
                   id='link_downl',
                   download="hist_data.csv",
                   href="",
                   target="_blank"
                   ),
        ], className='six columns',style={'marginLeft': '43%', 'verticalAlign': "middle"}), #

    ], className="row")
    return C
