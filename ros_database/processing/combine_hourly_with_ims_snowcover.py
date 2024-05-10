"""Combines IMS Snow Cover with hourly data files"""

import pandas as pd

from ros_database.filepath import SURFOBS_HOURLY_PATH, IMS_PATH, SURFOBS_COMBINED_PATH
from ros_database.processing.surface import load_hourly_observations


def load_snow_cover_for_stations(resolution='4km'):
    """Loads IMS Snowcover.

    Surface type is coded 1 for open sea, 2 for land, 3 for sea ice, 4 for snow cover
    and 0 for missing.

    Return dataframe with True for snow cover, False for snow free land and NaN for 
    all other codes.
    """
    filepath = IMS_PATH / f"ims.snow_cover.from_{resolution}.csv"
    df = pd.read_csv(filepath, parse_dates=True, index_col=0)
    df = df.where((df == 2.) | (df == 4.))
    df = df.mask((df == 2.) | (df == 4.), df == 4)
    return df


def reindex_snow_cover(snow_cover, index):
    return snow_cover.reindex(index, method="ffill", limit=23)


def combine_one(met, snow_cover):
    """Combines data for one station"""
    met['sog'] = reindex_snow_cover(snow_cover, met.index)
    return met


def get_station_id(df):
    """Returns station id from dataframe"""
    return df.iloc[0,df.columns.get_loc("station")]


def make_outfile(fp):
    """Returns output path for combined data"""
    return SURFOBS_COMBINED_PATH / fp.name.replace("hourly","hourly.combined")


def combine_files(verbose=False):
    """Loops through files in SURFOBS_HOURLY_PATH and combines
    with snow cover data"""

    snow_cover = load_snow_cover_for_stations()

    for fp in SURFOBS_HOURLY_PATH.glob('*.csv'):
        df = load_hourly_observations(fp)
        stnid = get_station_id(df)
        df_combine = combine_one(df, snow_cover[stnid])
        
        outfp = make_outfile(fp)
        outfp.parent.mkdir(parents=True, exist_ok=True)
        if verbose: print(f"Writing combine file to {outfp}")
        df_combine.to_csv(outfp)


if __name__ == "__main__":
    verbose = True
    combine_files(verbose=verbose)
