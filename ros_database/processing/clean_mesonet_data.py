"""Loads data for a single station for period of record, removes duplicate entries
and performs unit conversions

Remove duplicates
Remove rows where all NaN, except ID
Convert to SI units
"""
import pandas as pd

from ros_database.processing.surface import (read_iowa_mesonet_file,
                                             parse_iowa_mesonet_file)
from ros_database.processing.cleaning import remove_duplicate_records
from ros_database.filepath import SURFOBS_CONCAT_PATH, SURFOBS_CLEAN_PATH

from tests.test_fill import load_test_input

def clean_iowa_mesonet_asos_station(station_path, verbose=False, debug=False):
    """Cleans raw Iowa Mesonet ASOS data for a single station.  All data files for a single
    station are combined.  Duplicate data records are removed.  Fields are converted
    from Imperial (English) units to SI.  Weather codes (WXCODE) for precipitation
    type are interpretted and assigned to separate boolean fields.  Data are written
    to csv files.

    :station_path: Posix type or string type path to station files.

    :returns: None
    """

    if verbose: print(f"    Loading data for {station_path}")
    if debug:
        df = load_test_input()
        outpath = "test_data_cleaned.csv"
    else:
        df = read_iowa_mesonet_file(station_path, usecols=None)
        outpath = f"{SURFOBS_CLEAN_PATH / station_path.stem}.clean.csv"

    if verbose: print("    Removing duplicate records...")
    df_cleaned = remove_duplicate_records(df)
    if verbose: print("    Parsing records, and converting units")
    df_parsed = parse_iowa_mesonet_file(df_cleaned)

    if verbose: print(f"    Writing cleaned data to {outpath}") 
    df_parsed.to_csv(outpath)

    return


def clean_mesonet_data(verbose=False, debug=False):
    """Cleans all stations in raw/all_stations directory

    :verbose: verbose output
    :debug: debug flag for testing
    """
    if debug:
        filepaths = ["test data"]
    else:
        filepaths = SURFOBS_CONCAT_PATH.glob("*.csv")

    if verbose: print("Cleaning mesonet observation data")
    for fp in filepaths:
        clean_iowa_mesonet_asos_station(fp, verbose=verbose, debug=debug)


if __name__ == "__main__":

    verbose=True
    debug = False
    clean_mesonet_data(verbose=verbose, debug=debug)
