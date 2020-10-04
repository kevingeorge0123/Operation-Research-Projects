# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 10:59:42 2019

@author: Kevin George
"""

#importing the pyomo objects 
from pyomo.environ import *

#creating the model object
model = AbstractModel() 

#Sets
model.Job= Set() #Set of Job
model.Machine= Set()#Set of machine

#Parameters
model.Setup = Param(model.Machine)# setup time for machine i
model.Time = Param(model.Machine,model.Job) #operating time for machine i to do job j 
model.P =Param(model.Machine,model.Job) # presence of machine i for  job j

#decision variables

model.X= Var(model.Machine,model.Job,domain=Binary) # whether machine i used for job j -1 if used, 0 if not 
model.Y= Var(model.Machine,domain=Binary)# whether machine i is used -1 if used, 0 if not 
model.K = Var(domain=Binary) # if then constraint binary 

#minimizing setuptime and operating time
def Minimizetime(model):
    return (sum(model.Setup[i]*model.Y[i] for i in model.Machine)+sum(model.Time[i,j]*model.X[i,j]*model.P[i,j] for i in model.Machine for j in model.Job))
model.mintimeobj = Objective(rule=Minimizetime,sense=minimize)



#Constraints
# one job done by one machine constraint 
def OneJobOneMachine(model,j):
    return sum(model.X[i,j]*model.P[i,j] for i in model.Machine)==1
model.Constraint1 = Constraint(model.Job,rule=OneJobOneMachine)

#Alternate method  for  if machine 1 is used for job1 then it is used for job3
# =============================================================================
# def IfThenConstraint(model):
#     return (model.X[1,1]<=model.X[1,3])
# model.Constraint2 = Constraint(rule=IfThenConstraint)
# =============================================================================

#if machine 1 is used for job1 then it is used for job3 part1
def IfThenConstraint11(model):
    return ((1-model.X[1,3])<=model.K)
model.constraint11 = Constraint(rule=IfThenConstraint11)
#if machine 1 is used for job1 then it is used for job3 part2
def IfThenConstraint12(model):
    return (model.X[1,1]<=(1-model.K))
model.constraint12 = Constraint(rule=IfThenConstraint12)

# machine i can do max of 3 jobs- equvalent to which all machine is selected  
def maxjobconstraint(model,i):
    return (sum(model.X[i,j]*model.P[i,j] for j in model.Job)<=3*model.Y[i])
model.Constraint3 = Constraint(model.Machine,rule=maxjobconstraint)



#RUNNING AN ABSTRAT MODEL
#step1= combine model and data file
data= DataPortal() # a pomo objevct that knows how to mash up models and data files
data.load(filename="MachineShop.dat",model=model) #Loads the data file
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
