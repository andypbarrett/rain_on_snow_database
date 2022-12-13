'''Processes Canadian station data to hourly'''

from rain_on_snow.surfobs.surface import (station_paths_in_country,
                                          load_iowa_mesonet_file)
import pandas as pd


def load_iowa_mesonet_parsed_for_station(station_path):
    '''Loads all files for a given station using
       load_iowa_mesonet_file, which subsets and parses
       fields

    :country: country or region path
    '''
    df = pd.concat([load_iowa_mesonet_parsed_file(fp)
                    for fp in station_path.glob('*.txt')])
    df = df.sort_index()
    return df


