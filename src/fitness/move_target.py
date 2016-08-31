from algorithm.parameters import params

def move_target():
    params['DYNAMIC_ENVIRONMENT_TARGET'] = (params['DYNAMIC_ENVIRONMENT_TARGET'][0]+params['X_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][1]+params['Y_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][2]+params['Z_DELTA'])


#def move_target_vision(best_distance):
def move_target_vision():
    if(10 < 2):
        pass
    else:
       params['DYNAMIC_ENVIRONMENT_TARGET'] = (params['DYNAMIC_ENVIRONMENT_TARGET'][0]+params['X_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][1]+params['Y_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][2]+params['Z_DELTA'])


#def move_target_vision(best_distance):
def move_target_vision_avoid():
       #increase the target along the vector returned by dectect_surrounding
       params['DYNAMIC_ENVIRONMENT_TARGET'] = (params['DYNAMIC_ENVIRONMENT_TARGET'][0]+params['X_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][1]+params['Y_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][2]+params['Z_DELTA'])


def detect_surrounding(current_vector):
    #for all the inds find the closet
    #if(range > safe)
        #do nothing
        #return current_vector
    #else
        #get vector
        #return new_vector
