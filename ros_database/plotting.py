"""Plotting routines for database"""
from typing import Union, List
import datetime as dt

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



PTYPE_COLORS = [
    'tab:orange',  # UP
    'dodgerblue',  # RA
    'lightskyblue',  # FZRA
    '0.7'  # SOLID
]
PTYPES = ["UP", "RA", "FZRA", "SOLID"]


def add_valid_obs_bar(da, ax, axis_fraction=0.05, color='k', width=1):
    """Adds a bar to a plot showing when valid exist"""
    
    y0, y1 = ax.get_ylim()
    baseline = y0
    yrange = y1 - y0
    yextra = (yrange * axis_fraction)
    y0 = baseline - yextra
    ylim = (y0, y1)

    ax.set_ylim(ylim)
    ax.axhline(baseline, color=color, lw=1)
    ax.bar(da.index, da.notnull() * -1 * yextra,
           bottom=baseline, width=width, color='k')
    return ax


def extend_yaxis(ax: plt.Axes,
                 by: float=0.05,
                 extend: str="upper") -> None:
    """Increases yaxis limits to accomodate title or valid obs barcolor

    Parameters
    ----------
    ax : matplotlib.pyplot.Axes instance
    by : fraction to increate axis
    extent : either upper, lower or both

    Returns
    -------
    None
    """
    y0, y1 = ax.get_ylim()
    yrange = y1 - y0
    if extend == "upper":
        y1 += yrange * by
    elif extend == "lower":
        y0 -= yrange * by
    elif extend == "both":
        y1 += yrange * by
        y0 -= yrange * by
    else:
        raise ValueError("Unexpected value for keyword extend.  "
                         "Expected one of upper, lower or both")
    ax.set_ylim(y0, y1)

    return


def plot_ptype(df: pd.DataFrame,
               width: float=1.,
               ax: Union[plt.Axes, None]=None,
               title: str=None,
               add_obs_bar: bool=True,
               obs_bar_color: str='0.4',
               obs_bar_width: float=1,) -> plt.Axes:
    """Plots time series of precipitation types"""

    if not ax:
        ax = plt.gca()
        
    bottom = 0
    for ptype, color in zip(PTYPES, PTYPE_COLORS):
        ax.bar(df.index, (df[ptype] == True * 1.),
               width=width, bottom=bottom, color=color)
        bottom += 1
    ax.set_yticks([0.5, 1.5, 2.5, 3.5], PTYPES)

    if add_obs_bar:
        valid_obs = df[PTYPES].notnull().all(axis=1)
        add_valid_obs_bar(valid_obs, ax, color=obs_bar_color, width=obs_bar_width)

    # Add label to plot
    print(ax.get_ylim())
    if title:
        extend_yaxis(ax, 0.04, "upper")
        t = ax.text(0.013, 0.98, title,
                    va="top",
                    transform=ax.transAxes,
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
        print(t.get_window_extent())
    print(ax.get_ylim())

    return ax


def plot_line(da: pd.Series,
              ax: Union[plt.Axes, None]=None,
              add_obs_bar: bool=True,
              linecolor: str='k',
              linewidth: str=1.,
              obs_bar_color: str='0.4',
              obs_bar_width: float=1,
              ylabel: Union[str, None]=None,
              add_axhline: bool=False,
              axhline_kargs: dict={'value': 0., 'c': '0.6', 'zorder': 0},
              title: Union[str, None]=None) -> plt.Axes:
    """Adds a line plot

    Parameters
    ----------
    da : pandas.Series
    ax : matplotlib axes instance.  If None, adds to current axes
    add_obs_bar : adds a bar at the bottom to show when valid data values exist

    Returns
    -------
    Returns matplotlib.pyplot.Axes instance
    """

    if ax is None:
        ax = plt.gca()

    # Plot line
    ax.plot(da.index, da, color=linecolor, lw=linewidth)

    # Add valid obs bar
    add_valid_obs_bar(da, ax, color=obs_bar_color, width=obs_bar_width)

    # Add ylabel
    if ylabel:
        ax.set_ylabel(ylabel)

    # Add horizontal line 
    if add_axhline:
        ax.axhline(axhline_kargs['value'], **{k: axhline_kargs.get(k) for k in ['c', 'zorder']})

    # Add label to plot
    if title:
        ax.text(0.013, 0.98, title,
                va="top",
                transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))


def plot_bar(da: pd.Series,
             ax: plt.Axes=None,
             width: Union[float, None]=None,
             barcolor: Union[str, List[str]]='k',
             add_obs_bar: bool=True,
             obs_bar_color: str='0.4',
             obs_bar_width: Union[float, None]=None,
             ylabel: Union[str, None]=None,
             title: Union[str, None]=None
             ) -> plt.Axes:
    """Plots bar chart - for precipitation"""

    if not ax:
        ax = plt.gca()

    if not width:
        width = da.index[1] - da.index[0]
        
    # Plot bars
    ax.bar(da.index, da, width=width, color=barcolor)

    if add_obs_bar:
        if not obs_bar_width:
            obs_bar_width = width
        add_valid_obs_bar(da, ax, color=obs_bar_color, width=obs_bar_width)

    if ylabel:
        ax.set_ylabel(ylabel)

    # Add label to plot
    if title:
        t = ax.text(0.013, 0.98, title,
                    va="top",
                    transform=ax.transAxes,
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    return ax


def plot_period_of_record(df: pd.DataFrame,
                          add_obs_bar: bool=True,
                          title: str="") -> plt.Figure:
    """Generates a plot of station observations"""

    width = dt.timedelta(days=1)  # For bar plots

    fig, ax = plt.subplots(7, 1, figsize=(12,10), sharex=True)
    fig.tight_layout(h_pad=0.01)

    plot_line(df.t2m,
              ax=ax[0],
              add_axhline=True,
              ylabel="deg C",
              title="2m Air Temperature")
    
    plot_line(df.d2m,
              ax=ax[1],
              add_axhline=True,
              ylabel="deg C",
              title="2m Dewpoint Temperature")
    
    plot_line(df.psurf,
              ax=ax[2],
              ylabel="hPa",
              title="Surface Pressure")

    plot_bar(df.p01i,
             ax=ax[3],
             ylabel="mm",
             title="Precipitation")

    plot_line(df.wspd,
              ax=ax[4],
              ylabel="m/s",
              title="Wind Speed")
    
    plot_line(df.drct,
              ax=ax[5],
              ylabel="Degrees",
              title="Wind Direction")
    
    plot_ptype(df,
               ax=ax[6],
               width=width,
               title="Precipitation Type")

    fig.suptitle(title);
    plt.subplots_adjust(top=0.95)

    return fig, ax


def plot_metdata_histograms(df):
    """Plots histograms of meteorological variables"""
    varlist = ["t2m", "d2m", "psurf", "p01i", "wspd", "drct"]

    fig, axes = plt.subplots(2, 3, sharey=False, tight_layout=True)

    for var, ax in zip(varlist, axes.flatten()):
        if var != "p01i":
            bins = np.arange(np.floor(df[var].min()), np.ceil(df[var].max())+1)
            df[var].hist(ax=ax, bins=bins)
            ax.set_title(var)
        else:
            bins = np.arange(0., np.ceil(df[var].max())+1, 0.2)
            df[var][df[var] > 0].hist(ax=ax, bins=bins)
            ax.set_title(var)
            
    fig.suptitle(df["station"].iloc[0]);

