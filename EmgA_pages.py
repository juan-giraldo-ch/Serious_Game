# coding=utf-8


# -*- coding: utf-8 -*-
# import base64
# import io
# import dash
import dash_core_components as dcc
import dash_html_components as html
# import pandas as pd
# import numpy as np
from dash.dependencies import Input, Output, State
# from dash.exceptions import PreventUpdate
# import plotly.graph_objs as go
# import os  # Importing OS functions


from app import app
from apps import page_1, page_2



#  Layouts


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
    if pathname == '/' or pathname == '/Page_1':
        return page_1.layout
    if pathname == '/Page_2':
        return page_2.layout
    else:
        return '404 page not found'


#################################################


if __name__ == '__main__':
    app.run_server(debug=True)

