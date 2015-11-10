"""
Functions for selecting the surviving members of a population

NOTE: These functions CAN ASSUME that the input is sorted form best to worst
NOTE: These functions MUST maintain sorting
"""

import numpy


def ordered_random_sample(collection, k):
    # Uses reservoir sampling: https://en.wikipedia.org/wiki/Reservoir_sampling to perform in O(len(collection))
    number_selected = 0
    for index, element in enumerate(collection):
        # Optimization: Use reverse counter
        probability = float(k - number_selected) / (len(collection) - index)
        if numpy.random.random() < probability:
            yield element
            number_selected += 1


def uniform_random(population_size):
    def select(zipped):
        return list(ordered_random_sample(zipped, population_size))
    return select


def fitness_prop_selection(population_size):
    def select(zipped):
        # Use stochastic acceptance instead of naive CDF (https://en.wikipedia.org/wiki/Fitness_proportionate_selection)
        m = float(max(zipped, key=lambda x: x[0])[0])
        # Optimization: Use inverse Stochastic acceptance?
        for partition_index in range(population_size):
            # Optimization: Perform multiple comparisons at once?
            while True:
                dart = numpy.random.randint(partition_index, len(zipped))
                if numpy.random.random() < (zipped[dart][0] / m):
                    zipped[partition_index], zipped[dart] = zipped[dart], zipped[partition_index]
                    break
        return sorted(zipped[:population_size], key=lambda x: -x[0])
    return select


def truncate(population_size):
    def select(zipped):
        return zipped[:population_size]
    return select


def k_tournament_without_replacement(population_size, k):
    def select(zipped):
        for partition_index in range(len(zipped) - population_size):
            dead_index = max(numpy.random.randint(partition_index, len(zipped), size=k))
            zipped[partition_index], zipped[dead_index] = zipped[dead_index], zipped[partition_index]
        return sorted(zipped[len(zipped) - population_size:], key=lambda x: -x[0])
    return select
