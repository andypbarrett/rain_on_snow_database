"""Plotting routines for database"""

import maptplotlib.pyplot as plt
import pandas as pd


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


def plot_period_of_record(df: pd.DataFrame,
                          add_obs_bar: bool=True,
                          title: str="") -> plt.Figure:
    """Generates a plot of station observations"""

    width = dt.timedelta(days=1)  # For bar plots

    fig, ax = plt.subplots(7, 1, figsize=(12,10), sharex=True)
    fig.tight_layout(h_pad=0.01)
                 
    ax[0].plot(dfday.index, dfday.t2m, color='k', lw=1)
    add_valid_obs_bar(dfday.t2m, ax[0], color='0.4', width=width)
    ax[0].set_ylabel("deg C")
    ax[0].axhline(0., c='0.3', zorder=0)

    ax[1].plot(dfday.index, dfday.d2m, color='k', lw=1)
    add_valid_obs_bar(dfday.d2m, ax[1], color='0.4', width=width)
    ax[1].set_ylabel("deg C")
    ax[1].axhline(0., c='0.3', zorder=0)

    ax[2].plot(dfday.index, dfday.psurf, color='k', lw=1)
    add_valid_obs_bar(dfday.psurf, ax[2], color='0.4', width=width)
    ax[2].set_ylabel("hPa")

    ax[3].bar(dfday.index, dfday.p01i, width=width, color='k')
    add_valid_obs_bar(dfday.p01i, ax[3], color='0.4', width=width)
    ax[3].set_ylabel("mm")

    ax[4].plot(dfday.index, dfday.wspd, color='k', lw=1)
    add_valid_obs_bar(dfday.wspd, ax[4], color='0.4', width=width)
    ax[4].set_ylabel("m/s")
    
    ax[5].plot(dfday.index, dfday.drct, color='k', lw=1)
    ax[5].set_ylim(-180.,180.)
    add_valid_obs_bar(dfday.drct, ax[5], color='0.4')
    ax[5].set_ylabel("degrees")
    ax[5].axhline(0., c='0.3')

    # ax[6].

    fig.suptitle(df["station"].iloc[0]);
    plt.subplots_adjust(top=0.95)

    return fig, ax
