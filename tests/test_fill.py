import numpy as np
import datetime as dt
import pandas as pd

from ros_database.processing.cleaning import (fill_missing,
                                              remove_duplicate_for_index,
                                              remove_duplicate_records)


pd.set_option('display.max_rows', None)
# Test data

# Set up test dataset for cleaning datasets
# - Need to figure out how to assert this test
# Big test
raw_data = """                    station   tmpf   dwpf    relh   drct  sknt  p01i   alti   mslp wxcodes
datetime                                                                                  
2010-10-29 00:10:00    PATK  33.80  32.00   93.03   30.0   3.0  0.01  29.16    NaN  -SN BR
2010-10-29 00:49:00    PATK  33.80  32.00   93.03    0.0   0.0  0.02  29.15    NaN  -SN BR
2010-10-29 00:53:00    PATK  33.08  32.00   95.75   30.0   3.0  0.02  29.14  987.4  -SN BR
2010-10-29 01:14:00    PATK  33.80  32.00   93.03   30.0   3.0  0.01  29.13    NaN  -SN BR
2010-10-29 01:29:00    PATK  33.80  32.00   93.03    0.0   0.0  0.02  29.13    NaN  -SN BR
2010-10-29 01:51:00    PATK  33.80  32.00   93.03    0.0   0.0  0.03  29.12    NaN  -SN BR
2010-10-29 01:53:00    PATK  33.08  32.00   95.75    0.0   0.0  0.03  29.12  986.5  -SN BR
2010-10-29 02:01:00    PATK  33.80  32.00   93.03    0.0   0.0  0.01  29.11    NaN  -SN BR
2010-10-29 02:18:00    PATK  33.80  32.00   93.03    0.0   0.0  0.01  29.11    NaN  -SN BR
2010-10-29 02:26:00    PATK  33.80  32.00   93.03    0.0   0.0  0.02  29.10    NaN  -SN BR
2010-10-29 02:40:00    PATK  33.80  32.00   93.03    0.0   0.0  0.03  29.10    NaN  -SN BR
2010-10-29 02:53:00    PATK  33.08  32.00   95.75    0.0   0.0  0.04  29.09  985.5  -SN BR
2010-10-29 03:11:00    PATK  33.80  32.00   93.03    0.0   0.0  0.01  29.08    NaN  -SN BR
2010-10-29 03:23:00    PATK  32.00  32.00  100.00    0.0   0.0  0.01  29.07    NaN  -SN BR
2010-10-29 03:38:00    PATK  33.80  32.00   93.03    0.0   0.0  0.01  29.07    NaN      BR
2010-10-29 03:53:00    PATK  32.00  32.00  100.00    0.0   0.0  0.01  29.07  984.8      BR
2010-10-29 04:10:00    PATK  32.00  32.00  100.00    0.0   0.0   NaN  29.07    NaN      BR
2010-10-29 04:10:00    PATK  32.00  32.00  100.00    0.0   0.0   NaN  29.07    NaN      BR
2010-10-29 04:10:00    PATK  32.00  32.00  100.00    0.0   0.0   NaN  29.07    NaN      BR
2010-10-29 04:20:00    PATK  32.00  32.00  100.00    0.0   0.0   NaN  29.07    NaN  -SN BR
2010-10-29 04:20:00    PATK  32.00  32.00  100.00    0.0   0.0   NaN  29.07    NaN  -SN BR
2010-10-29 04:20:00    PATK  32.00  32.00  100.00    0.0   0.0   NaN  29.07    NaN  -SN BR
2010-10-29 04:32:00    PATK  32.00  32.00  100.00    0.0   0.0  0.01  29.07    NaN  -SN BR
2010-10-29 04:43:00    PATK  32.00  32.00  100.00    0.0   0.0  0.01  29.07    NaN  -SN BR
2010-10-29 04:43:00    PATK  32.00  32.00  100.00    0.0   0.0   NaN  29.07    NaN  -SN BR
2010-10-29 04:43:00    PATK  32.00  32.00  100.00    0.0   0.0  0.01  29.07    NaN  -SN BR
2010-10-29 04:53:00    PATK  33.08  32.00   95.75    0.0   0.0  0.01  29.07  984.7  -SN BR
2010-10-29 05:31:00    PATK  32.00  30.20   92.97  220.0   3.0  0.02  29.06    NaN  -SN BR
2010-10-29 05:41:00    PATK  32.00  32.00  100.00  200.0   4.0  0.02  29.06    NaN  -SN BR
2010-10-29 05:53:00    PATK  32.00  30.92   95.73  200.0   4.0  0.02  29.06  984.4  -SN BR
2010-10-29 06:07:00    PATK  32.00  30.20   92.97  200.0   4.0   NaN  29.05    NaN  -SN BR
2010-10-29 06:53:00    PATK  32.00  32.00  100.00  180.0   5.0   NaN  29.04  983.9  -SN BR
2010-10-29 07:05:00    PATK  32.00  32.00  100.00  190.0   4.0   NaN  29.03    NaN  -SN BR
2010-10-29 07:53:00    PATK  32.00  30.92   95.73  180.0   6.0   NaN  29.03  983.4      BR
2010-10-29 08:25:00    PATK  32.00  30.20   92.97  190.0   6.0   NaN  29.02    NaN      BR
2010-10-29 08:44:00    PATK  32.00  30.20   92.97  190.0   5.0   NaN  29.02    NaN      BR
2010-10-29 08:53:00    PATK  32.00  30.92   95.73  190.0   5.0   NaN  29.02  983.1      BR
2010-10-29 08:53:00    PATK  32.00  30.92   95.73  190.0   5.0   NaN  29.02  983.1      BR
2010-10-29 09:22:00    PATK  32.00  30.20   92.97  190.0   6.0   NaN  29.02    NaN      BR
2010-10-29 09:53:00    PATK  32.00  30.92   95.73  190.0   7.0   NaN  29.01  983.0      BR
2010-10-29 10:08:00    PATK  32.00  30.20   92.97  190.0   8.0   NaN  29.02    NaN      BR
2010-10-29 10:42:00    PATK  30.20  28.40   92.92  190.0   6.0   NaN  29.01    NaN     NaN
2010-10-29 10:53:00    PATK  30.92  28.04   88.92  180.0   7.0   NaN  29.02  983.1     NaN
2010-10-29 11:53:00    PATK  30.02  28.04   92.23    0.0   0.0   NaN  29.01  982.8     NaN
2010-10-29 12:53:00    PATK  28.94  28.04   96.38    0.0   0.0   NaN  29.00  982.4     NaN
2010-10-29 13:02:00    PATK  28.40  28.40  100.00    0.0   0.0   NaN  28.99    NaN     NaN
2010-10-29 13:21:00    PATK  28.40  26.60   92.86  170.0   5.0   NaN  28.99    NaN     NaN
2010-10-29 13:53:00    PATK  28.94  26.06   88.82    0.0   0.0   NaN  28.99  982.2     NaN
2010-10-29 14:36:00    PATK  28.40  26.60   92.86    0.0   0.0   NaN  28.98    NaN     NaN
2010-10-29 14:46:00    PATK  28.40  26.60   92.86    0.0   0.0   NaN  28.98    NaN     NaN
2010-10-29 14:53:00    PATK  28.04  26.06   92.16    0.0   0.0   NaN  28.98  982.0     -SN
2010-10-29 15:44:00    PATK  28.40  26.60   92.86    0.0   0.0   NaN  28.98    NaN     -SN
2010-10-29 15:53:00    PATK  28.04  26.06   92.16    0.0   0.0   NaN  28.98  982.0     NaN
2010-10-29 16:53:00    PATK  28.04  26.06   92.16    0.0   0.0   NaN  28.99  982.0     NaN
2010-10-29 17:53:00    PATK  28.04  26.06   92.16    0.0   0.0   NaN  28.99  982.2     NaN
2010-10-29 18:53:00    PATK  26.96  26.06   96.35    0.0   0.0  0.01  28.99  982.3  -SN BR
2010-10-29 19:53:00    PATK  28.04  26.06   92.16    0.0   0.0   NaN  29.00  982.6  -SN BR
2010-10-29 20:53:00    PATK  28.94  26.96   92.19    0.0   0.0   NaN  29.01  983.0  -SN BR
2010-10-29 21:25:00    PATK  28.40  26.60   92.86    0.0   0.0  0.01  29.02    NaN  -SN BR
2010-10-29 21:53:00    PATK  30.02  26.96   88.22    0.0   0.0  0.01  29.02  983.2     NaN
2010-10-29 21:55:00    PATK  30.20  26.60   86.28    0.0   0.0   NaN  29.02    NaN     NaN
2010-10-29 22:53:00    PATK  30.02  28.04   92.23    0.0   0.0   NaN  29.03  983.7  -SN BR
2010-10-29 23:53:00    PATK  30.02  28.04   92.23  220.0   3.0   NaN  29.04  983.9  -SN BR"""


