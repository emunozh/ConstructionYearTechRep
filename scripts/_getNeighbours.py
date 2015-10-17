#!/usr/bin/env python
# encoding: utf-8

import pandas as pd


def _getNeighbours(uuid, Buildings, ID):
    cols = ["baw", "bja", "sqm", "shell_wall",
            "geometry", "distance", "rank"]
    mask = ([(a in uuid and b > 0) for a, b in zip(
        Buildings.index.tolist(), Buildings.bja.tolist())])
    if sum(mask) < 1:
        return []
    else:
        N = Buildings.loc[mask, cols]
        N.baw = N.baw == Buildings.loc[ID, "baw"]
        N.baw = pd.get_dummies(N.baw)
        sqmDif = abs(N.sqm - Buildings.loc[ID, "sqm"])
        N.sqm = sqmDif / max(sqmDif)
        shellDif = abs(N.shell_wall -
                       Buildings.loc[ID, "shell_wall"])
        N.shell_wall = shellDif / max(shellDif)
        N.distance = [abs(a.distance(
            Buildings.loc[ID, "geometry"])) for a in N.geometry]
        N.distance = N.distance / max(N.distance)
        N.rank = N.loc[:, ["baw", "sqm",
                           "shell_wall", "distance"]].sum(axis=1)
        N.loc[:, "rank"] = N.rank / max(N.rank)
        return N
