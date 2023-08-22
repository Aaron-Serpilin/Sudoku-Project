#Local tests are run with python -m unittest -v, and remote tests are run with udacity submit

from utils import *

board = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[rows[i] + cols[i] for i in range(9)]] + [[rows[i] + cols[::-1][i] for i in range(9)]]
unit_list = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes) 
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) 
diagonal_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

def grid_values(grid):

    values = []
    all_digits = '123456789'

    for value in grid:
        if value == '.':
            values.append(all_digits)
        elif value in all_digits:
            values.append(value)

    assert len(values) == 81
    grid_dictionary = dict(zip(boxes, values))
    return grid_dictionary


def naked_twins(values):

    for unit in unit_list:
        for box in unit:
            #print(f'The box is {box} and its value is {values[box]}\n')


    raise NotImplementedError

#naked_twins(grid_values(diagonal_grid))

def eliminate(values):
    value_keys = values.keys()
    solved_values = [box for box in value_keys if len(values[box]) == 1] #Returns the boxes that have solved values based on the prompted grid

    for box in solved_values: #Loop through every box in the grid
        digit = values[box] #Digit equals the values of the solved boxes
        peers_of_solved_boxes = peers[box] #Equals the peers of the solved box

        for peer in peers_of_solved_boxes: #Systematically loop through all the peers of the solved boxes, and if the digit of the solved box is in the digit string of one of its peers, it is removed. This is done repeatedly
            values[peer] = values[peer].replace(digit,'')

    return values #Returns a grid that has only solved boxes and a smaller list of possible numbers for the unsolved boxes

def only_choice(values):

    all_digits = '123456789'
    
    for unit in unit_list: 
        for digit in all_digits: 
            boxes_with_digit = [box for box in unit if digit in values[box]] #This variable stores the peer boxes that contain the certain digit 
            if len(boxes_with_digit) == 1: #If only one box from the peer boxes contains the certain digit, it means it is the only possible place where it can fit, it is the only choice
                values[boxes_with_digit[0]] = digit

    return values

def reduce_puzzle(values):

    # TODO: Modify it to complete this function

    stalled = False
    while not stalled:

        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1]) #Checks how many boxes have a determined value, meaning they have been solved
        values = eliminate(values) #Use the Eliminate Strategy
        values = only_choice(values) #Use the Only Choice Strategy
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1]) #Checks how many boxes have a determined value, to compare
        stalled = solved_values_before == solved_values_after  #If no new values were added, stop the loop. This means it cannot further reduce the sudoku grid through merely these two constraints

        if len([box for box in values.keys() if len(values[box]) == 0]): #Sanity check, return False if there is a box with zero available values:
            return False
        
    return values

def search(values):
     
    # TODO: Modify it to complete this function
    
    if values is False: #Sanity check for if it fails earlier. A false value would mean the grid is unsolvable
        return False 
    
    if all(len(values[chosen_box]) == 1 for chosen_box in boxes): #Checks if it has been solved
        return values 
    
    fewest_possibilities, chosen_box = min((len(values[chosen_box]), chosen_box) for chosen_box in boxes if len(values[chosen_box]) > 1) #Chooses one of the unfilled squares with the minimal possibilities
   
    for value in values[chosen_box]:  #Recursively creates a new sudoku and attempts at solving it
        new_sudoku = values.copy()
        new_sudoku[chosen_box] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
   
    raise NotImplementedError


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