no_duplicate_data = """                    station   tmpf   dwpf    relh   drct  sknt  p01i   alti   mslp wxcodes
datetime                                                                                  
2010-10-29 00:10:00    PATK  33.80  32.00   93.03   30.0   3.0  0.01  29.16    NaN  -SN BR
2010-10-29 00:49:00    PATK  33.80  32.00   93.03    0.0   0.0  0.02  29.15    NaN  -SN BR
2010-10-29 00:53:00    PATK  33.08  32.00   95.75   30.0   3.0  0.02  29.14  987.4  -SN BR
2010-10-29 01:14:00    PATK  33.80  32.00   93.03   30.0   3.0  0.01  29.13    NaN  -SN BR
2010-10-29 01:29:00    PATK  33.80  32.00   93.03    0.0   0.0  0.02  29.13    NaN  -SN BR
2010-10-29 01:51:00    PATK  33.80  32.00   93.03    0.0   0.0  0.03  29.12    NaN  -SN BR
2010-10-29 01:53:00    PATK  33.08  32.00   95.75    0.0   0.0  0.03  29.12  986.5  -SN BR
2010-10-29 02:01:00    PATK  33.80  32.00   93.03    0.0   0.0  0.01  29.11    NaN  -SN BR
2010-10-29 02:18:00    PATK  33.80  32.00   93.03    0.0   0.0  0.01  29.11    NaN  -SN BR
2010-10-29 02:26:00    PATK  33.80  32.00   93.03    0.0   0.0  0.02  29.10    NaN  -SN BR
2010-10-29 02:40:00    PATK  33.80  32.00   93.03    0.0   0.0  0.03  29.10    NaN  -SN BR
2010-10-29 02:53:00    PATK  33.08  32.00   95.75    0.0   0.0  0.04  29.09  985.5  -SN BR
2010-10-29 03:11:00    PATK  33.80  32.00   93.03    0.0   0.0  0.01  29.08    NaN  -SN BR
2010-10-29 03:23:00    PATK  32.00  32.00  100.00    0.0   0.0  0.01  29.07    NaN  -SN BR
2010-10-29 03:38:00    PATK  33.80  32.00   93.03    0.0   0.0  0.01  29.07    NaN      BR
2010-10-29 03:53:00    PATK  32.00  32.00  100.00    0.0   0.0  0.01  29.07  984.8      BR
2010-10-29 04:10:00    PATK  32.00  32.00  100.00    0.0   0.0   NaN  29.07    NaN      BR
2010-10-29 04:20:00    PATK  32.00  32.00  100.00    0.0   0.0   NaN  29.07    NaN  -SN BR
2010-10-29 04:32:00    PATK  32.00  32.00  100.00    0.0   0.0  0.01  29.07    NaN  -SN BR
2010-10-29 04:43:00    PATK  32.00  32.00  100.00    0.0   0.0  0.01  29.07    NaN  -SN BR
2010-10-29 04:53:00    PATK  33.08  32.00   95.75    0.0   0.0  0.01  29.07  984.7  -SN BR
2010-10-29 05:31:00    PATK  32.00  30.20   92.97  220.0   3.0  0.02  29.06    NaN  -SN BR
2010-10-29 05:41:00    PATK  32.00  32.00  100.00  200.0   4.0  0.02  29.06    NaN  -SN BR
2010-10-29 05:53:00    PATK  32.00  30.92   95.73  200.0   4.0  0.02  29.06  984.4  -SN BR
2010-10-29 06:07:00    PATK  32.00  30.20   92.97  200.0   4.0   NaN  29.05    NaN  -SN BR
2010-10-29 06:53:00    PATK  32.00  32.00  100.00  180.0   5.0   NaN  29.04  983.9  -SN BR
2010-10-29 07:05:00    PATK  32.00  32.00  100.00  190.0   4.0   NaN  29.03    NaN  -SN BR
2010-10-29 07:53:00    PATK  32.00  30.92   95.73  180.0   6.0   NaN  29.03  983.4      BR
2010-10-29 08:25:00    PATK  32.00  30.20   92.97  190.0   6.0   NaN  29.02    NaN      BR
2010-10-29 08:44:00    PATK  32.00  30.20   92.97  190.0   5.0   NaN  29.02    NaN      BR
2010-10-29 08:53:00    PATK  32.00  30.92   95.73  190.0   5.0   NaN  29.02  983.1      BR
2010-10-29 09:22:00    PATK  32.00  30.20   92.97  190.0   6.0   NaN  29.02    NaN      BR
2010-10-29 09:53:00    PATK  32.00  30.92   95.73  190.0   7.0   NaN  29.01  983.0      BR
2010-10-29 10:08:00    PATK  32.00  30.20   92.97  190.0   8.0   NaN  29.02    NaN      BR
2010-10-29 10:42:00    PATK  30.20  28.40   92.92  190.0   6.0   NaN  29.01    NaN     NaN
2010-10-29 10:53:00    PATK  30.92  28.04   88.92  180.0   7.0   NaN  29.02  983.1     NaN
2010-10-29 11:53:00    PATK  30.02  28.04   92.23    0.0   0.0   NaN  29.01  982.8     NaN
2010-10-29 12:53:00    PATK  28.94  28.04   96.38    0.0   0.0   NaN  29.00  982.4     NaN
2010-10-29 13:02:00    PATK  28.40  28.40  100.00    0.0   0.0   NaN  28.99    NaN     NaN
2010-10-29 13:21:00    PATK  28.40  26.60   92.86  170.0   5.0   NaN  28.99    NaN     NaN
2010-10-29 13:53:00    PATK  28.94  26.06   88.82    0.0   0.0   NaN  28.99  982.2     NaN
2010-10-29 14:36:00    PATK  28.40  26.60   92.86    0.0   0.0   NaN  28.98    NaN     NaN
2010-10-29 14:46:00    PATK  28.40  26.60   92.86    0.0   0.0   NaN  28.98    NaN     NaN
2010-10-29 14:53:00    PATK  28.04  26.06   92.16    0.0   0.0   NaN  28.98  982.0     -SN
2010-10-29 15:44:00    PATK  28.40  26.60   92.86    0.0   0.0   NaN  28.98    NaN     -SN
2010-10-29 15:53:00    PATK  28.04  26.06   92.16    0.0   0.0   NaN  28.98  982.0     NaN
2010-10-29 16:53:00    PATK  28.04  26.06   92.16    0.0   0.0   NaN  28.99  982.0     NaN
2010-10-29 17:53:00    PATK  28.04  26.06   92.16    0.0   0.0   NaN  28.99  982.2     NaN
2010-10-29 18:53:00    PATK  26.96  26.06   96.35    0.0   0.0  0.01  28.99  982.3  -SN BR
2010-10-29 19:53:00    PATK  28.04  26.06   92.16    0.0   0.0   NaN  29.00  982.6  -SN BR
2010-10-29 20:53:00    PATK  28.94  26.96   92.19    0.0   0.0   NaN  29.01  983.0  -SN BR
2010-10-29 21:25:00    PATK  28.40  26.60   92.86    0.0   0.0  0.01  29.02    NaN  -SN BR
2010-10-29 21:53:00    PATK  30.02  26.96   88.22    0.0   0.0  0.01  29.02  983.2     NaN
2010-10-29 21:55:00    PATK  30.20  26.60   86.28    0.0   0.0   NaN  29.02    NaN     NaN
2010-10-29 22:53:00    PATK  30.02  28.04   92.23    0.0   0.0   NaN  29.03  983.7  -SN BR
2010-10-29 23:53:00    PATK  30.02  28.04   92.23  220.0   3.0   NaN  29.04  983.9  -SN BR"""


