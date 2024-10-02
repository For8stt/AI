from main import main
import os
import pprint
import time
import matplotlib.pyplot as plt
from collections import Counter



if __name__ == "__main__":

    if os.path.exists("./results"):
        os.remove("./results")
    # possible selection functions: roulette, tournament
    # possible crossover functions: single_point_crossover, uniform_crossover
preferences = {
    "population_size": 100,
    "mutation_rate": 0.04,
    "elitism_rate": 0.01,
    "field_props": (12, 10, [(1, 2), (2, 4), (4, 3), (5, 1), (8, 6), (9, 6)]),
    "amount_of_generations": 100,
    "selection_function": "tournament",
    "crossover_function": "single_point_crossover",
    "offspring_factor": 8.6 / 10
    }
test_runs = 100

start_time = time.time()
for i in range(test_runs):
    print(f"Test run {i + 1}")
    main(preferences)

end_time = time.time()

print("Finished in " + time.ctime(end_time - start_time))
with open("results", "r") as f:
    results = f.read()

solution_fitness = preferences["field_props"][0] * preferences["field_props"][1] - len(preferences["field_props"][2])
solutions = results.split('\n').count(str(solution_fitness))
#solutoins= results.split('\n').count(str(solution_fitness-1))
#solutions+=solutoins

print(f"Found {solutions} solutions in {test_runs} test runs")
solution_percentage = solutions / test_runs * 100

with open("stats", "a") as stats:
    stats.write("------------BEGIN------------\n")
    formatted_preferences = pprint.pformat(preferences).replace('{', '').replace('}', '').replace('\'', '')
    stats.write(f"Preferences:\n {formatted_preferences}\n")
    stats.write(f"Found {solutions} solutions in {test_runs} test runs\n")
    stats.write(f"{solution_percentage} % in {preferences['amount_of_generations']} generations and {preferences['population_size']} population_size\n")
    stats.write("------------END------------\n")







plot=False
if plot:
    with open('results', 'r') as file:
        data = [int(line.strip()) for line in file]

    data_counts = Counter(data)
    sorted_data = sorted(data_counts.items())  # This will give a list of tuples (number, count)

    numbers = [item[0] for item in sorted_data]  # The numbers (keys)
    frequencies = [item[1] for item in sorted_data]  # The counts (values)
    # Plotting the data
    plt.plot(numbers, frequencies, label='Averege number of passage of the entire map', marker='o')

    # Adding titles and labels
    plt.title('Passage of the entire map and the number of them ')
    plt.xlabel('Fitness')
    plt.ylabel('Amount')
    plt.legend()

    # Show grid for better readability
    plt.grid(True)

    # Display the plot
    plt.show()