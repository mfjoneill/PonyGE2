from algorithm import step, evaluate_fitness
from stats.stats import stats, get_stats
from algorithm.parameters import params
from utilities.trackers import cache
from fitness.move_target import move_target, move_target_vision_avoid, move_target_vision_avoid_alt, move_target_realworldmapping, move_target_spiral
from utilities.display_population import display_3D_population, display_3D_population_dual_target, display_3D_plotly_population

def search_loop_wheel():
    """Allows the user to select different main search functions."""
    if params['COMPLETE_EVALS']:
        return search_loop_complete_evals()
    elif params['DYNAMIC_ENVIRONMENT']:
        return search_dynamic_loop()
    else:
        return search_loop()


def search_loop():
    """Loop over max generations"""

    # Initialise population
    individuals = params['INITIALISATION'](params['POPULATION_SIZE'])

    # Evaluate initial population
    individuals = evaluate_fitness.evaluate_fitness(individuals)

    # Generate statistics for run so far
    get_stats(individuals)

    # Traditional GE
    for generation in range(1, (params['GENERATIONS']+1)):
        stats['gen'] = generation

        # New generation
        individuals = step.step(individuals)

        # Generate statistics for run so far
        get_stats(individuals)

    return individuals


def search_loop_complete_evals():
    """Loop over total evaluations"""

    # Initialise population
    individuals = params['INITIALISATION'](params['POPULATION_SIZE'])

    # Evaluate initial population
    individuals = evaluate_fitness.evaluate_fitness(individuals)

    # Generate statistics for run so far
    get_stats(individuals)

    # Runs for a specified number of evaluations
    while len(cache) < (params['GENERATIONS'] * params['POPULATION_SIZE']):

        stats['gen'] += 1

        # New generation
        individuals = step.step(individuals)

        # Generate statistics for run so far
        get_stats(individuals)

    return individuals


def search_dynamic_loop():
    """Loop over max generations in a dynamic fitness environment"""

    # Initialise population
    individuals = params['INITIALISATION'](params['POPULATION_SIZE'])

    # Evaluate initial population
    individuals = evaluate_fitness.evaluate_fitness(individuals)

    # Generate statistics for run so far
    get_stats(individuals)

    # if 'PROBLEM' == "moving_point"
    # display the population & the target
    if params['PROBLEM'] in ("moving_point", "moving_point_vision"):
        display_3D_population(individuals,0)
        display_3D_plotly_population(individuals, 0)
        # plot.ly dashboard
    elif params['PROBLEM'] in ("moving_point_dual", "new_problem_here"):
        display_3D_population_dual_target(individuals, 0)

    # Traditional GE
    for generation in range(1, (params['GENERATIONS']+1)):
        stats['gen'] = generation

        # Do we change the fitness environment?
        if generation%params['DYNAMIC_ENVIRONMENT_PERIOD'] == 0:
            print("----+CHANGE FITNESS TARGET+----")
            if params['PROBLEM'] == "moving_point":
                move_target()
                print("gen: ", generation, "\t target: ", params['DYNAMIC_ENVIRONMENT_TARGET'])
            elif params['PROBLEM'] == "moving_point_vision":
                move_target_vision_avoid(individuals)
                print("gen: ", generation, "\t target: ", params['DYNAMIC_ENVIRONMENT_TARGET'])
            elif params['PROBLEM'] == "moving_point_spiral":
                move_target_spiral(generation,'DYNAMIC_ENVIRONMENT_TARGET_SPIRAL')
                print("gen: ", generation, "\t target: ", params['DYNAMIC_ENVIRONMENT_TARGET_SPIRAL'])
            elif params['PROBLEM'] == "moving_point_dual":
                move_target_vision_avoid_alt(individuals, 'DYNAMIC_ENVIRONMENT_TARGET' , 'MP_DESTINATION_INDEX')
                move_target_vision_avoid_alt(individuals, 'DYNAMIC_ENVIRONMENT_TARGET_ALT' , 'MP_DESTINATION_INDEX_ALT')
                print("gen: ", generation, "\t target: ", params['DYNAMIC_ENVIRONMENT_TARGET'], params['DYNAMIC_ENVIRONMENT_TARGET_ALT'])
            elif params['PROBLEM'] == "moving_point_realworld":
                move_target_realworldmapping()
                print("gen: ", generation, "\t target: ", params['DYNAMIC_ENVIRONMENT_TARGET'])

            # Re-evaluate the entire population with this new fitness target
            individuals = evaluate_fitness.evaluate_fitness(individuals)
            # Reset the population level statistics
            get_stats(individuals) # this also generates an additional entry/gen in the reports e.g.,stats.csv


        # New generation
        individuals = step.step(individuals)

        # Generate statistics for run so far
        get_stats(individuals)

        # if 'PROBLEM' == "moving_point"
        # display the population & the target
        if params['PROBLEM'] in ("moving_point","moving_point_vision","moving_point_realworld","new_problem_here"):
            display_3D_population(individuals,generation)
            display_3D_plotly_population(individuals, generation)
        elif params['PROBLEM'] == "moving_point_spiral":
            display_3D_population(individuals, generation, 'DYNAMIC_ENVIRONMENT_TARGET_SPIRAL')
        elif params['PROBLEM'] in ("moving_point_dual","new_problem_here"):
            display_3D_population_dual_target(individuals, generation)


    return individuals
