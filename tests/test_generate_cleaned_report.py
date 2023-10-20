"""Testing for helpers to check cleaned data"""
import pytest

import numpy as np
import pandas as pd

import ros_database.processing.generate_cleaned_data_report as rep


def make_test_data(nperiod = 5):
    """Creates a test dataframe"""
    index = pd.date_range('2023-06-20 00:00:00', periods=nperiod, freq='1H') + \
        pd.to_timedelta(np.random.randint(1, 59, nperiod), unit='m')
    test_df = pd.DataFrame(
        {'UP': [np.nan, True, False, False, True],
         'FZRA': [np.nan, False, True, False, True],
         'RA': np.nan,
         'SOLID': np.nan,
         #          'p01i': precip,
         },
        index = index
    )
    return test_df

df = make_test_data()

@pytest.mark.parametrize(
    "p01i, expected",
    [
        (np.nan, [False]*5),
        (0.2, [True]*5),
        (1.0, [True]*5),
        (0.0, [False]*5),
        ([np.nan, 0.2, 1.0, 0.5, 0.0],
         [False, True, True, True, False]),
    ]
)
def test_is_precip(p01i, expected):
    df['p01i'] = p01i
    assert all(rep.is_precip(df) == expected)


@pytest.mark.parametrize(
    "p01i, expected",
    [
        (np.nan, [False]*5),
        (0.2, [True]*5),
        (1.0, [False]*5),
        (0.0, [False]*5),
        ([np.nan, 0.2, 1.0, 0.5, 0.0],
         [False, True, False, False, False]),
    ]
)
def test_is_trace(p01i, expected):
    df['p01i'] = p01i
    assert all(rep.is_trace(df) == expected)


@pytest.mark.parametrize(
    "p01i, expected",
    [
        (np.nan, [False]*5),
        (0.2, [False]*5),
        (1.0, [False]*5),
        (0.0, [True]*5),
        ([np.nan, 0.2, 1.0, 0.5, 0.0],
         [False, False, False, False, True]),
    ]
)
def test_is_zero_precip(p01i, expected):
    df['p01i'] = p01i
    assert all(rep.is_zero_precip(df) == expected)

    
@pytest.mark.parametrize(
    "p01i, expected",
    [
        (np.nan, [True]*5),
        (0.2, [False]*5),
        (1.0, [False]*5),
        (0.0, [False]*5),
        ([np.nan, 0.2, 1.0, 0.5, 0.0],
         [True, False, False, False, False]),
    ]
)
def test_precip_isnan(p01i, expected):
    df['p01i'] = p01i
    assert all(rep.precip_isnan(df) == expected)

    
@pytest.mark.parametrize(
    "df, expected",
    [
        (df, [False, True, True, False, True]),
    ]
)
def test_any_ptype(df, expected):
    assert all(rep.any_ptype(df) == expected)


@pytest.mark.parametrize(
    "p01i, expected",
    [
        (np.nan, 0),
        (0.2, 5),
        (1.0, 5),
        (0.0, 0),
        ([np.nan, 0.2, 1.0, 0.5, 0.0], 3),
    ]
)
def test_count_precip_events(p01i, expected):
    df['p01i'] = p01i
    assert rep.count_precip_events(df) == expected


@pytest.mark.parametrize(
    "p01i, expected",
    [
        (np.nan, 0),
        (0.2, 5),
        (1.0, 0),
        (0.0, 0),
        ([np.nan, 0.2, 1.0, 0.5, 0.0], 1),
    ]
)
def test_count_trace_precip(p01i, expected):
    df['p01i'] = p01i
    assert rep.count_trace_precip(df) == expected


@pytest.mark.parametrize(
    "df, expected",
    [
        (df, 3),
    ]
)
def test_count_any_ptype(df, expected):
    assert rep.count_any_ptype(df) == expected


@pytest.mark.parametrize(
    "p01i, expected",
    [
        (np.nan, 0),
        (0.2, 3),
        (1.0, 3),
        (0.0, 0),
        ([np.nan, 0.2, 1.0, 0.5, 0.0], 2),
    ]
)
def test_count_ptype_with_precip(p01i, expected):
    df['p01i'] = p01i
    assert rep.count_ptype_with_precip(df) == expected


@pytest.mark.parametrize(
    "p01i, expected",
    [
        (np.nan, 0),
        (0.2, 3),
        (1.0, 0),
        (0.0, 0),
        ([np.nan, 0.2, 1.0, 0.5, 0.0], 1),
    ]
)
def test_count_ptype_with_trace(p01i, expected):
    df['p01i'] = p01i
    assert rep.count_ptype_with_trace(df) == expected


@pytest.mark.parametrize(
    "p01i, expected",
    [
        (np.nan, 0),
        (0.2, 0),
        (1.0, 0),
        (0.0, 3),
        ([np.nan, 0.2, 1.0, 0.5, 0.0], 1),
    ]
)
def test_count_ptype_with_zero_precip(p01i, expected):
    df['p01i'] = p01i
    assert rep.count_ptype_with_zero_precip(df) == expected

@pytest.mark.parametrize(
    "p01i, expected",
    [
        (np.nan, 3),
        (0.2, 0),
        (1.0, 0),
        (0.0, 0),
        ([np.nan, 0.2, 1.0, 0.5, 0.0], 0),
    ]
)
def test_count_ptype_with_precip_isnan(p01i, expected):
    df['p01i'] = p01i
    assert rep.count_ptype_with_precip_isnan(df) == expected
