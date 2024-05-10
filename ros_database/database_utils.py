import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import matplotlib.dates as mdates

import numpy as np
import pandas as pd

from ros_database.processing.surface import read_iowa_mesonet_file, load_station_metadata
from ros_database.filepath import SURFOBS_HOURLY_PATH

# Datbase analysis
def get_name(df):
    return df["station"].dropna().unique()[0]

def count_observations(df, columns=["t2m"]):
    """Counts the number of valid hourly observations"""
    return df[columns].notna().all(axis=1).resample('D').sum()

def get_observation_counts(fp):
    df = read_iowa_mesonet_file(fp)
    count = count_observations(df)
    count.name = get_name(df)
    return count

def make_observation_counts(station_paths, columns=["t2m"], outfile="aross.database.daily_observation_counts.csv"):
    counts_all = pd.concat([get_observation_counts(fp) for fp in station_paths], axis=1)
    counts_all.to_csv(outfile)


def make_station_event_counts(season="winter"):
    """Count number of events per station by type"""

    # Get station metadata
    indices = []
    data = []
    for fp in SURFOBS_HOURLY_PATH.glob("*.hourly.csv"):
        df = read_iowa_mesonet_file(fp) 
        indices.append(get_stationid(df)) 
        data.append(get_total_events(df, season))

    total_events = pd.DataFrame(data, index=indices)
    # Generate summary columns for Rain on Snow (ROS) and Total number of events
    total_events["ROS"] = total_events[["RA","FZRA"]].sum(axis=1)
    total_events["Total"] = total_events[["RA","FZRA","SOLID"]].sum(axis=1)

    # Get station metadata and merge coordinates with total_events
    stations = load_station_metadata()
    total_events = total_events.join(stations[['longitude', 'latitude']])
    total_events.to_csv(f"station_event_counts_{season}.csv")


def get_total_events(df, season): 
    """Return total number of events"""
    if season == "winter":
        months = [10,11,12,1,2,3,4]
    else:
        months = np.arange(13)
    return df.loc[df.index.month.isin(months),["UP", "RA", "FZRA", "SOLID"]].sum().to_dict()
    

def get_stationid(df):
    """Return station id"""
    return df.iloc[0]["station"]


    
# Plotting
def make_yticklabels(y, interval=5.):
    """Returns yticks and ylabels"""
    if y.dtype != 'float64':
        raise TypeError(f"Expects float, got {y.dtype}")
    ylabels = np.arange(y.min().round(-1), y.max().round(-1)+interval, interval)
    yticks = np.interp(ylabels, y, np.arange(len(y)))
    return yticks, ylabels

def heatmap(X, y=None, ax=None, fig=None, aspect=0.4, cmap='viridis', norm=None, 
            levels=None, extend="max", **kwargs):
    """Plots a heat map with date labels
    
    :X: pd.DataFrame containing counts
    :y: alternative y labels, expects np.array
    """
    if fig is None:
        fig = plt.gcf()
        
    # if ax is None:
    #     ax = plt.gca()

    x = X.index
    if y is None:
        y = X.columns
        yticks = np.arange(len(y))
        ylabels = y
    else:
        raise NotImplementedError("Alternative y-labels are not implemented yet")
        yticks, ylabels = make_yticklabels(y, interval=2.)
    data = X.T.values
    
    yticks = [0, 53,  76,  90,  94, 120, 146, 169, 244]
    ylabels = ['CA', 'FI', 'GL', 'IS', 'NO', 'RU', 'SE', 'US']
    xticks = np.where(X.index.month == 1)[0][::2]
    xlabels = X.index.year[xticks]

    if not levels:
        vmin = np.nanmin(data)
        vmax = np.nanmax(data)
        levels = np.linspace(vmin, vmax, 10)
    cmap = mcolors.ListedColormap(mpl.colormaps[cmap](np.linspace(0.,1.,len(levels))))
    norm = mcolors.BoundaryNorm(levels, ncolors=cmap.N, clip=False)
    im = ax.imshow(data, aspect=aspect, cmap=cmap, origin='lower', norm=norm,
                   extent=[X.index.min(), X.index.max(), 0, len(y)],
                   interpolation="none", **kwargs)

    ax.xaxis.set_major_locator(mdates.YearLocator(base=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # ax.set_xticks(xticks)
    # ax.set_xticklabels(xlabels, fontsize=15)
    ax.set_yticks(yticks)
    ax.set_yticklabels([])
    ax.set_yticks([(yticks[i]+yticks[i+1])*0.5 for i in range(len(yticks)-1)], minor=True)
    ax.set_yticklabels(ylabels, fontsize=20, minor=True)
    
    ax.grid(axis='y', which='major', linewidth=1, color='0.5')
    
    fig.colorbar(im, shrink=0.7, pad=0.01, extend=extend)