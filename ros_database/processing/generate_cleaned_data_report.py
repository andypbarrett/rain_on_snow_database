"""Generates a listing with file stats on cleaned data

This is to check processing and is not required.
"""

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
    return df.index().min(), df.index().max()


def any_ptype(df)
    """Returns a boolean array with True if trace precip"""
    columns = ['UP', 'FZRA', 'RA', 'SOLID']
    return df[columns].any(axis=1)


def data_and_ptype(df, columns=required_columns):
    """Returns boolean series with True for all required columns
    and at least one ptype"""


# From notebook

