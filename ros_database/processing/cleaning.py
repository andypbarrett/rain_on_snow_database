"""Code used to clean raw Iowa mesonet datafiles"""
import warnings

import numpy as np
import pandas as pd

from ros_database.processing.quality_control import (expected_range,
                                                     replacement_values)


def fill_missing(df, method_for_multiple="skip"):
    """Fills missing values for each column in a duplicate record

    :df: pandas.DataFrame

    :method_for_multiple: method to deal with more than one unique value for a
                          duplicate timestamp.  Default is to "skip" the timestamp.
                          If 'last' is chosen, then the last value is selected.  This 
                          assumes that the last value in the sequence is the last
                          transmission and is an update."""
    fill_dict = {}
    for col in df.columns:
        if df[col].isna().all(): continue
        unique_values = df[col].dropna().unique()
        if len(unique_values) > 1:
            if method_for_multiple == "last":
                fill_dict[col] = unique_values[-1]
                warnings.warn(f"More that one unique value for {col} "
                              f"from {unique_values} in row {df.index.unique()}: "
                              "selecting last value")
            else:
                fill_dict[col] = np.nan
                warnings.warn(f"More that one unique value for {col} "
                              f"from {unique_values} in row {df.index.unique()}: "
                              "cannot select fill value")
            df.loc[:, col] = np.nan
        else:
            fill_dict[col] = unique_values[0]
    return df.fillna(fill_dict)


def remove_duplicate_for_index(df, method_for_multiple="last"):
    #try:
    filled_df = fill_missing(df.copy(deep=True), method_for_multiple=method_for_multiple)
    #except Exception as err:
    #    print(err)
    #    return None
    return filled_df.drop_duplicates()


def check_all_none(list_of_dataframes):
    """Check if all members of lis are None"""
    return all([df is None for df in list_of_dataframes])


def remove_duplicated_indices(df, debug=False):
    """Removes duplicated records from a DataFrame containing duplicated records

    :df: pandas DataFrame containg duplicated records

    :return: returns a DataFrame containing unique records
    """
    unique_indices = df.index.unique()
    result = []
    for idx in unique_indices:
        result.append(remove_duplicate_for_index(df.loc[idx]))
    if check_all_none(result):
        return None
    return pd.concat(result)


def remove_duplicate_records(df, ignore_fill_warnings=False):
    """Removes duplicate records from an DataFrame containg ASOS data
    retreived from the Iowa Mesonet Site.

    ASOS data files hosted by the Iowa Mesonet archive can contain
    multiple records for the same timestamp.  These duplicates can arise
    from repeated transmission of the same data, or corrected or updated
    transmissions.  For the purposes of data cleaning, we assume that valid
    data values supercede missing data (NaN).

    Duplicated records are searched for and removed on a timestamp by 
    timestamp basis.  This is necessary because multiple unique timestamps
    may have the same values, and appear to be duplicated.  Consevutive 
    duplicated records may be a problem but these are dealt with by a 
    different process.  He we focus on removing duplicated time records.

    Duplicated timestamps are first identified and copied to a separate
    DataFrame.  Records with unique timestamps are copied to another DataFrame.
    For each timestamp with duplicate records, the records are inspected and
    missing values (NaN) are filled to maximise data retention, then only
    one of the duplicate records is retained.  These, now unique records,
    are written to a new DataFrame.  This DataFrame is then concatenated with
    the initial DataFrame containing unique records and sorted by time index.  
    This new unique DataFrame is returned. 

    :df:  pandas DataFrame

    :returns: pandas.DataFrame with unique date sorted indices"""
    # split into two DataFrames with duplicated indices and unique indices
    isduplicated = df.index.duplicated(keep=False)
    nduplicated = sum(isduplicated)
    if nduplicated == 0:
        return df
    
    df_duplic = df[isduplicated]
    df_unique = df[~isduplicated]

    # Remove duplicate records
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        df_removed = remove_duplicated_indices(df_duplic)
    
    # Concatenate unique and removed DataFrame, and sort
    df_cleaned = pd.concat([df_unique, df_removed]).sort_index()

    # Check for duplicates just in case something failed
    if df_cleaned.index.duplicated().any():
        raise Exception("Duplicated records still present!")

    return df_cleaned


def range_check(df, varname):
    """Sets values outside of expected range for a variable to NaN

    :df: (pandas.DataFrame) containing variables
    :varname: (string) name of variable

    :returns: does replacement in place
    """
    expmin = expected_range[varname]['min']
    expmax = expected_range[varname]['max']
    df[varname].where((df[varname] >= expmin) & (df[varname] <= expmax), inplace=True)
    return

    
def range_check_relh(df: pd.DataFrame):
    """Check if relh values are within expected range.  Values above range are set_option
    set to 100%.  Values below range are set to NaN."""
    df['relh'].where((df['relh'] <= 105.) |
                      df['relh'].isna(), 100., inplace=True)
    df['relh'].where(df['relh'] >= 0., inplace=True)
    return


def qc_range_check(df: pd.DataFrame, verbose=False):
    """Does quality control on expected ranges for variables.  Variables outside
    of range are set to NaNs

    :df: pandas.DataFrame from parsing
    
    replacements are performed in place
    """
    range_check_relh(df)
    
    for col in ['drct', 'p01i', 'mslp', 'psurf',
                't2m', 'd2m', 'wspd', 'uwnd', 'vwnd']:
        if verbose: print(f"      Checking {col}")
        range_check(df, col)
    return
