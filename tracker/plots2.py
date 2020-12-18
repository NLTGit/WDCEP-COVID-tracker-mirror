from tracker.config import PLOT_DIR
import pandas as pd
from collections import Counter
import contextily as ctx
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date
from matplotlib import gridspec
from pathlib import Path
import ipywidgets as widgets
from tracker.dataprep import ot_ts_prep, get_opentable_all_cities

OTDATA = get_opentable_all_cities()

def ot_dc_usa_all(df=OTDATA,
                  window=7,
                  title='Open Table seated diner change year-over-year (%)'):
    fig, ax = plt.subplots(1, figsize=(15,5))
    ax.plot(ot_ts_prep(df.loc['District of Columbia',:], window=window),
            lw=5,
            color='indianred',
            label='District of Columbia')
    ax.plot(ot_ts_prep(df.loc['United States',:], window=window),
            label='USA cities (avg)')
    ax.plot(ot_ts_prep(df.loc[df.index!= 'United States',:], window=window).mean(axis=1),
            label='Global cities (avg)')
    ax.set_ylabel("% change YoY", fontsize=20)
    ax.set_xlabel("Month", fontsize=20)
    plt.legend()
    plt.title(title, fontsize=20)

out = widgets.Output()
def select_plot(locations,
                df=OTDATA,
                window=7,
                title='Open Table seated diner change year-over-year (%)'):
    with out:
        fig, ax = plt.subplots(1, figsize=(15,5))
        X = ot_ts_prep(df.loc[locations,:], window=window)
        for col in X:
            ax.plot(X[col], label=col)
        ax.set_ylabel("% change YoY", fontsize=20)
        ax.set_xlabel("Month", fontsize=20)
        plt.legend()
        plt.title(title, fontsize=20)
        out.clear_output()
        plt.show()

city_widget = widgets.SelectMultiple(
    options=OTDATA.index.to_list(),
    # value=['District of Columbia'],
    description='Location(s)',
    disabled=False)

def on_value_change(change):
    select_plot(locations=change['new'])

city_widget.observe(on_value_change, 'value')


def plot_clusters(data):
    ncols = 1
    nrows = round(data["labels"].nunique() / ncols)
    gs = gridspec.GridSpec(nrows, ncols)
    fig = plt.figure(figsize=(15, 7 * nrows))
    for i, clust in enumerate(sorted(data["labels"].unique())):
        X = data.loc[data["labels"] == clust, :].drop("labels", axis=1)
        ax = fig.add_subplot(gs[i])
        X.T.plot(color="gray", alpha=0.3, ax=ax)
        X.mean().plot(color="steelblue", label="cluster mean", ax=ax)
        data.drop("labels", axis=1).mean().plot(
            color="indianred", label="all mean", ax=ax
        )
        ax.legend(bbox_to_anchor=(1.04, 1), fontsize=12).set_title("")
        ax.set_title(f"cluster: {clust+1}")
        ax.set_ylim([-100,100])
    plt.show();


def compare_weekdays(data, title):
    fig, ax = plt.subplots(1, figsize=(15, 5))
    days = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
    }
    data["weekday"] = [days[i.weekday()] for i in data.index]
    for v in days.values():
        plotdata = (
            data.loc[data["weekday"] == v, :].groupby(pd.Grouper(freq="M")).mean()
        )
        ax.plot(plotdata, label=v)
    plt.ylabel("% change YoY")
    plt.xlabel("Month", fontsize=20)
    plt.legend()
    plt.title(title, fontsize=20)


def barweekdays(data):
    plotdata = data.groupby([pd.Grouper(freq="M"), "weekday"])["seated_diners"].mean()
    plotdata = plotdata.unstack()
    plotdata.index = plotdata.index.to_period("M")
    plotdata = plotdata.loc[
        :,
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    ]
    plotdata.plot(kind="bar", legend=True, figsize=(15, 10))
    plt.title("% YOY change by weekday (monthly avg)", fontsize=20)
    plt.xlabel("Month", fontsize=20)
    plt.ylabel("% change", fontsize=20)


def plot_daily_hrs_dist(data,plotdir=PLOT_DIR):
    fig = plt.figure(figsize=(15, 7))
    weekcols = [f"{d.lower()}_hrs" for d in ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]]
    _ = [sns.kdeplot(data.loc[:, col], label=col[:-4]) for col in weekcols]
    plt.legend()
    plt.xlabel("daily hrs", fontsize=20)
    title = f"Dist of hours open by day of week as of {date.today()}"
    plt.title(title, fontsize=20)
    plt.savefig(Path(PLOT_DIR,title+'__KDplot.png'), bbox='tight')
    plt.show();


def violin_plot_daily_hrs(data):
    fig, ax = plt.subplots(1, figsize=(15, 7))
    X = data.melt(
        value_vars=[
            f"{d.lower()}_hrs" for d in ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
        ]
    )
    X["variable"] = X["variable"].str[:-4]
    ax = sns.violinplot(x="variable", y="value", data=X)
    plt.xlabel("Day", fontsize=20)
    title = f"Dist of hours open by day of week as of {date.today()}"
    plt.title(title, fontsize=20)
    plt.savefig(Path(PLOT_DIR, title + '__violin.png'), bbox='tight')
    plt.show();
