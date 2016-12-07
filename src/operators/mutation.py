from algorithm.mapper import tree_derivation
from random import randint, random, choice
from algorithm.parameters import params
from representation import individual


def mutation(pop):
    """ Perform mutation on a population """

    return list(map(params['MUTATION'], pop))


def int_flip(ind):
    """Mutate the individual by randomly choosing a new int with probability
    p_mut. Works per-codon, hence no need for "within_used" option."""

    if params['MUTATION_PROBABILITY']:
        p_mut = params['MUTATION_PROBABILITY']
    else:
        p_mut = params['MUTATION_EVENTS']/len(ind.genome)

    for i in range(len(ind.genome)):
        if random() < p_mut:
            ind.genome[i] = randint(0, params['CODON_SIZE'])

    new_ind = individual.Individual(ind.genome, None)

    return new_ind

def int_flip_constrained(ind):
    """Mutate the individual by randomly choosing a new int with probability
    p_mut. Works per-codon, hence no need for "within_used" option."""
    leading_zeros = ['','0','00','000','0000','00000']

    if params['MUTATION_PROBABILITY']:
        p_mut = params['MUTATION_PROBABILITY']
    else:
        p_mut = params['MUTATION_EVENTS']/len(ind.genome)

    max_gaurd = str(0) + leading_zeros[params['MP_X_LIM_zeros']] + str(params[
                                                                        'MP_X_LIM']) \
            + leading_zeros[params['MP_X_LIM_zeros']] + str(params['MP_Y_LIM']) \
            + leading_zeros[params['MP_X_LIM_zeros']] + str(params['MP_Z_LIM'])

    print(max_gaurd)
    for i in range(len(ind.genome)):
        if random() < p_mut:
            #Need to put guard in to make sure we don't exceed max values.
            #What about the minimum gaurd?
            #Not used in current version of problem.
            a = False
            while not a:
                new_codon = randint(0, params['CODON_SIZE'])
                if(int(max_gaurd[i]) == 0):
                    #mutate to another zero
                    a = True
                    ind.genome[i] = 0
                elif(new_codon%10 < int(max_gaurd[i])):
                    a = True
                    ind.genome[i] = new_codon
                else:
                    a = False

    new_ind = individual.Individual(ind.genome, None)

    return new_ind


def subtree(ind):
    """Mutate the individual by replacing a randomly selected subtree with a
    new subtree. Guaranteed one event per individual if called."""

    for i in range(params['MUTATION_EVENTS']):
        tail = ind.genome[ind.used_codons:]
        ind.phenotype, genome, ind.tree = subtree_mutate(ind.tree)
        ind.used_codons = len(genome)
        ind.genome = genome + tail
        ind.depth, ind.nodes = ind.tree.get_tree_info(ind.tree)
        ind.depth += 1

    return ind


def subtree_mutate(ind_tree):
    """ Creates a list of all nodes and picks one node at random to mutate.
        Because we have a list of all nodes we can (but currently don't)
        choose what kind of nodes to mutate on. Handy. Should hopefully be
        faster and less error-prone to the previous subtree mutation.
    """

    # Find which nodes we can mutate from
    targets = \
        ind_tree.get_target_nodes([],
                                  target=params['BNF_GRAMMAR'].non_terminals)

    # Pick a node
    number = choice(targets)

    # Get the subtree
    new_tree = ind_tree.return_node_from_id(number, return_tree=None)

    # Set the depth limits for the new subtree
    new_tree.max_depth = params['MAX_TREE_DEPTH'] - \
                         new_tree.get_current_depth()

    # Mutate a new subtree
    tree_derivation(new_tree, [], "random", 0, 0, 0, new_tree.max_depth)

    return ind_tree.get_output(), ind_tree.build_genome([]), ind_tree
