"""Checks data types and range of parameters in cleaned mesonet files"""

import datetime as dt
import pandas as pd
import numpy as np

from ros_database.filepath import SURFOBS_CLEAN_PATH
from ros_database.processing.surface import read_iowa_mesonet_file


expected_dtypes = {
    'station': 'object',
    'relh': 'float64',
    'drct': 'float64',
    'p01i': 'float64',
    'alti': 'float64',
    'mslp': 'float64',
    't2m': 'float64',
    'd2m': 'float64',
    'wspd': 'float64',
    'UP': 'object',
    'RA': 'object',
    'FZRA': 'object',
    'SOLID': 'object',
    'uwnd': 'float64',
    'vwnd': 'float64',
}


expected_range = {
    'relh': {'min': 0., 'max': 100.},
    'drct': {'min': 0., 'max': 360.},
    'p01i': {'min': 0., 'max': 100.},
    #    'alti': {'min': None, 'max': None},
    'mslp': {'min': 900., 'max': 1090.},
    't2m': {'min': -60., 'max': 50.},
    'd2m': {'min': -60., 'max': 50.},
    'wspd': {'min': 0., 'max': 100.},   # Based on Mt Washington record 231 mph
    'UP': {'min': False, 'max': True},
    'RA': {'min': False, 'max': True},
    'FZRA': {'min': False, 'max': True},
    'SOLID': {'min': False, 'max': True},
    'uwnd': {'min': -100, 'max': 100.},
    'vwnd': {'min': -100, 'max': 100.},
}


expected_values = {
    'UP': [True, False, np.nan],
    'RA': [True, False, np.nan],
    'FZRA': [True, False, np.nan],
    'SOLID': [True, False, np.nan],
}


# Notes on changing values:
# for relh set > 100 to 100
# for other out of range values set to NaN

def check_type(df, col):
    expected_dtype = expected_dtypes[col]
    assert df[col].dtype == expected_dtype, f"    For {col} expected {expected_dtype}, found {df[col].dtype} instead"


def check_range(df, col):
    """Checks that values are within expected range"""
    min_value = df[col].min()
    max_value = df[col].max()
    ex_min = expected_range[col]['min']
    ex_max = expected_range[col]['max']
    if np.isnan(min_value) & np.isnan(max_value):
        return None
    assert (min_value >= ex_min) and (max_value <= ex_max), f"    {col} failed range test, got ({min_value}, {max_value})"

    
def check_expected_values(df, col):
    """Checks that only expected values are included"""
    unique_values = df[col].unique()
    if col in ['UP', 'RA', 'FZRA', 'SOLID']:
        isexpected = np.array([uval in expected_values[col] for uval in unique_values])
        assert isexpected.all(), f"   Unexpected value {isexpected[isexpected == False]} in {col}"
        
        
def column_stats(df, col, quantiles=[0.99, 0.9, 0.75, 0.5, 0.25, 0.1, 0.01]):
    """Prints column stats

    different stats are output depending on data types
    """
    dtype = df[col].dtype
    unique_values = df[col].unique()
    if dtype == 'float64':
        min_value = df[col].min()
        max_value = df[col].max()
        quantiles = df[col].quantile(quantiles)
        quantile_str = ', '.join([f"{q:8.2f}" for q in quantiles])
        upper_extreme = df[col][df[col] > quantiles[0.99]]
        lower_extreme = df[col][df[col] < quantiles[0.01]]
        # add list of extremes if they exist
        report = f"{col:7} {str(dtype):7} {min_value:8.2f} {max_value:8.2f} {quantile_str}"
    else:
        report = f"{col:7} {str(dtype):7} {unique_values}"
    print(report)
    
def check_one_file(fp, verbose=False):
    """Checks a single file for data type and range"""
    print(f"Checking {fp.stem}")
    df = read_iowa_mesonet_file(fp) 
    for col in df.columns:

        if verbose:
            column_stats(df, col)
            
        try:
            check_type(df, col)
        except AssertionError as err:
            print(err)
        
        if col not in ['station', 'UP', 'RA', 'FZRA', 'SOLID', 'alti']:
            try:
                check_range(df, col)
            except AssertionError as err:
                print(err)

        try:
            check_expected_values(df, col)
        except AssertionError as err:
            print(err)
            

def check_cleaned_files(verbose=False):
    """Main script"""
    for fp in SURFOBS_CLEAN_PATH.glob('*clean.csv'):
        check_one_file(fp, verbose=verbose)
        break

if __name__ == "__main__":
    verbose = True
    check_cleaned_files(verbose=verbose)
