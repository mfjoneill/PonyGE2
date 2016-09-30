from utilities.save_plots import save_best_fitness_plot, save_fitness_histogram_movie, save_3Dgenotype_movie, merge_3Dgenotype_fitnesshistogram_movie
from algorithm.parameters import params
from os import path, mkdir, getcwd
from datetime import timedelta
from utilities import trackers
from sys import stdout
from copy import copy
import time
from scipy.stats import entropy, variation, iqr, tstd
from scipy.spatial import distance


"""Algorithm statistics"""
stats = {
        "gen": 0,
        "best_ever": None,
        "total_inds": 0,
        "regens": 0,
        "invalids": 0,
        "unique_inds": len(trackers.cache),
        "unused_search": 0,
        "ave_genome_length": 0,
        "max_genome_length": 0,
        "min_genome_length": 0,
        "ave_used_codons": 0,
        "max_used_codons": 0,
        "min_used_codons": 0,
        "ave_tree_depth": 0,
        "max_tree_depth": 0,
        "min_tree_depth": 0,
        "ave_tree_nodes": 0,
        "max_tree_nodes": 0,
        "min_tree_nodes": 0,
        "ave_fitness": 0,
        "best_fitness": 0,
        "time_taken": 0,
        "total_time": 0,
        "fitness_entropy": 0,
        "fitness_variation": 0,
        "fitness_iqr": 0,
        "fitness_std": 0,
        "convexhullvolume": 0,
        "accuracy": 0
}