## Test data for filling missing data
# One missing value
index = [
    dt.datetime.strptime("2010-10-29 04:43:00", "%Y-%m-%d %H:%M:%S"),
    dt.datetime.strptime("2010-10-29 04:43:00", "%Y-%m-%d %H:%M:%S"),
    dt.datetime.strptime("2010-10-29 04:43:00", "%Y-%m-%d %H:%M:%S"),
]
columns = "station  tmpf  dwpf   relh drct sknt  p01i   alti  mslp wxcodes".split()

one_missing = pd.DataFrame(
    [
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, 0.01, 29.07, np.nan, "-SN BR"],
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, 0.01, 29.07, np.nan, "-SN BR"],
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, np.nan, 29.07, np.nan, "-SN BR"],
    ],
    index=index, columns=columns)

one_missing_expected = pd.DataFrame(
    [
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, 0.01, 29.07, np.nan, "-SN BR"],
    ],
    index=[index[0]], columns=columns)


two_missing = pd.DataFrame(
    [
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, np.nan, 29.07, np.nan, "-SN BR"],
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, 0.01, 29.07, np.nan, "-SN BR"],
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, np.nan, 29.07, np.nan, "-SN BR"],
    ],
    index=index, columns=columns)

two_missing_expected = pd.DataFrame(
    [
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, 0.01, 29.07, np.nan, "-SN BR"],
    ],
    index=[index[0]], columns=columns)

