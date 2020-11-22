import pandas
import numpy
from pyomo.environ import *
import matplotlib.pyplot as plt

UnitData = pandas.read_excel('ED_input.xlsx', sheet_name = 'Units', index_col= 0)

print(UnitData.index)

#Also, let us define a python variable that hosts the value of the load 
D = 975

model = ConcreteModel()

#import suffixes (marginal values) -- "import them from the solver"
model.dual = Suffix(direction=Suffix.IMPORT) 

model.I = Set(ordered = True, initialize = UnitData.index)


model.Pmax = Param(model.I, within = NonNegativeReals, mutable = True)
model.Pmin = Param(model.I, within = NonNegativeReals, mutable = True)

model.a = Param(model.I, within = NonNegativeReals, mutable = True)
model.b = Param(model.I, within = NonNegativeReals, mutable = True)
model.c = Param(model.I, within = NonNegativeReals, mutable = True)

#Give values to Pmax, Pmin, a, b, c

for i in model.I:
    model.Pmax[i] = UnitData.loc[i,'Max']
    model.Pmin[i] = UnitData.loc[i,'Min']
    model.a[i] = UnitData.loc[i, 'a']
    model.b[i] = UnitData.loc[i, 'b']
    model.c[i] = UnitData.loc[i, 'c']

    
#Define decision variables

model.P = Var(model.I, within = PositiveReals)

#Define constraints of the problem

def cost_rule(model):
    return sum(model.a[i] + model.b[i]*model.P[i]+model.c[i]*model.P[i]*model.P[i] for i in model.I)

def minmax_rule(model, i):
    return (model.Pmin[i],model.P[i],model.Pmax[i])

def pbalance_rule(model):
    return sum(model.P[i] for i in model.I) == D

#Add them to the model

model.cost = Objective(rule = cost_rule)
model.unit_out_constraints = Constraint(model.I, rule = minmax_rule)
model.balance = Constraint(rule = pbalance_rule)

#opt=SolverFactory('gurobi')

opt=SolverFactory('CPLEXamp')
results=opt.solve(model)

#print(model.S.value)

#print the marginal value of the power balance constraint
print ("Marginal cost: ",model.balance.get_suffix_value(model.dual))  

#print the total production cost
print ("Total cost: ", model.cost())

#print the optimal power output of the generators

print ("Unit1 ", model.P['Unit1'].value)
print ("Unit2 ",model.P['Unit2'].value)
print ("Unit3 ",model.P['Unit3'].value)

print ('----------')

#An alternative way:
for i in model.I:
    print (i, model.P[i].value)

print ('----------')

