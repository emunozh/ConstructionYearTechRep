#!/usr/bin/env python
# encoding: utf-8

# import python libraries
import numpy as np

# import local libraries
from scripts._getNeighbours import _getNeighbours

# global variables
MIN_RANK = 1


def _estimateByearMedian(row, buildings, minRank=MIN_RANK):
    """Compute the missing construction year as the median of
    all neighbours. Returns the estimated construction year"""
    N = _getNeighbours(row["neighbours"], buildings, row.name)
    if len(N) >= 1:
        estimatedYear = N.bja.median()
        if estimatedYear > 0 and not np.isnan(estimatedYear):
            year = estimatedYear
        else:
            year = np.nan
        return year
    else:
        np.nan
