"""Code used to clean raw Iowa mesonet datafiles"""
import pandas as pd

def fill_missing(df):
    """Fills missing values"""
    fill_dict = {}
    for col in df.columns:
        if df[col].isna().all(): continue
        unique_values = df[col].dropna().unique()
        if len(unique_values) > 1:
            raise Exception(f"More that one unique value for {col} from {unique_values} in row {df.index.unique()}: cannot select fill value") 
        fill_dict[col] = unique_values[0]
    return df.fillna(fill_dict)


def remove_duplicate_for_index(df):
    try:
        filled_df = fill_missing(df)
    except Exception as err:
        print(err)
        return None
    return filled_df.drop_duplicates()


def remove_duplicated_indices(df):
    """Removes duplicated records from a DataFrame containing duplicated records

    :df: pandas DataFrame containg duplicated records

    :return: returns a DataFrame containing unique records
    """
    unique_indices = df.index.unique()
    result = []
    for idx in unique_indices:
        result.append(remove_duplicate_for_index(df.loc[idx]))
    return pd.concat(result)


def remove_duplicate_records(df):
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
    df_duplic = df[isduplicated]
    df_unique = df[~isduplicated]
    
    # Remove duplicate records
    df_removed = remove_duplicated_indices(df_duplic)
    
    # Concatenate unique and removed DataFrame, and sort
    df_cleaned = pd.concat([df_unique, df_removed]).sort_index()

    # Check for duplicates just in case something failed
    if df_cleaned.index.duplicated().any():
        raise Exception("Duplicated records still present!")

    return df_cleaned
