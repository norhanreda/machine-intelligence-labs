from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        # NotImplemented()
        # if the state is terminal return 0
        if self.mdp.is_terminal(state):
            return 0
        # U(s) = max( sum( P(s'|s,a) * (R(s,a,s') + gamma * U(s')) for s' in S ) for a in A )
        return max([sum([self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action)]) for action in self.mdp.get_actions(state)])    
    
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function
        # NotImplemented()
        # update the utilities of all the states using the bellman equation and store them in a dictionary 
        utility_updates = {state: self.compute_bellman(state) for state in self.mdp.get_states()}
        #get the max utility change
        max_utility_change = max([abs(utility_updates[state] - self.utilities[state]) for state in self.mdp.get_states()])
        # update the utilities in the agent 
        self.utilities = utility_updates
        # return True if the maximum change in the utilities is less than or equal the tolerance and false otherwise
        return   max_utility_change <= tolerance
            

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        #TODO: Complete this function to apply value iteration for the given number of iterations
        # NotImplemented()
        # Initialize the iteration counter
        iteration = 0
        # Continue iterating until the specified number of iterations is reached or indefinitely if 'iterations' is None
        while iterations is None or iteration < iterations:
            # Increment the iteration counter
            iteration += 1
            # Check if the update method with the given tolerance returns True 
            if self.update(tolerance):
                # Break out of the loop if the update is successful
                break
        # return the total number of iterations performed
        return iteration
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        # NotImplemented()
        # if the state is terminal return None
        if self.mdp.is_terminal(state):
            return None   
        
        else:
            # get the action that have the maximum expected utility
            # same code as bellman equation  instead of computing the maximum utility compute the action that has the maximum utility and if there is more than action return the first of them
            return max([action for action in self.mdp.get_actions(state)], key=lambda action: sum([self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action)]))

    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
