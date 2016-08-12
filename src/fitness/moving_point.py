from scipy.spatial import distance

class MovingPoint:
    """Fitness function for the moving point problem.
    .....calculate the euclidean distance from the target (x,y,z) point to the guess point
    Usage: MovingPoint(...) returns a *callable object*, ie the fitness
    function."""

    maximise = False

    def __init__(self, target):
        self.target = target

    def __call__(self, guess, target):
        # (re)set target in case it has changed
        self.target = target
        # the phenotype x y z coordinates are contained in guess
        # we need to parse out the strings and cast each to a float
        position_xyz = guess.split()
        position_xyz[0] = float(position_xyz[0])
        position_xyz[1] = float(position_xyz[1])
        position_xyz[2] = float(position_xyz[2])
        # calculate the distance to the self.target to this guess at position_xyz
        # simple euclidean distance between n-dimensional points is employed
        fitness = distance.euclidean(position_xyz,self.target)
        return fitness
