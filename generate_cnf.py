__author__ = 'Tarnasa'

import argparse
import random
import os


parser = argparse.ArgumentParser(
    description='Generate a cnf file and an associated configuration file for use with run.py.')

parser.add_argument('--name', '-n', dest='name', default='generated_cnf', type=str, required=False,
                    help="The name of the CNF set, will be used in file names.")
parser.add_argument('--variables', '-v', dest='number_of_variables', default=5, type=int, required=False,
                    help="Number of variable.")
parser.add_argument('--clauses', '-c', dest='number_of_clauses', default=5, type=int, required=False,
                    help="Number of clauses.")

args = parser.parse_args()

if not os.path.exists('{0}'.format(args.name)):
    os.makedirs('{0}'.format(args.name))
with open('{0}/{0}.cnf'.format(args.name), 'w') as cnf:
    cnf.write('c {0} CNF file\n'.format(args.name))
    cnf.write('p cnf {0} {1}\n'.format(args.number_of_variables, args.number_of_clauses))
    for clause_index in range(args.number_of_clauses):
        # Use a random number of literals in the clause favoring small sizes
        number_of_literals = random.gauss(0.2 * args.number_of_variables, args.number_of_variables * 0.3)
        number_of_literals = min(max(int(number_of_literals), 1), args.number_of_variables)
        literal_mask = [random.choice([-1, 1]) for _ in range(number_of_literals)] +\
                       [False] * (args.number_of_variables - number_of_literals)
        random.shuffle(literal_mask)
        cnf.write(' '.join(str(x * literal_mask[x]) for x in range(args.number_of_variables) if literal_mask[x]) +
                  ' 0\n')

with open('{0}.args'.format(args.name), 'w') as config:
    config.write("""--cnf
{args.name}/{args.name}.cnf
--seed
int
--runs
30
--evals
10000
--log
{args.name}/log.txt
--solution
{args.name}/solution.txt
""".format(**locals()))
