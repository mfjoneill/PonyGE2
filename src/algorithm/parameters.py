from multiprocessing import cpu_count
from socket import gethostname
from random import seed
import time

hostname = gethostname().split('.')
machine_name = hostname[0]


"""Algorithm parameters"""
params = {
        # Evolutionary Parameters
        'POPULATION_SIZE': 100,
        'GENERATIONS': 10,

        # Set optional experiment name
        'EXPERIMENT_NAME': None,

        # Class of problem
        'PROBLEM': "moving_point_spiral",
        # "regression"
        # "string_match"
        # "moving_point"  warning: need to set the DYNAMIC_ENVIRONMENT parameters below
        # "moving_point_vision" warning: need to set the DYNAMIC_ENVIRONMENT parameters below
        # "moving_point_dual"  warning: need to set the DYNAMIC_ENVIRONMENT parameters below
        # "moving_point_spiral"  warning: need to set the DYNAMIC_ENVIRONMENT parameters below
        # "moving_point_realworld" warning: need to set the DYNAMIC_ENVIRONMENT parameters below
        # "classification"


    # Select Regression Problem Suite
        'SUITE': "Vladislavleva4",
        # "Dow"
        # "Keijzer6"
        # "Vladislavleva4"

        # Specify String for StringMatch Problem
        'STRING_MATCH_TARGET': "ponyge_rocks",



        # Flag to run dynamic environment loop which changes the target fitness function
        'DYNAMIC_ENVIRONMENT': True,
        # N.B.
        # as well as writing the dynamic fitness function,
        # the user must also specify the move_target function in fitness.move_target.py
        # which is applied to 'DYNAMIC_ENVIRONMENT_TARGET'
        # at a frequency of 'DYNAMIC_ENVIRONMENT_PERIOD'
        # Specify initial target for moving_point Problem
        # 'DYNAMIC_ENVIRONMENT_TARGET': (34.1234,52.6789,1.9876),
        # 'DYNAMIC_ENVIRONMENT_TARGET': (100.0,100.0,100.0),
        'DYNAMIC_ENVIRONMENT_TARGET': (1.0, 1.0, 1.0),
        'DYNAMIC_ENVIRONMENT_TARGET_ALT': (10000.0,10000.0,10000.0),
        # change target every DYNAMIC_ENVIRONMENT_PERIOD generations
        'DYNAMIC_ENVIRONMENT_PERIOD': 1,
        # set the move_target xyz delta's for the moving_points problem
        'X_DELTA': 50.0,
        'Y_DELTA': 50.0,
        'Z_DELTA': 50.0,
        'DELTA': 50.0,
        'FLEE_DELTA': 200.0,
        # define the x,y,z axes range for display_population for moving_points problem
        'MP_X_LIM_MAX': 10000,
        'MP_Y_LIM_MAX': 10000,
        'MP_Z_LIM_MAX': 10000,
        'MP_X_LIM_MIN': 1,
        'MP_Y_LIM_MIN': 1,
        'MP_Z_LIM_MIN': 1,
        'MP_DESTINATION_POINTS': [(1,1,1),
                                  (1,1,10000),
                                  (1,10000,1),
                                  (1,10000,10000),
                                  (10000,1,1),
                                  (10000,1,10000),
                                  (10000, 10000, 1),
                                  (10000, 10000, 10000)],
        'MP_DESTINATION_INDEX': [7],
        'MP_DESTINATION_INDEX_ALT': [0],

        # "field of vision" for individuals in the population for moving_point_vision problem
        'MPV_INDIVIDUAL_FIELD_OF_VISION': 0.05,
        'MPV_VISION_ENABLED': False,

        # generate plot.ly charts/dashboard for dynamic problems
        'PLOTLY': True,
        # generate plot.ly charts/dashboard for dynamic problems
        # when in a Jupyter Notebook environment
        'JUPYTER': False,

        #Spiral Move Params
        'CIRCLE_SPEED': 10,
        'FORWARD_SPEED': 10,
        'CIRCLE_SIZE': 4500,
        'CIRCLE_GROW_SPEED': 10,
        'DYNAMIC_ENVIRONMENT_TARGET_SPIRAL': (5000.0,5000.0,0.0),

    # Set max sizes of individuals
        'MAX_TREE_DEPTH': 17,
        'CODON_SIZE': 100000,
        'GENOME_LENGTH': 500,

        #for grid init
        'GRID_SIZE': 64,
        #or 64, 125
        # INITIALISATION
        #'INITIALISATION': "operators.initialisation.rhh",
        #'INITIALISATION': "operators.initialisation.grid_init",
        'INITIALISATION': "operators.initialisation.random_plus_grid_init",
        #Grid needs a pop of 125
        #"operators.initialisation.random_init"
        # "operators.initialisation.rhh"
        'MAX_INIT_DEPTH': 10,
        # Set the maximum tree depth for initialisation.
        'GENOME_INIT': False,
        # If True, initialises individuals by generating random genomes (i.e.
        # doesn't use trees to initialise individuals).

        # SELECTION
        'SELECTION': "operators.selection.tournament",
        # "operators.selection.tournament"
        # "operators.selection.truncation",
        'TOURNAMENT_SIZE': 2,
        # For tournament selection
        'SELECTION_PROPORTION': 0.5,
        # For truncation selection
        'INVALID_SELECTION': False,
        # Allow for selection of invalid individuals during selection process.

        # CROSSOVER
        'CROSSOVER': "operators.crossover.onepoint",
        # "operators.crossover.onepoint",
        # "operators.crossover.subtree",
        'CROSSOVER_PROBABILITY': 0.75,

        # MUTATION
        'MUTATION': "operators.mutation.int_flip",
        # "operators.mutation.subtree",
        # "operators.mutation.int_flip",
        'MUTATION_PROBABILITY': None,
        'MUTATION_EVENTS': 1,

        # REPLACEMENT
        'REPLACEMENT': "operators.replacement.generational",
        # "operators.replacement.generational",
        # "operators.replacement.steady_state",
        # "operators.replacement.grid_generational",
        #If elite size = none defaults to 1% of population
        'ELITE_SIZE': 1,

        # DEBUGGING
        # Use this to turn on debugging mode. This mode doesn't write any files
        # and should be used when you want to test new methods.
        'DEBUG': False,

        # PRINTING
        # Use this to print out basic statistics for each generation to the
        # command line.
        'VERBOSE': False,
        # Use this to prevent anything being printed to the command line.
        'SILENT': False,

        # SAVING
        'SAVE_ALL': False,
        # Use this to save the phenotype of the best individual from each
        # generation. Can generate a lot of files. DEBUG must be False.
        'SAVE_PLOTS': True,
        # Saves a plot of the evolution of the best fitness result for each
        # generation.

        # MULTIPROCESSING
        'MULTICORE': False,
        # Multiprocessing of phenotype evaluations.
        'CORES': cpu_count() - 1,

        # CACHING
        'CACHE': False,
        # The cache tracks unique individuals across evolution by saving a
        # string of each phenotype in a big list of all phenotypes. Saves all
        # fitness information on each individual. Gives you an idea of how much
        # repetition is in standard GE/GP.
        'LOOKUP_FITNESS': False,
        # Uses the cache to look up the fitness of duplicate individuals. CACHE
        #  must be set to True if you want to use this.
        'LOOKUP_BAD_FITNESS': False,
        # Uses the cache to give a bad fitness to duplicate individuals. CACHE
        # must be True if you want to use this (obviously)"""
        'MUTATE_DUPLICATES': False,
        # Removes duplicate individuals from the population by replacing them
        # with mutated versions of the original individual. Hopefully this will
        # encourage diversity in the population.
        'COMPLETE_EVALS': False,
        # Using the cache doesn't execute the full number of fitness
        # evaluations. Use this to continue the run in order to execute the
        # full number of fitness evaluations.

        # Set machine name (useful for doing multiple runs)
        'MACHINE': machine_name,

        # Set Random Seed
        'RANDOM_SEED': None
}


