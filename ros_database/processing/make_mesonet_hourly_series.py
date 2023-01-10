"""Resamples cleaned surface observation files to hourly"""
import warnings
from pandas.errors import DtypeWarning

from ros_database.processing.surface import read_iowa_mesonet_file, get_hourly_obs
from ros_database.filepath import SURFOBS_CLEAN_PATH, SURFOBS_HOURLY_PATH


def make_outpath(fp):
    """Returns output path for hourly files"""
    outpath = '.'.join(fp.stem.split('.')[:-1]) + ".hourly.csv"
    return SURFOBS_HOURLY_PATH / outpath

def clean_to_hourly(filepath, verbose=False):
    """Resample cleaned file to hourly file

    :filepath: pathlib.Path POSIX path object

    :returns: None
    """
    outpath = make_outpath(filepath) 
    
    if verbose: print(f"   Loading data from {filepath}...")
    # Some files through DTypeWarning this seems inconsequential
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DtypeWarning)
        df = read_iowa_mesonet_file(filepath)
    
    if verbose: print("   Aggregating sub-hourly records to hourly...")
    df_hour = get_hourly_obs(df)

    if verbose: print(f"   Writing hourly resampled data to {outpath}")
    df_hour.to_csv(outpath)

    return


def make_mesonet_hourly_series(verbose=False):
    """Resamples cleaned files to hourly"""
    for fp in SURFOBS_CLEAN_PATH.glob("*.clean.csv"):
        if verbose: print(f"Resampling {fp.stem}")
        clean_to_hourly(fp, verbose=verbose)
    return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Resample cleaned files to hourly data")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    
    make_mesonet_hourly_series(verbose=args.verbose)
