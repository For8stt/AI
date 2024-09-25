import random
import copy

my2dlist = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0],
    [0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
my2dlist_copy = copy.deepcopy(my2dlist)

width = 12
high = 10
stones = 6
allScore = width * high - stones
which_side = ['left', 'top', 'right', 'bottom']
Directions = {
    'left': (0, -1),  # Move right
    'right': (0, 1),  # Move left
    'top': (-1, 0),  # Move down
    'bottom': (1, 0)  # Move up
}


def swap_choice(choice):
    return {
        'left': 'right',
        'right': 'left',
        'top': 'bottom',
        'bottom': 'top'
    }.get(choice)


class Person:
    def __init__(self, number, genLenght):
        self.number = number
        self.steps = 0
        self.movement = 0

        self.genes = []
        self.genLenght = genLenght
        self.acGenes = 0
        self.acGenesModify = 0

    def increaseSteps(self):
        self.steps += 1

    def increaseMoves(self):
        self.movement += 1

    def addGenes(self, gene):
        self.genes.append(gene)
        self.acGenes += 1


class Gene:
    def __init__(self):
        self.sequence = []  # This will store the moves

    def addDNA(self, dna):
        self.sequence.append(dna)


def print_mas(arr, b, k):
    for i in range(b):
        for j in range(k):
            print(f'{arr[i][j]:>3}', end='')
        print()


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
    if choice in ['left', 'right']:
        if any([my2dlist[start_point][0] != 0, my2dlist[start_point][width - 1] != 0]):
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
        if free_entrance is None:
            return False
        row_start, col_start, choice = free_entrance
    else:
        # Set start row and column based on the chosen side
        row_start = start_point if choice in ['left', 'right'] else (0 if choice == 'top' else high - 1)
        col_start = start_point if choice in ['top', 'bottom'] else (0 if choice == 'left' else width - 1)

    print(f'Starting from: raw {row_start}, column {col_start}, direction: {choice}')

    position = [row_start, col_start]
    gen = Gene()
    gen.addDNA(position)
    person.addGenes(gen)

    person.increaseMoves()

    person.acGenesModify = person.movement-1
    kof = walking(my2dlist, choice, row_start, col_start, person)
    if not kof:
        return False
    return True


def turn_left_or_right(choice):
    if choice == 'left' or choice == 'right':
        return random.choice(['top', 'bottom'])
    else:
        return random.choice(['left', 'right'])


def can_move(row, col, map):
    return (0 <= row < len(map) and 0 <= col < len(map[0]) and map[row][col] == 0)


def is_edge(row, col, width, high):
    return row == -1 or row == high or col == -1 or col == width


flag = -1


def walking(map, choice, start_row, start_col, person):
    if map[start_row][start_col] != 0:
        free_entrance = change_position(width, high, map)
        start_row, start_col, choice = free_entrance
        print('===============')
        print(f'colision: {person.genes[person.acGenesModify]}')
        person.genes[person.acGenesModify] = [start_row, start_col]
        print(f'colision: {person.genes[person.acGenesModify ]}')
        print('===============')

    current_row = start_row
    current_col = start_col
    choice = swap_choice(choice)

    first = 1
    while True:
        # my2dlist[current_row][current_col] = person.movement
        if flag == -1:
            map[current_row][current_col] = person.movement
        else:
            map[current_row][current_col] = flag

        person.increaseSteps()

        next_row = current_row + Directions[choice][0]
        next_col = current_col + Directions[choice][1]
        if can_move(next_row, next_col, map):
            current_row = next_row
            current_col = next_col
        elif is_edge(next_row, next_col, width, high):
            return True
        else:
            choice = turn_left_or_right(choice)

            next_row = current_row + Directions[choice][0]
            next_col = current_col + Directions[choice][1]
            if can_move(next_row, next_col, map) is False:
                choice = swap_choice(choice)
                next_row = current_row + Directions[choice][0]
                next_col = current_col + Directions[choice][1]

            if first:
                # print(f'{person.acGenes} : {person.genes[person.acGenes - 1].sequence[0]} ')
                person.genes[person.acGenes - 1].addDNA('lastDNA')
                first = 0

            if can_move(next_row, next_col, map):
                current_row = next_row
                current_col = next_col
            else:
                # If no valid move is possible, stop walking
                person.genes[person.acGenes - 1].sequence[1] = 'lastDNA'
                return False


def init_population(pop_size, genLenght):
    population = []
    for i in range(pop_size):
        my2dlist_copy1 = copy.deepcopy(my2dlist_copy)
        chromosome = Person(i, genLenght)
        a = True
        while a:
            if not starting_position(width, high, my2dlist_copy1, chromosome):
                a = False
        population.append(chromosome)
        print_mas(my2dlist_copy1, high, width)
    return population


def fitness_function(individual):
    my2dlist_copy11 = copy.deepcopy(my2dlist_copy)
    individual.steps = 0
    for k in range(individual.acGenes):
        genn = individual.genes[k]
        mass = genn.sequence[0]
        choice = check_direction(mass)
        individual.acGenesModify = k

        walking(my2dlist_copy11, choice, mass[0], mass[1], individual)
    return individual.steps


def check_direction(mass):
    if mass[0] == 0:
        return 'top'
    elif mass[0] == 9:
        return 'bottom'
    elif mass[1] == 0:
        return 'left'
    else:
        return 'right'


def main(genLenght):
    population = init_population(pop_size, genLenght)
    print(fitness_function(population[0]))

pop_size = 3
genLenght = 28
main(genLenght)
