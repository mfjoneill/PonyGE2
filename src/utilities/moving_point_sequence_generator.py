import random
from scipy.spatial import distance
from math import pi,cos,sin,acos

def generate_sequence(name, max_p=10000,interval=None, seed=None,max_s=20):
    points = []
    dists = []
    if seed is None:
        random.seed(12345)
    else:
        random.seed(seed)
    prev_point = (0,0,0)
    while len(points)<max_p:
        if interval is None:
            gard = max_p - len(points)
            seq_len = random.randrange(1,max_s)
            new_point = (random.randint(0, 10000),
                           random.randint(0, 10000),
                           random.randint(0, 10000))
            if seq_len > gard:
                for i in range(gard):
                    points.append(new_point)
                    dists.append(distance.euclidean(prev_point,new_point))
                    #print(dists)
                    prev_point = new_point
            else:
                for i in range(seq_len):
                    points.append(new_point)
                    dists.append(distance.euclidean(prev_point, new_point))
                    #print(dists)
                    prev_point = new_point
        elif interval > 1:
            gard = max_p - len(points)
            new_point = (random.randint(0, 10000),
                           random.randint(0, 10000),
                           random.randint(0, 10000))
            if interval > gard:
                for i in range(gard):
                    points.append(new_point)
                    dists.append(distance.euclidean(prev_point, new_point))
                    prev_point = new_point
            else:
                for i in range(interval):
                    points.append(new_point)
                    dists.append(distance.euclidean(prev_point, new_point))
                    prev_point = new_point
        elif interval==1:
            new_point = (random.randint(0, 10000),
                           random.randint(0, 10000),
                           random.randint(0, 10000))
            points.append(new_point)
            dists.append(distance.euclidean(prev_point, new_point))
            prev_point = new_point
        else:
            print("Specify an interval greater than 0 "
                  "or else provide no interval for random interval")
            exit()

    f = open(name+'.csv', 'w')
    g = open(name+'_dists.csv','w')
    for i in range(len(points)):
        f.write("%d,%d,%d\n" % points[i])
        g.write("%d\n"% dists[i])
    f.close()
    g.close()

def get_point_on_sphere(point, radius):
    not_found = True
    x,y,z = -1,-1,-1
    while not_found:
        u = random.random()
        v = random.random()
        theta = 2 * pi * u
        phi = acos(2 * v - 1)
        x = point[0] + (radius * sin(phi) * cos(theta))
        y = point[1] + (radius * sin(phi) * sin(theta))
        z = point[2] + (radius * cos(phi))
        if x < 10000 and x > 0 and y < 10000 and y > 0 and z<10000 and z>0:
           not_found = False
    return (x, y, z)

def generate_sequence_with_fixed_amplitude(name, max_p=10000, interval=None,
                                   seed=None, amplitude=None):
    points = []
    dists = []
    if seed is None:
        random.seed(12345)
    else:
        random.seed(seed)
    prev_point = (0, 0, 0)
    points.append(prev_point)
    dists.append(0)
    while len(points) < max_p:
        if interval is None:
            gard = max_p - len(points)
            seq_len = random.randrange(1, 20)
            new_point = get_point_on_sphere(points[len(points)-1], amplitude)
            print(new_point)
            if seq_len > gard:
                for i in range(gard):
                    points.append(new_point)
                    dists.append(distance.euclidean(prev_point, new_point))
                    prev_point = new_point
            else:
                for i in range(seq_len):
                    points.append(new_point)
                    dists.append(distance.euclidean(prev_point, new_point))
                    prev_point = new_point
        elif interval > 1:
            gard = max_p - len(points)
            new_point = get_point_on_sphere(points[len(points)-1], amplitude)
            if interval > gard:
                for i in range(gard):
                    points.append(new_point)
                    dists.append(distance.euclidean(prev_point, new_point))
                    prev_point = new_point
            else:
                for i in range(interval):
                    points.append(new_point)
                    dists.append(distance.euclidean(prev_point, new_point))
                    prev_point = new_point
        elif interval == 1:
            new_point = get_point_on_sphere(points[len(points)-1], amplitude)
            points.append(new_point)
            dists.append(distance.euclidean(prev_point, new_point))
            prev_point = new_point
        else:
            print("Specify an interval greater than 0 "
                  "or else provide no interval for random interval")
            exit()

    f = open(name + '.csv', 'w')
    g = open(name + '_dists.csv', 'w')
    for i in range(len(points)):
        f.write("%d,%d,%d\n" % points[i])
        g.write("%d\n" % dists[i])
    f.close()
    g.close()

def read_target_points(filename):
    points = []
    f = open(filename, 'r')
    for line in f:
        input = line.split(',')
        point = (int(input[0]),int(input[1]),int(input[2]))
        points.append(point)
    return points

if __name__ == "__main__":
    #print("Uncomment as needed")
    #generate_sequence('random')
    #generate_sequence('10_steps',interval=10)
    #generate_sequence('20_steps',interval=20)
    #generate_sequence('1_step',interval=1)
    generate_sequence('longrandom',max_p=100000,max_s=50)

    #max_distance = distance.euclidean((0,0,0),(10000,10000,10000))
    #print("First")
    #generate_sequence_with_fixed_amplitude('random_10', amplitude = max_distance*0.1)
    #print("Second")
    #generate_sequence_with_fixed_amplitude('random_30',
    #                                       amplitude= max_distance * 0.3)
    #print("Third")
    #generate_sequence_with_fixed_amplitude('random_50',
    #                                       amplitude= max_distance * 0.5)
    #print("Fourth")
    #generate_sequence_with_fixed_amplitude('random_70',
    #                                       amplitude=max_distance * 0.7)
    #read_target_points('1_step.csv')