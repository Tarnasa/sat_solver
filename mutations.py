"""
These functions add small variation to a list of individuals
"""

import numpy


def flip_bits(genome_length):
    flip_chance = 1.0 / genome_length

    def mutate(individuals):
        for individual in individuals:
            for index, chance in enumerate(numpy.random.random(size=genome_length)):
                if chance < flip_chance:
                    individual[index] = numpy.random.random_integers(-1, 1)
        return individuals
    return mutate


def swap_bit(genome_length):
    def mutate(individuals):
        for individual in individuals:
            i1, i2 = numpy.random.randint(0, genome_length, size=2)
            individual[i1], individual[i2] = individual[i2], individual[i1]
        return individuals
    return mutate
