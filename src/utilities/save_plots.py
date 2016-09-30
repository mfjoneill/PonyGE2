from utilities.trackers import best_fitness_list, fitness_list, genotype_list, target_list
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rc('font', family='Times New Roman')


def save_best_fitness_plot():
    """
    Saves a plot of the current fitness
    :return: Nothing
    """
    from algorithm.parameters import params

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(best_fitness_list)
    ax1.set_ylabel('fitness', fontsize=14)
    ax1.set_xlabel('Generation', fontsize=14)
    plt.title("Best fitness")
    plt.savefig(
        params['FILE_PATH'] + str(params['TIME_STAMP']) + '/fitness.pdf')
    plt.close()


def save_plot_from_data(data, name):
    """
    Saves a plot of a given set of data.
    :param data: the data to be plotted
    :param name: the name of the data to be plotted.
    :return: Nothing.
    """
    from algorithm.parameters import params

    # Plot the data
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(data)
    plt.title(name)
    plt.savefig(
        params['FILE_PATH'] + str(params['TIME_STAMP']) + '/' + name + '.pdf')
    plt.close()


def save_plot_from_file(filename, stat_name):
    """
    Saves a plot of a given stat from the stats file.
    :param filename: a full specified path to a .csv stats file.
    :param stat_name: the stat of interest for plotting.
    :return: Nothing.
    """

    # Read in the data
    data = pd.read_csv(filename, sep="\t")
    try:
        stat = list(data[stat_name])
    except KeyError:
        print("\nError: stat", stat_name, "does not exist")
        quit()

    # Plot the data
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(stat)
    plt.title(stat_name)

    # Get save path
    save_path = "/".join(filename.split("/")[:-1])

    # Save plot
    plt.savefig(save_path + '/' + stat_name + '.pdf')
    plt.close()


def save_fitness_histogram_movie():
    from moviepy.editor import VideoClip
    from moviepy.video.io.bindings import mplfig_to_npimage
    from algorithm.parameters import params

    def make_frame(t):
        """ returns an image of the frame at time t """
        # ... create the frame with any library
        fitness = fitness_list[int(t)]
        __sum_fit = sum(fitness)
        __mean_fit = float(__sum_fit)/float(len(fitness))
        from scipy.stats import tstd, iqr, variation, entropy
        __sd_fit = tstd(fitness)
        __iqr = iqr(fitness)
        __v = variation(fitness)
        __e = entropy(fitness)

        fig = plt.figure()
        plt.hist(fitness)  # ,bins=int(params['POPULATION_SIZE']*0.1))
        plt.title("Moving Point - Population Fitness Histogram - Generation " + str(int(t)))
        plt.axis([0, 20000, 0, params['POPULATION_SIZE']])
        plt.ylabel('#Individuals')
        plt.xlabel('Fitness')
        plt.grid(True)
        __hist_text = "$\mu=" + "{0:.2f}".format(__mean_fit) + ",\ \sigma=" + "{0:.2f}".format(
            __sd_fit) + ",\ entropy=" + "{0:.2f}".format(__e) + ",\ iqr=" + "{0:.2f}".format(__iqr) + "$"
        plt.text(1000, params['POPULATION_SIZE'] * .9, __hist_text)
        return mplfig_to_npimage(fig)  # (Height x Width x 3) Numpy array

    filename = params['FILE_PATH'] + str(params['TIME_STAMP']) + '/fitnessdistribution'
    fps = 1
    duration = params['GENERATIONS']+1
    animation = VideoClip(make_frame, duration=duration)
    #animation.resize(width=1280,height=720)
    animation.write_videofile(filename+".mp4", fps=fps)  # export as video
    animation.write_gif(filename+".gif", fps=fps)  # export as GIF (slow)

