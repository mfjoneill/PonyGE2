from fitness.moving_point import MovingPoint
from fitness.moving_point_dual import MovingPointDual
from fitness.string_match import StringMatch
from fitness.regression import Regression
from utilities.error_metrics import inverse_f1_score


def set_fitness_params(problem, params):
    if problem in ("regression", "classification"):
        return "grammars/" + params['SUITE'] + ".bnf", params['SUITE']
    elif problem == "string_match":
        return "grammars/letter.bnf", params['STRING_MATCH_TARGET']
    elif problem == "moving_point":
        return "grammars/movingpoint_10000_max.bnf", params['DYNAMIC_ENVIRONMENT_TARGET']
    elif problem == "moving_point_dual":
        return "grammars/movingpoint_10000_max.bnf", params['DYNAMIC_ENVIRONMENT_TARGET']
    else:
        print("Error: Problem not specified correctly")
        exit(2)


def set_fitness_function(problem, alternate=None):
    # Regression Problem
    if problem == "regression":
        return Regression(alternate)
    elif problem == "classification":
        return Regression(alternate, error=inverse_f1_score)
    # String Match Problem
    elif problem == "string_match":
        return StringMatch(alternate)
    elif problem == "moving_point":
        return MovingPoint(alternate)
    elif problem == "moving_point_dual":
        return MovingPointDual(alternate)
    elif problem == "new":
        print("new problem goes here")
        # parameters.FITNESS_FUNCTION = whatever
    else:
        print("Please specify a valid fitness function")
        exit()
