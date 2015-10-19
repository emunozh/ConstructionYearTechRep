#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import numpy as np
from shapely.wkt import loads

from root.GeoData.GIS_key import GFK_key
from root.PostgreSQL.dbData2 import GeoData

PLACE = [3002, 3003, 3004,       3006, 3007, 3008, 3009, 3010, 3011, 3012, 3013,
         1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 2001]
SG = ", ".join(["'{}'".format(a) for a in PLACE])
RK = ", ".join(["'{}'".format(k) for k in GFK_key.keys() if GFK_key[k][3]])

TABLE = 'neoalkis'
PARENT = 'statistische_gebiete_utm'

# neighbourhood radius
R = 500
# k number of neighbours
K = 30


def _fetchBuildings():
    """fetch buildings from PostgeSQL database."""

    # W = "WHERE p.statgeb in ({0}) AND ch.gfk in ({1})".format(SG, RK)
    W = "WHERE p.statgeb in ({0})".format(SG)
    Q = """SELECT ch.uuid, ch.baw, ch.gfk, ch.bja, ch.stadtteil, ch.sqm,
                    ch.shell_wall, ch.shell,
                    ch.neighbours,
                    ST_AsText(ch.wkb_geometry_simple::geometry),
                    p.statgeb
    FROM {0} ch
    LEFT JOIN {1} p ON ST_Within(
        ST_Centroid(ch.wkb_geometry), p.wkb_geometry)
    {2}""".format(TABLE, PARENT, W)

    geoData = GeoData(PARENT, specificQ=Q)
    Buildings = pd.DataFrame(geoData.data)
    geoData.closeDB()
    columns = ["uuid", "baw", "gfk", "bja", "stadtteil", "sqm", "shell_wall",
               "shell", "neighbours", "geometry", "statgeb"]
    Buildings.columns = columns
    Buildings = Buildings.set_index("uuid")
    Buildings.loc[Buildings.bja == 0, "bja"] = np.nan
    Buildings.geometry = Buildings.geometry.apply(loads)
    Buildings.to_hdf("data.h5", "Buildings", mode="w")
    return Buildings
