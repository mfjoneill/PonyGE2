from algorithm.evaluate_fitness import evaluation
from operators.crossover import crossover
from operators.mutation import mutation
from operators.replacement import replacement
from operators.selection import selection
from algorithm.parameters import params
from copy import deepcopy
import random


def step(individuals):
    """Return individuals and best ever individual from a step of
    the EA iteration"""

    if params['BASELINE_STEPS']:
        individuals = evaluation(individuals)
    else:
        # Select parents
        parents = selection(individuals)

        # Crossover parents and add to the new population
        cross_pop = crossover(parents)

        # Mutate the new population
        new_pop = mutation(cross_pop)

        # Evaluate the fitness of the new population
        new_pop = evaluation(new_pop)

        # Replace the sorted individuals with the new populations
        individuals = replacement(new_pop, individuals)

    return individuals

def step_reload(individuals,initial_population):
    individuals.sort(reverse=True)
    print(str(individuals[0].fitness) + " -v- " + str(params['RESET_FITNESS']))
    if individuals[0].fitness > params['RESET_FITNESS']:
        if params['DYNAMIC_ENVIRONMENT_RELOAD_PERCENTAGE']:
            print("RESETTING PERCENTAGE OF POP")
            new_inds = int(len(initial_population)*params['DYNAMIC_ENVIRONMENT_RELOAD_PERCENTAGE_VALUE'])
            #sample from initial pop randomly
            reload_pop_a = deepcopy(random.sample(initial_population, new_inds))
            reload_pop_b = deepcopy(individuals[:-new_inds])
            reload_pop = reload_pop_a + reload_pop_b
            reload_pop = evaluation(reload_pop)
            reload_pop.sort(reverse=True)
            params['RESET_FITNESS'] = reload_pop[0].fitness
            print("Reload Threshold now: " + str(params['RESET_FITNESS']))
            params['RELOAD_PERFORMED'] = 1
            rep_inds = deepcopy(reload_pop)
            # If we want to use replacement :D
            # individuals = replacement(initial_population, individuals)
        else:
            print("RESETTING POP")
            initial_population = evaluation(initial_population)
            initial_population.sort(reverse=True)
            params['RESET_FITNESS'] = initial_population[0].fitness
            print("Reload Threshold now: "+ str(params['RESET_FITNESS']))
            params['RELOAD_PERFORMED'] = 1
            rep_inds = deepcopy(initial_population)
            #If we want to use replacement :D
            #individuals = replacement(initial_population, individuals)
    else:
        # Select parents
        parents = selection(individuals)

        # Crossover parents and add to the new population
        cross_pop = crossover(parents)

        # Mutate the new population
        new_pop = mutation(cross_pop)

        # Evaluate the fitness of the new population
        new_pop = evaluation(new_pop)

        # Replace the sorted individuals with the new populations
        rep_inds = replacement(new_pop, individuals)

        params['RELOAD_PERFORMED'] = 0

    return rep_inds