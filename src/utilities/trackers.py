"""Utilities for tracking progress of runs,
 including time taken per generation,
 fitness plots, fitness caches, etc."""

cache = {}
# This dict stores the cache for an evolutionary run. The key for each entry
# is the phenotype of the individual, the value is its fitness.

best_fitness_list = []
# fitness_plot is simply a list of the best fitnesses at each generation.
# Useful for plotting evolutionary progress.

time_list = []
# time_list stores the system time after each generation has been completed.
# Useful for keeping track of how long each generation takes.

stats_list = []
# List for storing stats at each generation
# Used when verbose mode is off to speed up program

fitness_list = []
#  useful for plotting histogram of fitness of population over time

fitness_entropy_list = []
#  useful for plotting entropy of fitness of population over time

fitness_variation_list = []
#  useful for plotting variation of fitness of population over time

fitness_iqr_list = []
#  useful for plotting variation of fitness of population over time

mean_fitness_list = []
# fitness_plot is simply a list of the best fitnesses at each generation.
# Useful for plotting evolutionary progress.

fitness_std_list = []
#  useful for plotting std of fitness of population over time

genotype_list = []
# WARNING: Memory intensive - stores genome of every individual in each generation
# useful for calculating population/run statistics on genomes
# used for 3D population visualisation

target_list =[]
# keeps track of the global optimum target at each generation
# used in dynamic problem environments