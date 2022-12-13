'''Generates an observation heat map for a Country'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from rain_on_snow.filepath import SURFOBS_RAW_PATH
from rain_on_snow.surfaceobs.surface import (load_iowa_mesonet_for_station,
                                             get_obs_count_distribution_minute,
                                             station_paths_in_country)


def get_timedelta_in_hours(df):
    '''Returns number of hours between start and end'''
    time_diff = df.index[-1] - df.index[0]
    return np.floor(time_diff.total_seconds() / 3600)


def heatmap_for_station(station_path, element=None):
    '''Returns a heatmap for a station'''
    df = load_iowa_mesonet_for_station(station_path)
    if element:
        df = df[element].dropna()
    nhours = get_timedelta_in_hours(df)
    h = np.histogram(df.index.minute, bins=np.arange(61))
    return station_path.name, h[0]/nhours


def plot_heatmap(station_names, heatmap, country):
    '''Creates heatmap plot'''
    nstation = len(station_names)
    
    fig, ax = plt.subplots(figsize=(15,20))

    ax.imshow(heatmap)

    ax.set_xticks(np.arange(0,61,5))
    ax.set_xlabel('Minutes', fontsize=20)
    ax.tick_params(axis='x', labelsize=15)
    
    ax.set_yticks(np.arange(nstation))
    ax.set_yticklabels(station_names, fontsize=15)

    ax.set_title(country, fontsize=25)

    return fig, ax


def plot_observations_heatmap_by_country(country, element=None, verbose=False):
    '''Generates a heatmap of obervations for a country archive'''

    if verbose: print(f'Generating observation time heatmap for {country.title()}')

    if verbose: print('   Generating station heatmaps...')
    station_name = []
    minute_heatmap = []
    for station_path in station_paths_in_country(country.title()):
        name, heatmap = heatmap_for_station(station_path, element=element)
        station_name.append(name)
        minute_heatmap.append(heatmap)

    minute_heatmap = np.vstack(minute_heatmap)
    minute_heatmap = np.where(minute_heatmap <= 0, np.nan, minute_heatmap)

    if verbose: print('   Creating plot...')
    fig, ax = plot_heatmap(station_name, minute_heatmap, country)

    if element:
        heatmap_image_file = SURFOBS_RAW_PATH / f'{country.lower()}.{element}.observation_time_heatmap.png'
    else:
        heatmap_image_file = SURFOBS_RAW_PATH / f'{country.lower()}.observation_time_heatmap.png'
    if verbose: print(f'   Writing heatmap image to {heatmap_image_file}')
    fig.savefig(heatmap_image_file)

    return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Create heatmap for country or region')
    parser.add_argument('region', type=str, help='Name of region to process')
    parser.add_argument('--element', '-e', default=None, help='valid element name')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='verbose output')

    args = parser.parse_args()
    
    plot_observations_heatmap_by_country(args.region, element=args.element, verbose=args.verbose)
