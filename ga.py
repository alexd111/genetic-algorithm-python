import random
import time
import json
import os

GENE_SIZE = 64
POPULATION_SIZE = 50
GENERATIONS = 100
CROSSOVER_PROBABILITY = 0.5
MUTATION_PROBABILITY = 0.002


def initial_population_setup():
    population = []
    for i in range(POPULATION_SIZE):
        population.append([[0] * GENE_SIZE, 0])

    for i in range(POPULATION_SIZE):
        for j in range(GENE_SIZE):
            population[i][0][j] = random.randint(0, 1)
    return population


def calculate_fitness(population):
    population = reset_population_fitness(population)
    for key, value in input_data.items():
        for i in range(POPULATION_SIZE):

            chunks = [population[i][0][x:x + 7] for x in range(0, len(population[i][0]), 7)]
            for j in range(len(chunks)):
                match = 0
                condition = list(map(str, chunks[j][:6]))
                condition = ''.join(condition)
                action = chunks[j][-1]
                for k in range(len(key)):
                    if (key[k] == condition[k]) or (condition[k] == "2"):
                        match += 1
                if match == 6:
                    if value == str(action):
                        population[i][1] += 1

    return population


def reset_population_fitness(population):
    for i in range(POPULATION_SIZE):
        population[i][1] = 0
    return population


def calculate_total_and_highest_fitness(population):
    total = 0
    highest = 0
    for item in population:
        total += item[1]
        if item[1] > highest:
            highest = item[1]
    return [total, highest]


def shuffle(population):
    population = random.sample(population, len(population))
    return population


def tournament_selection(population):
    offspring = []
    for i in range(POPULATION_SIZE):
        parent1 = random.randint(0, POPULATION_SIZE - 1)
        parent2 = random.randint(0, POPULATION_SIZE - 1)
        if population[parent1][1] >= population[parent2][1]:
            offspring.append(population[parent1])
        else:
            offspring.append(population[parent2])
    return offspring


def crossover(population):
    offspring = []
    probability = random.random()
    for i in range(0, POPULATION_SIZE, 2):
        first_parent = population[i][0]
        second_parent = population[i + 1][0]
        if probability >= CROSSOVER_PROBABILITY:
            offspring.append([first_parent, 0])
            offspring.append([second_parent, 0])
        else:
            crossover_point = random.randint(0, GENE_SIZE - 1)
            first_child = first_parent[:crossover_point] + second_parent[crossover_point:]
            second_child = first_parent[crossover_point:] + second_parent[:crossover_point]
            first_action_list = first_child[::7]
            second_action_list = second_child[::7]
            if (2 not in first_action_list) or (2 not in second_action_list):
                offspring.append([first_child, 0])
                offspring.append([second_child, 0])
            else:
                offspring.append([first_parent, 0])
                offspring.append([second_parent, 0])

    return offspring


def mutation(population):
    for i in range(POPULATION_SIZE):
        for j in range(GENE_SIZE):
            mutation_chance = random.random()
            if (mutation_chance <= MUTATION_PROBABILITY) and (not((j + 1) % 7 == 0)):
                population[i][0][j] = random.randint(0, 2)
    return population


def read_file_in():
    lines = [line.rstrip('\n') for line in open('data2.txt')]
    data_dict = {}
    for i in range(int(len(lines))):
        data_dict[lines[i].split(" ")[0]] = lines[i].split(" ")[1]
    return data_dict

start = time.clock()

input_data = read_file_in()

json_list = []

population = initial_population_setup()

population = calculate_fitness(population)

initial_fitness_stats = calculate_total_and_highest_fitness(population)
print("Initial average fitness:")
print(initial_fitness_stats[0] / POPULATION_SIZE)
print("Initial highest fitness:")
print(initial_fitness_stats[1])

offspring = population

# for b in range(10):
#     json_list.append([])
# print("Iteration: " + str(b))
for i in range(GENERATIONS):
    print("Gen: " + str(i))
    offspring = shuffle(offspring)

    offspring = tournament_selection(offspring)

    offspring = crossover(offspring)

    offspring = mutation(offspring)

    offspring = calculate_fitness(offspring)

    fitness_stats = calculate_total_and_highest_fitness(offspring)

    # print("Total fitness:")
    # print(fitness_stats[0])
    # print("Average fitness:")
    average_fitness = fitness_stats[0] / POPULATION_SIZE
    # print(average_fitness)
    # print("Highest fitness:")
    # print(fitness_stats[1])

    json_list.append([fitness_stats[0], average_fitness, fitness_stats[1]])

stop = time.clock()

if os.path.isfile('results.json'):
    os.remove('results.json')

file = open('results.json', 'w')

file.write(json.dumps(json_list))

print("Number of milliseconds to execute:")
print((stop - start) * 1000)
