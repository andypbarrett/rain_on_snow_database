"""Loads data for a single station for period of record, removes duplicate entries
and performs unit conversions

Remove duplicates
Remove rows where all NaN, except ID
Convert to SI units
"""
import warnings

import pandas as pd

from ros_database.processing.surface import (read_iowa_mesonet_file,
                                             parse_iowa_mesonet_file)
from ros_database.processing.cleaning import remove_duplicate_records
from ros_database.filepath import SURFOBS_CONCAT_PATH, SURFOBS_CLEAN_PATH

# Suppresses FutureWarning about conflict in how strings and scalars are compared
# see: https://stackoverflow.com/questions/40659212/futurewarning-elementwise-comparison-failed-returning-scalar-but-in-the-futur
# Using
# python                    3.7.6           h8356626_5_cpython    conda-forge
# numpy                     1.18.4           py37h8960a57_0    conda-forge
warnings.simplefilter(action='ignore', category=FutureWarning)

def clean_iowa_mesonet_asos_station(station_path, verbose=False,
                                    ignore_fill_warnings=False):
    """Cleans raw Iowa Mesonet ASOS data for a single station.  All data files for a single
    station are combined.  Duplicate data records are removed.  Fields are converted
    from Imperial (English) units to SI.  Weather codes (WXCODE) for precipitation
    type are interpretted and assigned to separate boolean fields.  Data are written
    to csv files.

    :station_path: Posix type or string type path to station files.

    :returns: None
    """

    if verbose: print(f"    Loading data for {station_path}")
    df = read_iowa_mesonet_file(station_path, usecols=None)
    outpath = f"{SURFOBS_CLEAN_PATH / station_path.stem}.clean.csv"

    if verbose: print("    Removing duplicate records...")
    df_cleaned = remove_duplicate_records(df, ignore_fill_warnings=ignore_fill_warnings)
    if verbose: print("    Parsing records, and converting units")
    df_parsed = parse_iowa_mesonet_file(df_cleaned)

    if verbose: print(f"    Writing cleaned data to {outpath}") 
    df_parsed.to_csv(outpath)

    return


def clean_mesonet_data(verbose=False, ignore_fill_warnings=False):
    """Cleans all stations in raw/all_stations directory

    :verbose: verbose output
    """
    filepaths = SURFOBS_CONCAT_PATH.glob("*.csv")

    if verbose: print("Cleaning mesonet observation data")
    for fp in filepaths:
        if verbose: print(f"Processing {fp}")
        clean_iowa_mesonet_asos_station(fp, verbose=verbose,
                                        ignore_fill_warnings=ignore_fill_warnings)
        break


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="For each station in database, removes "
                                     "duplicate records, parses records and converts units")
    parser.add_argument("--verbose", help="verbose output", action="store_true")
    parser.add_argument("--ignore_fill_warnings", help="silence warnings", action="store_true")

    args = parser.parse_args()
    clean_mesonet_data(verbose=args.verbose, ignore_fill_warnings=args.ignore_fill_warnings)
