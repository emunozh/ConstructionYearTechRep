#!/usr/bin/env python
# encoding: utf-8

import pandas as pd


def _getNeighbours(uuid, Buildings, ID):
    cols = ["baw", "gfk", "bja", "sqm", "shell_wall",
            "geometry", "distance", "rank"]
    mask = ([(a in uuid and b > 0) for a, b in zip(
        Buildings.index.tolist(), Buildings.bja.tolist())])
    if sum(mask) < 1:
        return []
    else:
        # select neighbours
        N = Buildings.loc[mask, cols]

        # (1) BAW
        Buildings.loc[Buildings.baw.isnull(), "baw"] = "n.a"
        if Buildings.loc[ID, "baw"] != "n.a":
            N.loc[N.baw == Buildings.loc[ID, "baw"], "baw"] = 0
            N.loc[N.baw != Buildings.loc[ID, "baw"], "baw"] = 0.5
            N.loc[N.baw.isnull(), "baw"] = 1
        else:
            N.loc[N.baw.isnull(), "baw"] = 0
            N.loc[N.baw != 0, "baw"] = 1

        # (2) GFK
        N.gfk = N.gfk == Buildings.loc[ID, "gfk"]
        N.gfk = pd.get_dummies(N.gfk)

        # (3) SQM
        sqmDif = abs(N.sqm - Buildings.loc[ID, "sqm"])
        N.sqm = sqmDif / max(sqmDif)

        # (4) Shell
        shellDif = abs(N.shell_wall -
                       Buildings.loc[ID, "shell_wall"])
        N.shell_wall = shellDif / max(shellDif)

        # (5) Distance
        N.distance = [abs(a.distance(
            Buildings.loc[ID, "geometry"])) for a in N.geometry]
        N.distance = N.distance / max(N.distance)

        # = Rank
        N.rank = N.loc[:, ["baw", "gfk", "sqm",
                           "shell_wall", "distance"]].sum(axis=1)
        N.loc[:, "rank"] = N.rank / max(N.rank)
        return N
