from algorithm.parameters import params
from scipy.spatial import distance
from scipy.stats import entropy, variation, iqr, tstd
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
    trackers.target_list.append(xyz)

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
    icolor = []
    __ano_gen = [generation,]
    trackers.genotype_list.append(__ano_gen)
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
        nextx, nexty, nextz = [], [], []
        nextx.append(float(next_xyz[0]))
        nexty.append(float(next_xyz[1]))
        nextz.append(float(next_xyz[2]))
        xs, ys, zs = xs+nextx, ys+nexty, zs+nextz
        __genotype = [nextx, nexty, nextz]
        trackers.genotype_list[generation].append(__genotype)

    c = ['r'] + icolor
    s = [5 for n in range(params['POPULATION_SIZE'])]
    s = [15] + s

# COMMENTED OUT CODE BELOW WHICH GENERATIONS .pdf of each generation 3D scatterplot
# A MOVIE IS NOW GENERATED in save_plots USING data generated in trackers above
#
#
#    fig = plt.figure()
#    ax1 = fig.add_subplot(111, projection='3d')
#    ax1.set_autoscale_on(False)
#    ax1.scatter(xs,ys,zs,c=c,s=s)
#    ax1.set_xlim(params['MP_X_LIM_MIN'],params['MP_X_LIM_MAX'])
#    ax1.set_ylim(params['MP_Y_LIM_MIN'],params['MP_Y_LIM_MAX'])
#    ax1.set_zlim(params['MP_Z_LIM_MIN'],params['MP_Z_LIM_MAX'])
#    ax1.set_ylabel('y', fontsize=14)
#    ax1.set_xlabel('x', fontsize=14)
#    ax1.set_zlabel('z', fontsize=14)
#    ax1.view_init(30,135)
#    plt.title("Moving Point - Generation " +  str(generation))
#    plt.show()
#
#    time1 =  datetime.now()
#    hms = "%02d%02d%02d" % (time1.hour, time1.minute, time1.second)
#
#    plt.savefig(
#        params['FILE_PATH'] + str(params['TIME_STAMP']) + '/movingpointpopulation_' + str(hms) + '_' + str(generation) + '.pdf')
#    plt.savefig(
#        params['FILE_PATH'] + str(params['TIME_STAMP']) + '/' + str(generation) + '.png')
#    plt.close()


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
        #plotly.plotly.plot(data)
        title = "Moving Point - Generation " + str(generation)
        layout = Layout(title=title,
                        #xaxis=dict(range=[0,params['MP_X_LIM_MAX']]),
                        #yaxis=dict(range=[0,params['MP_Y_LIM_MAX']])
                        )
        fig1 = Figure(data=data,layout=layout)
        filename = "movingpointdisplay.html"
        if not params['JUPYTER']:
            mpd_div = plotly.offline.plot(fig1, filename=filename, auto_open=True, output_type='div',show_link=False)


        # create fitness plot
        #

        trace4 = Scatter(x=generation, y=trackers.best_fitness_list,
                          mode='lines+markers',
                          marker=dict(
                              # color='rgb(127, 127, 127)',
                              color='blue',
                              size=6,
                              symbol='circle-open',
                          ),
                          opacity=0.9,
                          name='Best Fitness'
                          )

        trace4a = Scatter(x=generation, y=trackers.mean_fitness_list,
                          mode='lines+markers',
                          marker=dict(
                              # color='rgb(127, 127, 127)',
                              color='green',
                              size=6,
                              symbol='circle-open',
                          ),
                          opacity=0.9,
                          name='Mean Fitness'
                          )

        trace5 = Scatter(x=generation, y=trackers.fitness_entropy_list,
                          mode='lines+markers',
                          marker=dict(
                              color='red',
                              size=4,
                              symbol='circle',
                          ),
                          opacity=0.9,
                          name='Entropy',
                          yaxis='y2'
                          )

        #plotly.offline.plot([trace5])

        trace6 = Scatter(x=generation, y=trackers.fitness_variation_list,
                          mode='lines+markers',
                          marker=dict(
                              color='black',
                              size=4,
                              symbol='circle-open',
                          ),
                          opacity=0.9,
                          name='Variation',
                          yaxis='y2'
                          )

        trace6a = Scatter(x=generation, y=trackers.fitness_iqr_list,
                          mode='lines+markers',
                          marker=dict(
                              color='grey',
                              size=4,
                              symbol='circle-open',
                          ),
                          opacity=0.9,
                          name='IQR'#,
                          #yaxis='y2'
                          )

        #fig = tools.make_subplots(1,1)
        #fig.append_trace(trace4,1,1)
        #fig.append_trace(trace4a,1,1)
        #fig.append_trace(trace5,1,1)
        #fig.append_trace(trace6,1,1)

        data = [trace4,trace4a,trace5,trace6,trace6a]
        #plotly.offline.plot(data)
        title = ""#"Moving Point - Generation " + str(generation)
        #fig['layout'].update(title=title, legend=dict(orientation='h'),
        #                     yaxis1=dict(side='left',autorange=True),
        #                     yaxis2=dict(title='Diversity/Dispersion',type='linear',side='right',overlaying='y',range=[0,4])) #,yaxis=dict(type='log',autorange=True)
        #fig['layout']['yaxis1'].update(title='Fitness',type='log')
        #fig['layout']['yaxis2'].update(title='Diversity/Dispersion',side='right',type='log')
        layout = Layout(title=title, legend=dict(orientation='h'),
                            #yaxis=dict(range=[0,100000]),
                            yaxis1=dict(title='Fitness',type='log'),
                            #xaxis=dict(range=[0,params['GENERATIONS']],title='Generation')
                            xaxis=dict(title='Generations'),
                            yaxis2=dict(title='Entropy/Variation/IQR',side='right',overlaying='y',type='linear',autorange=True)
                        )
        fig2 = Figure(data=data,layout=layout)
        filename = "movingpointdisplay_fitness.html"
        if not params['JUPYTER']:
            mpdfit_div = plotly.offline.plot(fig2,filename=filename,auto_open=True,output_type='div',show_link=False)


        # plot correlations
        #
        trace7 = Scatter(y=trackers.best_fitness_list, x=trackers.fitness_variation_list,
                          mode='markers',
                          marker=dict(
                              color='black',
                              size=4,
                              symbol='circle-open',
                          ),
                          opacity=0.9,
                          name='Variation',
                          xaxis='x2'
                          )
        data = [trace7]
        title = "Best Fitness vs Variation"
        layout = Layout(title=title, legend=dict(orientation='h'),
                            #yaxis=dict(range=[0,100000]),
                            yaxis=dict(title='Best Fitness'),
                            #xaxis=dict(range=[0,params['GENERATIONS']],title='Generation')
                            xaxis=dict(title='Variation')
                        )
        figcorr1 = Figure(data=data,layout=layout)
        filename = "movingpointdisplay_fitness_variation.html"
        if not params['JUPYTER']:
            mpdfitvarcorr_div = plotly.offline.plot(figcorr1,filename=filename,auto_open=True,output_type='div',show_link=False)

        trace8 = Scatter(y=trackers.best_fitness_list, x=trackers.fitness_entropy_list,
                          mode='markers',
                          marker=dict(
                              color='red',
                              size=4,
                              symbol='circle',
                          ),
                          opacity=0.9,
                          name='Entropy',
                          xaxis='x3'
                          )
        data = [trace7,trace8]
        title = ""#"Best Fitness vs Entropy"
        layout = Layout(title=title, legend=dict(orientation='v'),
                            yaxis=dict(title='Best Fitness'),
                            xaxis2=dict(title='Variation',autorange=True),
                            xaxis3=dict(title='Entropy',overlaying='x2',side='top',autorange=True)
                        )
        figcorr2 = Figure(data=data,layout=layout)
        filename = "movingpointdisplay_fitness_entropy.html"
        if not params['JUPYTER']:
            mpdfitentropycorr_div = plotly.offline.plot(figcorr2,filename=filename,auto_open=True,output_type='div',show_link=False)


        # Create fitness histogram plot
        #
        # retrieve a fitness list for the population
        #
        fitness = []
        fitness = trackers.fitness_list[generation]
