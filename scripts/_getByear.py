#!/usr/bin/env python
# encoding: utf-8

# import numpy
import numpy as np

# import local libraries
from scripts._estimateByearMedian import _estimateByearMedian as estimateByear
#from scripts._estimateByearRank import _estimateByearRank as estimateByear
from scripts.plots import plotBuildings

# define global variables
MAX_ITERATIONS = 20


def _getByear(buildings, plot=True):
    """Estimate the construction year iteratively for of all 
    buildings or until a maximum number of iterations is reached.
    Returns the buildings data frame."""
    missing_byear = sum(np.isnan(buildings['bja']))
    improvement = True
    iteration = 0
    while missing_byear >= 1 and improvement and\
          iteration <= MAX_ITERATIONS:
        print("iter = ", iteration)
        iteration += 1
        buildings.loc[
            np.isnan(buildings['bja']), 'bja'] = buildings.loc[
                np.isnan(buildings['bja']), :].apply(
                    estimateByear, buildings=buildings, axis=1)
        improvement = sum(
            np.isnan(buildings['bja'])) < missing_byear
        missing_byear = sum(np.isnan(buildings['bja']))
        if plot:
            plotBuildings(buildings, iteration=iteration,
                          legend=False)
    return buildings
