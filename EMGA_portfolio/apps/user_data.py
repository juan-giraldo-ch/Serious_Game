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
                'Drag and Drop or ',
                html.A('Select Bid File', style={'color': app.color_line})
            ],style={'color': app.color_3}),
            style={
                'width': '25vw', 'height': '3vw', 'lineHeight': '2.5vw',
                'borderWidth': '0.15vw', 'borderStyle': 'ridge',
                'borderRadius': '1.5vw', 'textAlign': 'center', 'border-color': app.color_3,
                'backgroundColor': app.color_1, 'font-size': '1.2vw'
            },
        ),
    ], style={'textAlign': 'center', },)

    return file
        ##########################################

def nominal_P():
    # ---------- TYPE IN NOMINAL POWER ----------- #
    nomP = html.Div([
        html.Div([
            html.Div(id='insert_data', children='Nominal Power of Wind Farm [MW]:',
                     style={'textAlign': 'center', 'font-size': '2vw', 'disable':True, 'color':app.color_4,
                             # 'marginLeft': '-15%',
                            # 'marginTop': '5%'
                     }
                     ),
            dcc.Input(id='Pnom', value=float(25.0), type='number', debounce=True,
                      style={'backgroundColor':app.color_6,}
                      ),
        ]),

    ]) #, className="row"

    return nomP


def table_data():
    tab = html.Div([
        # -- Table with datafile information
            html.Div([
                dt.DataTable(id='table_data',
                             style_table={'overflowX': 'scroll', 'overflowY': 'scroll', 'maxHeight': '20vw',},
                                          # 'width': '300px'},
                             editable=False,
                             style_as_list_view=True,
                             style_cell={'textAlign': 'center','backgroundColor':app.color_3,
                                         'color': app.color_4, 'font-size': '0.8vw'},
                             style_header={'backgroundColor':app.color_1, 'color':app.color_3},
                             sort_action="native",
                             sort_mode="multi",
                             ),
            ], id='datatable-container', style={'display': 'none', 'marginLeft':'5vw'}),
    ])
    return tab
        ################################################



