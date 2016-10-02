import random
import time

GENE_SIZE = 100
POPULATION_SIZE = 50
GENERATIONS = 500
CROSSOVER_PROBABILITY = 0.6
MUTATION_PROBABILITY = 0.05


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
            if population[i][0][j] is 1:
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


def tournament_selection(population):
    offspring = []
    for i in range(POPULATION_SIZE):
        parent1 = random.randint(0, POPULATION_SIZE - 1)
        parent2 = random.randint(0, POPULATION_SIZE - 1)
        if population[parent1][1] >= population[parent2][1]:
            child = crossover(population[parent1][0], population[parent2][0])
            child = mutation(child)
            offspring.append([child, 0])
            # offspring.append(population[parent1])
        else:
            child = crossover(population[parent2][0], population[parent1][0])
            child = mutation(child)
            offspring.append([child, 0])
            # offspring.append(population[parent2])
    return offspring


def crossover(first_parent, second_parent):
    probability = random.random()
    if probability >= CROSSOVER_PROBABILITY:
        return first_parent
    else:
        crossover_point = random.randint(0, 9)
        new_child = first_parent[:crossover_point] + second_parent[crossover_point:]
        return new_child


def mutation(child):
    for i in range(GENE_SIZE):
        mutation_chance = random.random()
        if mutation_chance <= MUTATION_PROBABILITY:
            if child[i] == 0:
                child[i] = 1
            else:
                child[i] = 0
    return child

start = time.clock()

population = initial_population_setup()

population = calculate_fitness(population)

initial_fitness_stats = calculate_total_and_highest_fitness(population)
print("Initial average fitness:")
print(initial_fitness_stats[0] / POPULATION_SIZE)
print("Initial highest fitness:")
print(initial_fitness_stats[1])

for i in range(GENERATIONS):
    offspring = tournament_selection(population)

    offspring = calculate_fitness(offspring)

    fitness_stats = calculate_total_and_highest_fitness(offspring)

    print("Average fitness:")
    print(fitness_stats[0] / POPULATION_SIZE)
    print("Highest fitness:")
    print(fitness_stats[1])

stop = time.clock()

print("Number of milliseconds to execute:")
print((stop - start) * 1000)
