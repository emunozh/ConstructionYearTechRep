#!/usr/bin/env python
# encoding: utf-8

# import python libraries
import numpy as np

# import local libraries
from scripts._getNeighbours import _getNeighbours

# global variables
MIN_RANK = 1


def _estimateByearRank(row, buildings, minRank=MIN_RANK):
    """Compute the missing construction year by ranking all
    neighbours based on their attributes and euclidean distance.
    Returns the estimated construction year"""
    N = _getNeighbours(row["neighbours"], buildings, row.name)
    if MIN_RANK < 1:
        N = N.dropna()
    if len(N) >= 1:
        if min(N.loc[:,"rank"]) <= minRank:
            estimatedYear = N.loc[N.loc[:,"rank"] == min(N.loc[:,"rank"]), "bja"].tolist()
            estimatedYear = estimatedYear[0]
            if estimatedYear > 0:
                year = estimatedYear
            else:
                year = np.nan
        else:
            year = np.nan
        return year
    else:
        return np.nan