def save_3Dgenotype_movie():
    from moviepy.editor import VideoClip
    from moviepy.video.io.bindings import mplfig_to_npimage
    from algorithm.parameters import params

    def make_frame(t):
        """ returns an image of the frame at time t """
        # ... create the frame with any library
        __genotype = genotype_list[int(t)]
        print("__genotype:", __genotype)
        print("__genotype[1]:", __genotype[1],type(__genotype[1]))
        print("__genotype[1][0]:", __genotype[1][0],type(__genotype[1][0]))
        #        print("__genotype[1][0][0]:", __genotype[1][0][0],type(__genotype[1][0][0]))

        print("target: ",target_list)
        print("t: ",t)
        __target = target_list[int(t)]

        xs, ys, zs = [], [], []
        xs.append(__target[0])
        ys.append(__target[1])
        zs.append(__target[2])

        # colour code the target as red, and the population members as blue
        icolor = []
        for i in range(params['POPULATION_SIZE']):
            icolor.append('b')
            nextx, nexty, nextz = [], [], []
            print("__genotype[i+1][0]:", __genotype[i+1][0], type(__genotype[i+1][0]))
            #            print("__genotype[i+1][0][1]:", __genotype[i+1][1][0], type(__genotype[i+1][1][0]))
            #            print("__genotype[i+1][0][2]:", __genotype[i+1][2][0], type(__genotype[i+1][2][0]))
            nextx.append(float(__genotype[i+1][0]))
            nexty.append(float(__genotype[i+1][1]))
            nextz.append(float(__genotype[i+1][2]))
            xs, ys, zs = xs + nextx, ys + nexty, zs + nextz

        c = ['r'] + icolor
        s = [5 for n in range(params['POPULATION_SIZE'])]
        s = [15] + s

        fig = plt.figure()
        ax1 = fig.add_subplot(111, projection='3d')
        ax1.set_autoscale_on(False)
        ax1.scatter(xs, ys, zs, c=c, s=s)
        ax1.set_xlim(params['MP_X_LIM_MIN'], params['MP_X_LIM_MAX'])
        ax1.set_ylim(params['MP_Y_LIM_MIN'], params['MP_Y_LIM_MAX'])
        ax1.set_zlim(params['MP_Z_LIM_MIN'], params['MP_Z_LIM_MAX'])
        ax1.set_ylabel('y', fontsize=14)
        ax1.set_xlabel('x', fontsize=14)
        ax1.set_zlabel('z', fontsize=14)
        # ax1.view_init(15,180)
        ax1.view_init(30, 135)
        plt.title("Moving Point - Generation " + str(int(t)))

        return mplfig_to_npimage(fig)  # (Height x Width x 3) Numpy array

    filename = params['FILE_PATH'] + str(params['TIME_STAMP']) + '/3Dgenotypes'
    fps = 1
    duration = params['GENERATIONS']+1
    animation = VideoClip(make_frame, duration=duration)
    #animation.resize(width=1280,height=720)
    animation.write_videofile(filename+".mp4", fps=fps)  # export as video
    animation.write_gif(filename+".gif", fps=fps)  # export as GIF (slow)

def merge_3Dgenotype_fitnesshistogram_movie():
    from algorithm.parameters import params
    import moviepy.editor as mpy

    fps = 1
    __filename1 = params['FILE_PATH'] + str(params['TIME_STAMP']) + '/3Dgenotypes.mp4'
    __filename2 = params['FILE_PATH'] + str(params['TIME_STAMP']) + '/fitnessdistribution.mp4'
    __outputfilename = params['FILE_PATH'] + str(params['TIME_STAMP']) + '/merge_3Dgenotype_fitnesshistogram.mp4'
    clip_mayavi = mpy.VideoFileClip(__filename1)
    clip_mpl = mpy.VideoFileClip(__filename2)
    animation = mpy.clips_array([[clip_mpl, clip_mayavi]])
    animation.write_videofile(__outputfilename, fps=fps)

    # Make the white color transparent in clip_mayavi
    clip_mayavi2 = (clip_mpl.fx(mpy.vfx.mask_color, [255, 255, 255])
                    .set_opacity(.8)  # whole clip is semi-transparent
                    #.resize(height=0.33 * clip_mpl.h)    # needs pillow 2.9
                    #  (more recent packages break resize)
                    .set_pos('left'))
    # resize giving error messages!!

    __outputfilename2 = params['FILE_PATH'] + str(params['TIME_STAMP']) + '/merge_3Dgenotype_fitnesshistogram_2.mp4'
    animation = mpy.CompositeVideoClip([clip_mayavi, clip_mayavi2])
    animation.write_videofile(__outputfilename2, fps=fps)