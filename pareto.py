"""
Functions for handling pareto fronts
"""

import itertools
import collections


def dominates(a, b):
    return (a[1] > b[1] or a[2] > b[2]) and a[1] >= b[1] and a[2] >= b[2]


def not_dominates(a, b):
    return a[1] <= b[1] or a[2] <= b[2]


def generate_zipped_from_fronts(fronts):
    """
    Not only does this function flatten the fronts into a single list,
    it also tags the individuals with an index corresponding to which front they are in, higher being better
    """
    zipped = list()
    top = len(fronts)
    for front_index, front in enumerate(fronts):
        zipped += [(top - front_index, individual[1], individual[2], individual[3]) for individual in front]
    return zipped


def generate_fronts(zipped):
    """
    Generates a list of pareto fronts from a possibly unsorted list of zipped individuals
    """
    fronts = list()
    zipped = list(zipped)
    zipped.sort(key=lambda x: -x[1])
    while zipped:
        best_secondary = -999999
        front = list()
        new_zipped = collections.deque()
        for individual in zipped:
            if individual[2] > best_secondary or (individual[2] == best_secondary and
                                                  individual[1] == front[-1][1]):
                best_secondary = individual[2]
                front.append(individual)
            else:
                new_zipped.append(individual)
        fronts.append(front)
        zipped = new_zipped
    return fronts


def verify_fronts(fronts):
    for front_index, front in enumerate(fronts):
        for lesser_front in itertools.islice(fronts, front_index, None):
            for better, lesser in itertools.product(front, lesser_front):
                if dominates(lesser, better):
                    return False
    return True


def add_to_pareto_fronts(fronts, individual):
    for front_index, front in enumerate(fronts):
        alive_mask = [True] * len(front)
        for member_index, member in enumerate(front):
            if individual[1] > member[1] and individual[2] > member[2]:
                alive_mask[member_index] = False
                if front_index >= len(fronts) - 1:
                    fronts.append(list())
                fronts[front_index + 1].append(member)
            elif individual[1] < member[1] and individual[2] < member[2]:
                break
        else:
            front.append(individual)
            front[:] = itertools.compress(front, alive_mask)
            break


# TODO: Insert into fronted zipped list


def get_best_front(zipped):
    best_front = zipped[0][0]
    return itertools.takewhile(lambda x: x[0] == best_front, zipped)


def compare_fronts(a, b):
    # Label the two fronts
    assert len(a[0]) == 4
    a = [(0, x[1], x[2], x[3]) for x in a]
    b = [(1, x[1], x[2], x[3]) for x in b]

    # Generate a new set of fronts from the combination of them
    combined = generate_fronts(a + b)

    # Count tags in top front
    from_a = sum(1 for x in combined[0] if x[0] == 0)
    return from_a / float(len(combined[0]))


def fronts_equal(a, b):
    if len(a) != len(b):
        return False
    for a_x, b_x in itertools.izip(a, b):
        if a_x[1] != b_x[1] or a_x[2] != b_x[2]:
            return False
    return True
