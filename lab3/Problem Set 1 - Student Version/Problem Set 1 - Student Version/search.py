from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import heapq
from queue import Empty, Queue
import queue
from collections import deque

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()

        #create the frontier  wich will be represented as a queue here (FIFO)    
        frontier = [(initial_state, [])]
        #create the explored set that will represent the explored states
        explored = set()
         # while there are more stetes in the frontier to be explored :
        while frontier: 
            # Choose the shallowest node in the frontier
            state, path = frontier.pop(0)
            # if the current state is the goal of the problem return the path that represent the solution
            if problem.is_goal(state):
                    return path
            # if the state is not explored before 
            if state not in explored:   # If unexplored node
             # add the current state to the explored set
                explored.add(state)

                #  loop over all the next states (get the children of the state)
                for action in problem.get_actions(state):#get the actions
                    successor = problem.get_successor(state, action)#get the successor
                    # this condition is repeated to make sure that we return as we find the solution and don't append exra unwanted nodes to the path
                    if problem.is_goal(successor): 
                     return path+ [action] 
                     # Append the next states to the frontier to get explored
                    frontier.append((successor, path + [action]))

        # if there is no solution then  return None :(
        return None
    
def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()
    #create the explored set that will represent the explored states
    explored = set()
    #create the frontier  wich will be represented as a stack here (LIFO)  
    frontier = [(initial_state, [])] #stack
     # while there are more stetes in the frontier to be explored :
    while frontier:
        state,path=frontier.pop()  #stack pop from last element
         # if the state is not explored before 
        if state not in explored:
            # if the current state is the goal of the problem return the path that represent the solution
            if problem.is_goal(state):
                return path
              # add the current state to the explored set
            explored.add(state) 
             #  loop over all the next states (get the children of the state)   
            for action in problem.get_actions(state):
                successor=problem.get_successor(state,action)#get the successor
                # Append the next states to the frontier to get explored 
                frontier.append((successor,path+[action]))  
           # if there is no solution then  return None :(     
    return None
    

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()

    #create the explored set that will represent the explored states
    explored = set()

    # create a dictionary to keep track of the cost of each state
    cost = {initial_state : 0}

    # create a priority queue using min heap to keep track of the frontier and the priority is the cost of the state 
    frontier = []
    #the second element of the tuple is an index to make sure that the priority queue is stable     
    heapq.heappush(frontier, (0 , 0 , initial_state , []))

    #  counter to make sure that the priority queue is stable
    counter = 1
    # while there are more stetes in the frontier to be explored :
    while frontier:

        # pop the state with that has the lowest cost  from the frontier
        path_cost , _ , state , path = heapq.heappop(frontier)

        # if the state is in the explored set continue
        if state in explored:
            continue

        # if the current state is the goal of the problem return the path that represent the solution
        if problem.is_goal(state):
            return path
            
        # add the current state to the explored set
        explored.add(state)

        #  loop over all the next states (get the children of the state)   
        for action in problem.get_actions(state):

            # get the successors 
            successor = problem.get_successor(state, action)

            # check if the successor is not in the explored set
            if successor not in explored:

                # calculate the cost of the successor
                new_cost = path_cost + problem.get_cost(state, action)

                # if the successor have a lower cost than the current cost then continue
                if successor in cost and new_cost >= cost[successor]:
                    continue

                # create the new path by appending the current action to the current path
                new_path = list(path)
                new_path.append(action)

                # update the cost of the successor to the new cost in the cost dictionary
                cost[successor] = new_cost

                # add the successor to the frontier with the new path and the new cost
                heapq.heappush(frontier, (new_cost, counter, successor,new_path))

                # increment the counter
                counter += 1
    
# if there is no solution then  return None :(  
    return None
    

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()
    #create the explored set that will represent the explored states
    explored = set()
   
   # the estimated cost of the initial state is the heuristic value of the initial state
    estimated_cost = heuristic(problem,initial_state)

    # create a dictionary to keep track of the sum of actual cost and heuristic of each state
    estimated_cost_map = { initial_state : estimated_cost }



# create a priority queue using min heap to keep track of the frontier and the priority is the sum of actual cost and heuristic of the state
    frontier = []
    # the second element of the tuple is an index to make sure that the priority queue is stable,the third element of the tuple is the actual cost of the state to use it later in the heuristic function of the successors
    # the fourth element of the tuple is the path to the current state,the fifth element of the tuple is the path
    heapq.heappush(frontier, (estimated_cost , 0 ,0, initial_state , []))

    # create a counter to keep track of the index to make sure that the priority queue is stable
    counter = 1

    # while there are more stetes in the frontier to be explored :
    while frontier:

        # pop the state with the lowest cost from the frontier
        _ , _ , actual_cost , state , path = heapq.heappop(frontier)

        # if the state is in the explored set continue
        if state in explored:
            continue

       # if the current state is the goal of the problem return the path that represent the solution
        if problem.is_goal(state):
            return path

         # add the current state to the explored set
        explored.add(state)

        #  loop over all the next states (get the children of the state) 
        for action in problem.get_actions(state):

            # get the successors
            successor = problem.get_successor(state, action)

            # check if the successor is not in the explored set
            if successor not in explored:

                # calculate the actual cost of the successor
                new_cost = actual_cost + problem.get_cost(state, action) 

                # calculate the estimated cost of the successor
                new_heuristic = heuristic(problem,successor) + new_cost

                # if the successor have a lower cost than the current cost then continue
                if successor in estimated_cost_map and new_heuristic >= estimated_cost_map[successor]:
                    continue

                # create the new path by appending the current action to the current path
                new_path = list(path)
                new_path.append(action)

                # update the estimated cost of the successor to the new estimated cost in the estimated_cost_map dictionary
                estimated_cost_map[successor] = new_heuristic

                # add the successor to the frontier with the new path and the new estimated cost
                heapq.heappush(frontier, (new_heuristic, counter,new_cost,  successor, new_path))

                # increment the counter
                counter += 1
   # if there is no solution then  return None :(  
    return None

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # NotImplemented()

    # create a counter to keep track of the index to make sure that the priority queue is stable
    counter = 1
    # create a priority queue using min heap to keep track of the frontier and the priority is the heuristic of the state 
    frontier = [(0, (counter, initial_state), [])] #(cumulative_path_cost, (node_string_representation, node), path)
    #create the explored set that will represent the explored states
    explored = set() 
    #store initial cost         
    cost = {initial_state: 0}   
    # while there are more stetes in the frontier to be explored :
    while frontier:  
         # pop the state with the lowest cost from the frontier
        _, state, path = heapq.heappop(frontier)
        state = state[1]
        # if the state is in the explored set 
        if state not in explored:     
            # if the current state is the goal of the problem return the path that represent the solution
            if problem.is_goal(state):
                return path
            # add the current state to the explored set
            explored.add(state)

             #  loop over all the next states (get the children of the state) 
            for action in problem.get_actions(state):
                # get the successors
                successor = problem.get_successor(state, action)
                if successor not in explored or cost[successor] > cost[state]:
                    cost[successor] = cost[state]
                   
                    # add the successor to the frontier with the new path and the new estimated cost
                    heapq.heappush(frontier, (cost[state]+heuristic(problem, successor),(counter, successor), path + [action]))
                    counter += 1
  # if there is no solution then  return None :(  
    return None