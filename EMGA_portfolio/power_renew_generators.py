import numpy as np
import pandas as pd

def powerG126(speed, Number_WT):
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
                # print(t, s, speed.iloc[s, t])
                raise ValueError

    # Dates here are artificial in order to resample the dataframe
    powerDf = pd.DataFrame(index=['s' + str(s) for s in range(1, power.shape[0] + 1)],
                           columns=pd.date_range('2015-01-01 00:00', periods=power.shape[1], freq='10min'), data=power)
    powerH = powerDf.T.resample('H').mean().T*Number_WT

    return powerH.values/2.5

def power_solar(irrad, Pnom):


    power = np.zeros(irrad.shape)
    # powerH = np.zeros((speed.shape[0], int(speed.shape[0] / (6 * 24))))
    t = 1
    for s in range(power.shape[0]):
        for t in range(power.shape[1]):
            power[s,t] = Pnom * irrad.iloc[s,t]/1000

    powerDf = pd.DataFrame(index=['s' + str(s) for s in range(1, power.shape[0] + 1)],
                           columns=pd.date_range('2015-01-01 00:00', periods=power.shape[1], freq='10min'), data=power)
    powerH = powerDf.T.resample('H').mean().T

    return powerH.values