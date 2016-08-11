from algorithm.parameters import params

def move_target():
#    xdelta, ydelta, zdelta =  0.1001,  0.1001, 0.1001
#    xdelta, ydelta, zdelta =  1.1001,  1.1001, 1.1001
#    xdelta, ydelta, zdelta =  2.1001,  2.1001, 2.1001
#    xdelta, ydelta, zdelta =  3.1001,  3.1001, 3.1001
#    xdelta, ydelta, zdelta =  0.0101,  0.0101, 0.0101
    xdelta, ydelta, zdelta =  1.0000,  1.0000, 1.0000
#    xdelta, ydelta, zdelta = 0.001, 0.001, 10.001
#    xdelta, ydelta, zdelta = 0.001, 10.001, 0.001
    params['DYNAMIC_ENVIRONMENT_TARGET'] = (params['DYNAMIC_ENVIRONMENT_TARGET'][0]+xdelta, params['DYNAMIC_ENVIRONMENT_TARGET'][1]+ydelta, params['DYNAMIC_ENVIRONMENT_TARGET'][2]+zdelta)
