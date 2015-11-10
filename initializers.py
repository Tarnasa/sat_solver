"""
These functions initialize a population
"""

import re

import numpy


def initialize(population_size, number_of_variables):
    return numpy.random.random_integers(-1, 1, size=(population_size, number_of_variables))


def read_from_file(f, number_of_variables):
    individuals = list()
    for line in f.readlines():
        if not line or line[0] == 'c':
            continue
        if re.match(string=line, pattern=r'[0-9v\-]'):
            if line[0:2] == 'v ':
                line = line[2:]
                solution = numpy.full(shape=number_of_variables, fill_value=-1, dtype=numpy.int32)
                for var in line.split(' '):
                    solution[abs(int(var)) - 1] = int(var) > 0
                individuals.append(solution)
    return individuals
