#! /usr/bin/env python

# statify.py
# Copyright (c) 2016 Michael O'Neill
#
# Hereby licensed under the GNU GPL v3.

import os
import sys
import getopt
import pandas as pd
import numpy as np
import scipy.stats



def loadStatsFiles(directory):
    # assume output from PonyGE2 into a results directory with a timestamped directory for each independent run
    # collect stats.tsv from each directory
    #print("the directory containing the stats files is: ",directory)

    __dirname = "../"+directory
    __files = os.listdir(__dirname)
    #print(__files)
    __stats = []    # container for all the stats.tsv's
    for i in __files:
        __path = __dirname + i + "/stats.tsv"
        #print("__path: ",__path)
        __stats.append(pd.read_csv(__path,sep="\t"))


    # calculate the average value of the statistic (__colname) at each __gennumber across all __numfiles runs
    #
    # print("#generations: ",len(__stats[__numfiles][__colname]))
    __stats_means = []    # container for all the _colname, __gennumber mean values across __numfiles runs
    #    print("#files: ", len(__files))
    #    for __numfiles in range(len(__files)):
    #        for __colname in __stats[__numfiles].columns.values:
    #            for __gennumber in range(len(__stats[__numfiles][__colname])):
    #                print(__stats[__numfiles][__colname][__gennumber])

    __numfiles = len(__files)
    __colnames = __stats[0].columns.values
    __numgens = len(__stats[0][__colnames[0]])
    __stats_agg = [] # container to aggregate the values of each statistic at each generation

    # create _colnames numpy arrays


    # for each array add cols
    for f in range(__numfiles):
        __stats_agg.append(__stats[f][__colnames[0]])
    print(__stats_agg)
    __col0 = np.array(__stats_agg)
    print("col0: ",__col0)

    #for __file in range(__numfiles):
    #    for __col in __stats[__file].columns.values:
    #        print(__stats[__file][__col])
    #__stats.mean(0,numeric_only=True)


    #print("column names: ",list(__stats[0].columns.values))
    #print(__stats[0]['accuracy'][0])





def help_message():
    print("There is one parameter: the directory name containing the results\n",
          "e.g., python --directory 'results/my_experiment/'"
          "Run python statify.py --help for more info")
    exit(2)


if __name__ == "__main__":
    # process command line args which should specify where the stats files are located
    # defaults to the directory called "results"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "",
                                   ["help", "directory="])
    except getopt.GetoptError as err:
        print("There is one parameter: the directory name containing the results\n",
              "e.g., python --directory 'results/my_experiment/'"
              "Run python statify.py --help for more info")
        print(str(err))
        exit(2)

    for opt, arg in opts:
        if opt == "--help":
            help_message()
            exit()

        # POPULATION OPTIONS
        elif opt == "--directory":
            loadStatsFiles(arg)



