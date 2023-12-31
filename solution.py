from utils import *

board = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[rows[i] + cols[i] for i in range(9)]] + [[rows[j] + cols[::-1][j] for j in range(9)]]
unit_list = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes) 
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) 
diagonal_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
hard_grid = '.....6....59.....82....8....45........3........6..3.54...325..6..................'

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

def naked_twins(values):

    print(f'\nThe initial values are:\n')
    display(values)
    list_of_twin_pairs = []

    for unit in unit_list:
        for box in unit:
            box_value = values[box]
            if len(box_value) == 2:
                first_twin = (box_value, box)
                if first_twin not in list_of_twin_pairs:
                    for peer in unit:
                        peer_value = values[peer]
                        if peer != box and box_value == peer_value:
                            second_twin = (peer_value, peer)
                            list_of_twin_pairs.append((first_twin, second_twin))

    for twin_pairs in list_of_twin_pairs:
        
        first_twin = twin_pairs[0]
        first_twin_location = first_twin[1]
        second_twin = twin_pairs[1]
        second_twin_location = second_twin[1]
        twins_pair_value = first_twin[0]
        twin_first_digit = twins_pair_value[0]
        twin_second_digit = twins_pair_value[1]
        twin_boxes = []

       
       #Boxes in the same unit as the twins and not all the peers. The problem is that I have blank values for some reason. Have to debug this
        for unit in units[first_twin_location]:
            if first_twin_location in unit and second_twin_location in unit:
                twin_boxes.append(unit)

        #print(f'The twin boxes are:\n{twin_boxes}\n')
        # print(f'The intermediary table is:\n')
        # display(values)

        for current_twin_unit in twin_boxes:
           for current_unit_value in current_twin_unit:
                #print(f'The current unit value is:\n{current_unit_value}\n')
                if values[current_unit_value] != twins_pair_value:
                    #print(f'The current value is: {values[current_unit_value]}\nThe twin number is: {twins_pair_value}')
                    values[current_unit_value] = values[current_unit_value].replace(twin_first_digit, '')
                    values[current_unit_value] = values[current_unit_value].replace(twin_second_digit, '')
                    #print(f'The current value after changing is: {values[current_unit_value]}\n')
            
    # print('The final values are:\n')
    # display(values)
    return values

def reduce_puzzle(values):

    stalled = False
    while not stalled:

        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1]) #Checks how many boxes have a determined value, meaning they have been solved
        values = eliminate(values) #Use the Eliminate Strategy
        values = only_choice(values) #Use the Only Choice Strategy
        values = naked_twins(values) #Use the Naked Twins Strategy
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1]) #Checks how many boxes have a determined value, to compare
        stalled = solved_values_before == solved_values_after  #If no new values were added, stop the loop. This means it cannot further reduce the sudoku grid through merely these two constraints

        if len([box for box in values.keys() if len(values[box]) == 0]): #Sanity check, return False if there is a box with zero available values:
            return False
        
    return values


def search(values):
      
    values = reduce_puzzle(values)

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

def solve(grid):

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
