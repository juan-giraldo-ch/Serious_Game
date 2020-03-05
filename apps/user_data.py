import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from app import app




# ---------- LOAD BID_FILE ----------- #
def drag_file():
    file = html.Div([
        dcc.Upload(
            id='Drag_file',
            children=html.Div([
                '2. Drag and Drop or ',
                html.A('Select Bid File', style={'color': app.color_7})
            ],style={'color': app.color_4}),
            style={
                'width': '50%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1.2px', 'borderStyle': 'dashed',
                'borderRadius': '50px', 'textAlign': 'center', 'margin': '80px',
                'marginLeft':'20%', 'font-size': '20px'
            },
        ),
    ])

    return file
        ##########################################

def nominal_P():
    # ---------- TYPE IN NOMINAL POWER ----------- #
    nomP = html.Div([
        html.Div([
            html.Div(id='insert_data', children='Nominal Power of Wind Farm [MW]:',
                     style={'textAlign': 'center', 'font-size': '20px', 'disable':True, 'color':app.color_4,
                             'marginLeft': '-15%',
                            'marginTop': '5%'}),
            dcc.Input(id='Pnom', value=float(1000.0), type='number', debounce=True,
                      style={
                             'backgroundColor':app.color_6,
                            'marginLeft': '35%'}),
        ]),

    ]) #, className="row"

    return nomP


def table_data():
    tab = html.Div([
        # -- Table with datafile information
        html.Div([
            html.Div([
                dt.DataTable(id='table_data',
                             style_table={'overflowX': 'scroll', 'overflowY': 'scroll', 'maxHeight': '400px',
                                          'width': '300px'},
                             editable=False,
                             style_as_list_view=True,
                             style_cell={'textAlign': 'left','backgroundColor':app.color_3,
                                         'color': app.color_4},
                             style_header={'backgroundColor':app.color_1},
                             sort_action="native",
                             sort_mode="multi",
                             ),
            ], id='datatable-container', style={'display': 'block', 'marginLeft':'20%'}),

        ]),

    ])
    return tab
        ################################################



