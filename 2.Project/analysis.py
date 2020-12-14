#!/usr/bin/env python3.8
# coding=utf-8
# Autor: Marius Iustin Grossu xgross10
# Projekt 2 do IZV
# script takes the data from a file and visualize them

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
import numpy as np
import os


def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    """Return a pd.Dataframe.

    Keyword arguments:
    filename -- input file to be analysed
    verbose  -- output on stdout (default False)
    """
    orig_size = 0
    new_size = 0

    if not os.path.isfile(filename):
        print("ERROR: The file does not exists in working directory")
        exit(1)

    df_org = pd.read_pickle(filename, compression="gzip")

    orig_size = df_org.memory_usage(deep=True).sum()/1048576

    df_new = df_org.rename({'p2a': 'date'}, axis=1)

    for col in list(df_new.columns):
        if col != "date" and col != "region":
            df_new[col] = df_new[col].astype("category")
        if col == "date":
            df_new[col] = pd.to_datetime(df_new[col])

    new_size = df_new.memory_usage(deep=True).sum()/1048576

    if verbose:
        print("orig_size={:.1f} MB".format(orig_size))
        print("new_size={:.1f} MB".format(new_size))

    return df_new


def plot_conseq(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    """Show the fatality of acidents in each region.

    Keyword arguments:
    df            -- pd.Dataframe from get_dataframe()
    filename      -- saving the graph
    show_figure   -- show the graph (default False)
    """

    df = df[["p1", "p13a", "p13b", "p13c", "region"]]
    df = df.astype({"p13a": int, "p13b": int, "p13c": int})

    all_accidents = pd.DataFrame({"p13a": df.groupby("region")["p13a"].sum(),
                                  "p13b": df.groupby("region")["p13b"].sum(),
                                  "p13c": df.groupby("region")["p13c"].sum(),
                                  "total": df.groupby("region")["p1"].count()})

    # multi-index fix
    all_accidents = all_accidents.reset_index()

    total_sort = all_accidents.sort_values(by=["total"], ascending=False)

    # creating the plot
    sns.set_theme(style="darkgrid")
    fig = plt.figure(constrained_layout=True, figsize=(7, 7))
    ax1, ax2, ax3, ax4 = (fig.add_gridspec(nrows=4, ncols=1).subplots())
    sns.barplot(x="region", y="p13a", data=all_accidents, color="red",
                ax=ax1, order=total_sort["region"])
    sns.barplot(x="region", y="p13b", data=all_accidents, color="orange",
                ax=ax2, order=total_sort["region"])
    sns.barplot(x="region", y="p13c", data=all_accidents, color="yellow",
                ax=ax3, order=total_sort["region"])
    sns.barplot(x="region", y="total", data=all_accidents, palette="Greys_r",
                ax=ax4, order=total_sort["region"])
    # graph with fatal
    ax1.title.set_text('Úmrti')
    ax1.set(xlabel="", ylabel="Počet")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.axes.xaxis.set_visible(False)
    # graph with severe injuries
    ax2.title.set_text('Těžce ranění')
    ax2.set(xlabel="", ylabel="Počet")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.axes.xaxis.set_visible(False)
    # graph with easy injuries
    ax3.title.set_text('Lehce ranění')
    ax3.set(xlabel="", ylabel="Počet")
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.axes.xaxis.set_visible(False)
    # graph with total injuries in each region
    ax4.title.set_text('Celkem nehod')
    ax4.set(xlabel="", ylabel="Počet")
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)

    if fig_location is not None:
        fig.savefig(fig_location)

    if show_figure:
        plt.show()


def plot_damage(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    """Show the cause of damage of acidents in 4 region.

    Keyword arguments:
    df            -- pd.Dataframe from get_dataframe()
    filename      -- saving the graph
    show_figure   -- show the graph (default False)
    """
    df = df[["region", "p12", "p53"]]
    df = df.astype({"p53": float})
    df["p53"] = df["p53"].div(10)

    # new df with categorizing the values
    causes = ["nezaviněná řidičem", "nepřiměřená rychlost jízdy",
              "nesprávné předjíždění", "nedání přednosti v jízdě",
              "nesprávný způsob jízdy", "technická závada vozidla"]
    prices = ["< 50", "50-200", "200-500", "500-1000", "> 1000"]

    df2 = pd.DataFrame({"region": df.region,
                        "p12": pd.cut(df.p12, [0, 200, 209, 311, 414, 516, 615], labels=causes),
                        "p53": pd.cut(df.p53, [0, 50, 200, 500, 1000, float("inf")], labels=prices, include_lowest=True)})

    df3 = df2[df2["region"].isin(["JHM", "PLK", "ZLK", "KVK"])]

    # creating the plot using catplot
    sns.set_theme(style="darkgrid")
    g = sns.catplot(x="p53", hue="p12", col="region", col_wrap=2, data=df3, kind="count", legend=True)
    g.set_titles("{col_name}")
    g.set_axis_labels("Škoda [tisic Kč]", "Počet", labelpad=0.5)
    g.legend.set_title("Přičina nehody")
    g.set(yscale="log")
    g.fig.set_size_inches(12, 10)

    if fig_location is not None:
        g.fig.savefig(fig_location)

    if show_figure:
        plt.show()


def plot_surface(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """Show the number of accidents by the state of surface of the road in the last years in 4 regions.

    Keyword arguments:
    df            -- pd.Dataframe from get_dataframe()
    filename      -- saving the graph
    show_figure   -- show the graph (default False)
    """
    df = df[["region", "date", "p16", "p1"]]
    df = df[df["region"].isin(["JHM", "PLK", "ZLK", "KVK"])]
    # naming the state of the road accoriding to datasheet from CR Policie
    df["p16"] = df["p16"].replace({1: "suchý neznečištěný",
                                   2: "suchý znečištěný",
                                   3: "povrch mokrý",
                                   4: "bláto",
                                   5: "náledí, ujetý sníh - posypané",
                                   6: "náledí, ujetý sníh - neposypané",
                                   7: "rozlitý olej, nafta apod",
                                   8: "souvislá sněhová vrstva",
                                   9: "náhlá změna stavu",
                                   0: "jiný stav"})

    df2 = df.groupby(["region", "date", "p16"])["p1"].count()
    df2 = df2.reset_index()
    df2["date"] = pd.to_datetime(df2["date"]).dt.strftime("%Y-%m")
    df3 = df2.groupby(["region", "date", "p16"])["p1"].sum()
    df3 = df3.reset_index()
    df3["date"] = pd.to_datetime(df3["date"])

    # ploat using relplot
    sns.set_theme(style="darkgrid")
    g = sns.relplot(data=df3, x="date", y="p1", hue="p16", kind="line", col="region", col_wrap=2)
    g.set_titles("{col_name}")
    g.set_axis_labels("Datum vzniku nehody", "Počet nehod", labelpad=0.5)
    g.legend.set_title("Stav vozovky")
    g.fig.set_size_inches(13, 10)
    axes = g.axes.flatten()
    axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    axes[0].xaxis.set_major_locator(mdates.YearLocator())

    if fig_location is not None:
        g.fig.savefig(fig_location)

    if show_figure:
        plt.show()


if __name__ == "__main__":
    pass
