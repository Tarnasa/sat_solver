"""
This module contains all classes and functions relevant to any sat solver
"""

# Third party
import numpy


class Equation:
    def __init__(self, clauses):
        """
        clauses should be a 2d numpy array,
         axis 0: length = number of clauses, elements = clauses
         axis 1: length = number of variables, elements = literals
          -2 for a literal not used in the clause
           1 for a normal literal
           0 for a negated literal
        :param clauses: numpy.array
        """
        self.clauses = clauses
        self.number_of_clauses = self.clauses.shape[0]
        self.number_of_variables = self.clauses.shape[1]

    def evaluate(self, organisms):
        """
        Counts how many clauses are true for multiple solutions

        Organisms is a 2d array
         axis 0: length = number of organisms, elements = SAT solutions
         axis 1: length = number of clauses, elements = values for each variable (0 or 1)

        :param organisms: numpy.array
        :return: list[int]
        """
        clauses = self.clauses
        numpy_sum = numpy.sum
        numpy_any = numpy.any
        return [numpy_sum(numpy_any(clauses == organism, axis=1)) for organism in organisms]

    def count_free_variables(self, organisms):
        all_free = numpy.full(shape=self.number_of_variables, fill_value=-1, dtype=numpy.int32)
        numpy_sum = numpy.sum
        return list(numpy_sum(organisms == all_free, axis=1))


def hamming_distance(s1, s2):
    """Return the Hamming distance between equal-length sequences"""
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


def measure(front, objectives, mins, maxs):
    """
    Calculates the normalized hyper-volume between each point on a Pareto front and its neighbors
    Returns the percentage of the total normalized volume NOT taken up by these volumes
        A higher return value corresponds to a better distributed Pareto front
    front: non-empty list of class objects with an objectives dictionary member variable
    objectives: list of objective names (needs to match what's in the individual's objectives dictionary)
    mins: dictionary with objective names as keys and the minimum possible value for that objective as values
    maxs: dictionary with objective names as keys and the maximum possible value for that objective as values
    """
    front = [(index, x[1], x[2], x[3]) for index, x in enumerate(front)]
    # This will store the hyper-volume between neighboring individuals on the front; initialize all volumes to 1
    volumes = {individual[0]: 1.0 for individual in front}
    # There is one more volume of interest than there is points on the front, so associate it with the max value
    volumes['max'] = 1.0
    for objective in objectives:
        # Sort the front by this objective's values
        sorted_front = sorted(front, key=lambda x: x[objective])
        # Calculate the volume between the first solution and minimum
        volumes[sorted_front[0][0]] *= float(sorted_front[0][objective]-mins[objective])/(maxs[objective]-mins[objective])
        # Calculate the volume between adjacent solutions on the front
        for i in range(1, len(sorted_front)):
            volumes[sorted_front[i][0]] *= float(sorted_front[i][objective]-sorted_front[i-1][objective])/(maxs[objective]-mins[objective])
        # Calculate the volume between the maximum and the last solution
        volumes['max'] *= float(maxs[objective]-sorted_front[-1][objective])/(maxs[objective]-mins[objective])
    # The normalized volume of the entire objective space is 1.0, subtract the volumes we calculated to turn this into maximization
    return 1.0 - sum(volumes.values())
