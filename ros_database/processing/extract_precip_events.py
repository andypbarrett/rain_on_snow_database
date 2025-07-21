"""Extract precipitation events"""
import pandas as pd
import numpy as np

PTYPES = ['UP','RA','FZRA','SOLID']


def identify_events(df):
    """Returns a modified dataframe containing contiguous precipitation events
    identified with an event index"""
    df["PRECIP"] = df[PTYPES].any(axis=1)
    df['event'] = (df['PRECIP'].diff(1) != 0).cumsum()
    return df[df["PRECIP"]]


# Helper routines for summarizing events
def event_start(x):
    return x.index[0]


def event_end(x):
    return x.index[-1]


def duration(x):
    return len(x)


def count_ptype(x, ptype):
    """Return counts of precipitation type"""
    return int(x[ptype].sum())


def t2m_mean(x):
    return np.round(x['t2m'].mean(), 1)


def t2m_min(x):
    return x['t2m'].min()


def t2m_max(x):
    return x['t2m'].max()


def is_sog(x):
    if pd.isnull(x['sog']).all():
        return pd.NA
    elif x['sog'].any():
        return True
    else:
        return False


def precip_sum(x, skipna=False):
    return x['p01i'].sum(skipna=skipna)


def summarize_events(df):
    """Returns summary statitistics for each event"""
    grouper = df.groupby(df.event)
    summary = pd.DataFrame(
                      {
                          "start": grouper.apply(event_start),
                          "end": grouper.apply(event_end),
                          "duration": grouper.apply(duration),
                          "RA": grouper.apply(count_ptype, "RA"),
                          "UP": grouper.apply(count_ptype, "UP"),
                          "FZRA": grouper.apply(count_ptype, "FZRA"),
                          "SOLID": grouper.apply(count_ptype, "SOLID"),
                          "t2m_mean": grouper.apply(t2m_mean),
                          "t2m_min": grouper.apply(t2m_min),
                          "t2m_max": grouper.apply(t2m_max),
                          "precip": grouper.apply(precip_sum),
                          "sog": grouper.apply(is_sog),
                      }
    )
    summary.index = summary.start
    summary.index.name = "timestamp"
    return summary


def find_events(df):
    """Finds precipitation events"""
    df_precip = identify_events(df)
    result = summarize_events(df_precip)
    return result
