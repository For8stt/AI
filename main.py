import copy
import random

def cdirection(pos):
    if pos[0] == 0:
        return 'right'
    elif pos[0] == 11:
        return 'left'
    elif pos[1] == 0:
        return 'down'
    else:
        return 'up'

Directions = {
    "up": (-1, 0),   # Move up (row decreases)
    "down": (1, 0),  # Move down (row increases)
    "left": (0, -1), # Move left (column decreases)
    "right": (0, 1)  # Move right (column increases)
}
turn_table = {
    "left": {
        "right": "up",
        "left": "down",
        "down": "right",
        "up": "left"
    },
    "right": {
        "right": "down",
        "left": "up",
        "down": "left",
        "up": "right"
    }
}

def generate_field(fieldProps):
    columns, rows, stones = fieldProps
    field = [[0] * columns for i in range(rows)]# creates columns then cretes rows
    for stone in stones:
        x, y = stone
        field[y][x] = -1
    return field

def print_mas(arr, b, k):
    for i in range(b):
        for j in range(k):
            print(f'{arr[i][j]:>3}', end='')
        print()

def initialize(fieldProps, populationSize):
    return [generateGenes(fieldProps) for i in range(populationSize)]
def generateGenes(fieldProps):
    pos = []
    turns = []
    high,width,stones = fieldProps
    while len(pos)<high+width :
        result = genereteStartPosition(fieldProps, pos)
        if not result:
            continue
        pos1, pos2 = result
        pos.append(pos1)
        pos.append(pos2)

    while len(turns) < len(stones):
        turns.append('right' if random.randint(0,1) == 1 else 'left')

    return {'positions': pos, 'turns': turns, 'fitness': 0}

def genereteStartPosition(fieldProps, pos):
    lenght, width, unnecessaryStones =fieldProps
    pos1 = (random.randint(0,1) * (lenght - 1), random.randint(0, width - 1)) #left or right position
    pos2 = (random.randint(0,lenght-1), random.randint(0,1)*(width-1)) #top or bottom position

    if pos1 == pos2:
        return
    elif pos1 in pos or pos2 in pos:
        return
    elif pos1 in invalidPositions or pos2 in invalidPositions:
        return

    return pos1,pos2

def evaluation(population, fieldProps):
    newPopulation=copy.deepcopy(population)
    return [fitness(individual,fieldProps) for individual in newPopulation]

def can_move(row, col, map):
    return (0 <= row < len(map) and 0 <= col < len(map[0]) and map[row][col] == 0)
def is_edge(row, col, width, high):
    return row == -1 or row == high or col == -1 or col == width
def fitness(individual, fieldProps):
    positions, turns, fitness = individual.values()
    step = 1
    turn = 0
    field = generate_field(fieldProps)

    first_two_positions = positions[:2]
    # position=positions[0]
    for position in first_two_positions:
        if field[position[1]][position[0]] != 0:
            continue
        else:
            field[position[1]][position[0]] = step
            individual["fitness"] += 1
        direction = cdirection(position)
        turn_count = 0

        next_col = position[0] + Directions[direction][1]
        next_row = position[1] + Directions[direction][0]
        print(direction)
        print(next_row,next_col)
        while True:
            if is_edge(next_row, next_col, width, high):
                step += 1
                break
            if can_move(next_row, next_col, field):
                position=(next_col,next_row)
                field[position[1]][position[0]] = step
                next_col = position[0] + Directions[direction][1]
                next_row = position[1] + Directions[direction][0]
            else:
                if not (turn < len(turns)):
                    turn = 0
                direction = turn_table[turns[turn]][direction]
                next_col = position[0] + Directions[direction][1]
                next_row = position[1] + Directions[direction][0]
                turn_count += 1
                turn += 1
                if turn_count == 4:
                    step += 1
                    break

    print_mas(field,10,12)

def main():
    fitnesses = []
    populations = []
    population = initialize(fieldProps, 1)
    for i in range(1):
        print(f'{population[i]}')

    populations.append(evaluation(population, fieldProps))






invalidPositions = ((0, 0), (11, 9), (0, 9), (11, 0))
width=12
high=10
fieldProps = (12, 10, [(1, 2), (2, 4), (4, 3), (5, 1), (8, 6), (9, 6)])
main()