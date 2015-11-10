"""
Functions which produce a list of parents
"""

import numpy


def uniform_random(number_of_children):
    def select(fitnesses):
        for child_index in range(number_of_children):
            yield numpy.random.randint(0, len(fitnesses), size=2)
    return select


def fitness_prop_selection(number_of_children):
    def select(fitnesses):
        # Use stochastic acceptance instead of naive CDF (https://en.wikipedia.org/wiki/Fitness_proportionate_selection)
        m = max(fitnesses)
        for child_index in range(number_of_children):
            parents = list()
            while True:
                dart = numpy.random.randint(0, len(fitnesses))
                if numpy.random.random() < (float(fitnesses[dart]) / m):
                    if dart not in parents:  # Can we have replacement?
                        parents.append(dart)
                        if len(parents) >= 2:
                            break
            yield parents
    return select


def k_tournament_with_replacement(number_of_children, k):
    def select(fitnesses):
        for child_index in range(number_of_children):
            parents = list()
            for _ in range(2):
                parents.append(min(numpy.random.randint(0, len(fitnesses), size=k)))
            yield parents
    return select
