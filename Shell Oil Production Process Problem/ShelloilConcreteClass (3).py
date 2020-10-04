# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 10:59:42 2019

@author: KEVIN GEORGE
"""
#importing the pyomo libraries
from pyomo.environ import *
#makes a concrete model object (like a blank piece of paper we will write our model on)
model = ConcreteModel() 

#decision variables
model.Gas1 = Var(within=NonNegativeReals) #Non Negativity Constraint
model.Gas2 = Var(within=NonNegativeReals)  #Non Negativity Constraint  
model.Gas3 = Var(within=NonNegativeReals)  #Non Negativity Constraint
model.Process1 = Var(within=NonNegativeReals)  #Non Negativity Constraint
model.Process2 = Var(within=NonNegativeReals)  #Non Negativity Constraint
model.Process3 = Var(within=NonNegativeReals)   #Non Negativity Constraint
model.Crude1 = Var(within=NonNegativeReals)  #Non Negativity Constraint
model.Crude2 = Var(within=NonNegativeReals)  #Non Negativity Constraint

#objective function
model.maxProfit = Objective(expr=9*model.Gas1+10*model.Gas2+24*model.Gas3-5*model.Process1-4*model.Process2-1*model.Process3-2*model.Crude1-3*model.Crude2, sense=maximize)

#equal constraints
model.eqConstraint1 = Constraint(expr = 2*model.Process1-1*model.Gas1==0)  #Total barrel of gas1 to sell
model.eqConstraint2 = Constraint(expr = 1*model.Process1+3*model.Process2-3*model.Process3-1*model.Gas2==0 ) #Total barrel of gas2 to sell
model.eqConstraint3 = Constraint(expr = 2*model.Process3-1*model.Gas3==0 ) #Total barrel of gas3 to sell


#max Constraints
model.maxConstraint1 = Constraint(expr = 1*model.Crude1<=200) #Maximum available barrels of crude 1 per week
model.maxConstraint2 = Constraint(expr =1*model.Crude2<=300)  #Maximum available barrels of crude 2 per week
model.maxConstraint3 = Constraint(expr=1*model.Process1+1*model.Process2+1*model.Process3<=100) #Maximum available hours for process in catalytic cracker
model.maxConstraint4 = Constraint(expr=2*model.Process1+1*model.Process2-1*model.Crude1<=0)  #Amount of crude 1 to run the process
model.maxConstraint5 = Constraint(expr=3*model.Process1+3*model.Process2+2*model.Process3-1*model.Crude2<=0) #Amount of crude 2 to run the process
#model.maxConstraint6 = Constraint(expr=1*model.Process1+3*model.Process2>=3*model.Process3) #Total barrel of gas2 to sell


#activate / deactivate constraints (You don't need these if all your constraints will always be active)
#all constraints are active by default, if you would like to deactivate a constraint change activate() to deactivate()
model.eqConstraint1.activate()
model.eqConstraint2.activate()
model.eqConstraint3.activate()
model.maxConstraint1.activate()
model.maxConstraint2.activate()
model.maxConstraint3.activate()
model.maxConstraint4.activate()
model.maxConstraint5.activate()
#model.maxConstraint6.activate()


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
