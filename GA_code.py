# -*- coding: utf-8 -*-
"""
@author: Megha
"""
import random

def generate_population(size, w_boundaries, x_boundaries, y_boundaries, z_boundaries):
    lower_w_boundary, upper_w_boundary = w_boundaries
    lower_x_boundary, upper_x_boundary = x_boundaries
    lower_y_boundary, upper_y_boundary = y_boundaries
    lower_z_boundary, upper_z_boundary = z_boundaries
    population = []
    for i in range(size):
        individual = {
            "w": random.uniform(lower_w_boundary, upper_w_boundary),
            "x": random.uniform(lower_x_boundary, upper_x_boundary),
            "y": random.uniform(lower_y_boundary, upper_y_boundary),
            "z": random.uniform(lower_z_boundary, upper_z_boundary),
        }
        population.append(individual)

    return population

################################################################
import math

def apply_function(individual):
    w = individual["w"]
    x = individual["x"]
    y = individual["y"]
    z = individual["z"]
    return (1/(-62.00 + 35.011 * w + (-54.091) * x + (24.99) * y + (48.43) *z  + (-67.675)* w*w + (170.98)* w*x + (534.987)* w* y  + 133.285* w *z  + 297.741* x*x + (-45.87)* x* y + (-220.699)* x* z + (-148.697)* y*y + (-641.474)*y* z   + (-43.055)*z*z))


# generations = 1000

# population = generate_population(size=10, x_boundaries=(-4, 4), y_boundaries=(-4, 4))

# i = 1
# while True:
#     print(f"🧬 GENERATION {i}")

#     for individual in population:
#         print(individual)

#     if i == generations:
#         break

#     i += 1

    # Make next generation...
########################################################

def choice_by_roulette(sorted_population, fitness_sum):
    offset = 0
    normalized_fitness_sum = fitness_sum

    lowest_fitness = apply_function(sorted_population[0])
    if lowest_fitness < 0:
        offset = -lowest_fitness
        normalized_fitness_sum += offset * len(sorted_population)

    draw = random.uniform(0, 1)

    accumulated = 0
    for individual in sorted_population:
        fitness = apply_function(individual) + offset
        probability = fitness / normalized_fitness_sum
        accumulated += probability

        if draw <= accumulated:
            return individual
        
#############################################################
def sort_population_by_fitness(population):
    return sorted(population, key=apply_function)


def crossover(individual_a, individual_b):
    wa = individual_a["w"]
    xa = individual_a["x"]
    ya = individual_a["y"]
    za = individual_a["z"]

    wb = individual_b["w"]    
    xb = individual_b["x"]
    yb = individual_b["y"]
    zb = individual_b["z"]

    return {"w": (wa + wb) / 2, "x": (xa + xb) / 2, "y": (ya + yb) / 2, "z":(za+zb) / 2}


def mutate(individual):
    next_w = individual["w"] + random.uniform(-0.05, 0.05)
    next_x = individual["x"] + random.uniform(-0.05, 0.05)
    next_y = individual["y"] + random.uniform(-0.05, 0.05)
    next_z = individual["z"] + random.uniform(-0.05, 0.05)

    w_lower_boundary, w_upper_boundary = (380, 650)    
    x_lower_boundary, x_upper_boundary = (75.4, 96.5)
    y_lower_boundary, y_upper_boundary = (10, 30)
    z_lower_boundary, z_upper_boundary = (320, 580)
    # values are to be kept inside boundaries
    next_w = min(max(next_w, w_lower_boundary), w_upper_boundary)
    next_x = min(max(next_x, x_lower_boundary), x_upper_boundary)
    next_y = min(max(next_y, y_lower_boundary), y_upper_boundary)
    next_z = min(max(next_z, z_lower_boundary), z_upper_boundary)   
    return {"w": next_w, "x": next_x, "y": next_y, "z": next_z}


def make_next_generation(previous_population):
    next_generation = []
    sorted_by_fitness_population = sort_population_by_fitness(previous_population)
    population_size = len(previous_population)
    fitness_sum = sum(apply_function(individual) for individual in population)

    for i in range(population_size):
        first_choice = choice_by_roulette(sorted_by_fitness_population, fitness_sum)
        second_choice = choice_by_roulette(sorted_by_fitness_population, fitness_sum)

        individual = crossover(first_choice, second_choice)
        individual = mutate(individual)
        next_generation.append(individual)

    return next_generation

######################################################

generations = 1000

population = generate_population(size=10, w_boundaries=(380, 650), x_boundaries=(75.4, 96.5), y_boundaries=(10, 30), z_boundaries = (320, 580))
population
i = 1
while True:
    print(f"🧬 GENERATION {i}")

    for individual in population:
        print(individual, apply_function(individual))

    if i == generations:
        break

    i += 1

    population = make_next_generation(population)

best_individual = sort_population_by_fitness(population)[-1]
print("\n🔬 FINAL RESULT")
print(best_individual, apply_function(best_individual)) 
