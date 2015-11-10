#!/usr/bin/env python

"""
Runs an evolutionary algorithm on a given SAT problem,
prints fitness values to a log file
Prints solutions to a solution file
"""

# Built-ins
import time
import sys
import itertools

# Third-party libraries
import numpy

# Custom imports
import reader
import terminators
import parent_selectors
import recombination
import mutations
import survival_selectors
import initializers
import survival_strategies
import pareto
import sat_core

import configuration

args = configuration.args

# Start timer so that we know how long the task took
genesis = time.clock()

# Print all selected configuration options
print('\n'.join("{0}: {1}".format(k, v) for k, v in args.__dict__.iteritems()))

# Read the CNF file, but first try to give helpful error messages if it is not valid
equation_string = args.equation.read()
error = reader.verify_DIMACS(equation_string)
if error:
    print(error)
    sys.exit(1)

equation = reader.read_DIMACS(equation_string)

pareto_filename = args.pareto.name if args.pareto else 'None'
diversity_filename = args.diversity.name if args.diversity else 'None'

# Write log header
args.log.write("""CNF file: {args.equation.name}
Random number seed: {args.seed}
Number of runs: {args.runs}
Maximum number of fitness evaluations per run: {args.evals}
log file: {args.log.name}
solution file: {args.solution.name}
pareto front file: {pareto_filename}
diversity front file: {diversity_filename}
population size: {args.population_size}
offspring size: {args.children}
Terminate after static pareto front: {args.terminate_pareto}
Parent selection: {args.parent_selection}
Survival Selection: {args.survival_selection}
Parent tournament size: {args.parent_k}
Survival tournament size: {args.survival_k}
Seed File: {args.seed_file}
Evolution strategy: {args.survival_strategy}

Result Log
""".format(**locals()))

# Write solution header
args.solution.write("c Solution for: {args.equation.name}\n".format(**locals()))


def run():
    overall_best_front = list()

    # Load seeds if specified
    seeds = list()
    if args.seed_file:
        seeds = initializers.read_from_file(args.seed_file, equation.number_of_variables)

    # Setup termination functions
    terminator_functions = list()
    if args.terminate_pareto != -1:
        terminator = terminators.StablePareto(args.terminate_pareto)
        terminator_functions.append(terminator.evaluate)

    # Choose parent selection algorithm
    select_parents = {
        'random': parent_selectors.uniform_random(args.children),
        'FPS': parent_selectors.fitness_prop_selection(args.children),
        'kTourn': parent_selectors.k_tournament_with_replacement(args.children, args.parent_k)
    }[args.parent_selection]

    # Choose recombination function
    recombine = recombination.crossover(equation.number_of_variables)

    # Choose mutation function
    mutate = mutations.flip_bits(equation.number_of_variables)

    # Choose survival selection function
    select_survivors = {
        'random': survival_selectors.uniform_random(args.population_size),
        'FPS': survival_selectors.fitness_prop_selection(args.population_size),
        'Truncation': survival_selectors.truncate(args.population_size),
        'kTourn': survival_selectors.k_tournament_without_replacement(args.population_size, args.survival_k)
    }[args.survival_selection]

    # Choose survival strategy
    survival_strategy = {
        'plus': survival_strategies.plus,
        'comma': survival_strategies.comma
    }[args.survival_strategy]

    # Actually run the algorithm
    for run_index in range(args.runs):
        args.log.write('\nRun {0}\n'.format(run_index + 1))

        # Generate initial population randomly and/or with seeds
        individuals = initializers.initialize(args.population_size, equation.number_of_variables)
        if seeds:
            individuals = numpy.concatenate((individuals[:-len(seeds)], seeds))

        # Calculate fitness values
        pareto_indices = [0] * args.population_size
        fitnesses = equation.evaluate(individuals)
        simplicities = equation.count_free_variables(individuals)
        # Sort population by fitness
        zipped = zip(pareto_indices, fitnesses, simplicities, individuals)
        fronts = pareto.generate_fronts(zipped)
        zipped = pareto.generate_zipped_from_fronts(fronts)
        pareto_indices, fitnesses, simplicities, individuals = zip(*zipped)

        # Increment the number of evaluations that have occurred
        evals = args.population_size

        # Record average and best
        args.log.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(evals,
                       float(sum(fitnesses)) / len(fitnesses), max(fitnesses),
                       float(sum(simplicities)) / len(simplicities), max(simplicities)))
        if args.diversity:
            args.diversity.write('\nRun {0}\n'.format(run_index + 1))
            args.diversity.write(str(sat_core.measure(pareto.get_best_front(zipped), [1, 2], [0, 0, 0],
                                                      [0, equation.number_of_clauses,
                                                       equation.number_of_variables])) + '\n')

        for generation_index in itertools.count():
            sys.stdout.write('.')
            # Generate children
            children = [recombine((individuals[parent_indices[0]], individuals[parent_indices[1]]))
                        for parent_indices in select_parents(pareto_indices)]
            mutate(children)
            children_fitnesses = equation.evaluate(children)
            children_simplicity = equation.count_free_variables(children)
            evals += len(children)
            children_pareto = [0] * len(children)
            zipped_children = zip(children_pareto, children_fitnesses, children_simplicity, children)

            # Choose survivors
            zipped = survival_strategy(zipped, zipped_children, select_survivors)
            pareto_indices, fitnesses, simplicities, individuals = zip(*zipped)

            # Record average and best
            args.log.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(evals,
                           float(sum(fitnesses)) / len(fitnesses), max(fitnesses),
                           float(sum(simplicities)) / len(simplicities), max(simplicities)))
            if args.diversity:
                args.diversity.write(str(sat_core.measure(pareto.get_best_front(zipped), [1, 2], [0, 0, 0],
                                                          [0, equation.number_of_clauses,
                                                           equation.number_of_variables])) + '\n')

            # Check for termination
            if any(terminator(zipped) for terminator in terminator_functions):
                break
            if args.evals != -1 and evals >= args.evals:
                break

        print('Best of run: {0} {1}'.format(max(x[1] for x in zipped), max(x[2] for x in zipped)))

        best_front = list(pareto.get_best_front(zipped))

        # Write pareto front
        if args.pareto:
            args.pareto.write('c Run {run_index}\n'.format(**locals()))
            for solution in best_front:
                args.pareto.write("c MAXSAT fitness value: {0}\n".format(solution[1]))
                args.pareto.write("c Number of 'don't care' variables: {0}\n".format(solution[2]))
                args.pareto.write('v {0}\n'.format(' '.join(str((i + 1) * [-1, 1][x])
                                                            for i, x in enumerate(solution[3]) if x != -1)))

        # Update best of all runs
        percent_better = pareto.compare_fronts(best_front, overall_best_front)
        if percent_better > 0.5:
            print('New best front! ({})'.format(percent_better))
            overall_best_front = best_front

    # Write overall best pareto front
    args.solution.write("c Number of solutions in pareto front: {0}\n".format(len(overall_best_front)))
    for solution in overall_best_front:
        args.solution.write("c MAXSAT fitness value: {0}\n".format(solution[1]))
        args.solution.write("c Number of 'don't care' variables: {0}\n".format(solution[2]))
        args.solution.write('v {0}\n'.format(' '.join(str((i + 1) * [-1, 1][x])
                                                      for i, x in enumerate(solution[3]) if x != -1)))

#import cProfile; cProfile.run('run()')
run()

print("Done in {0} seconds.".format(time.clock() - genesis))
