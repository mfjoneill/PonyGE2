import random
from scipy.spatial import distance

def generate_sequence(name, max_p=10000,interval=None, seed=None):
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
            seq_len = random.randrange(1,20)
            new_point = (random.randint(0, 10000),
                           random.randint(0, 10000),
                           random.randint(0, 10000))
            if seq_len > gard:
                for i in range(gard):
                    points.append(new_point)
                    dists.append(distance.euclidean(prev_point,new_point))
                    prev_point = new_point
            else:
                for i in range(seq_len):
                    points.append(new_point)
                    dists.append(distance.euclidean(prev_point, new_point))
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

def read_target_points(filename):
    points = []
    f = open(filename, 'r')
    for line in f:
        input = line.split(',')
        point = (int(input[0]),int(input[1]),int(input[2]))
        points.append(point)
    return points

if __name__ == "__main__":
    print("Uncomment as needed")
    generate_sequence('random')
    generate_sequence('10_steps',interval=10)
    generate_sequence('20_steps',interval=20)
    generate_sequence('1_step',interval=1)
    #read_target_points('1_step.csv')