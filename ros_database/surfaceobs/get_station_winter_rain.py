"""Counts September to April precipitation types.  Results are written to a csv"""

import pandas as pd

from rain_on_snow.surfaceobs.surface import (station_paths_in_country,
                                             load_iowa_mesonet_for_station,
                                             parse_iowa_mesonet_file)


def get_one_station_precipitation_type(station_path):
    """Counts precip type for one station

    :station_path: POSIX style path to station directory
    
    :returns: pandas DataFrame of precip type counts
    """
    df = load_iowa_mesonet_for_station(station_path)
    df = parse_iowa_mesonet_file(df)

    name = df.station.iloc[0]
    
    df_count = df[['UP', 'RA', 'FZRA', 'SOLID']].groupby(df.index.month).sum()
    df_liquid = df_count.UP + df_count.RA + df_count.FZRA
    df_liquid.name = name
        
    return df_liquid.to_frame().T


def get_station_winter_rain(country):
    
    stations = station_paths_in_country(country)

    df = pd.concat([get_one_station_precipitation_type(station) for station in stations])
    df.to_csv(f'{country.lower()}.liquid_and_freezing_counts.csv')
    

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Finds winter precipitation records')
    parser.add_argument('country', type=str,
                        help='Name of country to process')
    args = parser.parse_args()
    get_station_winter_rain(args.country)
    