diff_missing = pd.DataFrame(
    [
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, 0.05, 29.07, np.nan, "-SN BR"],
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, 0.01, 29.07, np.nan, "-SN BR"],
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, np.nan, 29.07, np.nan, "-SN BR"],
    ],
    index=index, columns=columns)

the_same = pd.DataFrame(
    [
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, 0.01, 29.07, np.nan, "-SN BR"],
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, 0.01, 29.07, np.nan, "-SN BR"],
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, 0.01, 29.07, np.nan, "-SN BR"],
    ],
    index=index, columns=columns)

the_same_expected = pd.DataFrame(
    [
        ["PATK", 32.0, 32.0, 100.0, 0.0, 0.0, 0.01, 29.07, np.nan, "-SN BR"],
    ],
    index=[index[0]], columns=columns)


## Ingest test dataset
def read_test_data(input_stream):
    """Generates a test dataframe from a set of lines"""
    index = []
    data = []
    lines = input_stream.split("\n")
    columns = lines[0].split()
    for line in lines[2:]:
        index.append(dt.datetime.strptime(line[:20].strip(), "%Y-%m-%d %H:%M:%S"))
        values = line[20:].split()
        data.append(values[:9] + [' '.join(values[9:])])
    df = pd.DataFrame(data, index=index, columns=columns)
    df = df.where(df != "NaN")
    return df


