"""
Checks concatenated files for consistence

EXpects files are parsed correctly

- Make sure all fields, except wxcodes and station_id, are floats.
- If not generate a list of unique values but treat numeric elements as single entry
"""

import datetime as dt
import pandas as pd
import numpy as np

from ros_database.filepath import SURFOBS_CONCAT_PATH
from ros_database.processing.surface import read_iowa_mesonet_file


column_data_types = {
    'station': 'object',
    'tmpf': 'float64',
    'dwpf': 'float64',
    'relh': 'float64',
    'drct': 'float64',
    'sknt': 'float64',
    'p01i': 'float64',
    'alti': 'float64',
    'mslp': 'float64',
    'wxcodes': 'object',
    }

def check_type(df, column, expected_dtype):
    assert df[column].dtype == expected_dtype, f"    For {column} expected {expected_dtype}, found {df[column].dtype} instead"


def is_a_number(s):
    return s.replace('-','',1).replace('.','',1).replace('e-','',1).replace('e+','',1).replace('e','',1).replace('+','',1).isdigit() 


def get_values(s):
    """Returns a list of unique values"""
    unique_values = s.unique()
    numbers = [str(s) for s in unique_values if is_a_number(str(s)) ]
    not_numbers = [str(s) for s in unique_values if not is_a_number(str(s))]
    print("    [" + ', '.join(not_numbers + [numbers[0]]) + f"]: with {len(numbers)} unique numbers")

def is_all_zero(s): 
    return (s.dropna() <= 0.).sum() == s.dropna().count()
    

def check_all_zero_precip(s):
    if s.dtype == column_data_types['p01i']:
        #print(f"Precip min: {s.min()}, max: {s.max()} {s.min() == s.max()}")
        assert not is_all_zero(s), f"   Preciptation values are all zero"


def check_one_file(fp):
    df = read_iowa_mesonet_file(fp)
    #df['tmpf'] = df['tmpf'].astype('object')
    
    for column, expected_dtype in column_data_types.items():
        err_flag = False
        try:
            check_type(df, column, expected_dtype)
        except AssertionError as err:
            print(f"Checking {fp.stem}: FAILED")
            print(err)
            get_values(df[column])
            err_flag = True
        #break
    try:
        check_all_zero_precip(df['p01i'])
    except AssertionError as err:
        if not err_flag: print(f"Checking {fp.stem}: FAILED")
        print(err)
    
    #print ("   PASSED!")
    return


def main():

    for fp in SURFOBS_CONCAT_PATH.glob('*.csv'):
        check_one_file(fp)


if __name__ == "__main__":
    main()
    
