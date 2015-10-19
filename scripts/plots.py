#!/usr/bin/env python
# encoding: utf-8

from matplotlib.patches import Polygon
import pylab as pl
import matplotlib as mpl
import pandas as pd
import numpy as np
pd.options.display.mpl_style = 'default'

font = {'weight': 'bold',
        'size': 14}
mpl.rc('font', **font)


def plotBuildings(Buildings, iteration=0, legend=True):
    """plot the buildings :)"""
    fig, ax = pl.subplots(figsize=(8, 8), ncols=1)
    for b in Buildings.index:
        if np.isnan(Buildings.loc[b, "bja"]):
            fcol = "red"
        else:
            fcol = "black"
        mpl_poly = Polygon(
            np.array(Buildings.loc[b, "geometry"].exterior),
            facecolor=fcol, lw=0, alpha=0.7)
        ax.add_patch(mpl_poly)
    ax.set_title("Selected Buildings (iter={})".format(iteration))
    ax.relim()
    ax.autoscale()
    ax.set_ylabel("Northing")
    ax.set_xlabel("Easting")
    if legend:
        ax.legend(("known BJA", "unknown BJA"), loc="best")
    fig.savefig("../FIGURES/buildings_{}.png".format(iteration),
                bbox_inches="tight")


def plotNeighbours(Buildings, N, ID):
    """plot the neighbours and their rank."""
    fig, ax = pl.subplots(figsize=(8, 8), ncols=1)
    ax2 = fig.add_axes([0.95, 0.13, 0.05, 0.7])
    cmap = pl.cm.Oranges
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    bounds = np.linspace(min(N.loc[:, "rank"]), max(N.loc[:, "rank"]), 10)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cmaplist = [cmap(i) for i in range(cmap.N)]
    for e, polygon in enumerate(N.geometry):
        cmap_index = int(N.ix[e, "rank"] * 256) - 1
        mpl_poly = Polygon(
            np.array(polygon.exterior), facecolor=cmaplist[cmap_index],
            lw=0, alpha=0.8)
        ax.add_patch(mpl_poly)
        ax.text(polygon.centroid.x, polygon.centroid.y,
                N.index[e][-3:], fontsize=20)
        ax.plot(polygon.centroid.x, polygon.centroid.y,
                'x', markersize=10, color="w")
    mpl_poly_2 = Polygon(
        np.array(Buildings.loc[ID, "geometry"].exterior),
        facecolor="black", lw=0, alpha=1)
    ax.add_patch(mpl_poly_2)
    ax.plot(
        Buildings.loc[ID, "geometry"].centroid.x,
        Buildings.loc[ID, "geometry"].centroid.y,
        'o', markersize=10, color="r")
    ax.set_title("Neighbours ranking")
    ax.relim()
    ax.autoscale()
    ax.set_ylabel("Northing")
    ax.set_xlabel("Easting")
    cb = mpl.colorbar.ColorbarBase(
        ax2, cmap=cmap, norm=norm, spacing='proportional',
        ticks=bounds, boundaries=bounds, format='%0.1f')
    cb.set_label('Neighbour rank')
    fig.savefig(
        "../FIGURES/buildings_neighbour_rank.png", bbox_inches="tight")


def plotByear(Buildings, iteration=0):
    """plot the construction years."""
    fig, ax = pl.subplots(figsize=(8, 8), ncols=1)
    ax2 = fig.add_axes([0.95, 0.13, 0.05, 0.7])
    cmap = pl.cm.brg
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    bounds = np.linspace(Buildings.loc[:, "bja"].min(),
                         Buildings.loc[:, "bja"].max(), 10)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmaplist[0] = (.5, .5, .5, 1.0)

    for b in Buildings.index:
        year_index = (Buildings.loc[b, "bja"] - 
            Buildings.loc[:, "bja"].min()) / (Buildings.loc[:, "bja"].max() - 
                Buildings.loc[:, "bja"].min())
        if np.isnan(year_index):
            cmap_index = 0
        else:
            cmap_index = int(year_index * 256) - 1

        mpl_poly = Polygon(
            np.array(Buildings.loc[b, "geometry"].exterior),
            facecolor=cmaplist[cmap_index], lw=0, alpha=0.7)
        ax.add_patch(mpl_poly)
    ax.set_title("Construction Year (iter={})".format(iteration))
    ax.relim()
    ax.autoscale()
    ax.set_ylabel("Northing")
    ax.set_xlabel("Easting")

    cb = mpl.colorbar.ColorbarBase(
        ax2, cmap=cmap, norm=norm, spacing='proportional',
        ticks=bounds, boundaries=bounds, format='%0.0f')
    cb.set_label('COnstruction year')
    fig.savefig(
        "../FIGURES/buildings_constructionYear_{}.png".format(iteration),
        bbox_inches="tight")
