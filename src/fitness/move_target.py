from algorithm.parameters import params
from scipy.spatial import distance
from math import sqrt
from random import randint

def move_target():
    params['DYNAMIC_ENVIRONMENT_TARGET'] = (params['DYNAMIC_ENVIRONMENT_TARGET'][0]+params['X_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][1]+params['Y_DELTA'], params['DYNAMIC_ENVIRONMENT_TARGET'][2]+params['Z_DELTA'])

#
# map real-world datastreams to the target point in the moving_point dynamic problem
# "stocks" pulls datastreams from Yahoo Finance
#
def move_target_realworldmapping():
    REAL_WORLD_ENVIRONMENT = "stocks"
    # REAL_WORLD_ENVIRONMENT = "stocks" # pulls stocks/indices datastream from Yahoo Finance
    if(REAL_WORLD_ENVIRONMENT == "stocks"):
        #print("mapping to Yahoo Finance datastreams")
        from yahoo_finance import Share
        ftse = Share('^FTSE')
        ftse_price = float(ftse.get_price())
        #print (ftse_price)
        ndx = Share('^NDX')
        ndx_price = float(ndx.get_price())
        #print (ndx_price)
        n225 = Share('^N225')
        n225_price = float(n225.get_price())
        #print (n225_price)
        #ftse.refresh()
        #ndx.refresh()
        #n225.refresh()
        params['DYNAMIC_ENVIRONMENT_TARGET'] = (ftse_price, ndx_price, n225_price)

    else:
        # don't move_target
        print("Error, in the fitness function move_target_realworldmapping() the REAL_WORLD_ENVIRONMENT is not implmented!")


def new_target_point(current, dest, dist):
    vect = [dest[0] - current[0], dest[1] - current[1], dest[2] - current[2]]
    step = sqrt((vect[0] * vect[0]) + (vect[1] * vect[1]) + (vect[2] * vect[2])) / dist
    temp_vect = [(1 / step) * vect[0], (1 / step) * vect[1], (1 / step) * vect[2]]
    return [int(current[0] + temp_vect[0]), int(current[0] + temp_vect[0]), int(current[0] + temp_vect[0])]

#def move_target_vision(best_distance):
#need to tidy this up!!!!!
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
        old_index = params['MP_DESTINATION_INDEX'][0]
        temp_index = params['MP_DESTINATION_INDEX'][0]
        catch = True
        while catch:
            temp_index = randint(0, 7)
            if temp_index == params['MP_DESTINATION_INDEX'][0]:
                catch = True
            else:
                catch = False
        print("Changing index to ", temp_index)
        params['MP_DESTINATION_INDEX'][0] = temp_index
        temp_target = new_target_point(params['DYNAMIC_ENVIRONMENT_TARGET'],
                                       params['MP_DESTINATION_POINTS'][
                                           params['MP_DESTINATION_INDEX'][0]],
                                       params['FLEE_DELTA'])
        if temp_target[0] > params['MP_X_LIM_MAX'] or temp_target[0] < params['MP_X_LIM_MIN'] \
                or temp_target[1] > params['MP_Y_LIM_MAX'] or temp_target[1] < params['MP_Y_LIM_MIN'] \
                or temp_target[2] > params['MP_Z_LIM_MAX'] or temp_target[2] < params['MP_Z_LIM_MIN']:
            temp_index = params['MP_DESTINATION_INDEX'][0]
            catch = True
            while catch:
                temp_index = randint(0, 7)
                if temp_index == params['MP_DESTINATION_INDEX'][0]:
                    catch = True
                else:
                    catch = False
            print("Changing index to ", temp_index)
            params['MP_DESTINATION_INDEX'][0] = temp_index
            temp_target = new_target_point(params['DYNAMIC_ENVIRONMENT_TARGET'],
                                                params['MP_DESTINATION_POINTS'][params['MP_DESTINATION_INDEX'][0]],
                                                params['FLEE_DELTA'])
    else:
        #keep going
        print("Safe")
        temp_target = new_target_point(params['DYNAMIC_ENVIRONMENT_TARGET'],
                                                                params['MP_DESTINATION_POINTS'][params['MP_DESTINATION_INDEX'][0]],
                                                                params['DELTA'])
        if temp_target[0] > params['MP_X_LIM_MAX'] or temp_target[0] < params['MP_X_LIM_MIN'] \
                or temp_target[1] > params['MP_Y_LIM_MAX'] or temp_target[1] < params['MP_Y_LIM_MIN'] \
                or temp_target[2] > params['MP_Z_LIM_MAX'] or temp_target[2] < params['MP_Z_LIM_MIN']:
            temp_index = params['MP_DESTINATION_INDEX'][0]
            catch = True
            while catch:
                temp_index = randint(0, 7)
                if temp_index == params['MP_DESTINATION_INDEX'][0]:
                    catch = True
                else:
                    catch = False
            print("Changing index to ", temp_index)
            params['MP_DESTINATION_INDEX'][0] = temp_index
            temp_target = new_target_point(params['DYNAMIC_ENVIRONMENT_TARGET'],
                                            params['MP_DESTINATION_POINTS'][params['MP_DESTINATION_INDEX'][0]],
                                            params['DELTA'])
    params['DYNAMIC_ENVIRONMENT_TARGET'] = temp_target


