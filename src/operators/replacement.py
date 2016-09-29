from algorithm.parameters import params
from copy import copy


def replacement(new_pop, individuals):
    """
    Given a new population and an old population, performs replacement using
    specified replacement operator
    :param new_pop: Newly generated population (after selection, variation &
    evaluation).
    :param individuals: Previous generation population
    :return: Replaced population
    """
    return params['REPLACEMENT'](new_pop, individuals)


def generational(new_pop, individuals):
    """
    Replaces the old population with the new population. The ELITE_SIZE best
    individuals from the previous population are appended to new pop regardless
    of whether or not they are better than the worst individuals in new pop.
    :param new_pop: The new population (e.g. after selection, variation, &
    evaluation).
    :param individuals: The previous generation population, from which elites
    are taken.
    :return: The 'POPULATION_SIZE' new population with elites.
    """

    individuals.sort(reverse=True)
    new_pop.sort(reverse=True)
    for ind in individuals[:params['ELITE_SIZE']]:
        new_pop.insert(0,copy(ind))
    return new_pop[:params['POPULATION_SIZE']]


# Provided but no flag set. Need to append code to use this
def steady_state(new_pop, individuals):
    """Return individuals. If the best of new pop is better than the
    worst of individuals it is inserted into individuals"""
    individuals.sort(reverse=True)
    individuals[-1] = max(new_pop + individuals[-1:])
    return individuals

def grid_generational(new_pop, individuals):
    """Return new pop. The ELITE_SIZE best individuals are appended
    to new pop if they are better than the worst individuals in new
    pop"""
    from algorithm.evaluate_fitness import evaluation
    from representation import individual

    if params['GENERATION_SIZE']<params['GRID_SIZE']:
        print("Generations must be more than grid size with Grid Generational "
              "Replacement")
        quit()

    individuals.sort(reverse=True)
    for ind in individuals[:params['ELITE_SIZE']]:
        new_pop.append(copy(ind))
    new_pop.sort(reverse=True)

    new_pop = new_pop[:(params['GENERATION_SIZE']+params['ELITE_SIZE']- params['GRID_SIZE'])]
    grid_pop = []
    if params['GRID_SIZE'] == 64:
        index = [2, 4, 6, 8]
    else:
        index = [1, 3, 5, 7, 9]
    for x in range(len(index)):
        for y in range(len(index)):
            for z in range(len(index)):
                grid_pop.append(individual.Individual([0, (index[x] + 10), 0, 0, 0, (index[y] + 10), 0, 0, 0, (index[z] + 10), 0, 0, 0], None))
    grid_pop = evaluation(grid_pop)
    new_pop = new_pop + grid_pop
    new_pop.sort(reverse=True)
    return new_pop[:params['GENERATION_SIZE']+params['ELITE_SIZE']]
