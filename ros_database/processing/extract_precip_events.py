"""Extract precipitation events"""
import pandas as pd

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


def summarize_events(df):
    """Returns summary statitistics for each event"""
    grouper = df.groupby(df.event)
    summary = pd.DataFrame(
                      {
                          "start": grouper.apply(event_start),
                          "end": grouper.apply(event_end),
                          "duration": grouper.apply(duration),
                      }
    )
    summary.index = summary.start
    return summary


def find_events(df):
    """Finds precipitation events"""
    df_precip = identify_events(df)
    result = summarize_events(df_precip)
    return result
