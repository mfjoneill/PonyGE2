
class StringMatch:
    """Fitness function for matching a string. Takes a string and returns
    fitness. Penalises output that is not the same length as the target.
    Usage: StringMatch("golden") returns a *callable object*, ie the fitness
    function."""

    maximise = False

    def __init__(self, target):
        self.target = target

    def __call__(self, guess):
        fitness = max(len(self.target), len(guess))
        # Loops as long as the shorter of two strings
        for (t_p, g_p) in zip(self.target, guess):
            if t_p == g_p:
                fitness -= 1
        return fitness
