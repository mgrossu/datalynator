#!/usr/bin/python3.8
# coding=utf-8
# Autor: Marius Iustin Grossu xgross10
# Projekt 3 do IZV

import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster
import numpy as np


def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """ Konvertovani dataframe do geopandas.GeoDataFrame se spravnym kodovani """
    for col in list(df.columns):
        if col != 'p2a' and col != 'region':
            if df[col].dtype == 'object':
                df[col] = df[col].astype('category')
        if col == 'p2a':
            df[col] = pd.to_datetime(df[col])

    df = df[(df.p5a != -1) & (df.d != np.nan) & (df.e != np.nan)]
    gdf = geopandas.GeoDataFrame(df,
                                 geometry=geopandas.points_from_xy(df['d'], df['e']),
                                 crs='EPSG:5514')
    return gdf


def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """ Vykresleni grafu s dvemi podgrafy podle lokality nehody """
    gdf = gdf.loc[gdf['region'] == 'JHM']
    gdf2 = gdf.to_crs('epsg:3857')
    fig = plt.figure(constrained_layout=True, figsize=(16, 9))
    (ax1, ax2) = (fig.add_gridspec(ncols=2, nrows=1).subplots())
    gdf2[gdf2['p5a'] == 1].plot(ax=ax1, markersize=1, color='tab:red')
    gdf2[gdf2['p5a'] == 2].plot(ax=ax2, markersize=1, color='green')
    xmin, xmax = ax1.get_xlim()
    ymin, ymax = ax1.get_ylim()
    ax2.set_xlim(xmin, xmax)
    ax2.set_ylim(ymin, ymax)
    ax1.set_xlim(xmin, xmax)
    ax1.set_ylim(ymin, ymax)
    ax1.axis('off')
    ax2.axis('off')
    ax1.title.set_text('Nehody v JHM kraji: v obci')
    ax2.title.set_text('Nehody v JHM kraji: mimo obec')
    ctx.add_basemap(ax1, crs=gdf2.crs.to_string(),
                    source=ctx.providers.Stamen.TonerLite, zoom=10, alpha=0.9)
    ctx.add_basemap(ax2, crs=gdf2.crs.to_string(),
                    source=ctx.providers.Stamen.TonerLite, zoom=10, alpha=0.9)

    if fig_location is not None:
        fig.savefig(fig_location)

    if show_figure:
        plt.show()


def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """


    if fig_location is not None:
        fig.savefig(fig_location)

    if show_figure:
        plt.show()



if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", False)
    # plot_cluster(gdf, "geo2.png", True)
