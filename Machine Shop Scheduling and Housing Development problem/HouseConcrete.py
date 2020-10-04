# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 10:59:42 2019

@author: KEVIN GEORGE
"""
#importing the pyomo libraries
from pyomo.environ import *
#makes a concrete model object (like a blank piece of paper we will write our model on)
model = ConcreteModel() 

#decision variables
model.H = Var(within=NonNegativeIntegers) #Non Negativity Constraint-number of single house
model.D = Var(within=NonNegativeIntegers)  #Non Negativity Constraint-number of Duplex 
model.Z1 = Var(within=NonNegativeReals)  #Non Negativity Constraint - peicewise function DV
model.Z2 = Var(within=NonNegativeReals)  #Non Negativity Constraint-peicewise function DV
model.Z3 = Var(within=NonNegativeReals)  #Non Negativity Constraint -peicewise function DV
model.Z4 = Var(within=NonNegativeReals)   #Non Negativity Constraint-peicewise function DV
model.Y1 = Var(domain= Binary) #binary -peicewise function binary1
model.Y2 = Var(domain= Binary)  #binary -peicewise function binary2
model.Y3 = Var(domain= Binary) #binary -peicewise function binary3

#objective function
model.maxProfit = Objective(expr=140000*model.H-85000*model.D-90000*model.H+0*model.Z1+3000000*model.Z2+7050000*model.Z3+15800000*model.Z4, sense=maximize)#max profit

# constraints
model.Constraint1 = Constraint(expr = model.D + model.H <=120)  #
model.Constraint2 = Constraint(expr = 3*model.D >= model.H) #Duplex to house ratio
model.Constraint3 = Constraint(expr = model.D+1.75*model.H<=150) #acres of land constraint


#piecewise function constraint for selling price of Duplex 
model.Constraint11 = Constraint(expr = model.Z1<=model.Y1) #piecewise function constraint for selling price of Duplex 
model.Constraint12 = Constraint(expr =model.Z2<=model.Y1+model.Y2)  #piecewise function constraint for selling price of Duplex
model.Constraint13 = Constraint(expr=model.Z3<=model.Y2+model.Y3) 
model.Constraint14 = Constraint(expr=model.Z4<=model.Y3)  
model.Constraint15 = Constraint(expr=model.Y1+model.Y2+model.Y3==1) 
model.Constraint16 = Constraint(expr=model.Z1+model.Z2+model.Z3+model.Z4==1)
model.Constraint17 = Constraint(expr=0*model.Z1+20*model.Z2+50*model.Z3+120*model.Z4==model.D)


#activate / deactivate constraints (You don't need these if all your constraints will always be active)
#all constraints are active by default, if you would like to deactivate a constraint change activate() to deactivate()
# =============================================================================
# model.eqConstraint1.activate()
# model.eqConstraint2.activate()
# model.eqConstraint3.activate()
# model.maxConstraint1.activate()
# model.maxConstraint2.activate()
# model.maxConstraint3.activate()
# model.maxConstraint4.activate()
# model.maxConstraint5.activate()


optimizer = SolverFactory("glpk")#Loading the solver into an object we called optimizer
results = optimizer.solve(model)
model.pprint() # prints out all model constraints

if(results.solver.status==SolverStatus.ok) and (results.solver.termination_condition==TerminationCondition.optimal):
    model.display()
 
    
elif(results.solver.termination_condition==TerminationCondition.infeasible or results.solver.termination_condition == TerminationCondition.other):
    print("Model is INFEASIBLE. Consider removing/relaxing constraints")
else:
    print("Solver Status: ",results.solver.status)
    print("Termination Condition", results.solver.termination_condition)