def get_stats(individuals, end=False):
    """Generate the statistics for an evolutionary run"""

    if end or params['VERBOSE'] or not params['DEBUG']:

        # Time Stats
        trackers.time_list.append(time.clock())
        available = [i for i in individuals if not i.invalid]
        # TODO: Should we save time stats as raw seconds? Easier for parsing.
        stats['time_taken'] = \
            timedelta(seconds=trackers.time_list[-1] - trackers.time_list[-2])
        stats['total_time'] = timedelta(seconds=(trackers.time_list[-1] -
                                        trackers.time_list[0]))
        # Population Stats
        stats['total_inds'] = params['POPULATION_SIZE'] * (stats['gen'] + 1)
        stats['unique_inds'] = len(trackers.cache)
        stats['unused_search'] = 100 - stats['unique_inds'] / \
                                       stats['total_inds']*100
        stats['best_ever'] = max(individuals)

        # Genome Stats
        genome_lengths = [len(i.genome) for i in available]
        stats['max_genome_length'] = max(genome_lengths)
        stats['ave_genome_length'] = ave(genome_lengths)
        stats['min_genome_length'] = min(genome_lengths)

        # Used Codon Stats
        codons = [i.used_codons for i in available]
        stats['max_used_codons'] = max(codons)
        stats['ave_used_codons'] = ave(codons)
        stats['min_used_codons'] = min(codons)

        # Tree Depth Stats
        depths = [i.depth for i in available]
        stats['max_tree_depth'] = max(depths)
        stats['ave_tree_depth'] = ave(depths)
        stats['min_tree_depth'] = min(depths)

        # Tree Node Stats
        nodes = [i.nodes for i in available]
        stats['max_tree_nodes'] = max(nodes)
        stats['ave_tree_nodes'] = ave(nodes)
        stats['min_tree_nodes'] = min(nodes)

        # Fitness Stats
        fitnesses = [i.fitness for i in available]
        stats['ave_fitness'] = ave(fitnesses)
        stats['best_fitness'] = stats['best_ever'].fitness
        stats['fitness_entropy'] = entropy(fitnesses)
        stats['fitness_variation'] = variation(fitnesses)
        stats['fitness_iqr'] = iqr(fitnesses)
        stats['fitness_std'] = tstd(fitnesses)
        trackers.fitness_list.append(fitnesses)

        # calculate accuracy
        # used as a performance metric in dynamic environments
        # how close the best fitness individual is to the best possible fitness
        __max_euclidean = distance.euclidean(
            (params['MP_X_LIM_MAX'], params['MP_Y_LIM_MAX'], params['MP_Z_LIM_MAX']),
            (params['MP_X_LIM_MIN'], params['MP_Y_LIM_MIN'], params['MP_Z_LIM_MIN']))
        #print("__max_euclidean: ", __max_euclidean)
        __acc_top = (__max_euclidean - stats['best_ever'].fitness)
        __acc_bot = (__max_euclidean - 0.0)
        #print("__acc_top: ",__acc_top, "__acc_bot: ",__acc_bot)
        __acc = __acc_top / __acc_bot
        #print("_acc: ", __acc)
        stats['accuracy'] = __acc

        # Convex Hull Volume (3D Dynamic Environment)
        if (params['PROBLEM'] in ['moving_point', 'moving_point_spiral', 'moving_point_vision']):
            # store x,y,z of population in genotype_list
            track_xyz(individuals)
            # calculate convex hull volume
            from utilities.trackers import genotype_list
            import numpy as np
            from scipy.spatial import ConvexHull
            #print("genotype_list: ",genotype_list)
            if len(genotype_list) != 0:
                __genotype = copy(genotype_list[(stats['gen'])])
                #print("gen: ", stats['gen'])
                #print("genotypes[gen0]:",__genotype)
                __genotype.remove(stats['gen'])
                #print("2genotypes[gen0]:",__genotype)
                __points = []
                for i in range(params['POPULATION_SIZE']):
                    #print("i: ", i)
                    #print("__genotype[xyz]", __genotype[i])
                    #print("__genotype[x]", __genotype[i][0])
                    #print("__genotype[y]", __genotype[i][1])
                    #print("__genotype[z]", __genotype[i][2])
                    __points.append([float(__genotype[i][0]), float(__genotype[i][1]), float(__genotype[i][2])])
                #print("__points: ",__points)
                __garray = np.array(__points)
                #print("__garray: ",__garray)
                __cv = ConvexHull(__garray)
                #print("__cv: ",__cv)
                #print("__cvv: ",__cv.volume)
                stats['convexhullvolume'] = __cv.volume

    # Save fitness plot information
    if params['SAVE_PLOTS'] and not params['DEBUG']:
        if not end:
            trackers.best_fitness_list.append(stats['best_ever'].fitness)
            trackers.mean_fitness_list.append(stats['ave_fitness'])
            trackers.fitness_std_list.append(stats['fitness_std'])
            trackers.fitness_iqr_list.append(stats['fitness_iqr'])
            trackers.fitness_variation_list.append(stats['fitness_variation'])
            trackers.fitness_entropy_list.append(stats['fitness_entropy'])

        if params['VERBOSE'] or end:
            save_best_fitness_plot()
            save_fitness_histogram_movie()
            if(params['PROBLEM'] in ['moving_point','moving_point_spiral','moving_point_vision']):
                save_3Dgenotype_movie()
                merge_3Dgenotype_fitnesshistogram_movie()
                outputConvexHullVolume()

    # Print statistics
    if params['VERBOSE']:
        if not end:
            print_stats()
    elif not params['SILENT']:
        perc = stats['gen'] / (params['GENERATIONS']+1) * 100
        stdout.write("Evolution: %d%% complete\r" % perc)
        stdout.flush()

    # Generate test fitness on regression problems
    if params['PROBLEM'] in ("regression", "classification") and \
            (end or (params['COMPLETE_EVALS']
                     and stats['gen'] == params['GENERATIONS'])):
        stats['best_ever'].training_fitness = copy(stats['best_ever'].fitness)
        stats['best_ever'].evaluate(dist='test')
        stats['best_ever'].test_fitness = copy(stats['best_ever'].fitness)
        stats['best_ever'].fitness = stats['best_ever'].training_fitness

    if params['COMPLETE_EVALS'] and not params['DEBUG']:
        if stats['gen'] == params['GENERATIONS']:
            save_best_midway(stats['best_ever'])

    # Save statistics
    if not params['DEBUG']:
        save_stats(end)
        if params['SAVE_ALL']:
            save_best(end, stats['gen'])
        elif params['VERBOSE'] or end:
            save_best(end, "best")

    if end and not params['SILENT']:
        print_final_stats()


