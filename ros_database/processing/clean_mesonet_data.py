"""Loads data for a single station for period of record, removes duplicate entries
and performs unit conversions

Remove duplicates
Remove rows where all NaN, except ID
Convert to SI units
"""
import pandas as pd

from ros_database.processing.surface import (station_paths_in_country,  # not needed if we use new files
                                             load_iowa_mesonet_for_station,
                                             parse_iowa_mesonet_file)
from ros_database.processing.cleaning import remove_duplicate_records
from ros_database.filepath import SURFOBS_RAW_PATH

from tests.test_fill import load_test_input

country_list = ['alaska','canada','finland',
                'greenland', 'iceland', 'norway',
                'russia', 'sweden']

pd.set_option('display.max_rows', None)

def clean_iowa_mesonet_asos_station(station_path, verbose=False):
    """Cleans raw Iowa Mesonet ASOS data for a single station.  All data files for a single
    station are combined.  Duplicate data records are removed.  Fields are converted
    from Imperial (English) units to SI.  Weather codes (WXCODE) for precipitation
    type are interpretted and assigned to seprate boolean fields.  Data are written
    to csv files.

    :station_path: Posix type or string type path to station files.

    :returns: None
    """
    outpath = "test_data_cleaned.csv"
    
    if verbose: print(f"    Loading data for {station_path}")
    df = load_test_input()
    
    if verbose: print("    Removing duplicate records...")
    df_cleaned = remove_duplicate_records(df)
    if verbose: print("    Parsing records, and converting units")
    df_parsed = parse_iowa_mesonet_file(df_cleaned)

    if verbose: print(f"    Writing cleaned data to {outpath}") 
    df_cleaned.to_csv(outpath)

    return


if __name__ == "__main__":
    clean_iowa_mesonet_asos_station('test data', verbose=True)
    #count_mesonet_duplicates()
