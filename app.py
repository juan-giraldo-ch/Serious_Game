import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import datetime
import csv
import dash_auth


print(dcc.__version__)  # 0.6.0 or above is required

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # 'https://raw.githubusercontent.com/plotly/dash-sample-apps/master/apps/dash-opioid-epidemic/assets/opioid.css'
]

####################
# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}
##
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width"}])


auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
##################

# app = dash.Dash(__name__)
server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')
app.config.suppress_callback_exceptions = True

app.title = 'EmGA'

# path_prices = '"' + os.getcwd() + r'\Data\prices_20_01_2019.csv'

######## Colors #############
app.color_1 = '#454545'  # Background page
app.color_2 = '#8E9799'  # Background figures
app.color_3 = '#0D1F22'  # Color header and sidebar
app.color_4 = '#7fafdf'  # Main text color
app.color_5 = '#D8F7FF'  # Rate, positive
app.color_6 = '#C6C6D1'
app.color_7 = '#75DDDD'  # Warning messages
app.color_8 = '#75DDDD'  # OK status
app.color_9 = '#00D0F4'  # Bars  #00D0F4
app.color_10 = '#ED6A5A'  # Accumulated, negative
app.color_11 = '#8F3985'

# ---- NOT SHARED DATA ----- #

# app.WF_real_power = pd.read_csv(r'.\Data\next_days.csv')
url_next = 'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/next_days.csv'
app.WF_real_power = pd.read_csv(url_next)

app.WF_real_powerO = pd.DataFrame(app.WF_real_power)
app.dates_nextday = app.WF_real_powerO.iloc[:, 0]
app.WF_real_power = app.WF_real_powerO.iloc[:, 1]
# app.WF_forec_power = app.WF_real_powerO.iloc[:, 4]  #
A = app.WF_real_powerO.iloc[:, 2]  # Positive inbalance tariff
B = app.WF_real_powerO.iloc[:, 3]  # Negative inbalance tariff

days_play = len(app.WF_real_power) / 96

delta1 = (datetime.datetime.now() - datetime.datetime.strptime((app.dates_nextday.iloc[0]), "%d/%m/%Y %H:%M")).days


def parser2(x):
    B = (datetime.datetime.strptime(str(x), "%d/%m/%Y %H:%M") + datetime.timedelta(days=delta1)).strftime(
        "%d/%m/%Y %H:%M")
    return ((datetime.datetime.strptime(B, '%d/%m/%Y %H:%M')))  # + datetime.datetime.now()


app.dates_nextday = pd.read_csv(url_next, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser2)

j = 0
ener = 0
ener_fore = 0
Pprice = 0
Lprice = 0
h = 0
d = 1
app.WF_inj = np.zeros((24, 1 + int(days_play)))
app.UB_prices_pos = np.zeros((24, 1 + int(days_play)))
app.UB_prices_neg = np.zeros((24, 1 + int(days_play)))

# app.WF_forec = np.zeros((24,1+int(days_play)))

for i in range(len(app.dates_nextday)):
    # app.dates_nextday[i] = datetime.datetime.strptime(app.dates_nextday.iloc[i],'%d/%m/%Y %H:%M')
    j = j + 1
    if j <= 4:
        ener = ener + app.WF_real_power.iloc[i] * 0.25
        Pprice = Pprice + A.iloc[i] * 0.25
        Lprice = Lprice + B.iloc[i] * 0.25

        if j == 4 and h <= 24:
            if d == 1:
                app.WF_inj[h, 0] = h
                app.UB_prices_pos[h, 0] = h
                app.UB_prices_neg[h, 0] = h

            app.WF_inj[h, d] = ener
            app.UB_prices_pos[h, d] = Pprice
            app.UB_prices_neg[h, d] = Lprice

            ener = 0
            Pprice = 0
            Lprice = 0
            ener_fore = 0
            j = 0
            h = h + 1
        if h == 24:
            d = d + 1
            h = 0

            # TERMINAR AQUI DE ORGANIZAR LOS DATOS

# pd.DataFrame(app.WF_forec).to_csv('forecast.csv', index=False)

url_ndprices = 'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/day_ahead_prices.csv'
app.prices = pd.read_csv(url_ndprices)
# app.prices = pd.read_csv(r'.\Data\prices_20_01_2019.csv')       # Day ahead prices   see (https://www.nordpoolgroup.com/Market-data1/Dayahead/Area-Prices/nl/hourly/?view=table)

# app.real_P = pd.read_csv(r'.\Real_injection.csv')
app.real_P = app.WF_inj / 1000

# ---- SHARED DATA ----- #
url_hist = 'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/hist_data.csv'
app.wf_power = pd.read_csv(url_hist)
delta = (datetime.datetime.now() - datetime.datetime.strptime(str(app.wf_power.iloc[-1]['DateTime']),
                                                              "%d/%m/%Y %H:%M")).days


def parser(x):
    B = (datetime.datetime.strptime(str(x), "%d/%m/%Y %H:%M") + datetime.timedelta(days=delta)).strftime(
        "%d/%m/%Y %H:%M")
    return ((datetime.datetime.strptime(B, '%d/%m/%Y %H:%M')))  # + datetime.datetime.now()


app.wf_power = pd.read_csv(url_hist, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)

#

app.b2 = 0
app.b2p = 0
app.accum = 0
app.exp_accum = 0
app.acc1 = 0
app.accufig = [0.0]
app.bar_acum = [0.0]
app.lin_exp_accum = [0.0]
app.rate_accum = [0.0]
app.data = []
app.A = 0

app.global_rev = np.zeros((24, 1))
app.ddf = np.zeros((24, 2))
