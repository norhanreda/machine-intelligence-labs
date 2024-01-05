from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented

# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use
from typing import Dict, Tuple
# Define a global dictionary to store precomputed distances to goals for each box
# This will help avoid redundant calculations
box_to_goal_distances: Dict[Tuple[Point, frozenset], int] = {}


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
     #TODO: ADD YOUR CODE HERE
     #IMPORTANT: DO NOT USE "problem.get_actions" HERE.
     # Calling it here will mess up the tracking of the expanded nodes count
     # which is the number of get_actions calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
     # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
     # NotImplemented()
    """
    Calculate a strong heuristic value for the given Sokoban state using deadlocks.

    Args:
        problem (SokobanProblem): The Sokoban problem instance.
        state (SokobanState): The Sokoban state for which to calculate the heuristic.

    Returns:
        float: The strong heuristic value for the given state.
    """
    if problem.is_goal(state):
        return 0.0  # The state is already a goal state

    total_distance = 0

    # Calculate the distance from each crate to the nearest goal
    for box in state.crates:
        
        if box in state.layout.goals:
            continue
        # Check if the crate is in a deadlock state
        if is_deadlock(problem, state,box):
            # Return a large value  infinity
            return float('inf')  

        # Check if we have already computed this distance before
        if (box, frozenset(state.layout.goals)) in box_to_goal_distances:
            total_distance += box_to_goal_distances[(box, frozenset(state.layout.goals))]
        else:
            min_distance = float('inf')
            for goal in state.layout.goals:
                # Calculate the Manhattan distance from the box to the goal
                distance =  manhattan_distance(goal,box)
                min_distance = min(min_distance, distance)
            total_distance += min_distance
            # Cache the distance for future use
            box_to_goal_distances[(box, frozenset(state.layout.goals))] = min_distance

    return total_distance



def is_deadlock(problem: SokobanProblem, state: SokobanState, crate: Point) -> bool:

    # Extract the x and y coordinates of the crate
    bx, by = crate.x, crate.y 

    # Condition 1: Check for corner deadlocks
    # checks for corner deadlocks. It evaluates whether any of the four corners around the crate are blocked 
    # (state.layout.walkable represents the walkable areas of the layout). 
    # If all four corners are blocked, indicating that the crate is stuck in a corner, a corner deadlock is detected.
    
    if (
        (Point(bx - 1, by) not in state.layout.walkable and Point(bx, by - 1) not in state.layout.walkable) or 
        (Point(bx - 1, by) not in state.layout.walkable and Point(bx, by + 1) not in state.layout.walkable) or
        (Point(bx + 1, by) not in state.layout.walkable and Point(bx, by - 1) not in state.layout.walkable) or
        (Point(bx + 1, by) not in state.layout.walkable and Point(bx, by + 1) not in state.layout.walkable)
      ):
        return True  # Corner deadlock detected

  

    # Condition 2: Check for edge deadlocks
    # Check if the current crate is at the edge and there are no goals on that edge
    # checks if the crate is located at an edge and there are no goals on that edge. It evaluates whether the crate is positioned 
    # at the second-to-last row or column (bx == problem.layout.width - 2 or by == problem.layout.height - 2) 
    # and checks if there are no goals present on that edge. If these conditions are met, it indicates an edge deadlock.
    if(
            
            
            (bx == problem.layout.width - 2 and len([goal for goal in problem.layout.goals if goal.x == problem.layout.width - 2]) == 0) or
            (by == problem.layout.height - 2 and len([goal for goal in problem.layout.goals if goal.y == problem.layout.height - 2]) == 0) or
            (bx == 1 and len([goal for goal in problem.layout.goals if goal.x == 1]) == 0) or
            (by == 1 and len([goal for goal in problem.layout.goals if goal.y == 1]) == 0)
    ):
         return True #  Edge deadlock detected
    # Condition 3: Check for adjacent crates
    # Check if there is an adjacent crate and it is blocking the movement of the current crate
    # checks if there is an adjacent crate blocking the movement of the current crate. It evaluates whether there is a 
    # crate present at the positions adjacent to the current crate (Point(bx - 1, by), Point(bx, by - 1), Point(bx + 1, by), 
    #  Point(bx, by + 1)). It also checks if the adjacent crate is blocking the movement by verifying if there is an obstacle 
    #  (wall or boundary) either one step before or after the adjacent crate. 
    #  If any of these conditions are met, it indicates a deadlock caused by adjacent crates.
         
    if(
            Point(bx - 1, by) in state.crates and (bx - 2 == 0 or bx + 2 == state.layout.width) or
            Point(bx, by - 1) in state.crates and (by - 2 == 0 or by + 2 == state.layout.height) or
            Point(bx + 1, by) in state.crates and (bx - 1 == 0 or bx + 3 == state.layout.width) or
            Point(bx, by + 1) in state.crates and (by - 1 == 0 or by + 3 == state.layout.height)
     ):
             return True #adjacent crates deadlock detected
    
    
    # Condition 4: Check for box surrounded by other boxes deadlock
    # evaluates if the current crate is surrounded by other crates in all three cardinal directions or four  . 
    # It checks if the adjacent positions to the left, right, above, and below the current crate 
    # If three or four adjacent positions have crates, indicating that the current crate is surrounded by other crates,
    #  a box surrounded by other boxes deadlock is detected.

    sides_count = 0
    if( bx - 1 ==  0 or Point(bx - 1, by) not in state.layout.walkable or Point(bx - 1, by) in state.crates ):
        sides_count += 1
    if(Point(bx + 1, by) not in state.layout.walkable or Point(bx + 1, by) in state.crates or bx + 1 == state.layout.width - 1):
        sides_count += 1
    if( by - 1 == 0 or Point(bx , by + 1) not in state.layout.walkable or Point(bx, by + 1) in state.crates ):
        sides_count += 1
    if(Point(bx , by - 1) not in state.layout.walkable or Point(bx, by - 1) in state.crates or by + 1 == state.layout.height - 1):
        sides_count += 1

    if(sides_count ==3 or sides_count==4):
        return True # Box surrounded by other boxes deadlock detected
    
  
    # No deadlock condition found
    return False
    