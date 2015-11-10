"""
Classes which tell the EA when to stop
"""

import itertools

import pareto


# Hm... these can probably be made into closures with member variables
class StableAverage:
    def __init__(self, n):
        self.n = n
        self.matching_averages = 0
        self.previous_average = -1

    def evaluate(self, zipped):
        average = float(sum(x[0] for x in zipped)) / len(zipped)
        if average == self.previous_average:
            self.matching_averages += 1
            if self.matching_averages >= self.n:
                return True
        else:
            self.matching_averages = 0
            self.previous_average = average
        return False


class StableBest:
    def __init__(self, n):
        self.n = n
        self.matching_bests = 0
        self.previous_best = -1

    def evaluate(self, zipped):
        best = max(zipped)
        if best == self.previous_best:
            self.matching_bests += 1
            if self.matching_bests >= self.n:
                return True
        else:
            self.matching_bests = 0
            self.previous_best = best
        return False


class StablePareto:
    def __init__(self, n):
        self.n = n
        self.match_count = 1
        self.matching_front = list()

    def evaluate(self, zipped):
        front = list(pareto.get_best_front(zipped))
        if pareto.fronts_equal(front, self.matching_front):
            self.match_count += 1
            if self.match_count >= self.n:
                return True
        else:
            self.match_count = 1
            self.matching_front = list(front)
        return False
