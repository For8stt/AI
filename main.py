import copy
import random

def cdirection(pos): #from which side it starts then in the opposite direction moves
    if pos[0] == 0:
        return 'right'
    elif pos[0] == 11:
        return 'left'
    elif pos[1] == 0:
        return 'down'
    else:
        return 'up'

Directions = { #player movement in which direction
    "up": (-1, 0),   # Move up (row decreases)
    "down": (1, 0),  # Move down (row increases)
    "left": (0, -1), # Move left (column decreases)
    "right": (0, 1)  # Move right (column increases)
}
turn_table = {#turn the player if he hits an obstacle
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

def initialize(fieldProps, populationSize): #gene initialization
    return [generateGenes(fieldProps) for i in range(populationSize)]
def generateGenes(fieldProps): #gene generetion
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

def genereteStartPosition(fieldProps, pos):#generetion start position for genes
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

def evaluation(population, fieldProps): #evaluation of population (fitness)
    newPopulation=copy.deepcopy(population)
    return [fitness(individual,fieldProps) for individual in newPopulation]

def can_move(row, col, map): # checks whether he can go on
    return (0 <= row < len(map) and 0 <= col < len(map[0]) and map[row][col] == 0)
def is_edge(row, col, width, high): #checks if player went over the card
    return row == -1 or row == high or col == -1 or col == width
def fitness(individual, fieldProps):
    positions, turns, fitness = individual.values()
    step = 1
    turn = 0
    field = generate_field(fieldProps)

    first_two_positions = positions[:7]
    # for position in positions:
    # counter=0
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

        # counter += 1
        # print(direction,counter)
        # print(next_row,next_col)
        while True:
            if is_edge(next_row, next_col, width, high):
                step += 1
                break
            if can_move(next_row, next_col, field):
                position=(next_col,next_row)
                field[position[1]][position[0]] = step
                individual["fitness"] += 1
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
    return individual
def SelectionTheBest(population, bestPersonRatio): #sorts populations by the best fitness
    sorted_population = sorted(population, key=lambda individual: individual["fitness"], reverse=True)
    return sorted_population[:int(len(population) * bestPersonRatio)]

def selection(population, selection_function, desired_amount): #roulette or tournament
    return selection_function(population, desired_amount)
def roulette(population, desire_amount):#the best individuals from the current generation and carry them over to the next generation.
    new_population = random.choices(population, weights=[individual["fitness"] for individual in population], k=desire_amount)
    return new_population

def crossover(population, crossover_function):#singlePointCrossover or uniformCrossover
    return [child for i in range(0, len(population) - 1, 2) for child in
            crossover_function(population[i], population[i + 1])]
def singlePointCrossover(parent1, parent2):
    positionPoint = random.randint(0, len(parent1['positions'])-1)
    turnsPoint = random.randint(0, len(parent1['turns'])-1)
    offspring1={
        'positions': parent1['positions'][:positionPoint]+parent2['positions'][positionPoint:],
        'turns': parent1['turns'][:turnsPoint]+parent2['turns'][turnsPoint:],
        'fitness': 0
    }
    offspring2={
        'positions': parent2['positions'][:positionPoint]+parent1['positions'][positionPoint:],
        'turns': parent2['turns'][:turnsPoint]+parent1['turns'][turnsPoint:],
        'fitness': 0
    }
    return offspring1, offspring2
def mutation(population, mutationRate,fieldProps):#return mutated populations
    newPopulation=copy.deepcopy(population)
    return [mutate(individual,mutationRate,fieldProps)for individual in newPopulation]
def mutate(individual,mutationRate,fieldProps):
    for i in range(len(individual['positions'])):
        if random.random()<mutationRate:
            result = None
            while not result:
                result = genereteStartPosition(fieldProps,individual['positions'])
            pos1, pos2=result
            individual['positions'][i] = pos1 if random.randint(0,1) == 0 else pos2
    for i in range(len(individual['turns'])):
        if random.random()<mutationRate:
            individual['turns'][i] = 'right' if random.randint(0,1) == 0 else 'left'
    return individual
def tournament(population, desiredAmount): #none use
    newPopulation=[]
    while len (newPopulation)<desiredAmount:
        selected=random.sample(population,3)
        newPopulation.append(max(selected, key=lambda individual: individual['fitness']))
    return newPopulation
def uniformCrossover(parent1,parent2): #none use
    positionMask=[random.randint(0,1) for i in range(len(parent1['positions']))]
    turnMask=[random.randint(0,1)for i in range(len(parent1['turns']))]

    position1=[]
    position2=[]

    turns1=[]
    turns2=[]

    for i,bit in enumerate(positionMask):
        if bit==0:
            position1.append(parent1['positions'][i])
            position2.append(parent2['positions'][i])
        else:
            position1.append(parent2['positions'][i])
            position2.append(parent1['positions'][i])

    for i,bit in enumerate(turnMask):
        if bit==0:
            turns1.append(parent1['turns'][i])
            turns2.append(parent2['turns'][i])
        else:
            turns1.append(parent2['turns'][i])
            turns2.append(parent1['turns'][i])

    offspring1={
        'positions':position1,
        'turns': turns1,
        'fitness': 0
    }
    offspring2={
        'positions': position2,
        'turns': turns2,
        'fitness': 0
    }
    return offspring1,offspring2

def main():
    fitnesses = []
    populations = []
    population = initialize(fieldProps, population_size)
    for i in range(3):
        print(f'{population[i]}')

    a=1
    while a:
        populations.append(evaluation(population, fieldProps))
        fitnesses.append(max(populations[-1], key=lambda individual: individual["fitness"])["fitness"]) # function is used to find the individual with the highest fitness in the latest population
        if len(populations) == amountOfGenerations:
            break
        if fitnesses[-1] == fieldProps[0] * fieldProps[1] - len(fieldProps[2]):
            break

        future_population = copy.deepcopy(populations[-1])

        new_population = SelectionTheBest(population, bestPersonRatio)

        future_population = selection(future_population, selection_function, int((population_size * offspring_factor)))

        future_population = crossover(future_population, crossover_function)

        new_population += mutation(future_population, mutation_rate, fieldProps)

        new_population += initialize(fieldProps, population_size - len(new_population))

        population = new_population

        print(populations)
        print(fitnesses)
        a=0

    print(f"Best fitness over {len(populations)} generations: {max(fitnesses)}")
    with open("results", "a") as myfile:
        myfile.write(f'Best fitness over {len(populations)} generations: {max(fitnesses)}' + "\n")





width=12
high=10

mutation_rate = 0.10
population_size = 4
offspring_factor = 3 / 4
selection_function = roulette
crossover_function = singlePointCrossover
invalidPositions = ((0, 0), (11, 9), (0, 9), (11, 0))
amountOfGenerations = 100
bestPersonRatio = 0.05
fieldProps = (12, 10, [(1, 2), (2, 4), (4, 3), (5, 1), (8, 6), (9, 6)])
main()
#tournament()
#uniformCrossover()