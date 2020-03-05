import dash
import dash_core_components as dcc
import dash_html_components as html


def mesag_size():
    # ---------- FILE HAS WRONG SIZE ----------- #
    A = dcc.ConfirmDialog(
        id='table_size',
        message='Table must contain 24 rows and 2 columns',
    )
    ##############################################
    return  A


def mesag_nom():
    # ---------- BID > THAN NOMINAL P ----------- #
    B = dcc.ConfirmDialog(
        id='compare_p',
        message='CAUTION!  There are Bid values greater than Nominal Power.',
    )
    ##############################################
    return B
