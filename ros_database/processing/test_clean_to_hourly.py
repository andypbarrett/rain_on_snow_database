"""Tests processing hourly data"""
import warnings

from pathlib import Path

from ros_database.processing.surface import read_iowa_mesonet_file, get_hourly_obs
#from ros_database.filepaths import SURFOBS_CLEAN_PATH
TEST_PATH = Path('tests')

def clean_to_hourly(filepath: Path, verbose=False):
    """Converts cleaned files to hourly files

    :filepath: pathlib.Path POSIX path object

    :returns: None
    """

    if verbose: print(f"   Loading data from {filepath}...")
    df = read_iowa_mesonet_file(filepath)

    if verbose: print("   Aggregating sub-hourly records to hourly...")
    df_hour = get_hourly_obs(df)

    print(df_hour)

    return


def test_data_raw():
    testfile = TEST_PATH / "test_data_raw.clean.csv"
    clean_to_hourly(testfile, verbose=True)


def test_data_all_zero():
    testfile = TEST_PATH / "test_data_all_zero.clean.csv"
    clean_to_hourly(testfile, verbose=True)


def test_data_with_trace():
    testfile = TEST_PATH / "test_data_with_trace.clean.csv"
    clean_to_hourly(testfile, verbose=True)


def main():
    test_data_raw()
    print('-'*20)
    test_data_all_zero()
    print('-'*20)
    test_data_with_trace()


if __name__ == "__main__":
    main()
    
