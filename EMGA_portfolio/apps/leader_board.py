import dash
import dash_core_components as dcc
import dash_html_components as html
from app import app
import dash_bootstrap_components as dbc
import dash_table as dt
import flask




params = [
    'index', 'Accum', 'day'
]


# print(app.lead_board)


def L_table():
    A = html.Div(
        [
            html.Button(
                "Leaderboard", id="popover-target", className='button-primary',
                style={'font-size': '1.0vw', 'height': '2vw', 'width': '100%', 'textAlign': 'center'}
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader("Leaderboard", style={'backgroundColor': app.color_6, 'color': app.color_4,
                                                            'font-size': '1.2vw', 'textAlign': 'center'}),
                    dbc.PopoverBody([
                        html.Div([
                            dt.DataTable(
                                id='table-editing-simple',
                                # columns=(
                                #         [{'id': p, 'name': p} for p in app.lead_board.columns]
                                # ),
                                # data=[
                                #     {p : app.lead_board.at[i,p] for p in app.lead_board.columns}
                                #     # dict(Model=i, **{param: app.lead_board[i]['index'] for param in params})
                                #
                                #     # dict(Model=i, **{param: 0 for param in params})
                                #     for i in range(len(app.lead_board['index']))
                                # ],
                                editable=False,
                                style_table={'overflowX': 'scroll', 'overflowY': 'scroll', 'maxHeight': '19vw',
                                             'maxWidth': '39vw', 'font-size': '1.0vw'},
                                style_cell={'textAlign': 'center', 'backgroundColor': app.color_1,
                                            'color': app.color_3, 'font-size': '0.8vw'},
                                style_header={'backgroundColor': app.color_3,'color': app.color_4},
                                sort_action="native",
                                sort_mode="multi",


                            ),
                        ],style={'width': '40vw', 'textAlign': 'right'},)
                    ], style={'width': '40vw', 'height': '20vw'}),
                ],
                id="popover",
                is_open=False,
                target="popover-target",
                style={'backgroundColor': app.color_6},
            ),
        ], style={'textAlign': 'center'}
    )

    return A
