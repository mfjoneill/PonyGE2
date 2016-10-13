from algorithm.evaluate_fitness import evaluation
from operators.crossover import crossover
from operators.mutation import mutation
from operators.replacement import replacement
from operators.selection import selection
from algorithm.parameters import params
from copy import deepcopy


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
    # Select parents
    parents = selection(individuals)

    # Crossover parents and add to the new population
    cross_pop = crossover(parents)

    # Mutate the new population
    new_pop = mutation(cross_pop)

    # Evaluate the fitness of the new population
    new_pop = evaluation(new_pop)
    initial_population = evaluation(initial_population)
    individuals = replacement(new_pop, individuals)

    initial_population.sort(reverse=True)
    individuals.sort(reverse=True)
    if individuals[0].fitness > initial_population[0].fitness:
        print("RESETTING POP")
        individuals = deepcopy(initial_population)

    return individuals