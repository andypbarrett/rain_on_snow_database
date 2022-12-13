"""Generates analysis files containing precipitation type 
columns and snow cover from IMS"""

import pandas as pd

from rain_on_snow.surfaceobs.surface import (station_paths_in_country,
                                             load_iowa_mesonet_for_station,
                                             parse_iowa_mesonet_file)
from rain_on_snow.filepath import SURFOBS_COMBINED_PATH

IMS_SNOW_PATH = 'asos_station_snow_from_ims.csv'

country_list = ['alaska','canada','finland',
                'greenland', 'iceland', 'norway',
                'russia', 'sweden']


def load_station_data(station_path):
    """Loads and parses IOWA mesonet data for a station

    :station_path: POSIX style path to station data

    :returns: pandas dataframe
    """
    df = load_iowa_mesonet_for_station(station_path)
    df = parse_iowa_mesonet_file(df)
    return df


def combine_for_station(station_path, ims_df):
    """Creates combined file for a station"""
    asos_df = load_station_data(station_path)

    station_id = asos_df.station.iloc[0]
    ims_s = ims_df[station_id]
    ims_s = ims_s.reindex_like(asos_df.station, method='pad')
    #TODO set IMS to -1 for missing
    
    asos_df = asos_df.join(ims_s.rename('snog'), how='left')

    outfile = SURFOBS_COMBINED_PATH / f"{station_id}.asos_combined.csv"
    print(f"      Writing combined file to {outfile}")
    asos_df.to_csv(outfile)
    return


def load_ims_for_stations():
    return pd.read_csv('asos_station_snow_from_ims.csv',
                       index_col=0, header=0,
                       parse_dates=True)


def main():
    ims_df = load_ims_for_stations()
    
    for country in country_list:
        print(f"Processing stations in {country.title()}")
        stations = station_paths_in_country(country)
        for station in stations:
            print(f"   Combining IMS snow cover with {station.name}...")
            combine_for_station(station, ims_df)


if __name__ == "__main__":
    main()
