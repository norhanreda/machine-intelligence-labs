from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point] # mhtaga ttfhm

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        # return the initial state which is the initial place of the cars
        return self.cars
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()

        #check if all cars are in their correct parking slots so we reach goal
        for point in self.slots:
            if state[self.slots[point]] != point :
                return False
        return  True       

    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        # List of actions that could happen  for each car
        actions = [] #list of action
        # this index represents the  car
        index = 0
        
        #for each car
        for point in state:
            #loop over all possible actions (R,L,U,D)
            for direction in Direction:
                # add the direction to the car current position to get the new location 
                new_location = point +direction.to_vector() # convert the direction to vector to be addable to point
                check=True 
                 #disallow hitting a wall
                if new_location not in self.passages:
                    continue
                #disallow walking on another car
                for i in range(len(state)):
                    #check for all car states positions that aren't  the same as the position I want to go to 
                    if new_location == state[i]:
                        check=False
                        break
                # if the action is a valid action append it to the action lists
                if check:
                    actions.append((index,direction.__str__()))    
             #increase the index to the next car       
            index=index+1    
        return actions



            
     

    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # NotImplemented()
        #get the car number that the action will be performed on it 
        car_num = action[0]
        # get the direction of the action
        direction = action[1].to_vector()
        #get the current car state(position)
        car_position = state[car_num]
        #get the new location of the car based on the action
        new_location = car_position + direction
        #make the new state from old state
        new_state = list(state)
        #update the state of the current car num based on the action
        new_state[car_num] = new_location

        #return the state after updating the action 
        return tuple(new_state)
    

    #     return rank_cost  # Cost based on the rank only (no annoying)
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #get the car number that the action will be performed on it 
        car_num = action[0]
        # get the direction of the action
        direction = action[1].to_vector()
         #get the current car state(position)
        car_position = state[car_num]
        #get the new location of the car based on the action
        new_location = car_position + direction

        # Calculate rank based on car number
        rank = chr(ord('A') - car_num) 

        # Calculate action cost based on rank 
        action_cost = ord(rank) - ord('A') + 26  
        # Check if the new position is not in the parking slots
        if new_location not in self.slots:
            # Return the action cost if the new position is not a parking slot
            return action_cost
        # Check if the new position is occupied by another car
        elif self.slots[new_location] != car_num:
            # Return the action cost with an additional penalty for attempting to move into an occupied space
            return action_cost + 100
        else:
            # The new position is a valid parking slot, return the action cost
            return action_cost




    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
