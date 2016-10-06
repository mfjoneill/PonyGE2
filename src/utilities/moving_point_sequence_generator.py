import random

def generate_sequence(name, max_p=10000,interval=None, seed=None):
    points = []
    if seed is None:
        random.seed(12345)
    else:
        random.seed(seed)
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
            else:
                for i in range(seq_len):
                    points.append(new_point)
        elif interval > 1:
            gard = max_p - len(points)
            new_point = (random.randint(0, 10000),
                           random.randint(0, 10000),
                           random.randint(0, 10000))
            if interval > gard:
                for i in range(gard):
                    points.append(new_point)
            else:
                for i in range(interval):
                    points.append(new_point)
        elif interval==1:
            points.append((random.randint(0, 10000),
                           random.randint(0, 10000),
                           random.randint(0, 10000)))
        else:
            print("Specify an interval greater than 0 "
                  "or else provide no interval for random interval")
            exit()

    f = open(name+'.csv', 'w')
    for point in points:
        f.write("%d,%d,%d\n" % point)
    f.close()

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
    #generate_sequence('random')
    #generate_sequence('10_steps',interval=10)
    generate_sequence('20_steps',interval=20)
    #generate_sequence('1_step',interval=1)
    #read_target_points('1_step.csv')