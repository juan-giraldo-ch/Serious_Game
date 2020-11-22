import pandas as pd
import numpy as np
from pyomo.environ import *
import matplotlib.pyplot as plt
import psycopg2
import os  # Importing OS functions
import csv
from app import app


import pyutilib
pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False #this is required to avoid the threading problem (Pyomo + solver signals)


############################################################################
def feasibility_check(username, portf, bids):
    ####### Get parameters for model #########

    # url_data = os.popen("heroku config:get DATABASE_URL -a emga").read().strip()  # When local machine
    # # url_data = os.popen("heroku config:get DATABASE_URL -a emgaportfolio").read().strip() #When local machine
    #
    # DATABASE_URL = url_data
    #
    # # user_active = flask.request.cookies.get('custom-auth-session')
    #
    # conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM portfolio WHERE Player = (%s);", (username,))
    # accum = cur.fetchall()
    # conn.close()
    # cur.close()

    accum = portf

    constraints = {'Thermal':[accum[0][2],accum[0][2]*app.rampU_thermal,accum[0][2]*app.rampD_thermal, accum[0][2]*app.min_thermal,accum[0][2]*app.max_thermal,0,0,0],
                   'Wind':[accum[0][3],accum[0][3]*app.rampU_wind,accum[0][3]*app.rampD_wind, app.min_wind,accum[0][3]*app.max_wind,0,0,0],
                   'Solar':[accum[0][4],accum[0][4]*app.rampU_solar,accum[0][4]*app.rampD_solar, app.min_solar,accum[0][4]*app.max_solar,0,0,0],
                   'Storage':[accum[0][5],accum[0][5]*app.rampU_storage,accum[0][5]*app.rampD_storage, accum[0][5]*app.min_storage,accum[0][5]*app.max_storage,app.min_SOC_storage,app.max_SOC_storage,app.initial_SOC_storage]
                   }

    constraints = pd.DataFrame(constraints,
                               index=['Nominal MWh', 'Ramp-up MWh', 'Ramp-down MWh', 'Min MWh', 'Max MWh', 'max_SOC %',
                                      'min_SOC %', 'SOC_initial %'])



    # bids = pd.read_csv(
    #     r'C:\Users\20194851\Google Drive\Postdoc TUe\Project Serious Game\Dash_tests\EMGA_portfolio\Bids.csv', header=0)
    bids = bids.set_index('Hour')
    # bids = bids
    # print(constraints)

    model = ConcreteModel()

    T = range(24)
    S = range(4)

    model.T = Set(ordered=True, initialize=T)  # Set of time periods
    model.S = Set(ordered=True, initialize=S)  # Set of energy sources of portfolio

    Pnom = {S[i]: constraints.iloc[0, i] for i in S}

    Pmax = {S[i]: constraints.iloc[4, i] for i in S}
    Pmin = {S[i]: constraints.iloc[3, i] for i in S}
    Rampup = {S[i]: constraints.iloc[1, i] for i in S}
    Rampdown = {S[i]: constraints.iloc[2, i] for i in S}
    soc_max = {S[i]: constraints.iloc[6, i] / 100 for i in S}
    soc_min = {S[i]: constraints.iloc[5, i] / 100 for i in S}
    soc_ini = {S[i]: constraints.iloc[7, i] / 100 for i in S}


    Enom = {(S[i], T[t]): bids.iloc[t, i] for i in S for t in T}

    model.Pmax = Param(model.S, initialize=Pmax, mutable=True)  # Max power
    model.Pmin = Param(model.S, initialize=Pmin, mutable=True)  # Min power
    model.Rampup = Param(model.S, initialize=Rampup, mutable=True)  # Max power ramp
    model.Rampdown = Param(model.S, initialize=Rampdown, mutable=True)  # Min power ramp
    model.soc_max = Param(model.S, initialize=soc_max, mutable=True)  # Max state of charge storage
    model.soc_min = Param(model.S, initialize=soc_min, mutable=True)  # Min state of charge storage
    model.soc_ini = Param(model.S, initialize=soc_ini, mutable=True)  # Initial state of charge storage
    model.Enom = Param(model.S, model.T, initialize=Enom, mutable=True)
    model.Pnom = Param(model.S, initialize=Pnom, mutable=True)

    # Define Variables
    model.zeta_plus = Var(model.S, model.T, initialize=0, within=NonNegativeReals)  # Acive power flowing in lines
    model.zeta_minus = Var(model.S, model.T, initialize=0, within=NonNegativeReals)  # Reacive power flowing in lines
    model.phi_plus = Var(model.S, model.T, initialize=0, within=NonNegativeReals)  # Acive power flowing in lines
    model.phi_minus = Var(model.S, model.T, initialize=0, within=NonNegativeReals)  # Reacive power flowing in lines
    model.rho_plus = Var(model.S, model.T, initialize=0, within=NonNegativeReals)  # Acive power flowing in lines
    model.rho_minus = Var(model.S, model.T, initialize=0, within=NonNegativeReals)  # Reacive power flowing in lines
    model.SOC = Var(model.S, model.T, initialize=0)  # Reacive power flowing in lines

    # %% Define Objective Function
    def feasib_check(model):
        return sum(sum(model.zeta_plus[i, t] + model.zeta_minus[i, t] + model.phi_plus[i, t] + model.phi_minus[i, t] +
                       model.rho_plus[i, t] + model.rho_minus[i, t] for i in model.S) for t in model.T)

    model.obj = Objective(rule=feasib_check)

    # %% Define Constraints

    def Pmax_power_rule(model, i, t):
        return (model.Enom[i, t] - model.phi_plus[i, t] <= model.Pmax[i])

    model.Pmax_power = Constraint(model.S, model.T, rule=Pmax_power_rule)

    def Pmin_power_rule(model, i, t):
        return (model.Enom[i, t] + model.phi_minus[i, t] >= model.Pmin[i])

    model.Pmin_power = Constraint(model.S, model.T, rule=Pmin_power_rule)

    def Ramp_max_power_rule(model, i, t):
        if t > 0 and (i==0 or i==3):
            return (model.Enom[i, t] - model.Enom[i, t - 1] - model.zeta_plus[i, t] <= model.Rampup[i])
        else:
            return (model.Enom[i, t] - model.zeta_plus[i, t] <= model.Pmax[i]) # Error es por esto

    model.Ramp_max_power = Constraint(model.S, model.T, rule=Ramp_max_power_rule)

    def Ramp_min_power_rule(model, i, t):
        if t > 0 and (i==0 or i==3):
            return (model.Enom[i, t] - model.Enom[i, t - 1] + model.zeta_minus[i, t] >= model.Rampdown[i])
        else:
            return (model.Enom[i, t] + model.zeta_minus[i, t] >= model.Pmin[i])

    model.Ramp_min_power = Constraint(model.S, model.T, rule=Ramp_min_power_rule)

    def SOC_rule(model, i, t):
        if t > 0 and i == 3:
            return (model.SOC[i, t] == model.SOC[i, t - 1] - model.Enom[i, t] / model.Pnom[i])
        elif t == 0 and i == 3:
            return (model.SOC[i, t] == model.soc_ini[i] - model.Enom[i, t] / model.Pnom[i])
        else:
            return model.SOC[i, t] == 0.0

    model.SOC_constr = Constraint(model.S, model.T, rule=SOC_rule)

    def SOC_max_rule(model, i, t):
        if i == 3:
            return (model.SOC[i, t] - model.rho_plus[i, t] <= model.soc_max[i])
        else:
            return (model.SOC[i, t] == 0.0)

    model.SOC_max = Constraint(model.S, model.T, rule=SOC_max_rule)

    def SOC_min_rule(model, i, t):
        if i == 3:
            return (model.SOC[i, t] + model.rho_minus[i, t] >= model.soc_min[i])
        else:
            return (model.SOC[i, t] == 0.0)

    model.SOC_min = Constraint(model.S, model.T, rule=SOC_min_rule)

    def SOC_end_rule(model, i, t):
        if i == 3:
            return (model.SOC[i, t] + model.rho_minus[i, t] >= model.soc_ini[i])
        else:
            return (model.SOC[i, t] == 0.0)

    model.SOC_end = Constraint(model.S, model.T, rule=SOC_end_rule)

    # Define the Solver
    solver = SolverFactory('ipopt')  # couenne
    solver.options['print_level'] = 0


    # Solve
    solver.solve(model, tee=True)

    total_inf = np.zeros((24,1))

    phi_plus = np.zeros((24, 1))
    phi_minus = np.zeros((24, 1))
    zeta_plus = np.zeros((24, 1))
    zeta_minus = np.zeros((24, 1))
    rho_plus = np.zeros((24, 1))
    rho_minus = np.zeros((24, 1))

    # print('\n')
    for i in model.S:
       for t in model.T:
           # print('{:>16d}{:>16d}{:>16.6f}'.format(i,t,model.phi_plus[i,t].value), end=" ")
           # print('{:>16.6f}'.format(model.phi_minus[i,t].value), end=" ")
           # print('{:>16.6f}'.format(model.zeta_plus[i,t].value), end=" ")
           # print('{:>16.6f}'.format(model.zeta_minus[i,t].value), end=" ")
           # print('{:>16.6f}'.format(model.rho_plus[i,t].value), end=" ")
           # print('{:>16.6f}'.format(model.rho_minus[i,t].value), end=" ")
           # print('{:>16.6f}'.format(model.SOC[i,t].value*100))
           total_inf[t] = total_inf[t] + model.phi_plus[i,t].value + model.phi_minus[i,t].value + model.zeta_plus[i,t].value \
                        + model.zeta_minus[i,t].value + model.rho_plus[i,t].value*model.Pnom[i].value + model.rho_minus[i,t].value*model.Pnom[i].value
           phi_plus[t] = phi_plus[t] + model.phi_plus[i,t].value
           phi_minus[t] = phi_minus[t] + model.phi_plus[i,t].value
           zeta_plus[t] = zeta_plus[t] + model.zeta_plus[i,t].value
           zeta_minus[t] = zeta_minus[t] + model.zeta_minus[i,t].value
           rho_plus[t] = model.rho_plus[i, t].value * model.Pnom[i].value
           rho_minus[t] = model.rho_minus[i, t].value * model.Pnom[i].value

    return model, pd.DataFrame(total_inf), pd.DataFrame(phi_plus), pd.DataFrame(phi_minus), pd.DataFrame(zeta_plus),\
           pd.DataFrame(zeta_minus), pd.DataFrame(rho_plus), pd.DataFrame(rho_minus)
