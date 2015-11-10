"""
These functions determine how to choose the next generation
"""

import pareto


def plus(zipped, zipped_children, select_survivors):
    zipped += zipped_children
    zipped = pareto.generate_zipped_from_fronts(pareto.generate_fronts(zipped))
    return select_survivors(zipped)


def comma(zipped, zipped_children, select_survivors):
    del zipped
    zipped_children = pareto.generate_zipped_from_fronts(pareto.generate_fronts(zipped_children))
    return select_survivors(zipped_children)
