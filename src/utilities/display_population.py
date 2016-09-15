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
from utilities import trackers


def display_3D_population(individuals,generation,target='DYNAMIC_ENVIRONMENT_TARGET'):
    """
    Displays each individual in the moving_point population
    where each individual is a set of x,y,z coordinates
    Also displays the current DYNAMIC_ENVIRONMENT_TARGET
    :return: Nothing
    """

    # store the x,y,z coordinates of the target[0]
    #
    xs, ys, zs = [], [], []  
    xyz = params[target]
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


def display_3D_plotly_population(individuals,generation):
    """
    Using plotly.offline.plot - displays each individual in the moving_point population
    where each individual is a set of x,y,z coordinates
    Also displays the current DYNAMIC_ENVIRONMENT_TARGET
    :return: Nothing
    """
    if (params['PLOTLY']):
        # generate PLOTLY dashboard/charts
        print("generate plot.ly charts....")
        from plotly import tools
        import plotly
        from plotly.graph_objs import Scatter, Scatter3d, Layout, Figure, Histogram

        # retrieve the x,y,z coordinates of the target[0]
        #
        xyz = params['DYNAMIC_ENVIRONMENT_TARGET']
        txs, tys, tzs = [], [], []
        # print("xyz:", xyz)
        txs.append(xyz[0])
        tys.append(xyz[1])
        tzs.append(xyz[2])

        trace1 = Scatter3d(x=txs, y=tys, z=tzs,
                          mode='markers',
                          marker=dict(
                              # color='rgb(127, 127, 127)',
                              color='red',
                              size=8,
                              symbol='circle',
                          ),
                          opacity=0.9,
                          name='Target'
                          )

        # retrieve the x,y,z coordinates of the individuals
        #
        xs, ys, zs = [], [], []
        for i in range(params['POPULATION_SIZE']):
            next_xyz = individuals[i].phenotype.split()
            # print("next_xyz:",next_xyz)
            nextx, nexty, nextz = [], [], []
            nextx.append(float(next_xyz[0]))
            nexty.append(float(next_xyz[1]))
            nextz.append(float(next_xyz[2]))
            xs, ys, zs = xs + nextx, ys + nexty, zs + nextz

        trace2 = Scatter3d(x=xs, y=ys, z=zs,
                          mode='markers',
                          marker=dict(
                              # color='rgb(127, 127, 127)',
                              color='blue',
                              size=4,
                              symbol='circle',
                          ),
                          opacity=0.9,
                          name='Population'
                          )

        data = [trace1,trace2]
        #plotly.offline.plot(data)
        title = "Moving Point - Generation " + str(generation)
        layout = Layout(title=title,
                        #xaxis=dict(range=[0,params['MP_X_LIM_MAX']]),
                        #yaxis=dict(range=[0,params['MP_Y_LIM_MAX']])
                        )
        fig = Figure(data=data,layout=layout)
        filename = "movingpointdisplay.html"
        mpd_div = plotly.offline.plot(fig,filename=filename,auto_open=True,output_type='div')

        # Create fitness histogram plot
        #
        # retrieve a fitness list for the population
        #
        fitness = []
        for i in range(params['POPULATION_SIZE']):
            fitness.append(individuals[i].fitness)

        #        max_fit = max(fitness)
        #        min_fit = min(fitness)
        #        sum_fit = sum(fitness)
        #        mean_fit = float(sum_fit)/float(len(fitness))

        # create fitness plot
        #

        trace4 = Scatter(x=generation, y=trackers.best_fitness_list,
                          mode='lines+markers',
                          marker=dict(
                              # color='rgb(127, 127, 127)',
                              color='blue',
                              size=4,
                              symbol='circle',
                          ),
                          opacity=0.9,
                          name='Best Fitness'
                          )

        data = [trace4]
        #plotly.offline.plot(data)
        title = "Moving Point - Generation " + str(generation)
        layout = Layout(title=title,
                        #yaxis=dict(range=[0,100000]),
                        yaxis=dict(title='Best Fitness'),
                        xaxis=dict(range=[0,params['GENERATIONS']],title='Generation')
                        )
        fig = Figure(data=data,layout=layout)
        filename = "movingpointdisplay_fitness.html"
        mpdfit_div = plotly.offline.plot(fig,filename=filename,auto_open=True,output_type='div')


        # plot fitness distribution histogram
        #

        trace3 = Histogram(x=fitness)
        data = [trace3]
        title = "Moving Point - Population Fitness Distribution - " + str(generation)
        layout = Layout(title=title,
        #                xaxis=dict(range=[0, 100000]),
                        yaxis=dict(range=[0, params['POPULATION_SIZE']])
                        )
        fig = Figure(data=data, layout=layout)
        filename = "movingpointdisplay_fitnessdistribution.html"
        mpdfd_div = plotly.offline.plot(fig, filename=filename,auto_open=True,output_type='div')
        file_html = open('test.html','w')
        file_html.write('<html>')
        file_html.write('''<div style="width: 100%;">''')
        file_html.write('''<div style="width: 50%; height: 600; float: left;">''')
        file_html.write(mpd_div)
        file_html.write('</div>')
        file_html.write('''<div style="width: 50%; height: 300; display: inline-block;">''')
        file_html.write(mpdfd_div)
        file_html.write(mpdfit_div)
        file_html.write('</div></div>')
        file_html.write('<div>')
        # another row
        file_html.write('</div></html>')
        file_html.close()
        import webbrowser
        webbrowser.open('file:///Users/mike/work/PyCharmProjects/PonyGE2/src/test.html',new=0)
        time.sleep(1)


def display_3D_population_dual_target(individuals,generation):
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

    xyz_alt = params['DYNAMIC_ENVIRONMENT_TARGET_ALT']
    # print("xyz:", xyz)
    xs.append(xyz_alt[0])
    ys.append(xyz_alt[1])
    zs.append(xyz_alt[2])
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

    c = ['r','y'] + icolor

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