def load_test_input():
    return read_test_data(raw_data)


def test_one_missing():
    """Tests that fill missing does the right thing for DataFrame with one
       missing value"""
    result = fill_missing(one_missing).drop_duplicates()
    assert result.equals(one_missing_expected)
    return


def test_two_missing():
    """Tests that fill missing does the right thing for DataFrame with one
       missing value"""
    result = fill_missing(two_missing).drop_duplicates()
    assert result.equals(two_missing_expected)
    return


def test_the_same():
    """Tests that fill missing does the right thing for DataFrame with one
       missing value"""
    result = fill_missing(the_same).drop_duplicates()
    assert result.equals(the_same_expected)
    return

# Add test for fill_missing to fail


def test_fill_missing():
    """Tests fill_missing function"""
    # Test for one missing
    
    for df in [one_missing, two_missing, diff_missing, the_same]:
        if not df.duplicated().all():  # All rows are not the same
            try:
                df = fill_missing(df)
            except Exception as err:
                print(err)
        print(df)
        print(df.drop_duplicates())


def test_remove_duplicates_for_single_index():
    assert the_same_expected.equals(remove_duplicate_for_index(the_same))


def test_remove_duplicates_for_single_index_for_diff():
    assert the_same_expected.equals(remove_duplicate_for_index(diff_missing))

def test_remove_duplicate_records():
    raw_df = read_test_data(raw_data)
    test_df = read_test_data(no_duplicate_data)

    clean_df = remove_duplicate_records(raw_df)

    assert clean_df.equals(test_df)


def main():
    test_one_missing()
    test_two_missing()
    test_the_same()
    test_remove_duplicates_for_single_index()
    #test_remove_duplicates_for_single_index_for_diff()
    test_remove_duplicate_records()
    

if __name__ == "__main__":
    main()

