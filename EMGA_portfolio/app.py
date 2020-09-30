import dash
import dash_core_components as dcc
# import dash_html_components as html
import pandas as pd
import numpy as np
import datetime
# import csv
# import json
# from bson import json_util

# import dash_auth
import dash_bootstrap_components as dbc
# from foreUtils_2020 import powerG126

# from users import users_info

# user_pwd, user_names = users_info()




print(dcc.__version__)  # 0.6.0 or above is required

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # 'https://raw.githubusercontent.com/plotly/dash-sample-apps/master/apps/dash-opioid-epidemic/assets/opioid.css'
]

####################

#external_stylesheets=external_stylesheets
##
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])


app.database_url = 'Local' # 'Server'



##################

# app = dash.Dash(__name__)
server = app.server
# server.secret_key = os.environ.get('secret_key', 'secret')
app.config.suppress_callback_exceptions = True

app.title = 'EmGA'

# path_prices = '"' + os.getcwd() + r'\Data\prices_20_01_2019.csv'

######## Colors #############
app.color_1 = '#eeeeee'#'#9D9C9D'  # Background page
app.color_2 = '#FAFAFA'  # Background figures
# app.color_3 = '#222831'  # Color header and sidebar
app.color_3 = '#142850' # Color header and sidebar
app.color_4 = '#eeeeee'   # Main text color
app.color_5 = '#D8F7FF'  # Rate, positive
app.color_6 = '#27496d'    # Second color header
app.color_7 = '#00909e'#'#75DDDD'  # Warning messages
app.color_8 = '#00909e'#'#75DDDD'  # OK status
app.color_9 = '#00adb5 '  # Bars  #00D0F4
app.color_10 = '#ED6A5A'  # Accumulated, negative
app.color_11 = '#8F3985'
app.color_green = '#8aee59'
app.color_red = '#DA5151'
app.color_icon = '#32e0c4'
app.color_bar2 = '#4c5f87'
app.color_line = '#00909e'
app.color_bfig = '#dae1e7'
####
#393e46

####


# ######## Colors #############
# app.color_1 = '#454545'  # Background page
# app.color_2 = '#8E9799'  # Background figures
# app.color_3 = '#0D1F22'  # Color header and sidebar
# app.color_4 = '#8aee59'  # Main text color
# #app.color_4 = '#7fafdf'  # Main text color
# app.color_5 = '#D8F7FF'  # Rate, positive
# app.color_6 = '#C6C6D1'
# app.color_7 = '#FDFDFF'#'#75DDDD'  # Warning messages
# app.color_8 = '#FDFDFF'#'#75DDDD'  # OK status
# app.color_9 = '#00D0F4'  # Bars  #00D0F4
# app.color_10 = '#ED6A5A'  # Accumulated, negative
# app.color_11 = '#8F3985'

# ---- NOT SHARED DATA ----- #

###############################
################################



# app.lead_board = (pd.DataFrame.from_dict(user_pwd, orient='index'))
# app.lead_board= app.lead_board.reset_index()
# app.lead_board = app.lead_board.drop([0], axis=1)
#
#
#
#
# app.lead_board['Accum'] = 0.0
# app.lead_board['day'] = 0.0
# app.lead_board['rate'] = 0.0





url_nextW = 'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/next_wind.csv'


def parser2(x):
    B = (datetime.datetime.strptime(str(x), "%d/%m/%Y %H:%M"))
    return (B)  # + datetime.datetime.now()


next_wind = pd.read_csv(url_nextW, header=0, parse_dates=[0], squeeze=True, date_parser=parser2)


A = next_wind.resample('H', on='DateTime').mean()
# next_wind = next_wind.set_index('DateTime')


Number_WT = 10

def powerG126(speed):
    power = np.zeros(speed.shape)
    # powerH = np.zeros((speed.shape[0], int(speed.shape[0] / (6 * 24))))
    t = 1
    for s in range(power.shape[0]):
        for t in range(power.shape[1]):
            if speed.iloc[s, t] < 2 or speed.iloc[s, t] > 25:
                power[s, t] = 0
            elif speed.iloc[s, t] >= 2 and speed.iloc[s, t] < 10:
                power[s, t] = -7.1754 * (speed.iloc[s, t] ** 3) + 120.13 * (speed.iloc[s, t] ** 2) - 252.4 * speed.iloc[
                    s, t] + 186.36
            elif speed.iloc[s, t] >= 10 and speed.iloc[s, t] <= 21:
                power[s, t] = 2500
            elif speed.iloc[s, t] > 21 and speed.iloc[s, t] <= 25:
                power[s, t] = 9.3333 * (speed.iloc[s, t] ** 3) - 654.31 * (speed.iloc[s, t] ** 2) + 15059 * speed.iloc[
                    s, t] - 111619
            else:
                print(t, s, speed.iloc[s, t])
                raise ValueError

    # Dates here are artificial in order to resample the dataframe
    powerDf = pd.DataFrame(index=['s' + str(s) for s in range(1, power.shape[0] + 1)],
                           columns=pd.date_range('2015-01-01 00:00', periods=power.shape[1], freq='10min'), data=power)
    powerH = powerDf.T.resample('H').mean().T*Number_WT

    return powerH.values

