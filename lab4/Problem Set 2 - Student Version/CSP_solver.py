from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    #TODO: Write this function
    # NotImplemented()
    #loop over all the constrains to apply the binary constarins
    for constraint in problem.constraints:
         #check if the constrain is binary and the assigned variable in the constrain variables
         if(type(constraint) == BinaryConstraint) and (assigned_variable in constraint.variables): 
                #get the other variables that is in the constrain
                other_variable = constraint.get_other(assigned_variable)
                #If the other variable has no domain (in other words, it is already assigned), skip this constraint.
                if(other_variable not in domains):
                    continue
                # create a new domain for the variables
                new_domain = set()
                # loop over the values in the domain of the other variable
                for value in domains[other_variable]:
                    #make the new assignmengt that has the assigned value and the other variable to be assigned with value from its domain
                    assignment = {assigned_variable: assigned_value, other_variable: value}
                    #check if the assignment satisfy the constrain
                    if constraint.is_satisfied(assignment):
                          new_domain.add(value)     
                #if the new domain has no values to satisfy the constrain so there is no solution
                if len(new_domain)==0:
                    return False
                #update the domain of the other vaiable by the new domain as the new domain that have values that satisfy the constrain
                domains[other_variable]=new_domain
    # all the binary constraints are satisfied return True
    return True 

# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    #TODO: Write this function
    # NotImplemented()
    
    #list to store  [values that removes values from other variables ]= the number of removed values
    removed_values_from_domain_count = {}
    #inital values for all the removed values to be zero
    for value in domains[variable_to_assign]:
        removed_values_from_domain_count[value] = 0

    #loop over all  the values for the variable to be assigned
    for value in domains[variable_to_assign]:
        #loop over all the constaints of the problem
        for constraint in problem.constraints:
           #if the constraint is a binary constaraint and its a constraint for the variable  to be assigned 
           if(type(constraint) == BinaryConstraint and variable_to_assign in constraint.variables):
               #get the other vaiable for  the variable  to be assigned 
               other_vaiable = constraint.get_other(variable_to_assign)
               #  if the other variable has no domain =>it is already assigned skip this constraint
               if other_vaiable not in domains:
                   continue
               # loop over the values in the domain of the other variable
               for other_value in domains[other_vaiable]:
                   #make the assignment
                   assignment={variable_to_assign:value , other_vaiable:other_value}
                   #if the assignment doesn't satisfies the binary constraint
                   if not constraint.is_satisfied(assignment):
                        # if it does not increase the count of the removed values for this value
                       removed_values_from_domain_count[value] +=1
     #sort the list of removed_values_from_domain_count by the Primary Key  removed_values_from_domain_count[x] and Secondary Key 
    #if two values have the same number of removed values, the values are then sorted in alphabetical order.
    return sorted(removed_values_from_domain_count,key=lambda x: (removed_values_from_domain_count[x], x))

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    #TODO: Write this function
    # NotImplemented()
    # check if the problem is 1-consistent unary constraints is statisfied
    if one_consistency(problem): 
        # call the backtrack function to solve the problem even if it passes through endpoint then backtrack to choose another variable
        return backtracking(problem, {},problem.domains) 
    # if the problem is not 1-consistent then no solution because the unary constraints can't be satisfied
    else:
        return None
    

def backtracking(problem: Problem,assignment: Assignment, domains: Dict[str, set]) -> Optional[Assignment]:
    #if the problem is complete return the assignment
    if problem.is_complete(assignment):
        return assignment
    
    # get the next variable to be assigned using the MRV heuristic
    variable = minimum_remaining_values(problem, domains)
    # get the values for this variable in the domain using the least restraining value heuristic
    for value in least_restraining_values(problem, variable, domains):
         
        # create a copy of the assignment to prevent modifying the original assignment 
        new_assignment = assignment.copy()
        # create a copy of the domains to prevent modifying the original domains 
        new_domains = domains.copy() 
        # assign a value to the vaiable
        new_assignment[variable]=value
        #delete the vaiable from the domains because it has been assigned a value 
        del new_domains[variable]
        # check if the value is consistent with the constraints of the variable
        if forward_checking(problem, variable, value, new_domains):
            # backtrack to the next variable to be assigned 
            solution =backtracking(problem,new_assignment,new_domains)
             
            # if the solution is not none return it as it is the first solution found
            if solution is not None:
                return solution
            
    # return none as there is no solution :(
    return None        
   

