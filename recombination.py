"""
Functions which create children out of parents
"""

import numpy


def crossover(genome_size):
    def recombine(parents):
        crossover_point = numpy.random.randint(0, genome_size)
        return numpy.append(parents[0][:crossover_point], parents[1][crossover_point:])
    return recombine