aa = powerG126(A)

a = pd.DataFrame(data=aa, index=A.index)
days_play1 = int(len(a)/ 24)
# print(days_play1)

a1 = np.zeros((24, days_play1))

for h in range(24):
    for d in range(days_play1):
        a1[h,d] = a.iloc[d*h,0]








# app.WF_real_power = pd.read_csv(r'.\Data\next_days.csv')
#url_next = 'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/next_days.csv'
url_next = 'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/reduced_days.csv'
app.WF_real_power = pd.read_csv(url_next)



app.WF_real_powerO = pd.DataFrame(app.WF_real_power)

# app.dates_nextday = app.WF_real_powerO.iloc[:, 0]

app.dates_nextday = next_wind.iloc[:, 0]

app.WF_real_power = app.WF_real_powerO.iloc[:, 1]
# app.WF_forec_power = app.WF_real_powerO.iloc[:, 4]  #
A = app.WF_real_powerO.iloc[:, 2]  # Positive inbalance tariff
B = app.WF_real_powerO.iloc[:, 3]  # Negative inbalance tariff

days_play = len(app.WF_real_power) / 96

print(days_play)


delta1 = (datetime.datetime.now() - datetime.datetime.strptime(str(app.dates_nextday.iloc[0]), "%Y-%m-%d %H:%M:%S")).days  #"%Y-%m-%d %H:%M:%S"


def parser2(x):
    B = (datetime.datetime.strptime(str(x), "%d/%m/%Y %H:%M") + datetime.timedelta(days=delta1)).strftime(
        '%Y-%m-%d %H:%M')
    return ((datetime.datetime.strptime(B, '%Y-%m-%d %H:%M')))  # + datetime.datetime.now()
app.dates_nextday = pd.read_csv(url_nextW, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser2)



################################

url_DAP = 'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/DAP_Feb_2020.csv'
DAP = pd.read_csv(url_DAP)
DAP['DateTime'] = pd.to_datetime(DAP['DateTime'])
DAP['DateTime'] = DAP['DateTime'].dt.strftime('%Y-%m-%d %H:%M')

h = 0
d = 1
Lp = np.zeros((24, 1 + int(days_play1)))
Lm = np.zeros((24, 1 + int(days_play1)))
Pr = np.zeros((24, 1 + int(days_play1)))


for i in range(len(DAP['DateTime'])):
    # app.dates_nextday[i] = datetime.datetime.strptime(app.dates_nextday.iloc[i],'%d/%m/%Y %H:%M')
    # j = j + 1
    # if j <= 4:
    #     ener = ener + app.WF_real_power.iloc[i] * 0.25
    #     Pprice = Pprice + A.iloc[i] * 0.25
    #     Lprice = Lprice + B.iloc[i] * 0.25

    if h <= 24:
        if d == 1:
            Lp[h, 0] = h
            Lm[h, 0] = h
            Pr[h, 0] = h

        Pr[h, d] = DAP.iloc[i,1]    # Lambda^{D}
        Lp[h, d] = DAP.iloc[i,2]    # Lambda^{+}/Lambda^{D}
        Lm[h, d] = DAP.iloc[i,3]    # Lambda^{-}/Lambda^{D}

        h = h + 1
    if h == 24:
        d = d + 1
        h = 0



app.WF_inj = DAP['DAP']
app.UB_prices_pos = Lp
app.UB_prices_neg = Lm


###############################


url_ndprices = 'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/day_ahead_prices.csv'
app.prices = pd.read_csv(url_ndprices)

app.prices = Pr

# app.prices = pd.read_csv(r'.\Data\prices_20_01_2019.csv')       # Day ahead prices   see (https://www.nordpoolgroup.com/Market-data1/Dayahead/Area-Prices/nl/hourly/?view=table)

# app.real_P = pd.read_csv(r'.\Real_injection.csv')
app.real_P = a1/1000 # MW#app.WF_inj / 1000


# ---- SHARED DATA ----- #
# url_hist = 'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/hist_data.csv'
url_hist = 'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/windSpeed_2020.csv'
A = pd.read_csv(url_hist)
delta = (datetime.datetime.now() - datetime.datetime.strptime(str(A.iloc[-1]['DateTime']),
                                                              "%d/%m/%Y %H:%M")).days


def parser(x):
    B = (datetime.datetime.strptime(str(x), "%d/%m/%Y %H:%M") + datetime.timedelta(days=delta)).strftime(
        '%Y-%m-%d %H:%M')
    return ((datetime.datetime.strptime(B, '%Y-%m-%d %H:%M')))  # + datetime.datetime.now()


app.wf_power = pd.read_csv(url_hist, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)


app.aa = pd.read_csv(url_hist, header=0, parse_dates=[0], squeeze=True, date_parser=parser)



