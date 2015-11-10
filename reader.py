"""
A class for reading DIMACS-style equations
"""

import re
import numpy

import sat_core


def verify_DIMACS(s):
    """
    Verify that the multiline string is in proper DIMACS format
    See http://www.satcompetition.org/2009/format-benchmarks2009.html
    :param s: string
    :return: string
    """
    comments = True
    configured = False
    number_of_literals = 0
    number_of_clauses = 0
    clauses = 0
    for line in s.split('\n'):
        line = line.strip()
        if len(line) == 0:
            continue

        if line[0] != 'c':
            if comments:
                comments = False
        else:
            if not comments:
                return 'Comments found outside of initial comment block.'

        if line[0] == 'p':
            if not configured:
                match = re.match(r'p cnf ([0-9]+) ([0-9]+)', line)
                if not match:
                    return 'invalid p-line.'
                number_of_literals = int(match.group(1))
                number_of_clauses = int(match.group(2))
                configured = True
            else:
                return 'Multiple p lines found.'
        elif re.match(r'-?[0-9]+', line):
            if not configured:
                return 'clause before p-line.'
            literals = re.split(' ', line)
            for literal in literals[:-1]:
                if abs(int(literal)) > number_of_literals:
                    return 'Variable number greater than number of variables'
            if literals[-1] != '0':
                return 'Clause does not end with a zero.'
            clauses += 1
    if number_of_clauses != clauses:
        return 'Not enough clauses'
    if configured:
        return ''


def read_DIMACS(s):
    """
    Create an equation given a multiline string in DIMACS format
    See http://www.satcompetition.org/2009/format-benchmarks2009.html
    :param s: string
    :return: sat_core.Equation
    """

    sign_transform = {
        -1: 0,
        1: 1,
        0: -1,
    }

    clauses = None
    clause_index = 0
    for line in s.split('\n'):
        symbols = re.split(r' +', line)
        if symbols[0] in ['', 'c']:
            continue
        if symbols[0] == 'p' and symbols[1] == 'cnf':
            number_of_literals = int(symbols[2])
            number_of_clauses = int(symbols[3])
            clauses = numpy.full(shape=(number_of_clauses, number_of_literals), fill_value=-2, dtype=numpy.int8)
        else:
            for symbol in symbols:
                if symbol == '0':
                    continue
                clauses[clause_index, abs(int(symbol)) - 1] = sign_transform[numpy.sign(int(symbol))]
            clause_index += 1

    return sat_core.Equation(clauses)