def ave(x):
    """
    :param x: a given list
    :return: the average of param x
    """

    return sum(x)/len(x)


def print_stats():
    """Print the statistics for the generation and individuals"""

    print("______\n")
    for stat in sorted(stats.keys()):
        print(" ", stat, ": \t", stats[stat])
    print("\n")


def print_final_stats():
    """
    Prints a final review of the overall evolutionary process
    """

    if params['PROBLEM'] in ("regression", "classification"):
        print("\n\nBest:\n  Training fitness:\t",
              stats['best_ever'].training_fitness)
        print("  Test fitness:\t\t", stats['best_ever'].test_fitness)
    else:
        print("\n\nBest:\n  Fitness:\t", stats['best_ever'].fitness)
    print("  Phenotype:", stats['best_ever'].phenotype)
    print("  Genome:", stats['best_ever'].genome)
    for stat in sorted(stats.keys()):
        print(" ", stat, ": \t", stats[stat])
    print("\nTime taken:\t", stats['total_time'])


def save_stats(end=False):
    """Write the results to a results file for later analysis"""
    if params['VERBOSE']:
        filename = params['FILE_PATH'] + str(params['TIME_STAMP']) + \
                   "/stats.tsv"
        savefile = open(filename, 'a')
        for stat in sorted(stats.keys()):
            savefile.write(str(stat) + "\t" + str(stats[stat]) + "\t")
        savefile.write("\n")
        savefile.close()

    elif end:
        filename = params['FILE_PATH'] + str(params['TIME_STAMP']) + \
                   "/stats.tsv"
        savefile = open(filename, 'a')
        for item in trackers.stats_list:
            for stat in sorted(item.keys()):
                savefile.write(str(item[stat]) + "\t")
            savefile.write("\n")
        savefile.close()

    else:
        trackers.stats_list.append(copy(stats))


def save_stats_headers():
    """
    Saves the headers for all stats in the stats dictionary.
    :return: Nothing.
    """

    filename = params['FILE_PATH'] + str(params['TIME_STAMP']) + "/stats.tsv"
    savefile = open(filename, 'w')
    for stat in sorted(stats.keys()):
        savefile.write(str(stat) + "\t")
    savefile.write("\n")
    savefile.close()


def save_final_stats():
    """
    Appends the total time taken for a run to the stats file.
    """

    filename = params['FILE_PATH'] + str(params['TIME_STAMP']) + "/stats.tsv"
    savefile = open(filename, 'a')
    savefile.write("Total time taken: \t" + str(stats['total_time']))
    savefile.close()


def save_params():
    """
    Save evolutionary parameters
    :return: Nothing
    """

    filename = params['FILE_PATH'] + str(params['TIME_STAMP']) + \
               "/parameters.txt"
    savefile = open(filename, 'w')

    col_width = max(len(param) for param in params.keys())
    for param in sorted(params.keys()):
        savefile.write(str(param) + ": ")
        spaces = [" " for _ in range(col_width - len(param))]
        savefile.write("".join(spaces) + str(params[param]) + "\n")
    savefile.close()


def save_best(end=False, name="best"):

    filename = params['FILE_PATH'] + str(params['TIME_STAMP']) + "/" + \
               str(name) + ".txt"
    savefile = open(filename, 'w')
    savefile.write("Generation:\n" + str(stats['gen']) + "\n\n")
    savefile.write("Phenotype:\n" + str(stats['best_ever'].phenotype) + "\n\n")
    savefile.write("Genotype:\n" + str(stats['best_ever'].genome) + "\n")
    savefile.write("Tree:\n" + str(stats['best_ever'].tree) + "\n")
    if params['PROBLEM'] in ("regression", "classification"):
        if end:
            savefile.write("\nTraining fitness:\n" +
                           str(stats['best_ever'].training_fitness))
            savefile.write("\nTest fitness:\n" +
                           str(stats['best_ever'].test_fitness))
        else:
            savefile.write("\nFitness:\n" + str(stats['best_ever'].fitness))
    else:
        savefile.write("\nFitness:\n" + str(stats['best_ever'].fitness))
    savefile.close()


