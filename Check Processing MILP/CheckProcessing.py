# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 10:59:42 2019

@author: Kevin George
"""

#importing the pyomo objects 
from pyomo.environ import *

#creating the model object
model = AbstractModel() 

#Sets
model.Time= Set() #Set of time
model.Full= Set()#Set of full time shift
model.Part=Set()#Set of Part time shift

#Parameters
model.Fullpay = Param(model.Full)# Pay for full time worker
model.Partpay = Param(model.Part)#pay for part time worker
model.Checks = Param(model.Time)#checks processed per hour per machine
model.MaxMachine = Param(model.Time)# maximum number of machine in each time
model.Received = Param(model.Time)#max checks received in each time
model.Iteration1 = Param(model.Time,model.Full)#to represent presence of fulltime workers in each time
model.Iteration2 = Param(model.Time,model.Part)#to represent presence of parttime workers in each time
model.Minworker = Param()#minimum number of full time worker


#decision variables
#model.X= Var(model.Shift,within=NonNegativeReals) #People in each Shift
model.F= Var(model.Full,within=NonNegativeReals)# number of full time worker in each fulltime shift & nonnegative constraint
model.P= Var(model.Part,within=NonNegativeReals)# number of part time worker in each parttime shift & nonnegative constraint
model.I= Var(model.Time,within=NonNegativeReals)# number of inventory of check in each hour & nonnegative constraint


#our objective function
def minCostrule(model):
    return sum(model.Fullpay[i]*model.F[i] for i in model.Full) + sum(model.Partpay[j]*model.P[j] for j in model.Part)#sumproduct of pays of fulltime and part time worker to minimise the cost
model.minCostObj= Objective(rule=minCostrule,sense=minimize)


#Constraints
#min number of full time worker constraint
def FulltimeRule(model): 
    return sum(model.F[i] for i in model.Full)>= model.Minworker # Sum of all fulltime worker should be greater than 3 
model.FulltimeworkerConstraint = Constraint(rule=FulltimeRule)  #calling Rule 

#misleading constraint which is discarded
#def ReceivedRule(model,i): #it calls i over and over again like iteration that is why i is mentioned
    #return sum(model.Checks[i]*model.Iteration1[i,j]*model.F[j] for j in model.Full) + sum(model.Checks[i]*model.Iteration2[i,k]*model.P[k] for k in model.Part) <=model.Received[i] 
#model.ReceivedConstraints = Constraint(model.Time,rule=ReceivedRule)

#max number of workers in each hour constraint
def WorkerLimitRule(model,i): #it calls i over and over again like iteration that is why i is mentioned
    return sum(model.Iteration1[i,j]*model.F[j] for j in model.Full) + sum(model.Iteration2[i,k]*model.P[k] for k in model.Part) <=model.MaxMachine[i] # workers working at each time is less than the machine available at each time which is 13 
model.WorkerLimitConstraints = Constraint(model.Time,rule=WorkerLimitRule) #calling Rule 

#inventory checks constraint
def InventoryRule(model,i): #it calls i over and over again like iteration that is why i is mentioned
    if i==1: #considering first hour
        return sum(model.Checks[i]*model.Iteration1[i,j]*model.F[j] for j in model.Full) + sum(model.Checks[i]*model.Iteration2[i,k]*model.P[k] for k in model.Part) == model.Received[i]- model.I[i]# checks processed by full&part time people in first hour = Difference of check received in first hour and the inventory leftover of first hour
    else: #other time frames
        return sum(model.Checks[i]*model.Iteration1[i,j]*model.F[j] for j in model.Full) + sum(model.Checks[i]*model.Iteration2[i,k]*model.P[k] for k in model.Part) == model.Received[i] + model.I[i-1] - model.I[i] # checks processed by full&part time people in remaining hour = Difference of check received in each hour and the inventory leftover of that hour + previous inventory
model.InventoryConstraints = Constraint(model.Time,rule=InventoryRule)#calling Rule

def Lastinventoryrule(model):
    return model.I[10]==0 # inventory at the last hour of day =0
model.LastinventoryConstraints = Constraint(rule=Lastinventoryrule) #calling Rule


#RUNNING AN ABSTRAT MODEL
#step1= combine model and data file
data= DataPortal() # a pomo objevct that knows how to mash up models and data files
data.load(filename="CheckProcess.dat",model=model) #Loads the data file
instance= model.create_instance(data) #combine our model and data fikle to make concrtete model


optimizer = SolverFactory("glpk")#Loading the solver into an object we called optimizer
results = optimizer.solve(instance)#solving instance of the model ,
instance.pprint() # prints out all model constraints

if(results.solver.status==SolverStatus.ok) and (results.solver.termination_condition==TerminationCondition.optimal):
    instance.display() #tells us about solution
   
elif(results.solver.termination_condition==TerminationCondition.infeasible or results.solver.termination_condition == TerminationCondition.other):
    print("Model is INFEASIBLE. Consider removing/relaxing constraints")
else:
    print("Solver Status: ",results.solver.status)
    print("Termination Condition", results.solver.termination_condition)
