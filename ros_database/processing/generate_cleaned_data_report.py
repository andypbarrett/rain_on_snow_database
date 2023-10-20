"""Generates a listing with file stats on cleaned data

This is to check processing and is not required.
"""
import warnings

import numpy as np
#from pandas.errors import DtypeWarning

from ros_database.filepath import SURFOBS_CLEAN_PATH
from ros_database.processing.surface import load_station_combined_data


REQUIRED_COLUMNS = ['relh', 'drct', 'p01i', 'mslp', 't2m', 'd2m', 'wspd',
                    'psurf', 'UP', 'RA', 'FZRA', 'SOLID', 'uwnd', 'vwnd']

def is_duplicate_records(df):
    return (df.duplicated() & df.index.duplicated()).any()


def count_records(df):
    return len(df)


def all_columns_missing(df):
    return df.isna().all()


def count_all_columns_missing(df):
    return all_columns_missing(df).sum()


def columns_missing(df):
    return df.isna()


def count_columns_missing(df):
    return columns_missing(df).sum()


def get_date_range(df):
    return df.index.min(), df.index.max()


def date_range_to_string(df):
    """Returns are string with the date range"""
    tbeg, tend = get_date_range(df)
    return f"{tbeg.isoformat()}, {tend.isoformat()}"

    
def any_ptype(df):
    """Returns a boolean array with True if trace precip"""
    columns = ['UP', 'FZRA', 'RA', 'SOLID']
    return df[columns].any(axis=1)


def data_and_ptype(df, columns=REQUIRED_COLUMNS):
    """Returns boolean series with True for all required columns
    and at least one ptype"""


# From notebook
def is_precip(df):
    """Returns a boolean Series with True if precip"""
    return df.p01i > 0.


def is_zero_precip(df):
    """Returns a boolean series with True is precip is zero"""
    return np.isclose(0., df.p01i, atol=0.1)
    
    
def precip_isnan(df):
    """Returns a boolean series with True for precip is nan"""
    return df.p01i.isna()


def count_precip_events(df):
    """Counts non-zero precipitation"""
    return is_precip(df).sum()


def is_trace(df, trace=0.2):
    """Returns a boolean array with True if trace precip

    ! not sure why I use allclose instead of <!"""
    return np.isclose(trace, df.p01i, atol=0.01)

    
def count_trace_precip(df, trace=0.2):
    """Count trace precipitation events"""
    return is_trace(df).sum()


def any_ptype(df):
    """Returns a boolean array with True if any precip type columns is True"""
    columns = ['UP', 'FZRA', 'RA', 'SOLID']
    return df[columns].any(axis=1)

    
def count_any_ptype(df):
    """Counts timestamps with at least one precipitation type recorded"""
    return any_ptype(df).sum()


def count_ptype_with_precip(df):
    """Counts precipitation events that have a p-type"""
    return  (is_precip(df) & any_ptype(df)).sum()


def count_ptype_with_trace(df):
    """Counts trace events that have a ptype"""
    return (is_trace(df) & any_ptype(df)).sum()


def count_ptype_with_zero_precip(df):
    """Counts recorded ptypes with zero preciptation"""
    return (is_zero_precip(df) & any_ptype(df)).sum()


def count_ptype_with_precip_isnan(df):
    """Counts recorded ptypes with nan precip"""
    return (precip_isnan(df) & any_ptype(df)).sum()




def generate_cleaned_data_report():
    """Creates a inventory report for cleaned data"""

    warnings.simplefilter("ignore")
    
    for fp in SURFOBS_CLEAN_PATH.glob('*.clean.csv'):
        df = load_station_combined_data(fp)
        print(f"{fp.name}, {count_records(df):6d}, "
              f"{date_range_to_string(df)}, "
              f"{is_duplicate_records(df)}")


if __name__ == "__main__":
    generate_cleaned_data_report()
