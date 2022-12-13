"""Identifies rain on snow events based on weather codes and either observed 
snow depth or IMS snow cover data"""

import pandas as pd
import geopandas as gpd

from rain_on_snow.surfaceobs.surface import load_station_combined_data
from rain_on_snow.filepath import (SURFOBS_COMBINED_PATH,
                                   SURFOBS_EVENTS_PATH)


def station_list():
    """Returns generator of station combined data files"""
    return SURFOBS_COMBINED_PATH.glob('*')


def make_outfile(fp):
    return (SURFOBS_EVENTS_PATH /
            fp.name.replace("_combined",".rain_on_snow"))


def get_rain_on_snow(df):
    """Returns a DataFrame of winter rain events

    :df: Pandas DataFrame of observations
    """
    return df[(df['RA'] | df['FZRA']) & (df['snog'] == 4.)]

    
def get_station_rain_on_snow(station_path):
    """Extracts rain on snow events for a station 
    and writes to file

    :station_path: POSIX path to combined file
    """
    print("   Loading data...")
    df = load_station_combined_data(station_path)
    print("   Extracting events...")
    ros_df = get_rain_on_snow(df)
    outfile = make_outfile(station_path)
    print(f"   Writing events to {outfile}")
    ros_df.to_csv(outfile)
    return


def main():
    for station_path in station_list():
        print(f"Getting events for {station_path.name}")
        get_station_rain_on_snow(station_path)


if __name__ == "__main__":
    main()
