#! /usr/bin/env python

# PonyGE
# Copyright (c) 2009 Erik Hemberg, James McDermott,
#                   Michael Fenton and David Fagan
# Hereby licensed under the GNU GPL v3.
""" Python GE implementation """

from utilities.initialise_run import check_python_version
check_python_version()

from fitness.fitness_wheel import set_fitness_function
from algorithm.parameters import params, set_params
from stats.stats import get_stats, stats
from representation import grammar
from algorithm import search_loop
import sys


def mane():
    """ Run program """

    # Set Fitness Funtion
    params['FITNESS_FUNCTION'] = set_fitness_function(params['PROBLEM'],
                                                      params['ALTERNATE'])
    # Set Grammar File
    params['BNF_GRAMMAR'] = grammar.Grammar(params['GRAMMAR_FILE'])

    # Run evolution
    individuals = search_loop.search_loop_wheel()

    # Print final review
    get_stats(individuals, END=True)

    # Returns only needed if running experiment manager
    return params['TIME_STAMP'], stats['best_ever'].fitness

if __name__ == "__main__":
    set_params(sys.argv)
    mane()

    # dump an ave_fitness plot for the run
    from utilities import trackers, save_plots
    data = [i['ave_fitness'] for i in trackers.stats_list]
    save_plots.save_plot_from_data(data, 'ave_fitness')
