from random import randint

N = 10
P = 10


def initial_population_setup():
    population = []
    for i in range(P):
        population.append([[0] * N, 0])

    for i in range(P):
        for j in range(N):
            population[i][0][j] = randint(0, 1)
    return population


def calculate_total_fitness(population):
    total = 0
    for item in population:
        total += item[1]

    return total


def tournament_selection(population):
    offspring = []
    for i in range(P):
        parent1 = randint(0, P - 1)
        parent2 = randint(0, P - 1)
        if population[parent1][1] >= population[parent2][1]:
            offspring.append(population[parent1])
        else:
            offspring.append(population[parent2])
    return offspring


population = initial_population_setup()

for item in population:
    for index in range(len(item[0])):
        if item[0][index] is 1:
            item[1] += 1

print calculate_total_fitness(population)

offspring = tournament_selection(population)

print calculate_total_fitness(offspring)