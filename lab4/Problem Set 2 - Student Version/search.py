from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import math
# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()

    #get the turn of the  start agent 0 for the player and other for the enemies (initial turn )
    start_agent = game.get_turn(state)
   
        
        
    def min_max_decision(state,depth):
         #returns if the state is terminal or not  and return the values for all the agents
        terminal, values = game.is_terminal(state) 
         # if the state is terminal return the state utility, If the given state is terminal, the returned action should be None.
        if terminal: 
          return values[start_agent] , None
    
        #if we have reached the maximum depth return the heuristic 
        if depth ==0:
                
                return heuristic(game,state,start_agent),None
        

        # get the actions and the successors of the state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]    
        # get the current agent
        agent = game.get_turn(state)

        # if the agent is 0 return the maximum value of the successors
        if(agent==0):
            return max_value(state,depth,actions_states )
        else:
            # else return the minimum value of the successors
            return min_value(state,depth,actions_states )
         
      

    def max_value(state,depth,actions_states):
        #initialize the max value by negative infinity
        max_val = -math.inf
        #initialize  the good action by none
        good_action = None
        #loop over actions and successors
        for action,state in actions_states:
            # get the value of the successor
            successor_val = min_max_decision(state,depth-1)[0]
             #if the successor value is grater than the max value update the max value and get the good action
            if successor_val > max_val:
                max_val=successor_val
                good_action = action
        # return the max value and good action
        return max_val,good_action



    def min_value(state,depth,actions_states ):
         #initialize the min value by infinity
        min_val = math.inf
         #initialize  the good action by none
        good_action = None
         #loop over actions and successors
        for action,state in actions_states:
             # get the value of the successor
            successor_val = min_max_decision(state,depth-1)[0]
             #if the successor value is grater than the min value update the min value and get the good action
            if successor_val <=  min_val:
                min_val=successor_val
                good_action = action
              # return the min value and good action
        return  min_val,good_action
    
    return min_max_decision(state,max_depth) 


    
        
    

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()
    #get the turn of the  start agent 0 for the player and other for the enemies 
    start_agent = game.get_turn(state)
   
        
        
    def min_max_decision(state,depth,alpha,beta):
         #returns if the state is terminal or not  and return the values for all the agents
        terminal, values = game.is_terminal(state) 
         # if the state is terminal return the state utility, If the given state is terminal, the returned action should be None.
        if terminal: 
          return values[start_agent] , None
         #if we have reached the maximum depth return the heuristic 
        if depth ==0:
                
                return heuristic(game,state,start_agent),None
        # get the actions and the successors of the state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]    
       
        # get the current agent
        agent = game.get_turn(state)
        # if the agent is 0 return the maximum value of the successors
        if(agent==0):
            return max_value(state,depth,actions_states,alpha,beta )
        else:
             # else return the minimum value of the successors
            return min_value(state,depth,actions_states,alpha,beta )
         
      

    def max_value(state,depth,actions_states,alpha,beta):
          #initialize the max value by negative infinity
        max_val = -math.inf
         #initialize  the good action by none
        good_action = None
         #loop over actions and successors
        for action,state in actions_states:
             # get the value of the successor
            successor_val = min_max_decision(state,depth-1,alpha,beta)[0]
             #if the successor value is grater than the max value update the max value and get the good action
            if successor_val >max_val:
                max_val=successor_val
                good_action = action
             # if the maximum value is greater than or equal to the beta, return the maximum value and the good action
            if max_val >= beta: 
                return max_val , good_action 
             # set alpha value to the maximum of the alpha and the maximum value 
            alpha= max(alpha,max_val)  
         # return the max value and good action    
        return max_val,good_action



    def min_value(state,depth,actions_states,alpha,beta ):
        #initialize the min value by infinity
        min_val = math.inf
         #initialize  the good action by none
        good_action = None
         #loop over actions and successors
        for action,state in actions_states:
            #get the successor value
            successor_val = min_max_decision(state,depth-1,alpha,beta)[0]
             #if the successor value is grater than the min value update the min value and get the good action
            if successor_val <= min_val:
                min_val=successor_val
                good_action = action
            # if the minimum value is less than or equal to the alpha, return the minimum value and the good action
            if min_val <= alpha: 
                return min_val , good_action  
            # set beta value to the minimum of the beta and the minimum value 
            beta= min(beta,min_val)  
        # return the min value and good action
        return min_val,good_action

    return min_max_decision(state,max_depth,-math.inf,math.inf) 




# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()
    start_agent = game.get_turn(state)
   
        
        
    def min_max_decision(state,depth,alpha,beta):
         #returns if the state is terminal or not  and return the values for all the agents
        terminal, values = game.is_terminal(state) 
         # if the state is terminal return the state utility, If the given state is terminal, the returned action should be None.
        if terminal: 
          return values[start_agent] , None
        #if we have reached the maximum depth return the heuristic 
        if depth ==0:
                
                return heuristic(game,state,start_agent),None
        # get the actions and the successors of the state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]    
        # get the current agent
        agent = game.get_turn(state)
        # if the agent is 0 return the maximum value of the successors
        if(agent==0):
            return max_value(state,depth,actions_states,alpha,beta )
        else:
             # else return the minimum value of the successors
            return min_value(state,depth,actions_states,alpha,beta )
         
      

    def max_value(state,depth,actions_states,alpha,beta):
        # sort actions_states by heuristic value in descending order in a stable way
        actions_states.sort(key=lambda x: heuristic(game, x[1], 0), reverse=True)
         #initialize the max value by negative infinity
        max_val = -math.inf
         #initialize  the good action by none
        good_action = None
         #loop over actions and successors
        for action,state in actions_states:
             # get the value of the successor
            successor_val = min_max_decision(state,depth-1,alpha,beta)[0]
             #if the successor value is grater than the max value update the max value and get the good action
            if successor_val >max_val:
                max_val=successor_val
                good_action = action
             # if the maximum value is greater than or equal to the beta return the maximum value and the good action
            if max_val >= beta: 
                return max_val , good_action  
            # set alpha value to the maximum of the alpha and the maximum value
            alpha= max(alpha,max_val)  
         # return the max value and good action    
        return max_val,good_action



    def min_value(state,depth,actions_states,alpha,beta ):
        # sort actions_states by heuristic value in ascending order in a stable way
        actions_states.sort(key=lambda x: heuristic(game, x[1], 0))
        #initialize the min value by infinity
        min_val = math.inf
         #initialize  the good action by none
        good_action = None
         #loop over actions and successors
        for action,state in actions_states:
            #get the successor value
            successor_val = min_max_decision(state,depth-1,alpha,beta)[0]
             #if the successor value is grater than the min value update the min value and get the good action
            if successor_val <= min_val:
                min_val=successor_val
                good_action = action
            # if the minimum value is less than or equal to the alpha, return the minimum value and the good action
            if min_val <= alpha: 
                return min_val , good_action  
            
            # set beta value to the minimum of the beta and the minimum value 
            beta= min(beta,min_val)  
         # return the min value and good action    
        return min_val,good_action

    return min_max_decision(state,max_depth,-math.inf,math.inf) 


# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    # NotImplemented()
     #get the turn of the  start agent 0 for the player and other for the enemies 
    start_agent = game.get_turn(state)
   
        
        
    def min_max_decision(state,depth):
         #returns if the state is terminal or not  and return the values for all the agents
        terminal, values = game.is_terminal(state) 
         # if the state is terminal return the state utility, If the given state is terminal, the returned action should be None.
        if terminal: 
          return values[start_agent] , None
         #if we have reached the maximum depth return the heuristic 
        if depth ==0:
                
                return heuristic(game,state,start_agent),None
        # get the actions and the successors of the state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]    
        # get the current agent
        agent = game.get_turn(state)
        # if the agent is 0 return the maximum value of the successors
        if(agent==0):
            return max_value(state,depth,actions_states )
        else:
             # else return the expect value of the successors
            return expect_value(state,depth,actions_states )
         
      

    def max_value(state,depth,actions_states):
         #initialize the max value by negative infinity
        max_val = -math.inf
         #initialize  the good action by none
        good_action = None
         #loop over actions and successors
        for action,state in actions_states:
             # get the value of the successor
            successor_val = min_max_decision(state,depth-1)[0]
             #if the successor value is grater than the max value update the max value and get the good action
            if successor_val > max_val:
                max_val=successor_val
                good_action = action
         # return the max value and good action    
        return max_val,good_action



    def expect_value(state,depth,actions_states ):
        # initialize the expected value to 0
        expect_val = 0
        
        # loop over all the actions and the successors
        for action,state in actions_states:
            #get the successor value
            successor_val = min_max_decision(state,depth-1)[0]
            #add the successor value to the expected value
            expect_val +=successor_val
                
        expect_val = expect_val/len(actions_states) 
        
         # return the expected value and the good action   
        return  expect_val,None

    return min_max_decision(state,max_depth) 