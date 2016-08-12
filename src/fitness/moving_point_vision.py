from scipy.spatial import distance

class MovingPointVision:
    """Fitness function for the moving point problem.
    .....calculate the euclidean distance from the target (x,y,z) point to the guess point
    Usage: MovingPoint(...) returns a *callable object*, ie the fitness
    function."""

    maximise = False

    def __init__(self, target):
        self.target = target

    def __call__(self, guess, target):
        self.target = target
        #print ("hey I'm in the MovingPoints() fitness function!")
        #print ("the phenotype is: ", guess)
        #print (type(guess))
        position_xyz = guess.split()
        #print(position_xyz)
        position_xyz[0] = float(position_xyz[0])
        position_xyz[1] = float(position_xyz[1])
        position_xyz[2] = float(position_xyz[2])
        #print ("position_xyz is: ", position_xyz)
        #calculate the distance to the self.target to this guess at position_xyz
        #print(self.target)
        fitness = distance.euclidean(position_xyz,self.target)
        #print(fitness)
        #print ("...phew I'm leaving the MovingPoints() fitness function :-)")
        return fitness
