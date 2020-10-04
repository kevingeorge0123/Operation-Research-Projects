#Transportation Problem Formulation

from pyomo.environ import*
#Declare Model
model=AbstractModel()

#sets
model.SUPPLIES = Set() #set of supply nodes
model.DEMANDS = Set() #set of demand nodes

#parameters
model.s = Param(model.SUPPLIES) # the supply available at each node
model.d = Param(model.DEMANDS) # the demand required at each demand node
model.c = Param(model.SUPPLIES,model.DEMANDS) #the cost of shipping from supply point i to demand point j

#decision variables: x[i,j] = amount shipped from supply point i to demand point join
model.x= Var(model.SUPPLIES,model.DEMANDS,within=NonNegativeReals)


#objective function: minimize cost to meet demands
def objective_rule(model):
    return sum(model.c[i,j]*model.x[i,j] for i in model.SUPPLIES for j in model.DEMANDS)
model.minCost = Objective(rule=objective_rule,sense=minimize)



#Supply Constraints
def SupplyRule(model,i):
    return sum(model.x[i,j] for j in model.DEMANDS) == model.s[i]
model.supplyconstraint = Constraint(model.SUPPLIES,rule=SupplyRule)

#Demand Constraints
def demandrule(model,j):
    return sum(model.x[i,j] for i in model.SUPPLIES) == model.d[j]
model.demandconstraint = Constraint(model.DEMANDS,rule=demandrule)
    
    



#running the model
data = DataPortal() # creates a Data Portal object that knows how to read and manipulate data files
data.load(filename="PowerCoData.dat", model=model) # loads the data file 
instance = model.create_instance(data) # combines the model and data file into a 'concrete' model

optimizer = SolverFactory("glpk")
results = optimizer.solve(instance)
instance.pprint() # prints out all model constraints


if(results.solver.status==SolverStatus.ok) and (results.solver.termination_condition==TerminationCondition.optimal):
    instance.display()
elif(results.solver.termination_condition==TerminationCondition.infeasible or results.solver.termination_condition == TerminationCondition.other):
    print("\n\nModel is INFEASIBLE. Consider removing/relaxing constraints")
else:
    print("Solver Status: ",results.solver.status)
    print("Termination Condition", results.solver.termination_condition)
