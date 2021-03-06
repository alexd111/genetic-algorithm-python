import random
import time
import json
import os

GENE_SIZE = 50
POPULATION_SIZE = 50
GENERATIONS = 50
CROSSOVER_PROBABILITY = 0.9
MUTATION_PROBABILITY = 0.0


def initial_population_setup():
    population = []
    for i in range(POPULATION_SIZE):
        population.append([[0] * GENE_SIZE, 0])

    for i in range(POPULATION_SIZE):
        for j in range(GENE_SIZE):
            population[i][0][j] = random.randint(0, 1)
    return population


def calculate_fitness(population):
    for i in range(POPULATION_SIZE):
        population[i][1] = 0
        for j in range(GENE_SIZE):
            if population[i][0][j] == 1:
                population[i][1] += 1
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
            crossover_point = random.randint(0, 9)
            first_child = first_parent[:crossover_point] + second_parent[crossover_point:]
            second_child = first_parent[crossover_point:] + second_parent[:crossover_point]
            offspring.append([first_child, 0])
            offspring.append([second_child, 0])
    return offspring


def mutation(population):
    for i in range(POPULATION_SIZE):
        for j in range(GENE_SIZE):
            mutation_chance = random.random()
            if mutation_chance <= MUTATION_PROBABILITY:
                if population[i][0][j] == 0:
                    population[i][0][j] = 1
                else:
                    population[i][0][j] = 0
    return population

start = time.clock()

json_list = []

population = initial_population_setup()

population = calculate_fitness(population)

initial_fitness_stats = calculate_total_and_highest_fitness(population)
print("Initial average fitness:")
print(initial_fitness_stats[0] / POPULATION_SIZE)
print("Initial highest fitness:")
print(initial_fitness_stats[1])

offspring = population

for i in range(GENERATIONS):
    offspring = shuffle(offspring)

    offspring = tournament_selection(offspring)

    offspring = crossover(offspring)

    offspring = mutation(offspring)

    offspring = calculate_fitness(offspring)

    fitness_stats = calculate_total_and_highest_fitness(offspring)

    print("Total fitness:")
    print(fitness_stats[0])
    print("Average fitness:")
    average_fitness = fitness_stats[0] / POPULATION_SIZE
    print(average_fitness)
    print("Highest fitness:")
    print(fitness_stats[1])

    json_list.append([fitness_stats[0], average_fitness, fitness_stats[1]])

stop = time.clock()

if os.path.isfile('results.json'):
    os.remove('results.json')

file = open('results.json', 'w')

file.write(json.dumps(json_list))

print("Number of milliseconds to execute:")
print((stop - start) * 1000)
