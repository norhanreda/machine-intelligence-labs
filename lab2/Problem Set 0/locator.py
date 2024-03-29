from typing import Any, Set, Tuple
from grid import Grid
import utils

def locate(grid: Grid, item: Any) -> Set[Tuple[int,int]]:
    '''
    This function takes a 2D grid and an item
    It should return a list of (x, y) coordinates that specify the locations that contain the given item
    To know how to use the Grid class, see the file "grid.py"  
    '''
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
    result = set()
    for i in range(0,grid.width):
        for j in range(0,grid.height):
            returned_item = grid.__getitem__((i,j))
            if(returned_item == item ):
                result.add((i,j))
    return result

    