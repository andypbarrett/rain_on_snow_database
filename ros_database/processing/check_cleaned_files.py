"""Checks data types and range of parameters in cleaned mesonet files"""

import datetime as dt
import pandas as pd
import numpy as np

from ros_database.filepath import SURFOBS_CLEAN_PATH
from ros_database.processing.surface import read_iowa_mesonet_file
from ros_database.processing.quality_control import (expected_cleaned_dtypes,
                                                     expected_range,
                                                     expected_values)

# Notes on changing values:
# for relh set > 100 to 100
# for other out of range values set to NaN

def check_type(df, col):
    expected_dtype = expected_cleaned_dtypes[col]
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
        number_rows = len(df[col])
        number_missing = sum(df[col].isna())
        percent_missing = number_missing * 100. / number_rows
        min_value = df[col].min()
        max_value = df[col].max()
        quantiles = df[col].quantile(quantiles)
        quantile_str = ', '.join([f"{q:8.2f}" for q in quantiles])
        upper_extreme = df[col][df[col] > quantiles[0.99]]
        lower_extreme = df[col][df[col] < quantiles[0.01]]
        outside_expected_range = sum((df[col] < expected_range[col]['min']) |
                                     (df[col] > expected_range[col]['max']))
        # add list of extremes if they exist
        report = (f"{col:7} {str(dtype):7} | "
                  f"{number_missing:8d} {number_rows:8d} {percent_missing:5.1f} | "
                  f"{min_value:8.2f} {max_value:8.2f} | "
                  f"{quantile_str} | "
                  f"{len(lower_extreme):6d} {len(upper_extreme):6d} | "
                  f"{outside_expected_range:6d}")
    else:
        report = f"{col:7} {str(dtype):7} {unique_values}"
    print(report)


def check_one_file(fp, verbose=False, no_checking=False):
    """Checks a single file for data type and range"""
    print(f"Checking {fp.stem}")
    df = read_iowa_mesonet_file(fp) 
    for col in df.columns:

        if verbose:
            column_stats(df, col)

        if not no_checking:
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
            

def check_cleaned_files(verbose=False, no_checking=False):
    """Main script"""
    for fp in SURFOBS_CLEAN_PATH.glob('*clean.csv'):
        check_one_file(fp, verbose=verbose, no_checking=no_checking)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Verifys format, ranges and expected "
                                     "values of cleaned files")
    parser.add_argument("--variable_statistics", action="store_true",
                        help="Writes statistics for variables to stdout")
    parser.add_argument("--no_checking", action="store_true",
                        help="Just evaluate statistics for variables")
    
    args = parser.parse_args()
    check_cleaned_files(verbose=args.variable_statistics, no_checking=args.no_checking)
