from algorithm.parameters import params
from scipy.spatial import distance
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
plt.rc('font', family='Times New Roman')
from datetime import datetime
import time



def display_3D_population(individuals,generation):
    """
    Displays each individual in the moving_point population
    where each individual is a set of x,y,z coordinates
    Also displays the current DYNAMIC_ENVIRONMENT_TARGET
    :return: Nothing
    """

    # store the x,y,z coordinates of the target[0]
    #
    xs, ys, zs = [], [], []  
    xyz = params['DYNAMIC_ENVIRONMENT_TARGET']
    #print("xyz:", xyz)
    xs.append(xyz[0])
    ys.append(xyz[1])
    zs.append(xyz[2])
    #print("xs:",xs,"ys:",ys,"zs:",zs)

    # retrieve and append the populations x,y,z coordinates to xs, ys, zs
    #
    max_euclidean = distance.euclidean((params['MP_X_LIM_MAX'], params['MP_Y_LIM_MAX'], params['MP_Z_LIM_MAX']),
                                       (params['MP_X_LIM_MIN'], params['MP_Y_LIM_MIN'], params['MP_Z_LIM_MIN']))

    # colour code the target as red, and the population members as blue
    #icolor = ['b']
    #icolor = icolor * params['POPULATION_SIZE']
    # print(icolor)

    # print(c)
    icolor = []
    for i in range(params['POPULATION_SIZE']):
        #print(individuals[i].phenotype)
        if params['MPV_VISION_ENABLED']:
            if individuals[i].fitness > max_euclidean * params['MPV_INDIVIDUAL_FIELD_OF_VISION']:
                icolor.append('b')
            else:
                icolor.append('g')
        else:
            icolor.append('b')
        next_xyz = individuals[i].phenotype.split()
        #print("next_xyz:",next_xyz)
        nextx, nexty, nextz = [], [], []
        nextx.append(float(next_xyz[0]))
        nexty.append(float(next_xyz[1]))
        nextz.append(float(next_xyz[2]))
        xs, ys, zs = xs+nextx, ys+nexty, zs+nextz

    c = ['r'] + icolor

    #nx, ny, nz = [23.0, 22.0], [15.0, 14.0], [2.0, 1.0]
    #xs, ys, zs = xs+nx, ys+ny, zs+nz
    #print("xs:",xs,"ys:",ys,"zs:",zs)
    #print("type of xs[0] is:",type(xs[0]), "type of xs is:",type(xs))


    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.set_autoscale_on(False)
    ax1.scatter(xs,ys,zs,c=c)
    ax1.set_xlim(params['MP_X_LIM_MIN'],params['MP_X_LIM_MAX'])
    ax1.set_ylim(params['MP_Y_LIM_MIN'],params['MP_Y_LIM_MAX'])
    ax1.set_zlim(params['MP_Z_LIM_MIN'],params['MP_Z_LIM_MAX'])
    ax1.set_ylabel('y', fontsize=14)
    ax1.set_xlabel('x', fontsize=14)
    ax1.set_zlabel('z', fontsize=14)
    #ax1.view_init(15,180)
    ax1.view_init(30,135)
    plt.title("Moving Point - Generation " +  str(generation))
    plt.show()

    time1 =  datetime.now()
    hms = "%02d%02d%02d" % (time1.hour, time1.minute, time1.second)

    plt.savefig(
        params['FILE_PATH'] + str(params['TIME_STAMP']) + '/movingpointpopulation_' + str(hms) + '_' + str(generation) + '.pdf')
    plt.savefig(
        params['FILE_PATH'] + str(params['TIME_STAMP']) + '/' + str(generation) + '.png')
    plt.close()


