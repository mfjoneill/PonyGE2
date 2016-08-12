from algorithm.parameters import params

def move_target():
    params['DYNAMIC_ENVIRONMENT_TARGET'] = (params['DYNAMIC_ENVIRONMENT_TARGET'][0]+params['X_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][1]+params['Y_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][2]+params['Z_DELTA'])


def move_target_vision(best_distance):
    params['DYNAMIC_ENVIRONMENT_TARGET'] = (params['DYNAMIC_ENVIRONMENT_TARGET'][0]+params['X_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][1]+params['Y_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][2]+params['Z_DELTA'])