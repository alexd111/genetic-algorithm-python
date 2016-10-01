from random import randint
import time

N = 10
P = 10
GENERATIONS = 50
CROSSOVER_PROBABILITY = 6


def initial_population_setup():
    population = []
    for i in range(P):
        population.append([[0] * N, 0])

    for i in range(P):
        for j in range(N):
            population[i][0][j] = randint(0, 1)
    return population


def calculate_fitness(population):
    for i in range(P):
        population[i][1] = 0
        for j in range(N):
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
    for i in range(P):
        parent1 = randint(0, P - 1)
        parent2 = randint(0, P - 1)
        if population[parent1][1] >= population[parent2][1]:
            child = crossover(population[parent1][0], population[parent2][0])
            offspring.append([child, 0])
        else:
            child = crossover(population[parent2][0], population[parent1][0])
            offspring.append([child, 0])
    return offspring


def crossover(first_parent, second_parent):
    probability = randint(0, 10)
    if probability >= CROSSOVER_PROBABILITY:
        return first_parent
    else:
        crossover_point = randint(0, 9)
        new_child = first_parent[:crossover_point] + second_parent[crossover_point:]
        return new_child


start = time.clock()

population = initial_population_setup()

population = calculate_fitness(population)

initial_fitness_stats = calculate_total_and_highest_fitness(population)
print("Initial average fitness:")
print(initial_fitness_stats[0] / P)
print("Initial highest fitness:")
print(initial_fitness_stats[1])

for i in range(GENERATIONS):
    offspring = tournament_selection(population)

    offspring = calculate_fitness(offspring)

    fitness_stats = calculate_total_and_highest_fitness(offspring)
    print("Average fitness:")
    print(fitness_stats[0] / P)
    print("Highest fitness:")
    print(fitness_stats[1])

stop = time.clock()

print("Number of milliseconds to execute:")
print((stop - start) * 1000)
