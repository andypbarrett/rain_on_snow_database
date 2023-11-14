"""Loads data for a single station for period of record, removes duplicate entries
and performs unit conversions

Remove duplicates
Remove rows where all NaN, except ID
Convert to SI units
"""
import warnings
import shutil

import pandas as pd
import numpy as np

from ros_database.processing.surface import (read_iowa_mesonet_file,
                                             parse_iowa_mesonet_file)
from ros_database.processing.cleaning import (remove_duplicate_records,
                                              qc_range_check)
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

    :verbose: verbose output for progress
    :ignore_fill_warnings: suppress warnings when duplicate records are filled.  
                           Only necessary for debugging.

    :returns: None
    """

    if verbose: print(f"    Loading data for {station_path}")
    df = read_iowa_mesonet_file(station_path, usecols=None)
    
    outpath = f"{SURFOBS_CLEAN_PATH / station_path.stem}.clean.csv"
    
    if verbose: print("    Removing duplicate records...")
    df_cleaned = remove_duplicate_records(df, ignore_fill_warnings=ignore_fill_warnings)
    if verbose: print("    Parsing records, and converting units")
    df_parsed = parse_iowa_mesonet_file(df_cleaned)

    if verbose: print("    Checking for out of range values...")
    qc_range_check(df_parsed)
    
    if verbose: print(f"    Writing cleaned data to {outpath}") 
    df_parsed.to_csv(outpath)

    return


