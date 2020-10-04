#MCNFP
from pyomo.environ import*
from pyomo.opt import SolverStatus, TerminationCondition

#Declare Model
model=AbstractModel()

#Sets
model.NODES = Set() # the set of all nodes
model.PREP= Set()
model.TEACH1= Set()
model.TEACH2= Set()
model.SUBNODE1 = Set()
model.ARCS = Set(within = model.NODES*model.NODES) # arc nodes can only come from NODES set


#Parameters
model.netDemand = Param(model.SUBNODE1) #the net demand at each nodes
model.cost = Param(model.ARCS) # the cost to travel on the ARC from i to j
model.minworker = Param(model.PREP)# min worker for prep

#Decision Variables
model.x = Var(model.ARCS, within=NonNegativeReals) # the amount sent along the ARC from i to j 


#Objective Function (minimize total costs)
def objective_rule(model):
    return (sum(model.x[i,j]*model.cost[i,j] for (i,j) in model.ARCS))
model.minimise = Objective(rule= objective_rule,sense=minimize)

#net demand constraint for subnode
def net_demand_rule(model,i):
    return (sum(model.x[k,i] for k in model.NODES if (k,i) in model.ARCS)\
               - sum(model.x[i,j] for j in model.NODES if (i,j) in model.ARCS)==model.netDemand[i])
model.netDemandConstraints= Constraint(model.SUBNODE1,rule= net_demand_rule)

#teach 1 constraint
def net_demand_rule1(model,i):
    return (sum(model.x[k,i] for k in model.NODES if (k,i) in model.ARCS)\
               - sum(model.x[i,j] for j in model.NODES if (i,j) in model.ARCS)==(-1*sum(model.x[l,i] for l in model.NODES if (l,i) in model.ARCS)))
model.netDemandConstraints1= Constraint(model.TEACH1,rule= net_demand_rule1)

#teach 2 constraint
def net_demand_rule2(model,i):
    return (sum(model.x[k,i] for k in model.NODES if (k,i) in model.ARCS)\
               - sum(model.x[i,j] for j in model.NODES if (i,j) in model.ARCS)==(-2*sum(model.x[l,i] for l in model.NODES if (l,i) in model.ARCS)))
model.netDemandConstraints2= Constraint(model.TEACH2,rule= net_demand_rule2)

#minworker constriant
def weekrule(model,i):
    return(sum(model.x[j,i] for j in model.NODES if (j,i) in model.ARCS)>=model.minworker[i])
model.firstweekconstraint =Constraint(model.PREP,rule=weekrule)


#running the model
data = DataPortal() # creates a Data Portal object that knows how to read and manipulate data files
data.load(filename="Store opening.dat", model=model) # loads the data file 
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