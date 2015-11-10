"""
This file handles all command line and file configuration options to the program
"""

import argparse
import time
import itertools
import random

import numpy


def keys_and_values(d):
    return set(itertools.chain.from_iterable(d.iteritems()))


# Parse command line options
parser = argparse.ArgumentParser(description='Runs a (mu+lambda) EA to find a SAT solution.',
                                 fromfile_prefix_chars='@',
                                 conflict_handler='resolve',
                                 epilog='Use @more_args.txt to use command line options from a file with \n'
                                 'options on separate lines.')
parser.add_argument('--cnf', '-c', dest='equation', default='equation.cnf', type=argparse.FileType('r'),
                    required=True, help='Path to an existing CNF equation file.')
parser.add_argument('--seed', '-s', dest='seed', default='time', type=str, required=False,
                    help='Seeds the random number generator, use \'time\' to use the current time.')
parser.add_argument('--runs', '-r', dest='runs', default=30, type=int, required=False,
                    help='The number of runs of the algorithm.')
parser.add_argument('--population-size', '-p', dest='population_size', default=100, type=int, required=False,
                    help='The maximum number of organisms before reproduction.')
parser.add_argument('--children', '-i', dest='children', default=10, type=int, required=False,
                    help='The number of children produced each generation.')
parent_selection_models = {'Fitness Proportional Selection': 'FPS', 'k-Tournament Selection with Replacement': 'kTourn',
                           'Uniform Random': 'random'}
parser.add_argument('--parent-selection', '-o', dest='parent_selection', default='FPS', type=str, required=False,
                    choices=keys_and_values(parent_selection_models), help='The parent selection model.')
parser.add_argument('--parent-tournament-size', dest='parent_k', default=20, type=int, required=False,
                    help='Tournament size for the k-Tournament parent selection model.')
survival_selection_models = {'Truncation': 'Truncation', 'k-Tournament Selection without Replacement': 'kTourn',
                             'Uniform Random': 'random', 'Fitness Proportional Selection': 'FPS'}
parser.add_argument('--survival-selection', '-v', dest='survival_selection', default='Truncation', type=str,
                    required=False, choices=keys_and_values(survival_selection_models),
                    help='The survival selection model.')
parser.add_argument('--survival-tournament-size', dest='survival_k', default=20, type=int, required=False,
                    help='Tournament size for the k-Tournament survival selection model.')
parser.add_argument('--evals', '-e', dest='evals', default=10000, type=int, required=False,
                    help='Terminate the run after N generations.  -1 disables this.')
parser.add_argument('--terminate-pareto', dest='terminate_pareto', default=-1, type=int, required=False,
                    help='Terminate the run when the pareto front has not changed after N generations.'
                         '  -1 disables this.')
parser.add_argument('--seed-file', dest='seed_file', default=None, type=argparse.FileType('r'),
                    help='Seed the organism pool with solutions from a file.')
parser.add_argument('--survival-strategy', dest='survival_strategy', choices=['comma', 'plus'], default='plus',
                    help='The survival strategy to use.  (mu [+|,] lambda)')
# Use 'a' (append) mode so that we don't truncate existing files while trying to open multiple files
#  (For example, if you specified a filename in a config file, and also on the command line, it would try to open
#   both files, truncating both, even though we only wanted to open the latter one, but we still want to report an
#   error if the first was unsuccessful)
# TODO: Change the argparse class to interpret multiple filename arguments correctly
parser.add_argument('--log', '-l', dest='log', default='log.txt', type=argparse.FileType('a'), required=False,
                    help='Path to a log file to be generated.')
parser.add_argument('--solution', '-u', dest='solution', default='solution.txt', type=argparse.FileType('a'),
                    required=False, help='Path to a solution file to be generated.')
parser.add_argument('--pareto', default=None, type=argparse.FileType('a'),
                    required=False, help='Path to file to be generated containing best pareto fronts from all runs.')
parser.add_argument('--diversity', default=None, type=argparse.FileType('a'), required=False,
                    help='Path to file to be generated containing the diversity measure for all generations.')

args = parser.parse_args()

# Reopen output files as 'w'
args.log.close()
args.log = open(args.log.name, 'w')
args.solution.close()
args.solution = open(args.solution.name, 'w')
if args.pareto:
    args.pareto.close()
    args.pareto = open(args.pareto.name, 'w')
if args.diversity:
    args.diversity.close()
    args.diversity = open(args.diversity.name, 'w')

# Simplify choices
args.parent_selection = parent_selection_models.get(args.parent_selection, None) or args.parent_selection
args.survival_selection = survival_selection_models.get(args.survival_selection, None) or args.survival_selection

# Set the random seed
if args.seed == 'time':
    args.seed = int(round(time.time() * 1000)) % 4294967295
else:
    args.seed = int(args.seed)
random.seed(args.seed)
numpy.random.seed(args.seed)
