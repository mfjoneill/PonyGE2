from scipy.spatial import distance
from algorithm.parameters import params
from representation import individual

class MovingPoint:
    """Fitness function for the moving point problem.
    .....calculate the euclidean distance from the target (x,y,z) point to the guess point
    Usage: MovingPoint(...) returns a *callable object*, ie the fitness
    function."""

    maximise = False

    def __init__(self, target):
        self.target = target

    def __call__(self, guess, target, grid_eval=False):
        if grid_eval:
            self.target = target
            position_xyz = guess.split()
            position_xyz[0] = float(position_xyz[0])
            position_xyz[1] = float(position_xyz[1])
            position_xyz[2] = float(position_xyz[2])

            # calculate the distance to the self.target to this guess at position_xyz
            fitness = distance.euclidean(position_xyz, self.target)

            # calculate the max euclidean distance in this search space
            max_euclidean = distance.euclidean((params['MP_X_LIM_MAX'],
                                                params['MP_Y_LIM_MAX'],
                                                params['MP_Z_LIM_MAX']), (
                                               params['MP_X_LIM_MIN'],
                                               params['MP_Y_LIM_MIN'],
                                               params['MP_Z_LIM_MIN']))
            # print(max_euclidean)

            # is the target within params['MPV_FIELD_OF_VISION'] of the max_euclidean distance?
            # if not, the individual cannot "see" the target and is provided with the worst possible fitness
            return fitness
        else:
            self.target = target
            position_xyz = guess.split()
            position_xyz[0] = float(position_xyz[0])
            position_xyz[1] = float(position_xyz[1])
            position_xyz[2] = float(position_xyz[2])

            # calculate the distance to the self.target to this guess at position_xyz
            fitness = distance.euclidean(position_xyz,self.target)

            # calculate the max euclidean distance in this search space
            max_euclidean = distance.euclidean((params['MP_X_LIM_MAX'],params['MP_Y_LIM_MAX'],params['MP_Z_LIM_MAX']),(params['MP_X_LIM_MIN'],params['MP_Y_LIM_MIN'],params['MP_Z_LIM_MIN']))
            #print(max_euclidean)

            # is the target within params['MPV_FIELD_OF_VISION'] of the max_euclidean distance?
            # if not, the individual cannot "see" the target and is provided with the worst possible fitness
            if(params['MPV_VISION_ENABLED']):
                if fitness > max_euclidean*params['MPV_INDIVIDUAL_FIELD_OF_VISION']:
                    fitness = max_euclidean    # worst possible fitness
                    return fitness
                else:
                    return fitness
            else:
                return fitness