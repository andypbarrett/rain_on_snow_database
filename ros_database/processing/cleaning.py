"""Code used to clean raw Iowa mesonet datafiles"""

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