############################################################################


def redispatch(portf, imbalance, ubpr_pos, ubpr_neg, d, bids):

    accum = portf

    constraints = {'Thermal':[accum[0][2],accum[0][2]*app.rampU_thermal,accum[0][2]*app.rampD_thermal, accum[0][2]*app.min_thermal,accum[0][2]*app.max_thermal,0,0,0],
                   'Wind':[accum[0][3],accum[0][3]*app.rampU_wind,accum[0][3]*app.rampD_wind, app.min_wind,accum[0][3]*app.max_wind,0,0,0],
                   'Solar':[accum[0][4],accum[0][4]*app.rampU_solar,accum[0][4]*app.rampD_solar, app.min_solar,accum[0][4]*app.max_solar,0,0,0],
                   'Storage':[accum[0][5],accum[0][5]*app.rampU_storage,accum[0][5]*app.rampD_storage, accum[0][5]*app.min_storage,accum[0][5]*app.max_storage,app.min_SOC_storage,app.max_SOC_storage,app.initial_SOC_storage]
                   }

    constraints = pd.DataFrame(constraints,
                               index=['Nominal MWh', 'Ramp-up MWh', 'Ramp-down MWh', 'Min MWh', 'Max MWh', 'max_SOC %',
                                      'min_SOC %', 'SOC_initial %'])

    bids = bids.set_index('Hour')


    a_thermal =  np.min(0.02262 + 0.0005662*constraints.iloc[3, 0] - 0.0003439*constraints.iloc[4, 0] + 4.513e-06*constraints.iloc[3, 0]**2 - 4.356e-06*constraints.iloc[3, 0]*constraints.iloc[4, 0] + 1.184e-06*constraints.iloc[4, 0]**2, 0)
    b_thermal = np.min(25.81 -2.721*constraints.iloc[3, 0] + 0.5477*constraints.iloc[4, 0] -0.1922*constraints.iloc[3, 0]**2 + 0.133*constraints.iloc[3, 0]*constraints.iloc[4, 0] -0.02102*constraints.iloc[4, 0]**2,0)
    c_thermal = np.min(25.83 + -26.14*constraints.iloc[3, 0] + 8.122 *constraints.iloc[4, 0] -1.41*constraints.iloc[3, 0]**2 +  0.9836*constraints.iloc[3, 0]*constraints.iloc[4, 0] -0.16*constraints.iloc[4, 0]**2,0)

    model = ConcreteModel()

    T = range(24)
    S = range(4)

    model.T = Set(ordered=True, initialize=T)  # Set of time periods
    model.S = Set(ordered=True, initialize=S)  # Set of energy sources of portfolio


    Flex_max = {S[i]: constraints.iloc[0, i]*app.flex_th for i in S}
    Pmax = {S[i]: constraints.iloc[4, i] for i in S}
    Pmin = {S[i]: constraints.iloc[3, i] for i in S}

    Rampup = {S[i]: constraints.iloc[1, i] for i in S}
    Rampdown = {S[i]: constraints.iloc[2, i] for i in S}
    Imbalance = {T[t]: imbalance.iloc[t] for t in T}
    Price_plus = {T[t]: ubpr_pos.iloc[t] for t in T}
    Price_neg = {T[t]: ubpr_neg.iloc[t] for t in T}
    Enom = {(S[i], T[t]): bids.iloc[t, i] for i in S for t in T}


    model.Flex_max = Param(model.S, initialize=Flex_max, mutable=True)  # Max power
    model.Pmax = Param(model.S, initialize=Pmax, mutable=True)  # Max power
    model.Pmin = Param(model.S, initialize=Pmin, mutable=True)  # Max power

    model.Rampup = Param(model.S, initialize=Rampup, mutable=True)  # Max power ramp
    model.Rampdown = Param(model.S, initialize=Rampdown, mutable=True)  # Min power ramp
    model.Imbalance = Param(model.T, initialize=Imbalance, mutable=False)  # Min power ramp
    model.price_plus = Param(model.T, initialize=Price_plus, mutable=True)  # Min power ramp
    model.price_neg = Param(model.T, initialize=Price_neg, mutable=True)  # Min power ramp
    model.Enom = Param(model.S, model.T, initialize=Enom, mutable=True)

    # Variables

    model.flex = Var(model.S, model.T, initialize=0, within=NonNegativeReals)  #  , bounds=(0,50) Acive power flowing in lines
    model.cost = Var(model.S, model.T, initialize=0, within=NonNegativeReals)  # Acive power flowing in lines

    # t = 1


    # %% Define Objective Function
    def redisp_obj(model):
        if value(model.Imbalance[d]) >= 0:
            return sum(model.cost[i,d] + model.price_plus[d]*(model.Imbalance[d] - model.flex[i,d]) for i in model.S)
        if value(model.Imbalance[d]) < 0:
            return sum(model.cost[i,d] + model.price_neg[d]*(-model.Imbalance[d] - model.flex[i,d])for i in model.S)
    model.obj = Objective(rule=redisp_obj)


    def posit_diff_rule(model, i):
        if value(model.Imbalance[d]) >= 0:
            return (model.Imbalance[d] - model.flex[i,d] >= 0.0)
        if value(model.Imbalance[d]) < 0:
            return (-model.Imbalance[d] - model.flex[i,d] >= 0.0)
    model.posit_diff = Constraint(model.S,rule=posit_diff_rule)


    def cost_rule(model,i):
        if i == 0:
            return (model.cost[i,d] == a_thermal*model.flex[i,d] + b_thermal*model.flex[i,d] + c_thermal)
        else:
            return (model.cost[i,d] == 0.0)
    model.cost_constr = Constraint(model.S, rule=cost_rule)

    def flex_rule(model,i):
        if i == 0:
            return (0,model.flex[i,d],model.Flex_max[i])
        else:
            return (0,model.flex[i,d],0)
    model.flex_constr = Constraint(model.S, rule=flex_rule)


    def maxP_rule(model,i):
        if value(model.Imbalance[d]) >= 0:
            return (model.Enom[i,d] + model.flex[i,d] <= model.Pmax[i])
        elif value(model.Imbalance[d]) < 0:
            return (model.Enom[i,d] - model.flex[i,d] >= model.Pmin[i])
        # else:
        #     return (0,model.flex[i,d],0)
    model.maxP_constr = Constraint(model.S, rule=maxP_rule)

    # Define the Solver
    solver = SolverFactory('ipopt')  # couenne
    solver.options['print_level'] = 0

    # Solve
    solver.solve(model, tee=True)

    return model