#        __sum_fit = sum(fitness)
#        __mean_fit = float(__sum_fit)/float(len(fitness))
#        __sd_fit = tstd(fitness)
#        __iqr = iqr(fitness)
#        __v = variation(fitness)
#        __e = entropy(fitness)
        # plot fitness distribution histogram
        #

        trace3 = Histogram(x=fitness)
        data = [trace3]
        title = "Moving Point - Population Fitness Distribution - " + str(generation)
        layout = Layout(title=title,
        #                xaxis=dict(range=[0, 100000]),
                        yaxis=dict(range=[0, params['POPULATION_SIZE']])
                        )
        fig3 = Figure(data=data, layout=layout)
        filename = "movingpointdisplay_fitnessdistribution.html"
        if not params['JUPYTER']:
            mpdfd_div = plotly.offline.plot(fig3, filename=filename,auto_open=True,output_type='div',show_link=False)
            # create pyplots for movie generation...
#            plt.hist(fitness)#,bins=int(params['POPULATION_SIZE']*0.1))
#            plt.title("Moving Point - Population Fitness Histogram - Generation " + str(generation))
#            #plt.show()
#            plt.axis([0, 20000, 0, params['POPULATION_SIZE']])
#            plt.ylabel('#Individuals')
#            plt.xlabel('Fitness')
#            plt.grid(True)
#            __hist_text = "$\mu="+"{0:.2f}".format(__mean_fit)+",\ \sigma="+"{0:.2f}".format(__sd_fit)+",\ entropy="+"{0:.2f}".format(__e)+",\ iqr="+"{0:.2f}".format(__iqr)+"$"
#            plt.text(1000,params['POPULATION_SIZE']*.9, __hist_text)
#            time1 = datetime.now()
#            hms = "%02d%02d%02d" % (time1.hour, time1.minute, time1.second)
#            plt.savefig(
#                params['FILE_PATH'] + str(params['TIME_STAMP']) + '/movingpointpopulation_fitnessdistribution_' + str(hms) + '_' + str(
#                    generation) + '.pdf')
#            plt.close()



        if not params['JUPYTER']:
            file_html = open('test.html','w')
            file_html.write('<html>')
            #file_html.write('''<div style="clear:left/right/both;">''')
            #file_html.write(mpd_div)
            #file_html.write('</div>')
            #another row
            file_html.write('''<div style="width: 100%;">''')
            file_html.write('''<div style="width: 50%; height: 300; float: left;">''')
            file_html.write(mpd_div)
            #file_html.write(mpdfitvarcorr_div)
            file_html.write(mpdfitentropycorr_div)
            file_html.write('</div>')

            file_html.write('''<div style="width: 50%; height: 300; display: inline-block;">''')
            file_html.write(mpdfd_div)
            file_html.write(mpdfit_div)
            file_html.write('</div>')
            file_html.write('</div>')
            # another row
            file_html.write('</html>')
            file_html.close()
            import webbrowser
            webbrowser.open('file:///Users/mike/work/PyCharmProjects/PonyGE2/src/test.html',new=0)
            time.sleep(1)

        if (params['JUPYTER']):
            fig4 = tools.make_subplots(rows=2, specs=[[{'is_3d': True}], [{'is_3d': False}]])
            fig4.append_trace(trace1,1,1)
            fig4.append_trace(trace2,1,1)
            fig4.append_trace(trace3,2,1)
            #print(fig4.to_string())
            plotly.offline.iplot(fig4,show_link=False)
            #mpd_div = plotly.offline.iplot(fig1)
            #mpdfit_div = plotly.offline.iplot(fig2)
            #mpdfd_div = plotly.offline.iplot(fig3)


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
