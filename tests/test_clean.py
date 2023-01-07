"""Tests cleaning scripts - mostly check handling of precipitation at the moment"""

from pathlib import Path

from ros_database.processing.surface import (read_iowa_mesonet_file,
                                             parse_iowa_mesonet_file)
from ros_database.processing.cleaning import (remove_duplicate_records,
                                              qc_range_check)

TEST_PATH = Path('tests')


def test_one_case(station_path, verbose=True):
    """Mimics clean_iowa_mesonet_asos_station but outputs a human readable
       file"""

    if verbose: print(f"    Loading data for {station_path}")
    df = read_iowa_mesonet_file(station_path, usecols=None)
    outpath = f"{TEST_PATH / station_path.stem}.clean.csv"

    if verbose: print("    Removing duplicate records...")
    df_cleaned = remove_duplicate_records(df)
    if verbose: print("    Parsing records, and converting units")
    df_parsed = parse_iowa_mesonet_file(df_cleaned)

    if verbose: print("    Checking for out of range values...")
    qc_range_check(df)

    if verbose: print(f"    Writing cleaned data to {outpath}") 
    print(df_parsed)


def test_raw_input():
    """Test code for simple case"""
    test_file = TEST_PATH / "test_data_raw.csv"
    test_one_case(test_file, verbose=True)


def test_trace_precip_input():
    """Test code for simple case"""
    test_file = TEST_PATH / "test_data_with_trace.csv"
    test_one_case(test_file, verbose=True)


def test_zero_precip_input():
    """Test code for simple case"""
    test_file = TEST_PATH / "test_data_all_zero.csv"
    test_one_case(test_file, verbose=True)


if __name__ == "__main__":
    test_raw_input()
    print("-"*30+"\n")
    test_trace_precip_input()
    print("-"*30+"\n")
    test_zero_precip_input()
