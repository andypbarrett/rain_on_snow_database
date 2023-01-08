"""
Tests cleaning scripts - mostly check handling of precipitation at the moment

# TODO:
- create expected value and format datasets
- add test for dtypes
- add test for ranges
"""

from pathlib import Path

from ros_database.processing.surface import (read_iowa_mesonet_file,
                                             parse_iowa_mesonet_file)
from ros_database.processing.cleaning import (remove_duplicate_records,
                                              qc_range_check)

TEST_PATH = Path('tests')


def test_one_case(station_path, verbose=True, write_cleaned=True):
    """Mimics clean_iowa_mesonet_asos_station but outputs a human readable
       file"""

    if verbose: print(f"    Loading data for {station_path}")
    df = read_iowa_mesonet_file(station_path, usecols=None)
    outpath = f"{TEST_PATH / station_path.stem}.clean.csv"

    if verbose: print("    Removing duplicate records...")
    df_cleaned = remove_duplicate_records(df)
    if verbose: print("    Parsing records, and converting units...")
    df_parsed = parse_iowa_mesonet_file(df_cleaned)

    if verbose: print("    Checking for out of range values...")
    qc_range_check(df_parsed, verbose=True)

    if write_cleaned:
        if verbose: print(f"    Writing cleaned data to {outpath}")
        df_parsed.to_csv(outpath)
    
    print(df_parsed)


def test_raw_input(write_cleaned=True):
    """Test code for simple case"""
    test_file = TEST_PATH / "test_data_raw.csv"
    test_one_case(test_file, verbose=True, write_cleaned=write_cleaned)


def test_trace_precip_input(write_cleaned=True):
    """Test code for simple case"""
    test_file = TEST_PATH / "test_data_with_trace.csv"
    test_one_case(test_file, verbose=True, write_cleaned=write_cleaned)


def test_zero_precip_input(write_cleaned=True):
    """Test code for simple case"""
    test_file = TEST_PATH / "test_data_all_zero.csv"
    test_one_case(test_file, verbose=True, write_cleaned=write_cleaned)


if __name__ == "__main__":
    write_cleaned=True
    test_raw_input(write_cleaned=write_cleaned)
    print("-"*30+"\n")
    test_trace_precip_input(write_cleaned=write_cleaned)
    print("-"*30+"\n")
    test_zero_precip_input(write_cleaned=write_cleaned)
