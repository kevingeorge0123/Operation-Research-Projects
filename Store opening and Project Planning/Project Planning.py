#MCNFP
from pyomo.environ import*
from pyomo.opt import SolverStatus, TerminationCondition

#Declare Model
model=AbstractModel()

#Sets
model.NODES = Set() # the set of all nodes
model.SOURCE=Set()
model.ARCS = Set(within = model.NODES*model.NODES) # arc nodes can only come from NODES set


#Parameters
model.netDemand = Param(model.NODES) #the net demand at each nodes
model.capacity = Param(model.ARCS) # capacity param

#Decision Variables
model.x = Var(model.ARCS, within=NonNegativeReals) # the amount sent along the ARC from i to j 



#Objective Function (maximise man month)
def objective_rule(model):
    return (sum(model.x[i,j] for i in model.SOURCE for j in model.NODES if (i,j) in model.ARCS))
model.maximise = Objective(rule= objective_rule,sense=maximize)

#net demand constraint for each nodes
def net_demand_rule(model,i):
    return (sum(model.x[k,i] for k in model.NODES if (k,i) in model.ARCS)\
               - sum(model.x[i,j] for j in model.NODES if (i,j) in model.ARCS)==model.netDemand[i])
model.netDemandConstraints= Constraint(model.NODES,rule= net_demand_rule)

#capacity constraint
def capacityrule(model,i,j):
        return (model.x[i,j] <= model.capacity[i,j]  )
model.capacityConstraints = Constraint(model.ARCS,rule= capacityrule)



#running the model
data = DataPortal() # creates a Data Portal object that knows how to read and manipulate data files
data.load(filename="Project Planning.dat", model=model) # loads the data file 
instance = model.create_instance(data) # combines the model and data file into a 'concrete' model

optimizer = SolverFactory("glpk")
results = optimizer.solve(instance)
instance.pprint() # prints out all model constraints


if(results.solver.status==SolverStatus.ok) and (results.solver.termination_condition==TerminationCondition.optimal):
    instance.display()
    
    #print out only those rodes that are travelled from start to finish
    #end='T'     #where we want to end up
    #currentPosition = 'S' #where we start in the network
    #while currentPosition != end:
        #for (k,j) in instance.ARCS:
            #if k==currentPosition:
                #if instance.x[k,j]()>0:
                    #print("Go from ", k," to ",j)
                    #currentPosition = j
                    #break
    
elif(results.solver.termination_condition==TerminationCondition.infeasible or results.solver.termination_condition == TerminationCondition.other):
    print("\n\nModel is INFEASIBLE. Consider removing/relaxing constraints")
else:
    print("Solver Status: ",results.solver.status)
    print("Termination Condition", results.solver.termination_condition)