def set_params(command_line_args):
    from fitness.fitness_wheel import set_fitness_function, set_fitness_params
    from utilities.initialise_run import initialise_run_params
    from utilities.initialise_run import set_param_imports
    from utilities.helper_methods import return_percent
    from utilities.help_message import help_message
    import getopt

    try:
        opts, args = getopt.getopt(command_line_args[1:], "",
                                   ["help", "debug", "population=",
                                    "generations=", "initialisation=",
                                    "max_init_depth=", "genome_init",
                                    "max_tree_depth=", "codon_size=",
                                    "selection=", "selection_proportion=",
                                    "tournament_size=", "crossover=",
                                    "crossover_prob=", "replacement=",
                                    "mutation=", "mutation_events=",
                                    "random_seed=", "bnf_grammar=", "problem=",
                                    "problem_suite=", "target_string=",
                                    "verbose", "elite_size=", "save_all",
                                    "save_plots", "cache", "lookup_fitness",
                                    "lookup_bad_fitness", "mutate_duplicates",
                                    "complete_evals", "genome_length=",
                                    "invalid_selection", "silent",
                                    "dont_lookup_fitness", "experiment_name=",
                                    "multicore", "cores="])
    except getopt.GetoptError as err:
        print("Most parameters need a value associated with them \n",
              "Run python ponyge.py --help for more info")
        print(str(err))
        exit(2)

    for opt, arg in opts:
        if opt == "--help":
            help_message()
            exit()

        # POPULATION OPTIONS
        elif opt == "--population":
            params['POPULATION_SIZE'] = int(arg)
        elif opt == "--generations":
            params['GENERATIONS'] = int(arg)

        # INDIVIDUAL SIZE
        elif opt == "--max_tree_depth":
            params['MAX_TREE_DEPTH'] = int(arg)
        elif opt == "--codon_size":
            params['CODON_SIZE'] = int(arg)
        elif opt == "--genome_length":
            params['GENOME_LENGTH'] = int(arg)

        # INITIALISATION
        elif opt == "--initialisation":
            params['INITIALISATION'] = arg
        elif opt == "--max_init_depth":
            params['MAX_INIT_DEPTH'] = int(arg)
        elif opt == "--genome_init":
            params['GENOME_INIT'] = True
            params['INITIALISATION'] = "operators.initialisation.random_init"

        # SELECTION
        elif opt == "--selection":
            params['SELECTION'] = arg
        elif opt == "--invalid_selection":
            params['INVALID_SELECTION'] = arg
        elif opt == "--tournament_size":
            params['TOURNAMENT_SIZE'] = int(arg)
        elif opt == "--selection_proportion":
            params['SELECTION_PROPORTION'] = float(arg)

        # EVALUATION
        elif opt == "--multicore":
            params['MULTIPCORE'] = True
        elif opt == "--cores":
            params['CORES'] = int(arg)

        # CROSSOVER
        elif opt == "--crossover":
            params['CROSSOVER'] = arg
        elif opt == "--crossover_prob":
            params['CROSSOVER_PROBABILITY'] = float(arg)

        # MUTATION
        elif opt == "--mutation":
            params['MUTATION'] = arg
        elif opt == "--mutation_events":
            try:
                params['MUTATION_EVENTS'] = int(arg)
            except:
                print("Error: Please define mutation events as int")
                quit()
        elif opt == "--mutation_probability":
            try:
                params['MUTATION_PROBABILITY'] = float(arg)
            except:
                print("Error: Please define mutation probability as float")
                quit()
            if not 1 >= params['MUTATION_PROBABILITY'] >= 0:
                print("Error: Mutation prob outside allowed range [0:1]")
                quit()

        # REPLACEMENT
        elif opt == "--replacement":
            params['REPLACEMENT'] = arg
        elif opt == "--elite_size":
            params['ELITE_SIZE'] = int(arg)

        # PROBLEM SPECIFICS
        elif opt == "--bnf_grammar":
            params['GRAMMAR_FILE'] = arg
        elif opt == "--problem":
            params['PROBLEM'] = arg
        elif opt == "--problem_suite":
            params['SUITE'] = arg
        elif opt == "--target_string":
            params['STRING_MATCH_TARGET'] = arg
        elif opt == "--experiment_name":
            params['EXPERIMENT_NAME'] = arg

        # OPTIONS
        elif opt == "--random_seed":
            params['RANDOM_SEED'] = int(arg)
        elif opt == "--debug":
            params['DEBUG'] = True
        elif opt == "--verbose":
            params['VERBOSE'] = True
        elif opt == "--silent":
            params['SILENT'] = True
        elif opt == "--save_all":
            params['SAVE_ALL'] = True
        elif opt == "--save_plots":
            params['SAVE_PLOTS'] = True

        # CACHING
        elif opt == "--cache":
            params['CACHE'] = True
            params['LOOKUP_FITNESS'] = True
        elif opt == "--dont_lookup_fitness":
            params['CACHE'] = True
            params['LOOKUP_FITNESS'] = False
        elif opt == "--lookup_bad_fitness":
            params['LOOKUP_FITNESS'] = False
            params['LOOKUP_BAD_FITNESS'] = True
        elif opt == "--mutate_duplicates":
            params['LOOKUP_FITNESS'] = False
            params['MUTATE_DUPLICATES'] = True
        elif opt == "--complete_evals":
            params['LOOKUP_FITNESS'] = False
            params['COMPLETE_EVALS'] = True
        else:
            assert False, "Unhandled Option, use --help for available params"

    # Elite size is set to either 1 or 1% of the population size, whichever is
    # bigger if no elite size is previously set.
    if params['ELITE_SIZE'] is None:
        params['ELITE_SIZE'] = return_percent(1, params['POPULATION_SIZE'])

    # Set the size of a generation
    params['GENERATION_SIZE'] = params['POPULATION_SIZE'] - params[
        'ELITE_SIZE']

    # Set random seed
    if params['RANDOM_SEED'] is None:
        params['RANDOM_SEED'] = int(time.clock()*1000000)
    seed(params['RANDOM_SEED'])

    # Set GENOME_OPERATIONS automatically for faster linear operations
    if (params['MUTATION'] == 'operators.mutation.int_flip' or
                params['MUTATION'] == 'int_flip') and \
            (params['CROSSOVER'] == 'operators.crossover.onepoint' or
                     params['CROSSOVER'] == 'onepoint'):
        params['GENOME_OPERATIONS'] = True
    else:
        params['GENOME_OPERATIONS'] = False

    # Set problem specifics
    params['GRAMMAR_FILE'], \
    params['ALTERNATE'] = set_fitness_params(params['PROBLEM'], params)
    params['FITNESS_FUNCTION'] = set_fitness_function(params['PROBLEM'],
                                                      params['ALTERNATE'])

    # Initialise run lists and folders
    initialise_run_params()

    # Set correct param imports for specified function options
    set_param_imports()
