"""Resamples cleaned surface observation files to hourly"""
import warnings
from pandas.errors import DtypeWarning

from ros_database.processing.surface import read_iowa_mesonet_file, get_hourly_obs


def make_outpath(fp, outpath):
    """Returns output path for hourly files"""
    return outpath / ('.'.join(fp.stem.split('.')[:-1]) + ".hourly.csv")


def clean_to_hourly(filepath, outpath, verbose=False):
    """Resample cleaned file to hourly file

    :filepath: pathlib.Path POSIX path object

    :returns: None
    """
    outpath = make_outpath(filepath, outpath) 
    
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


