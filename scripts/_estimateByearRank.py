#!/usr/bin/env python
# encoding: utf-8

# import python libraries
import numpy as np

# import local libraries
from scripts._getNeighbours import _getNeighbours


def _estimateByearRank(row, buildings):
    """Compute the missing construction year by ranking all
    neighbours based on their attributes and euclidean distance.
    Returns the estimated construction year"""
    N = _getNeighbours(row["neighbours"], buildings, row.name)
    if len(N) >= 1:
        estimatedYear = N.loc[N.rank == min(N.rank), "bja"].tolist()
        estimatedYear = estimatedYear[0]
        if estimatedYear > 0:
            year = estimatedYear
        else:
            year = np.nan
        return year
    else:
        return np.nan
