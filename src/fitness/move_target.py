from algorithm.parameters import params
from scipy.spatial import distance

def move_target():
    params['DYNAMIC_ENVIRONMENT_TARGET'] = (params['DYNAMIC_ENVIRONMENT_TARGET'][0]+params['X_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][1]+params['Y_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][2]+params['Z_DELTA'])


#def move_target_vision(best_distance):
def move_target_vision():
    if(10 < 2):
        pass
    else:
       params['DYNAMIC_ENVIRONMENT_TARGET'] = (params['DYNAMIC_ENVIRONMENT_TARGET'][0]+params['X_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][1]+params['Y_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][2]+params['Z_DELTA'])


#def move_target_vision(best_distance):
def move_target_vision_avoid(individuals):
    safe_distance = distance.euclidean((params['MP_X_LIM_MAX'], params['MP_Y_LIM_MAX'], params['MP_Z_LIM_MAX']),
                                   (params['MP_X_LIM_MIN'], params['MP_Y_LIM_MIN'], params['MP_Z_LIM_MIN']))* params['MPV_INDIVIDUAL_FIELD_OF_VISION']
    #increase the target along the vector returned by dectect_surrounding
    min_dist = 10000
    closest_x = 0
    closest_y = 0
    closest_z = 0
    for ind in individuals:
       if ind.fitness < min_dist:
           min_dist = ind.fitness
           xyz = ind.phenotype.split()
           closest_x = float(xyz[0])
           closest_y = float(xyz[1])
           closest_z = float(xyz[2])

    if min_dist < safe_distance:
        #Run away
        print("Help")
        params['DYNAMIC_ENVIRONMENT_TARGET'] = (params['DYNAMIC_ENVIRONMENT_TARGET'][0] + (params['X_DELTA']*4),
                                                params['DYNAMIC_ENVIRONMENT_TARGET'][1] + (params['Y_DELTA']*4),
                                                params['DYNAMIC_ENVIRONMENT_TARGET'][2] + (params['Z_DELTA']*4))
    else:
        #keep going
        print("Safe")
        params['DYNAMIC_ENVIRONMENT_TARGET'] = (params['DYNAMIC_ENVIRONMENT_TARGET'][0] + params['X_DELTA'],
                                                params['DYNAMIC_ENVIRONMENT_TARGET'][1] + params['Y_DELTA'],
                                                params['DYNAMIC_ENVIRONMENT_TARGET'][2] + params['Z_DELTA'])