def save_best_midway(best_ever):
    filename = params['FILE_PATH'] + str(params['TIME_STAMP']) + "/best_" + \
               str(stats['gen']) + ".txt"
    savefile = open(filename, 'w')
    t1 = time.clock()
    trackers.time_list.append(t1)
    time_taken = timedelta(seconds=trackers.time_list[-1] -
                           trackers.time_list[0])
    savefile.write("Generation:\n" + str(stats['gen']) + "\n\n")
    savefile.write("Phenotype:\n" + str(best_ever.phenotype) + "\n\n")
    savefile.write("Genotype:\n" + str(best_ever.genome) + "\n")
    savefile.write("Tree:\n" + str(best_ever.tree) + "\n")
    if params['PROBLEM'] in ("regression", "classification"):
        savefile.write("\nTraining fitness:\t" +
                       str(stats['best_ever'].training_fitness))
        savefile.write("\nTest fitness:\t" +
                       str(stats['best_ever'].test_fitness))
    else:
        savefile.write("\nFitness:\t" + str(stats['best_ever'].fitness))
    savefile.write("\nTotal time:\t" + str(time_taken))
    savefile.close()


def generate_folders_and_files():
    """
    Generates necessary folders and files for saving statistics and parameters.
    """

    if params['EXPERIMENT_NAME']:
        params['FILE_PATH'] = getcwd() + "/results/" + params[
            'EXPERIMENT_NAME'] + "/"
    else:
        params['FILE_PATH'] = getcwd() + "/results/"

    # Generate save folders
    if not path.isdir(params['FILE_PATH']):
        mkdir(params['FILE_PATH'])
    if not path.isdir(params['FILE_PATH'] + str(params['TIME_STAMP'])):
        mkdir(params['FILE_PATH'] + str(params['TIME_STAMP']))

    save_params()
    save_stats_headers()


def outputConvexHullVolume():
    from scipy.spatial import ConvexHull
    from algorithm.parameters import params
    from utilities.trackers import genotype_list
    import numpy as np
    import matplotlib.pyplot as plt

    __cvv = []
    for p in range(params['GENERATIONS']):
        __genotype = genotype_list[p]
        #print("genotypes[gen0]:",__genotype)
        __genotype.remove(p)
        #print("2genotypes[gen0]:",__genotype)
        __points = []
        for i in range(params['POPULATION_SIZE']):
            __points.append([float(__genotype[i][0]), float(__genotype[i][1]), float(__genotype[i][2])])

        #print("__points: ",__points)
        __garray = np.array(__points)
        #print("__garray: ",__garray)
        __cv = ConvexHull(__garray)
        #print("__cv: ",__cv)
        __cvv.append(__cv.volume)
        #print("__cvv: ",__cvv)

    #print("Volumes: ",__cvv)
    stats['convexhullvolume'] = __cvv

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(__cvv)
    ax1.set_ylabel('Convex Hull Volume', fontsize=14)
    ax1.set_xlabel('Generation', fontsize=14)
    plt.title("Moving Point")
    plt.savefig(params['FILE_PATH'] + str(params['TIME_STAMP']) + '/convexhullvolume.pdf')
    plt.close()


def track_xyz(individuals):
    from utilities.trackers import genotype_list
    __ano_gen = [stats['gen'],]
    genotype_list.append(__ano_gen)
    for i in range(params['POPULATION_SIZE']):
        next_xyz = individuals[i].phenotype.split()
        __genotype = [float(next_xyz[0]), float(next_xyz[1]), float(next_xyz[2])]
        genotype_list[stats['gen']].append(__genotype)
