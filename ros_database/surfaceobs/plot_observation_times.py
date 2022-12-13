'''Generates plots of the temporal distribution of station observations for the AROSS archive
   by country'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from rain_on_snow.filepath import SURFOBS_RAW_PATH
from rain_on_snow.surfaceobs.surface import (load_iowa_mesonet_for_station,
                                             get_obs_count_distribution_minute)


def plot_obs_distribution_hour(s, ax, title=None):
    ax.stairs(s, np.append(s.index, 6), fill=True)
    ax.set_xticks(np.arange(0, 61, 10))
    ax.set_xlabel('Minutes')
    if title:
        ax.set_title(title)
    return 


def make_plot(df, station_name):
    nvar = len(df.columns)
    fig, axes = plt.subplots(ncols=nvar, figsize=(20,3),
                             constrained_layout=True,
                             sharey='all')
    
    for column, ax in zip(df, axes):
        plot_obs_distribution_hour(df[column], ax, title=column.upper())

    fig.suptitle(station_name, fontsize=20)
    
    fig.savefig('station_observations.png')

    
def plot_observation_times():
    '''Test function'''
    country = 'Alaska'
    station_name = 'Bettles-Field'
    filepath = SURFOBS_RAW_PATH / country / station_name

    df = load_iowa_mesonet_for_station(filepath)
    obs_df = get_obs_count_distribution_minute(df)
    make_plot(obs_df, station_name)

    return


if __name__ == "__main__":
    plot_observation_times()
    
