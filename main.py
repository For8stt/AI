import random

my2dlist = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0],
    [0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
width = 12
high = 10
which_side = ['left', 'top', 'right', 'bottom']
Directions = {
    'left': (0, -1),  # Move right
    'right': (0, 1),  # Move left
    'top': (-1, 0),  # Move down
    'bottom': (1, 0)  # Move up
}
class Person:
    def __init__(self, number):
        self.number = number
        self.steps = 0
        self.movement = 0
    def increaseSteps(self):
        self.steps += 1
    def increaseMoves(self):
        self.movement += 1

def print_mas(arr, b, k):
    for i in range(b):
        for j in range(k):
            print(f'{arr[i][j]:>3}', end='')
        print()


print_mas(my2dlist, high, width)

def change_position(width, high, my2dlist):
    for row in range(high):  # Left and Right sides
        if my2dlist[row][0] == 0:  # Left side (first column)
            return row, 0, 'left'
        if my2dlist[row][width - 1] == 0:  # Right side (last column)
            return row, width - 1, 'right'

    for col in range(width):  # Top and Bottom sides
        if my2dlist[0][col] == 0:  # Top side (first row)
            return 0, col, 'top'
        if my2dlist[high - 1][col] == 0:  # Bottom side (last row)
            return high - 1, col, 'bottom'

    return None  # No free position found
def start_point_occupied(start_point, choice, my2dlist, width, high):
    print('start point was occupied')
    if choice in ['left', 'right']:
        if any([my2dlist[start_point][0] != 0 , my2dlist[start_point][width - 1] != 0]):
            return True
        else:
           return False
    else:
        if any([my2dlist[0][start_point] != 0, my2dlist[high - 1][start_point] != 0]):
            return True
        else:
           return False

def starting_position(width, high, my2dlist, person):
    choice = random.choice(which_side)
    start_point = random.randint(0, high - 1 if choice in ['left', 'right'] else width - 1)
    if start_point_occupied(start_point, choice, my2dlist, width, high):
        free_entrance = change_position(width, high, my2dlist)
        if free_entrance == None:
            return False
        row_start, col_start, choice = free_entrance
    else:
        # Set start row and column based on the chosen side
        row_start = start_point if choice in ['left', 'right'] else (0 if choice == 'top' else high - 1)
        col_start = start_point if choice in ['top', 'bottom'] else (0 if choice == 'left' else width - 1)

    print(f'Starting from: raw {row_start}, column {col_start}, direction: {choice}')
    person.increaseMoves()
    kof = walking(my2dlist, choice, row_start, col_start, person)
    if not kof:
        return False
    return True

def turn_left_or_right(choice):
    if choice == 'left' or choice == 'right':
        return random.choice(['top', 'bottom'])
    else:
        return random.choice(['left', 'right'])

def can_move(row, col, my2dlist):
    return (0 <= row < len(my2dlist) and 0 <= col < len(my2dlist[0]) and my2dlist[row][col] == 0)

def is_edge(row, col, width, high):
    return row == -1 or row == high or col == -1 or col == width


def swap_choice(choice):
    return {
        'left': 'right',
        'right': 'left',
        'top': 'bottom',
        'bottom': 'top'
    }.get(choice)


def walking(my2dlist, choice, start_row, start_col,person):
    current_row = start_row
    current_col = start_col
    choice = swap_choice(choice)

    while True:
        my2dlist[current_row][current_col] = person.movement
        person.increaseSteps()

        next_row = current_row + Directions[choice][0]
        next_col = current_col + Directions[choice][1]
        if can_move(next_row, next_col, my2dlist):
            current_row = next_row
            current_col = next_col
        elif is_edge(next_row, next_col, width, high):
            return True
        else:
            choice = turn_left_or_right(choice)

            next_row = current_row + Directions[choice][0]
            next_col = current_col + Directions[choice][1]
            if not can_move(next_row, next_col, my2dlist):
                choice = swap_choice(choice)
                next_row = current_row + Directions[choice][0]
                next_col = current_col + Directions[choice][1]

            if can_move(next_row, next_col, my2dlist):
                current_row = next_row
                current_col = next_col
            else:
                # If no valid move is possible, stop walking
                return False

person1 = Person(1)
a = True
while a:
    if not starting_position(width, high, my2dlist, person1):
        a = False

print_mas(my2dlist, high, width)
print(person1.steps)
print(person1.movement)
