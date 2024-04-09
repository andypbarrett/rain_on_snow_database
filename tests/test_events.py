import pandas as pd
import numpy as np
import datetime as dt

from ros_database.processing.extract_precip_events import find_events

PTYPES = ['UP','RA','FZRA','SOLID']


# The following code generates a test file
def gen_ptype(ptype):
    """Return dictionary of precipitation types"""
    return {pcode: True  if pcode in ptype else False for pcode in PTYPES}


def create_event(start, duration, ptype):
    """Creates a test event"""
    index = pd.date_range(start, freq="H", periods=duration)
    return pd.DataFrame(
        [gen_ptype(pt) for pt in ptype],
        index=index,
    )


def create_test_series(start_time, periods, events):
    """Creates a test series for identifying precip events"""
    time_index = pd.date_range(start_time, periods=periods, freq='h')
    return pd.concat([create_event(*event) for event in events]).reindex(time_index)


def create_expected_event_summary(events):
    """Create a dataframe that contains and expected event summary"""
    expected_events_dict = []
    index = []
    for id, (start, duration, _) in enumerate(events):
        expected_events_dict.append(
            {
                'start': pd.to_datetime(start),
                'end': pd.date_range(start, freq='h', periods=duration)[-1],
                'duration': duration,
            }
        )
        index.append(start) 
    return pd.DataFrame(expected_events_dict, index=index)


def make_test_event_dataframe():
    """Generates a test dataframe for identifying events"""

    start_time = '2024-03-25'
    periods = 7*24
    events = [
        ('2024-03-26 06:00:00', 1, ["SOLID"]),
        ('2024-03-28 12:00:00', 2, ["RA", "SOLID"]),
        ('2024-03-28 15:00:00', 1, ["SOLID"]),
        ('2024-03-29 12:00:00', 1, ["FZRA"]),
        ('2024-03-29 14:00:00', 1, ["UP"]),
        ('2024-03-29 16:00:00', 1, ["SOLID"]),
        ('2024-03-29 22:00:00', 6, ["SOLID", "SOLID", "RA", ["SOLID", "RA"], "RA", "SOLID"]),
        ('2024-03-30 20:00:00', 4, ["RA", "FZRA", "SOLID", "SOLID"]),
    ]

    expected_summary = create_expected_event_summary(events)
    test_df = create_test_series(start_time, periods, events)
    return test_df, expected_summary


# Test for event identification
def test_identify_precipitation_event():
    df, expected = make_test_event_dataframe()
    result = find_events(df)
    try:
        assert result.equals(expected)
    except AssertionError:
        print(result)
        print(expected)
