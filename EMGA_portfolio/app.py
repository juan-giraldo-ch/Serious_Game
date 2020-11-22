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
import power_renew_generators as pwg
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


app.database_url = 'Server'#'Local' #
play_days = 10 # Define the number of days to be played

Number_WT = 1


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

######## Constants ################

app.rampU_thermal = 0.25    # Times nominal power from portfolio
app.rampD_thermal = -0.25   # Times nominal power from portfolio
app.min_thermal = 0.20  # Times nominal power from portfolio
app.max_thermal = 0.90  # Times nominal power from portfolio
app.flex_th = 0.15      # Times submited bid

app.rampU_wind = 10 
app.rampD_wind = -10
app.min_wind = 0.0
app.max_wind = 1.0

app.rampU_solar = 10
app.rampD_solar = -10
app.min_solar = 0.0
app.max_solar = 1.0

app.rampU_storage = 0.75
app.rampD_storage = -0.75
app.min_storage = -0.9
app.max_storage = 0.9
app.min_SOC_storage = 10        # Percentage nominal energy capacity from portfolio
app.max_SOC_storage = 90        # Percentage nominal energy capacity from portfolio
app.initial_SOC_storage = 50    # Percentage nominal energy capacity from portfolio


#app.a_thermal = 0.02881 + 0.0003589*x + -0.0003663*y + -1.923e-05*x^2 + 1.177e-05*x*y + -1.217e-06*y^2
#app.b_thermal = 25.81 + -2.721*x + 0.5477*y + -0.1922*x^2 + 0.133*x*y + -0.02102*y^2
#app.c_thermal = 25.83 + -26.14*x + 8.122 *y + -1.41*x^2 +  0.9836*x*y + -0.16*y^2
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

# print(A)

aa = pwg.powerG126(A, Number_WT)

a = pd.DataFrame(data=aa, index=A.index)

url_irrad = 'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/hist_irradiation.csv'
app.PV_irradiation = pd.read_csv(url_irrad, header=0, parse_dates=[0], squeeze=True, date_parser=parser2)

app.PV_irradiation = pd.DataFrame(app.PV_irradiation)

# A = app.PV_irradiation.resample('H', on='DateTime').mean()
# a_i = pd.DataFrame(data=A, index=A.index)


# p_pv = pwg.power_solar(A, 1)


# p_pv = pd.DataFrame(data=p_pv, index=A.index)
days_play1 = int(len(a)/ 24)


a1 = np.zeros((24, days_play1))

for h in range(24):
    for d in range(days_play1):
        a1[h,d] = a.iloc[d*h,0]







# app.WF_real_power = pd.read_csv(r'.\Data\next_days.csv')
url_next = 'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/next_days.csv'
#url_next = 'https://raw.githubusercontent.com/juan-giraldo-ch/Serious_Game/master/reduced_days.csv'
app.WF_real_power = pd.read_csv(url_next)

# app.play_days = len(app.WF_real_power) / 96

################################

days_next = app.WF_real_power

days_next['DateTime'] = pd.to_datetime(days_next['DateTime'], format="%d/%m/%Y %H:%M")
# WT_speed_dates_hist = WT_speed['DateTime']


time_mask = days_next['DateTime'] <= days_next['DateTime'].iloc[-1] - datetime.timedelta(days=play_days)

dates_irrad = days_next['DateTime'][time_mask]

#
#
delta2 = (datetime.datetime.now() - datetime.datetime.strptime(str(dates_irrad.iloc[-1]), "%Y-%m-%d %H:%M:%S")).days

days_next['DateTime'] = days_next['DateTime'] + datetime.timedelta(delta2)

days_next_hist = days_next[time_mask]
days_next_play = days_next[~time_mask]

app.play_days = len(days_next_play) / 96

# print(app.play_days)
################################


app.WF_real_powerO = pd.DataFrame(app.WF_real_power)

# app.dates_nextday = app.WF_real_powerO.iloc[:, 0]

app.dates_nextday = next_wind.iloc[:, 0]

app.WF_real_power = app.WF_real_powerO.iloc[:, 1]
# app.WF_forec_power = app.WF_real_powerO.iloc[:, 4]  #
A = app.WF_real_powerO.iloc[:, 2]  # Positive inbalance tariff
B = app.WF_real_powerO.iloc[:, 3]  # Negative inbalance tariff

days_play = len(app.WF_real_power) / 96

# print(days_play)


# delta1 = (datetime.datetime.now() - datetime.datetime.strptime(str(app.dates_nextday.iloc[0]), "%Y-%m-%d %H:%M:%S")).days  #"%Y-%m-%d %H:%M:%S"
#
#
# def parser3(x):
#     B = (datetime.datetime.strptime(str(x), "%d/%m/%Y %H:%M") + datetime.timedelta(days=delta1)).strftime(
#         '%Y-%m-%d %H:%M')
#     return ((datetime.datetime.strptime(B, '%Y-%m-%d %H:%M')))  # + datetime.datetime.now()
# app.dates_nextday = pd.read_csv(url_nextW, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser3)
#


################################################


# app.dates_irrad = app.PV_irradiation['DateTime']


# delta2 = (datetime.datetime.now() - datetime.datetime.strptime(str(app.dates_irrad.iloc[-1]),
#                                                               "%Y-%m-%d %H:%M:%S")).days
# print(delta2)
# def parser4(x):
#     B = (datetime.datetime.strptime(str(x), "%d/%m/%Y %H:%M") + datetime.timedelta(days=delta2)).strftime(
#         '%Y-%m-%d %H:%M')
#     return ((datetime.datetime.strptime(B, '%Y-%m-%d %H:%M')))  # + datetime.datetime.now()
# app.dates_irrad1 = pd.read_csv(url_irrad, header=0, parse_dates=[0], squeeze=True, date_parser=parser4)
# app.dates_irrad1 = app.dates_irrad1.reset_index()
# app.dates_irrad1 = app.dates_irrad1.drop('index', 1)
# # print(app.dates_irrad1)

##############################################################

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
app.wind_data = pd.read_csv(url_hist)


# delta = (datetime.datetime.now() - datetime.datetime.strptime(str(A.iloc[-1]['DateTime']),
#                                                               "%d/%m/%Y %H:%M")).days


# def parser(x):
#     B = (datetime.datetime.strptime(str(x), "%d/%m/%Y %H:%M") + datetime.timedelta(days=delta)).strftime(
#         '%Y-%m-%d %H:%M')
#     return ((datetime.datetime.strptime(B, '%Y-%m-%d %H:%M')))  # + datetime.datetime.now()
#
#
# app.wf_power = pd.read_csv(url_hist, header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
#
#
#
# app.aa = pd.read_csv(url_hist, header=0, parse_dates=[0], squeeze=True, date_parser=parser)
#
#
# print(app.aa)



