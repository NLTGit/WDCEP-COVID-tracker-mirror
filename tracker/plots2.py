import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from tracker.dataprep import ot_ts_prep, get_opentable_all_cities
from sklearn.cluster import KMeans

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

outcity = widgets.Output()
def select_plot(locations,
                df=OTDATA,
                window=7,
                title='Open Table seated diner change year-over-year (%)'):
    with outcity:
        fig, ax = plt.subplots(1, figsize=(15,5))
        X = ot_ts_prep(df.loc[locations,:], window=window)
        for col in X:
            ax.plot(X[col], label=col)
        ax.set_ylabel("% change YoY", fontsize=20)
        ax.set_xlabel("Month", fontsize=20)
        plt.legend()
        plt.title(title, fontsize=20)
        outcity.clear_output()
        plt.show()

city_widget = widgets.SelectMultiple(
    options=OTDATA.index.to_list(),
    # value=['District of Columbia'],
    description='Location(s)',
    disabled=False)

def on_value_change(change):
    select_plot(locations=change['new'])

city_widget.observe(on_value_change, 'value')

def cluster_analysis(clustermodel=KMeans,
                     seated_data=OTDATA,
                     window=7,
                     n_clusters=8,
                     random_state=32,
                     **clusterkwargs):

    ts = ot_ts_prep(seated_data, window=window)
    X = ts.fillna(0).T
    model = clustermodel(n_clusters=n_clusters,
                         random_state=random_state,
                         **clusterkwargs)
    X["labels"] = model.fit_predict(X)+1
    return X

CLUSTDATA = cluster_analysis()

def plot_clusters(data=CLUSTDATA.copy()):
    data[data == 0] = np.nan
    fig, ax = plt.subplots(1, figsize=(15, 5))
    for k in sorted(data["labels"].unique()):
        X = data.loc[data["labels"] == k, :].drop("labels", axis=1).mean()
        X.T.plot(alpha=0.9, ax=ax, label=f"Cluster {k}")
    dc = data.loc[['District of Columbia'], :].drop('labels',axis=1)
    dc.T.plot(lw=5, color="indianred", label="Dist. of Col.", ax=ax)
    data.drop('labels',axis=1).mean().T.plot(lw=5, ls=':', color='steelblue',
                                              label='All data avg.',
                                              ax=ax)
    plt.legend()
    plt.show();

outclust = widgets.Output()
def plot_single_cluster(k, data=CLUSTDATA.copy()):
    data[data == 0] = np.nan
    with outclust:
        fig, ax = plt.subplots(1, figsize=(15, 5))
        X = data.loc[data['labels']==k, :].drop('labels', axis=1)
        X.T.plot(alpha=0.6, ax=ax)
        dc = data.loc[['District of Columbia'],:].drop('labels', axis=1)
        dc.T.plot(lw=5, color="indianred", label="Dist. of Col.", ax=ax)
        data.drop('labels', axis=1).mean().T.plot(lw=5, ls=':', color='steelblue',
                                                  label='All data avg.',
                                                  ax=ax)
        ax.legend(bbox_to_anchor=(1.04, 1), fontsize=12).set_title("")
        plt.legend()
        outclust.clear_output()
        plt.show()

cluster_widget = widgets.Dropdown(
    options=sorted(CLUSTDATA['labels'].unique()),
    description='Cluster',
    disabled=False)

def on_cluster_change(change):
    plot_single_cluster(k=change['new'])

cluster_widget.observe(on_cluster_change, 'value')